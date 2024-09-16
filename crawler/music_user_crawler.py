#爬取用户信息
from selenium import webdriver
from bs4 import BeautifulSoup

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(options=option)

#从文件中获取所有歌单url数组
def get_playlist_url(file_name):
    playlist_url = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            data = line.split('\t')
            playlist_url.append(data[2])
        f.flush()
        f.close()
    return playlist_url

#根据歌单id获得当前歌单中共评论用户的信息，并存储起来，然后抓取他们的播放记录
def write_user(playlist_url):
    #发送url请求
    driver.get(playlist_url)
    #找到指定iframe标签（这里是g_iframe）然后跳入
    driver.switch_to.frame('g_iframe')
    #使用bs4解析文档
    html_soup = BeautifulSoup(driver.page_source, "html.parser")
    #获得评论部分文档
    all_user_div = html_soup.find(id='comment-box').find(class_='m-cmmt').find_all(class_='itm')
    print(all_user_div)
    #写入文件
    with open('dataset/user_info_init.txt', 'a', encoding='utf-8') as f:
        for user_div in all_user_div:
            user_info = user_div.find(class_='cntwrap').find('a')
            user_id = user_info.get('href')[14:]
            user_name = user_info.text
            user_url = 'https://music.163.com/#' + user_info.get('href')
            user_info_line = user_id + '\t' + user_name + '\t' + user_url
            print(user_info_line)
            f.write(user_info_line + '\n')
            f.flush()
        f.close()

#获取歌单id数组
all_playlist_url = get_playlist_url('./dataset/playlist_data.txt')
for playlist_id in all_playlist_url:
    write_user(playlist_id)