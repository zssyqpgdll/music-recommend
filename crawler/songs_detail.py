import requests
import json

#接口获取歌曲时长和图片链接
def get_song_time_picurl(song_id):
    response = requests.get("https://netease-cloud-music-api-psi-three.vercel.app/song/detail?ids=" + song_id, verify = False)
    if response.status_code == 200:
        if len(response.json()['songs']) < 1:
            return 'null', 'null'
        song_millseconds = response.json()['songs'][0].get('dt')
        song_picurl = response.json()['songs'][0].get('al').get('picUrl')
    else:
        song_millseconds = 'null'
        song_picurl = 'null'
    print("时长：" + str(song_millseconds) + ", 图片链接: " + song_picurl)
    return song_millseconds, song_picurl

#获取歌曲时长和图片信息
#get_song_time_picurl("1805305069")


#爬虫获取歌曲发行时间
def get_song_publish_time(song_id):
    response = requests.get("https://netease-cloud-music-api-psi-three.vercel.app/song/detail?ids=" + song_id, verify = False)
    if response.status_code == 200:
        if len(response.json()['songs']) < 1:
            return 'null', 'null'
        song_detail = response.json()['songs'][0]
        song_publish_time = song_detail.get('publishTime')
        print(song_id + "发行时间：" + str(song_publish_time))
        return song_publish_time, json.dumps(song_detail)
    else:
        song_publish_time = 'null'
        song_detail = 'null'
        print("发行时间：" + str(song_publish_time))
        return song_publish_time, song_detail

#爬虫获取歌曲详情
def get_song_detail(song_id):
    response = requests.get("https://netease-cloud-music-api-psi-three.vercel.app/song/detail?ids=" + song_id, verify = False)
    if response.status_code == 200:
        if len(response.json()['songs']) < 1:
            return 'null'
        song_detail = response.json()['songs'][0]
        print("歌曲细节：" + str(song_detail))
        return json.dumps(song_detail)
    else:
        song_detail = 'null'
        print("歌曲细节：" + str(song_detail))
        return song_detail

#从文件中获得歌曲id
def get_songs_id():
    songs_id = []
    with open('./dataset/song_info_remove.txt', 'r', encoding='utf-8') as f:
        for line in f:
            song_id = line.split('\t')[0]
            songs_id.append(song_id)
    f.close()
    return songs_id

songs_id = get_songs_id()
print("已获得所有歌曲id")

#获得所有歌曲的时长和图片链接写入文件
def get_all_songs_time_picurl():
    with open('./dataset/songs_time_picurl.txt', 'a', encoding='utf-8') as f:
        for song_id in songs_id[:]:
            song_time, song_picurl = get_song_time_picurl(song_id)
            print(song_id + '\t' + str(song_time) + '\t' + song_picurl)
            f.write(song_id + '\t' + str(song_time) + '\t' + song_picurl + '\n')
            f.flush()
    f.close()

# get_all_songs_time_picurl()

#获取所有歌曲的发行时间写入文件
def get_all_songs_publish_time():
    #这里从13980行开始收集歌曲详情信息，13980以前的后续在进行收集
    with open("./dataset/songs_publish_time.txt", 'a', encoding='utf-8') as f1, open("./dataset/songs_detail.txt", "a", encoding="utf-8") as f2:
        for song_id in songs_id[:]:
            song_publish_time, song_detail = get_song_publish_time(song_id)
            f1.write(song_id + '\t' + str(song_publish_time) + '\n')
            f1.flush()
            f2.write(song_id + '\t' + song_detail + '\n')
            f2.flush()
    f1.close()
    f2.close()

# get_all_songs_publish_time()

#获得所有歌曲的详情
def get_all_songs_detail():
    #这里开始收集13980以前的歌曲详情信息
    with open("./dataset/songs_detail_13980.txt", "a", encoding="utf-8") as f:
        for song_id in songs_id:
            song_detail = get_song_detail(song_id)
            f.write(song_id + '\t' + song_detail + '\n')
            f.flush()
    f.close()