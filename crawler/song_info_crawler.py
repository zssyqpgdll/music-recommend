#爬取音乐信息
from selenium import webdriver
import requests
import json

#webdriver实例化,为了进入iframe中获取数据,解决requests无法执行javaScript代码的问题,使用selenium
option = webdriver.ChromeOptions() #谷歌浏览器
#设置option,不弹出显示框,启动浏览器的时候不想看到浏览器运行，加载浏览器的静默模式，让它在后台偷偷运行
option.add_argument('headless')
#调用带参数的谷歌浏览器
driver = webdriver.Chrome(options=option)

#从文件中获取歌曲id
def get_songs_id():
    songs_id = []
    with open('./dataset/song_info_remove.txt', 'r', encoding='utf-8') as f:
        for line in f:
            songs_id.append(line.split('\t')[0])
        f.flush()
        f.close()
    return songs_id

#爬虫从指定url中获取歌曲对应的专辑
def get_album(song_url):
    print('发送请求')
    driver.get(song_url)
    #找到指定iframe标签(这里是g_iframe)
    driver.switch_to.frame('g_iframe')
    driver.implicitly_wait(10) #隐式等待
    try:
        album = driver.find_element_by_class_name('m-lycifo').find_element_by_class_name(
            'cnt').find_elements_by_tag_name('p')
    except:
        album = '歌曲无法找到'
        return album
    print(album)
    if len(album) > 1:#只有一个的为歌手，两个第二个为专辑
        #取出p标签中的文字，并按冒号分割
        album = album[1].text.split('：')
        if len(album) > 1:
            album = album[1]
        else:
            album = '暂无专辑'
    else:
        album = '暂无专辑'
    print(album)
    return album

# get_album("https://music.163.com/#/song?id=1805305069")
# get_album("https://music.163.com/#/song?id=1907123291")

#生成歌曲专辑信息为文件
def get_songs_album():
    with open('./dataset/song_album.txt', 'a', encoding='utf-8') as f:
        for song_id in songs_id[:]:
            # song_album = get_album("https://music.163.com/#/song?id=" + song_id)
            response = requests.get("https://netease-cloud-music-api-psi-three.vercel.app/song/detail?ids=" + song_id)
            song_album_name = '暂无专辑'
            if response.status_code == 200:
                try:
                    if response.json()['songs'][0].get('al').get('id') != 0:
                        song_album_name = response.json()['songs'][0].get('al').get('name')
                except:
                    song_album_name = '暂无专辑'
            print(song_id + '\t' + song_album_name)
            f.write(song_id + '\t' + song_album_name + '\n')
            f.flush()#把缓冲区中的内容放到磁盘中
        f.close()


#从文件中获取歌曲播放次数
def get_songs_playcnt():
    songs_playcnt = {}
    with open('./dataset/user_record_init.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip() #去首尾空格
            song_id = line.split('\t')[1]
            weight = int(line.split('\t')[2].strip())
            #没有记录的设为0
            songs_playcnt.setdefault(song_id, int(songs_playcnt.get(song_id, 0)) + weight)
    f.close()
    return songs_playcnt

#从文件中获取歌曲专辑
def get_songs_album_from_file():
    songs_album = {}
    with open('./dataset/song_album.txt', 'r', encoding='utf-8') as f:
        for line in f:
            song_id = line.split('\t')[0]
            song_album = line.split('\t')[1].strip()
            songs_album[song_id] = song_album
    f.close()
    return songs_album

#从文件中获取歌曲下载地址
def get_songs_download_url_from_file():
    songs_download_url = {}
    with open('./dataset/songs_download_url.txt', 'r', encoding='utf-8') as f:
        for line in f:
            song_id = line.split('\t')[0]
            songs_download_url[song_id] = line.split('\t')[1].strip()
    f.close()
    return songs_download_url

#从文件中获取歌曲时长和图片
def get_songs_time_picurl_from_file():
    songs_time = {}
    songs_picurl = {}
    with open('./dataset/songs_time_picurl.txt', 'r', encoding='utf-8') as f:
        for line in f:
            song_id = line.split('\t')[0]
            songs_time[song_id] = line.split('\t')[1].strip()
            songs_picurl[song_id] = line.split('\t')[2].strip()
    f.close()
    return songs_time, songs_picurl

#从文件中获取歌曲发布时间
def get_songs_publish_time_from_file():
    songs_publish_time = {}
    with open('./dataset/songs_publish_time.txt', 'r', encoding='utf-8') as f:
        for line in f:
            song_id = line.split('\t')[0]
            songs_publish_time[song_id] = line.split('\t')[1].strip()
    f.close()
    return songs_publish_time

def get_new_song_info():
    #歌曲播放次数
    songs_playcnt = get_songs_playcnt()
    print(songs_playcnt)
    #歌曲对应专辑
    songs_album = get_songs_album_from_file()
    #歌曲下载地址
    songs_download_url = get_songs_download_url_from_file()
    #歌曲时长和图片
    songs_time, songs_picurl = get_songs_time_picurl_from_file()
    #歌曲发布时间
    songs_publish_time = get_songs_publish_time_from_file()
    with open('./dataset/song_info_remove.txt', 'r', encoding='utf-8') as f1, open('./dataset/new_song_info1.txt', 'a', encoding='utf-8') as f2:
        for line in f1:
            line = line.strip()
            song_id = line.split('\t')[0]
            song_name = line.split('\t')[1]
            song_url = line.split('\t')[2]
            song_album = songs_album[song_id]
            song_playcnt = songs_playcnt[song_id]
            song_download_url = songs_download_url[song_id]
            song_time = songs_time[song_id]
            song_picurl = songs_picurl[song_id]
            song_publish_time = songs_publish_time[song_id]
            singer_id = line.split('\t')[3]
            singer_name = line.split('\t')[4]
            singer_url = line.split('\t')[5].strip()
            line = song_id + '\t' + song_name + '\t' + song_url + '\t' + song_album + '\t' + str(song_playcnt) + '\t' + \
                   song_download_url + '\t' + song_time + '\t' + song_picurl + '\t' + song_publish_time + '\t' + singer_id + '\t' + singer_name + '\t' + singer_url
            print(line)
            f2.write(line + '\n')
            f2.flush()
    f1.close()
    f2.close()

# songs_id = get_songs_id()
# get_songs_album()
get_new_song_info()