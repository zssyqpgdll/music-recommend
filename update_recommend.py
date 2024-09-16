# 基于皮尔逊相似的的物品推荐
from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import io
import pymysql
import pandas as pd
from surprise import KNNBaseline
from surprise import KNNBasic
from surprise import SVD
from surprise import Dataset
from surprise import Reader


#算法使用训练集进行训练
def get_trainset_algo():
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    record = pd.read_sql("select * from record", con=conn)
    conn.close()
    record = pd.DataFrame(record)
    reader = Reader(rating_scale=(0, 100))
    # 加载数据集
    data = Dataset.load_from_df(record[['uid', 'iid', 'weight']], reader=reader)
    # 将数据集转换成矩阵形式
    trainset = data.build_full_trainset() #训练集
    sim_options = {'name': 'pearson_baseline', 'user_based': True} #基于用户的协同过滤算法
    bsl_options = {'method': 'als', 'n_epochs': 20} #交替最小二乘法
    algo = KNNBaseline(sim_options=sim_options, bsl_options=bsl_options)

    # 训练数据集
    print('开始训练······')
    algo.fit(trainset)
    print('训练结束')
    return algo

algo = get_trainset_algo()

#得到指定物品的top-N个相似物品
def get_topN_items(current_item_raw_id, topK):
    """
    :param current_item_raw_id: 物品的原始id，必须为字符串类型
    :param topK: 相似度高的前topK首歌曲
    :return: 当前歌曲的相似歌曲id列表
    """
    print("歌曲原始id：")
    print(current_item_raw_id)
    # 得到矩阵中的歌曲id（内部id），参数为字符串格式
    current_song_inner_id = algo.trainset.to_inner_iid(current_item_raw_id)
    print("歌曲内部id：")
    print(current_song_inner_id)
    # 相似歌曲推荐，得到的是相似歌曲的内部id，得到topK个
    current_song_neighbors = algo.get_neighbors(current_song_inner_id % 3624, k=topK)
    # 推荐歌手的内部id如下
    print("推荐歌曲的内部id：")
    print(current_song_neighbors)
    # 从相似歌曲的内部id得到原始id
    current_song_neighbors = (algo.trainset.to_raw_iid(inner_id)
                              for inner_id in current_song_neighbors)

    return current_song_neighbors

# get_topN_items('448317748', 30)

#获得相似音乐好友推荐
def get_topN_users(current_user_raw_id, topK):
    """
    :param current_user_raw_id: 当前用户id
    :param topK: 相似度高的前topK个相似音乐好友
    :return: 当前用户的相似音乐好友id数组
    """
    print("用户原始id：")
    print(current_user_raw_id)
    # 得到矩阵中的用户id（内部id），方法是algo.trainset.to_inner_uid(uid)，参数为字符串格式
    current_user_inner_id = algo.trainset.to_inner_uid(current_user_raw_id)
    print("用户内部id：")
    print(current_user_inner_id)

    # 相似音乐好友推荐，得到的是相似音乐好友的内部id，得到topK个
    current_user_neighbors = algo.get_neighbors(current_user_inner_id, k=topK)

    # 推荐相似好友的内部id如下
    print("推荐用户的内部id：")
    print(current_user_neighbors)
    # 从相似音乐好友的内部id转化为原始id
    current_user_neighbors = (algo.trainset.to_raw_uid(inner_id)
                              for inner_id in current_user_neighbors)

    return current_user_neighbors

# 获得每首歌曲的相似歌曲推荐
def get_all_topN_songs():
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    song_iid = pd.read_sql("select iid from song", con=conn)
    # 获得Cursor对象
    cs = conn.cursor()
    # sql语句
    sql = 'insert into test (iid, topsongs) values (%s, %s)'

    for iid in song_iid['iid'][:100]:
        print('获得' + iid + '的推荐结果：')
        line = ''
        # 将得到的结果拼接成字符串
        for id in get_topN_items(iid, 20):
            line = line + id + ','
        # 定义一个参数元组
        param = (iid, line.strip(','))
        print(iid + '写入数据库···')
        cs.execute(sql, param)
    conn.commit()
    # 关闭数据库
    cs.close()
    conn.close()

get_all_topN_songs()

# 获得每个用户的相似音乐好友推荐
def get_all_topN_users():
    conn = pymysql.connect(host='localhost', port=3306, database='music_recommend', user='root',
                           password='zssyqpgdll88990', charset='utf8')
    user_uid = pd.read_sql("select DISTINCT uid from record", con=conn)
    # 获得Cursor对象
    cs = conn.cursor()
    # sql语句
    sql = 'insert into test_user (uid, topusers) values (%s, %s)'

    for uid in user_uid['uid'][:100]:
        print('获得' + uid + '的推荐结果：')
        line = ''
        # 将得到的结果拼接成字符串
        for id in get_topN_users(uid, 20):
            line = line + id + ','
        # 定义一个参数元组
        param = (uid, line.strip(','))
        print(uid + '写入数据库···')
        cs.execute(sql, param)
    conn.commit()
    # 关闭数据库
    cs.close()
    conn.close()

get_all_topN_users()