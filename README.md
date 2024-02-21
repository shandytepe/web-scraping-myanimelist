# **Web Scraping MyAnimeList**
---

- Goals dari repository ini adalah kita bisa membuat simple portfolio dengan melakukan Web Scraping
- Repository ini digunakan pada thread Pacmann yang ini (link soon)
- Website yang ingin kita scraping adalah https://myanimelist.net/
- Data yang discrape, akan disimpan di folder `data/`

## **How to Use Web Scrapper**
---

Untuk menjalankan Web Scrapper, kita bisa menjalankan command ini di Command Line

```python
python -m main --year <year_params> --season <season_params>
```

- `year_params`: bisa diisi dengan tahun. ex: 2024
- `season_params`: bisa diisi dengan season yang tersedia adalah `fall`, `winter`, `summer`, `spring`

Contoh pemakaian:

```python
python -m main --year 2024 --season "winter"
```