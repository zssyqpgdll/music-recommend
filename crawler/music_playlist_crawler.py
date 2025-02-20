#爬取歌单
from selenium import webdriver
from bs4 import BeautifulSoup
import time

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(options=option)

#获取歌单列表的url数组
def get_discover_playlist_url_list():
    #歌单偏移量,初始为0
    playlist_offset = 0
    #歌单列表的url数组,共有37页,每页有35个歌单
    discover_playlist_url_list = []
    #对歌单列表数组赋值
    for playlist_offset in range(0, 37):
        discover_playlist_url_list.append(
            # "https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%8D%8E%E8%AF%AD&limit=35&offset=" #华语
            # "https://music.163.com/#/discover/playlist/?order=hot&cat=%E7%B2%A4%E8%AF%AD&limit=35&offset=" #粤语
            # "https://music.163.com/#/discover/playlist/?order=hot&cat=%E6%AC%A7%E7%BE%8E&limit=35&offset=" #欧美
            "https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=" #全部
            + str(playlist_offset * 35))
    return discover_playlist_url_list

#将content内容添加到文件尾部
def write_to_file(fiel_name, content):
    with open(fiel_name, 'a', encoding='utf-8') as f:
        f.write(content + '\n')
        f.flush()
        f.close()

#解析歌单列表的数据，并写入到文件中
def parse_playlist_data(url):
    #发送url请求
    driver.get(url)
    #找到指定iframe标签（这里是g_iframe）然后跳入
    driver.switch_to.frame('g_iframe')
    driver.implicitly_wait(10)  #隐式等待   

    #使用bs4解析文档
    html_soup = BeautifulSoup(driver.page_source, "html.parser")
    #获得每一个歌单所在的li标签
    all_playlist_li = html_soup.find(id='m-pl-container').find_all('li')
    print(all_playlist_li)
    #打开文件
    with open('./dataset/playlist_data.txt', 'a', encoding='utf-8') as f:
        for li in all_playlist_li:
            playlist_id = li.find(class_='icon-play').get('data-res-id')  #歌单id
            playlist_name = li.find(class_='msk').get('title')  #歌单名称title
            playlist_url = "https://music.163.com/#" + li.find(class_='msk').get('href')  #歌单url
            img_url = li.find('img').get('src')  #歌单图片url
            creator_name = li.find('a', class_='s-fc3').get('title')  #创建者姓名title
            creator_url = "https://music.163.com/#" + li.find('a', class_='s-fc3').get('href')  #创建者首页url
            playlist_content = playlist_id + '\t' + playlist_name + '\t' + playlist_url + '\t' + creator_name + '\t' \
                               + creator_url + '\t' + img_url
            print(playlist_content)
            f.write(playlist_content + '\n')
            f.flush()
        f.close()

#获得所有歌单列表的url
discover_playlist_url_list = get_discover_playlist_url_list()
#遍历每一个歌单列表url，并将其中所有歌单数据解析之后存到文件中
for discover_playlist_url in discover_playlist_url_list:
    parse_playlist_data(discover_playlist_url)
    driver.implicitly_wait(10)  #隐式等待
    time.sleep(0.5)