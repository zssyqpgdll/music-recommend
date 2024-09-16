#爬取歌曲下载地址
import requests
import json

#获取歌曲id
def get_songs_id():
    songs_id = []
    with open('./dataset/song_info_remove.txt', 'r', encoding='utf-8') as f:
        for line in f:
            song_id = line.split('\t')[0]
            songs_id.append(song_id)
    f.close()
    return songs_id

#获取歌曲下载地址
def get_song_download_url(song_id):
    #接口：http://music.163.com/api/song/enhance/player/url?id=454828887&ids=%5B454828887%5D&br=3200000
    #response = requests.get("http://music.163.com/api/song/enhance/player/url?id=" + song_id + "&ids=%5B" + song_id + "%5D&br=3200000")
    for i in range(1,10):
        # response = requests.get("https://netease-cloud-music-api-psi-three.vercel.app/song/url?id=" + song_id)
        response = requests.get(
            "http://music.163.com/api/song/enhance/player/url?id=" + song_id + "&ids=%5B" + song_id + "%5D&br=3200000")
        if response.status_code == 200: #成功
            song_url = response.json()['data'][0].get('url')
            if song_url == None:
                for i in range(1, 10):
                    response2 = requests.get("https://netease-cloud-music-api-psi-three.vercel.app/song/url?id=" + song_id)
                    if response2.status_code == 200:#第二个接口成功
                        song_url = response2.json()['data'][0].get('url')
                        break
            break
    else:#没有200成功,break出来的不会走这条路
        song_url = 'null'
    print(song_url)
    return song_url

#获取所有歌曲的下载链接
def get_songs_download_url():
    songs_id = get_songs_id()
    with open('./dataset/songs_download_url.txt', 'a', encoding='utf-8') as f:
        for song_id in songs_id[44194:]:
            line = song_id + '\t' + str(get_song_download_url(song_id))
            print(line)
            f.write(line + '\n')
            f.flush()
    f.close()

get_songs_download_url()
# get_song_download_url("1346907833")#第一个接口没有url,第二个接口有的