# Music Recommend
This project is designed to build a music recommendation system by crawling data from NetEase Cloud Music. It collects music and user data through web scraping and applies recommendation algorithms to provide personalized music suggestions.

Including data collection, cleaning, analysis, storage.

## Crawing
Run the crawling scripts in the following order to gather the necessary data:
```python
python music_playlist_crawler.py
python music_playlist_crawler2.py
python music_user_crawler.py
python remove_same.py
python music_play_recode_crawler.py
python song_download_url_crawler.py
python song_detail.py
python song_info_crawler.py
```

## Data processing
```python
python pre_deal_util.py
```

## Recommend
```python
python music_recommend.py
```

## Store
Store the results in the mysql database
```python
python mysql_util.py
```
