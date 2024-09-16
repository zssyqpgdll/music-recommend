#根据已经获得用户的信息，来获取用户的播放记录，并记录对应的音乐的信息
from selenium import webdriver
from bs4 import BeautifulSoup
import time

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(options=option)

#从文件中获取用户的播放记录url数组
def get_user_record_url(file_name):
    user_record_url = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            data = line.split('\t')
            #用户听歌排行,data[0]为用户id
            user_record_url.append('https://music.163.com/#/user/songs/rank?id=' + data[0])
        f.flush()
        f.close()
    return user_record_url


def write_user_record2(user_record_url):
    for i in range(0,3):
        # 发送url请求
        driver.get(user_record_url)
        # 跳入iframe标签
        driver.switch_to.frame('g_iframe')
        driver.implicitly_wait(10)  # 隐式等待
        # 所有时间
        checkall = driver.find_element_by_id('songsall')
        # 定位、切换到所有时间的按钮标签
        checkall.click()
        # 模拟鼠标点击查看所有时间下的听歌排行
        driver.implicitly_wait(10)
        time.sleep(0.5)  # 这里需要强制等待加载时间，一般一秒内就可以了
        # 使用bs4解析文档
        html_soup = BeautifulSoup(driver.page_source, "html.parser")
        # 获得用户的播放记录的li标签
        all_user_record_li = html_soup.find(id='m-record').find('ul')
        # 判断播放记录是否可以访问，不能访问则直接返回结束
        if all_user_record_li == None:
            print(str(i) + '\t' + user_record_url)
            continue
        else:
            all_user_record_li = all_user_record_li.find_all('li')
            break
    else:
        print('播放记录不可访问' + user_record_url)
        return

    # 从用户播放记录的url上获取用户id
    user_id = user_record_url.split('=')[1]
    print(user_record_url)

    # 写入文件
    with open('./user_record_init.txt', 'a', encoding='utf-8') as record_f, open('./song_info.txt', 'a',
                                                                                 encoding='utf-8') as song_f:
        for user_record_li in all_user_record_li:
            song_info = user_record_li.find(class_='song').find(class_='txt').find_all('a')
            print(song_info)
            song_id = song_info[0].get('href')[9:]  # 解析得到歌曲id
            song_name = song_info[0].find('b').text  # 获得歌曲名字
            song_url = 'https://music.163.com/#/song?id=' + song_id  # 歌曲的url
            song_score = user_record_li.find(class_='tops').find('span').get('style').split(':')[1].split('%')[
                0]  # 歌曲评分
            # 歌手信息
            if len(song_info) == 2:
                singer_id = song_info[1].get('href')[11:]  # 歌曲对应的歌手的id
                singer_url = 'https://music.163.com/#/artist?id=' + singer_id  # 歌手的url
            else:
                singer_id = '00000000'  # 歌曲对应的歌手的id
                singer_url = "Don't have a url"  # 歌手的url
            singer_name = user_record_li.find(class_='song').find(class_='txt').find('span').find('span').get(
                'title')  # 歌手的姓名

            user_record_line = user_id + '\t' + song_id + '\t' + song_score
            song_info_line = song_id + '\t' + song_name + '\t' + song_url + '\t' + singer_id + '\t' + singer_name + '\t' + singer_url
            print(user_record_line)
            print(song_info_line)
            # 写入并刷新
            record_f.write(user_record_line + '\n')
            record_f.flush()
            song_f.write(song_info_line + '\n')
            song_f.flush()
        record_f.close()
        song_f.close()


def write_user_record(user_record_url):
    #发送url请求
    driver.get(user_record_url)
    #跳入iframe标签
    driver.switch_to.frame('g_iframe')
    driver.implicitly_wait(10)#隐式等待
    #所有时间
    checkall = driver.find_element_by_id('songsall')
    #定位、切换到所有时间的按钮标签
    checkall.click()
    #模拟鼠标点击查看所有时间下的听歌排行
    driver.implicitly_wait(10)
    time.sleep(0.5)#这里需要强制等待加载时间，一般一秒内就可以了

    #使用bs4解析文档
    html_soup = BeautifulSoup(driver.page_source, "html.parser")
    #获得用户的播放记录的li标签
    all_user_record_li = html_soup.find(id='m-record').find('ul')
    #判断播放记录是否可以访问，不能访问则直接返回结束
    if all_user_record_li == None:
        print('播放记录不可访问')
        return
    else:
        all_user_record_li = all_user_record_li.find_all('li')

    #从用户播放记录的url上获取用户id
    user_id = user_record_url.split('=')[1]
    print(user_record_url)

    #写入文件
    with open('./user_record_init.txt', 'a', encoding='utf-8') as record_f, open('./song_info.txt', 'a', encoding='utf-8') as song_f:
        for user_record_li in all_user_record_li:
            song_info = user_record_li.find(class_='song').find(class_='txt').find_all('a')
            print(song_info)
            song_id = song_info[0].get('href')[9:]  #解析得到歌曲id
            song_name = song_info[0].find('b').text  #获得歌曲名字
            song_url = 'https://music.163.com/#/song?id=' + song_id  #歌曲的url
            song_score = user_record_li.find(class_='tops').find('span').get('style').split(':')[1].split('%')[0]  #歌曲评分
            #歌手信息
            if len(song_info) == 2:
                singer_id = song_info[1].get('href')[11:]  #歌曲对应的歌手的id
                singer_url = 'https://music.163.com/#/artist?id=' + singer_id  #歌手的url
            else:
                singer_id = '00000000'  #歌曲对应的歌手的id
                singer_url = "Don't have a url"  #歌手的url
            singer_name = user_record_li.find(class_='song').find(class_='txt').find('span').find('span').get('title')  #歌手的姓名

            user_record_line = user_id + '\t' + song_id + '\t' + song_score
            song_info_line = song_id + '\t' + song_name + '\t' + song_url + '\t' + singer_id + '\t' + singer_name + '\t' + singer_url
            print(user_record_line)
            print(song_info_line)
            #写入并刷新
            record_f.write(user_record_line + '\n')
            record_f.flush()
            song_f.write(song_info_line + '\n')
            song_f.flush()
        record_f.close()
        song_f.close()

#获取用户播放记录的url
user_record_url = get_user_record_url('./dataset/user_info.txt')
print(user_record_url)
#遍历所有用户的播放记录
for url in user_record_url[:]:
    write_user_record2(url)