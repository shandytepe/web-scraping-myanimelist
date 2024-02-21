import pandas as pd
import requests 
from bs4 import BeautifulSoup   
from tqdm import tqdm
import time
import argparse

def init_scrapper_engine(year: int, season: str):
    resp = requests.get(f"https://myanimelist.net/anime/season/{year}/{season}")

    soup = BeautifulSoup(resp.text, "html.parser")

    return soup

def scrape_myanimelist(soup, html_tag, show_type):
    
    raw_data = soup.find_all("div", class_ = html_tag)

    anime_data = []

    for data in tqdm(raw_data):
        
        time.sleep(0.05)

        # get title
        title = data.find("a").text

        # get release date
        release_date = data.find("span", class_ = "item").text
        
        # get link mal
        link_mal = data.find("a").get("href")

        # get all info data like release date, anime minutes, and anime episode
        get_anime_info = data.find("div", class_ = "info")

        # get more detail info
        get_anime_detail_info = get_anime_info.find_all('span', class_='item')

        # get release date
        release_date = get_anime_detail_info[0].text

        # get episode
        anime_episode = get_anime_detail_info[1].contents[1].text

        # get duration
        anime_duration = get_anime_detail_info[1].contents[3].text

        # get genre anime data
        genre_raw = data.find_all("div", class_ = "genres-inner js-genre-inner")

        # Iterate through each <div> and extract genres
        for genre_div in genre_raw:

            genre_links = genre_div.find_all('a')
            
            # Extract and print genre names
            genres = [link.text for link in genre_links]

        # get img link
        img_link = data.find("img").get("src")

        # get description
        description = data.find("p").text

        # get studio name        
        get_studio = data.find_all("div", class_ = "property")[0]

        if get_studio.find("a") is not None:
            studio = get_studio.find("a").text

        else:
            studio = ""

        # get source 
        get_source = data.find_all("div", class_ = "property")[1]

        source = get_source.find("span", class_ = "item").text

        dict_data = {
            "title": title,
            "link_mal": link_mal,
            "release_date": release_date,
            "anime_episode": anime_episode,
            "anime_duration": anime_duration,
            "anime_genre": genres,
            "img_link": img_link,
            "description": description,
            "studio": studio,
            "source": source,
            "show_type": show_type
        }

        anime_data.append(dict_data)
    
    converted_data = pd.DataFrame(anime_data)

    return converted_data   

def concat_anime_data(anime_data):
    concat_data = pd.concat(anime_data)

    return concat_data

def save_output(data, filename):
    data = data

    data.to_csv(f"{filename}.csv", index = False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--year",
                        type = int,
                        help = "Insert Year that you want scrape",
                        required = True)
    
    parser.add_argument("--season",
                        type = str,
                        help = "Insert anime season. Available winter, fall, summer, spring",
                        required = True)
    
    args = parser.parse_args()

    soup = init_scrapper_engine(year = args.year,
                                season = args.season)
    
    get_anime_tv = scrape_myanimelist(soup = soup,
                                      html_tag = "js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-1",
                                      show_type = "TV")
    
    get_anime_ona = scrape_myanimelist(soup = soup,
                                       html_tag = "js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-5",
                                       show_type = "ONA")
    
    get_anime_ova = scrape_myanimelist(soup = soup,
                                       html_tag = "js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-2f",
                                       show_type = "OVA")
    
    get_anime_movie = scrape_myanimelist(soup = soup,
                                         html_tag = "js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-3",
                                         show_type = "Movies")
    
    concat_data = concat_anime_data(anime_data = [get_anime_tv, get_anime_ona,
                                                  get_anime_ova, get_anime_movie])
    
    save_output(data = concat_data,
                filename = f"data/raw/{args.season}_{args.year}_scrape_data")