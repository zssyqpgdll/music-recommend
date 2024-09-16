#python使用pymysql操作数据库MySQL
import random
import time
import pymysql
import pre_deal_util

#测试数据库连接
def test_connect():
    #打开数据库连接
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root', password='zssyqpgdll88990', charset='utf8')
    #获得Cursor对象
    cs = conn.cursor()
    a = '123'
    b = '123'
    c = '123'
    sql = 'insert into user (uid, name, password) values (%s, %s, %s)'
    param = (a, b, c)
    cs.execute(sql, param)
    conn.commit()
    cs.close()
    conn.close()

#读取用户信息并写入到数据库的user表中
def read_user_info_mysql():
    # 打开数据库连接
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()
    #sql语句
    sql = 'insert into user (user_id, user_name, user_password) values (%s, %s, %s)'

    #读取文件存入数据库
    with open('./dataset/user_info.txt', 'r', encoding='utf-8') as f:
        for line in f:
            user = line.strip().split('\t')
            user_id = user[0]
            user_name = user[1]
            user_password = '123'
            #定义一个参数元组
            param = (user_id, user_name, user_password)
            print(user_id + '写入数据库...')
            cs.execute(sql, param)
    #增删改类操作需要提交事务
    conn.commit()
    #关闭文件
    f.close()
    #关闭数据库
    cs.close()
    conn.close()

# read_user_info_mysql()

#读取歌手信息并写入到数据库的singer表中
def read_singer_info_mysql():
    # 打开数据库连接
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()
    # sql语句
    sql = 'insert into singer (singer_id, singer_name, singer_url) values (%s, %s, %s)'

    # 读取文件存入数据库
    with open('./dataset/singer_info.txt', 'r', encoding='utf-8') as f:
        for line in f:
            singer = line.strip().split('\t')
            singer_id = singer[0]
            singer_name = singer[1]
            singer_url = singer[2]
            # 定义一个参数元组
            param = (singer_id, singer_name, singer_url)
            print(singer_id + '写入数据库...')
            cs.execute(sql, param)
    # 增删改类操作需要提交事务
    conn.commit()
    # 关闭文件
    f.close()
    # 关闭数据库
    cs.close()
    conn.close()

# read_singer_info_mysql()

#读取歌曲信息并写入到数据库的song表中
def read_song_info_mysql():
    # 打开数据库连接
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()
    # sql语句
    sql = 'insert into song (iid, song_name, song_url, album, playcnt, down_url, song_time, picUrl, publishTime, suid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    # 读取文件存入数据库
    with open('./dataset/new_song_info1.txt', 'r', encoding='utf-8') as f:
        for line in f:
            song = line.strip().split('\t')
            song_id = song[0]
            song_name = song[1]
            song_url = song[2]
            song_album = song[3]
            song_playcnt = song[4]
            song_download_url = song[5]
            song_time = song[6]
            song_picurl = song[7]
            song_publish_time = song[8]
            singer_id = song[9]

            # 定义一个参数元组
            param = (song_id, song_name, song_url, song_album, song_playcnt, song_download_url, song_time, song_picurl, song_publish_time, singer_id)
            print(song_id + '写入数据库···')
            cs.execute(sql, param)
    # 增、删、改类操作需要提交事务
    conn.commit()
    # 关闭文件
    f.close()
    # 关闭数据库
    cs.close()
    conn.close()

# read_song_info_mysql()

#读取播放记录并写入到数据库的record表中
def read_record_mysql():
    # 打开数据库连接
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()
    # sql语句
    sql = 'insert into record (user_id, song_id, weight, timestamp) values (%s, %s, %s, %s)'

    # 读取文件存入数据库
    with open('./dataset/user_record.txt', 'r', encoding='utf-8') as f:
        for line in f:
            record = line.strip().split('\t')
            user_id = record[0]
            song_id = record[1]
            weight = record[2]
            timestamp = record[3]
            # 定义一个参数元组
            param = (user_id, song_id, weight, timestamp)
            print(user_id + '写入数据库···')
            cs.execute(sql, param)
    # 增、删、改类操作需要提交事务
    conn.commit()
    # 关闭文件
    f.close()
    cs.close()
    # 关闭数据库
    conn.close()

# read_record_mysql()

'''
#添加歌曲播放链接
def set_songs_down_url():
    # 打开数据库连接
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()

    with open('./dataset/songs_download_url.txt', 'r', encoding='utf-8') as f:
        for line in f:
            song_id = line.split('\t')[0]
            download_url = line.split('\t')[1].strip()
            print("更新：" + song_id)
            # sql语句,新增加一列
            sql = "update song set download_url = '{}' where song_id = '{}'".format(download_url, song_id)
            cs.execute(sql)
    conn.commit()
    conn.close()
    f.close()

#添加歌曲时长和图片链接
def set_songs_time_picRlr():
    # 打开数据库连接
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()

    with open('./dataset/songs_time_picurl.txt', 'r', encoding='utf-8') as f:
        for line in f:
            song_id = line.split('\t')[0].strip()
            song_time = line.split('\t')[1].strip()
            song_picurl = line.split('\t')[2].strip()
            print("更新：" + song_id)
            # sql语句
            sql = "update song set song_time = '{}',picUrl = '{}' where song_id = '{}'".format(song_time, song_picurl, song_id)
            cs.execute(sql)
    conn.commit()
    conn.close()
    f.close()

#添加歌曲的发行时间
def set_songs_publish_time():
    # 打开数据库连接
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()

    with open("./dataset/songs_publish_time.txt", 'r', encoding='utf-8') as f:
        for line in f:
            song_id = line.split('\t')[0]
            song_publish_time = line.split('\t')[1].strip()
            print("更新：" + song_id)
            # sql语句
            sql = "update song set publishTime = '{}' where song_id = '{}'".format(song_publish_time, song_id)
            cs.execute(sql)
    conn.commit()
    conn.close()
    f.close()
'''
#更新用户信息，添加性别、年龄等信息
def update_user_info():
    # 打开数据库连接
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()

    genders = ['男', '女']

    with open("./dataset/user_info.txt", 'r', encoding='utf-8') as f:
        for line in f:
            user_id = line.split('\t')[0]
            gender = random.choice(genders)
            age = random.randint(16, 30)
            province, city = pre_deal_util.get_random_city()
            description = '这个人很懒，什么也没有写'
            registerTime = int(round(time.time() * 1000))
            print("更新：" + user_id)
            # sql语句
            sql = "update user set gender = '{}',age = '{}',area = '{}',description = '{}',registerTime = '{}' where user_id = '{}'".format(
                gender, age, province + '-' + city, description, registerTime, user_id)
            cs.execute(sql)
    conn.commit()
    conn.close()
    f.close()

# update_user_info()




#读取好友推荐结果并写入到数据库的topusers表中
def read_top_users_mysql():
    # 打开数据库连接
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()
    # sql语句
    sql = 'insert into topusers (uid, topusers) values (%s, %s)'

    # 读取文件存入数据库
    with open('./resultset/topN_users_baseline.txt', 'r', encoding='utf-8') as f:
        for line in f:
            top_user = line.strip().split('\t')
            uid = top_user[0]
            topusers = top_user[1]
            # 定义一个参数元组
            param = (uid, topusers)
            print(uid + '写入数据库···')
            cs.execute(sql, param)
    # 增、删、改类操作需要提交事务
    conn.commit()
    # 关闭文件
    f.close()
    cs.close()
    # 关闭数据库
    conn.close()

# read_top_users_mysql()

#读取歌曲推荐结果并写入到数据库的topsongs表中
def read_top_songs_mysql():
    # 打开数据库连接
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()
    # sql语句
    sql = 'insert into topsongs (iid, topsongs) values (%s, %s)'

    # 读取文件存入数据库
    with open('./resultset/topN_songs_baseline.txt', 'r', encoding='utf-8') as f:
        for line in f:
            top_song = line.strip().split('\t')
            song_id = top_song[0]
            topsongs = top_song[1]
            # 定义一个参数元组
            param = (song_id, topsongs)
            print(song_id + '写入数据库···')
            cs.execute(sql, param)
    # 增、删、改类操作需要提交事务
    conn.commit()
    # 关闭文件
    f.close()
    cs.close()
    # 关闭数据库
    conn.close()

# read_top_songs_mysql()