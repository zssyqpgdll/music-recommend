import random
import time

#给用户播放记录添加时间戳
def add_timestamp():
    #打开文件
    with open('./dataset/user_record_init.txt', 'r', encoding='utf-8') as f1, open('./dataset/user_record.txt', 'a', encoding='utf-8') as f2:
        for line in f1:
            #添加时间戳
            line = line.strip() + '\t' + str(int(time.time()))
            #写入到结果文件中
            f2.write(line + '\n')
            f2.flush()
        #关闭文件
        f1.close()
        f2.close()

# add_timestamp()

#去除user_info.txt中不在user_record.txt中的用户
def remove_user_not_in_record():
    #播放记录中的用户id列表
    user_record_id_list = []
    with open('./dataset/user_record.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.split('\t')[0] not in user_record_id_list:
                user_record_id_list.append(line.split('\t')[0])
        f.close()

    #在播放记录中的用户信息
    user_info_in_record_list = []
    with open('./dataset/user_info.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.split('\t')[0] in user_record_id_list:
                user_info_in_record_list.append(line)
        f.close()

    #将筛选之后的用户信息添加到文件中
    with open('./dataset/user_in_record.txt', 'w', encoding='utf-8') as f:
        for line in user_info_in_record_list:
            f.write(line.strip() + '\n')
        f.flush()
    f.close()

# remove_user_not_in_record()

#去除song_info.txt中重复的歌曲
#调用remove_same.py中的file_remove_same()函数
# file_remove_same('./dataset/song_info.txt', './dataset/song_info_remove.txt')

#得到音乐信息的子集,将每个用户的听歌记录缩减至30首,原本每个用户听歌记录有100首
def get_min_song_info():
    #歌曲id列表
    song_id_list = []
    #歌曲音乐信息,内容唯一
    song_lines = []
    user_id = []
    i = 0
    print('读播放记录文件')
    with open('./dataset/user_record.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.split('\t')[0] not in user_id:
                user_id.append(line.split('\t')[0])
                i = 0
            #获取播放次数最多的前30首
            print('前30首')
            if i <30 and line.split('\t')[0] in user_id:
                song_id_list.append(line.split('\t')[1])
                i = i + 1
    f.close()

    #筛选数据
    print('读音乐信息文件')
    with open('./dataset/song_info_remove.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.split('\t')[0] in song_id_list:
                song_lines.append(line)
    f.close()

    #将筛选之后的音乐数据覆盖掉原来的音乐数据
    print('生成新的音乐信息文件')
    with open('./dataset/min_song_info.txt', 'a', encoding='utf-8') as f:
        for line in song_lines:
            f.write(line)
            f.flush()
    f.close()

# get_min_song_info()

#减少用户播放记录,每个用户30首
def get_min_user_record():
    user_id = []
    print('读播放记录文件')
    with open('./dataset/user_record.txt', 'r', encoding='utf-8') as f1, open('./dataset/min_user_record.txt', 'a', encoding='utf-8') as f2:
        for line in f1:
            if line.split('\t')[0] not in user_id:
                user_id.append(line.split('\t')[0])
                i = 0
            # 获取播放次数最多的前30首
            print(line.split('\t')[0] + '的前30首')
            if i < 30 and line.split('\t')[0] in user_id:
                f2.write(line)
                f2.flush()
                i = i + 1
    f1.close()
    f2.close()

# get_min_user_record()

#得到歌手信息的文件
def get_singer_info():
    singers_id = []
    with open('./dataset/song_info_remove.txt', 'r', encoding='utf-8') as f1,\
            open('./dataset/singer_info.txt', 'a', encoding='utf-8') as f2:
        for line in f1:
            if line.split('\t')[3] not in singers_id:
                singer_id = line.split('\t')[3]
                singer_name = line.split('\t')[4]
                singer_url = line.split('\t')[5].strip()
                singers_id.append(singer_id)
                singer = singer_id + '\t' + singer_name + '\t' + singer_url
                f2.write(singer + '\n')
                f2.flush()
    f1.close()
    f2.close()

# get_singer_info()

#随机获得一个省市地区
def get_random_city():
    area = {
        '北京市': ['北京市'],
        '天津市': ['天津市'],
        '河北省': ['石家庄市', '唐山市', '秦皇岛市', '邯郸市', '邢台市', '保定市', '张家口市', '承德市', '沧州市', '廊坊市', '衡水市'],
        '山西省': ['太原市', '大同市', '阳泉市', '长治市', '晋城市', '朔州市', '晋中市', '运城市', '忻州市', '临汾市', '吕梁市'],
        '内蒙古自治区': ['呼和浩特市', '包头市', '乌海市', '赤峰市', '通辽市', '鄂尔多斯市', '呼伦贝尔市', '巴彦淖尔市', '乌兰察布市', '兴安盟', '锡林郭勒盟', '阿拉善盟'],
        '辽宁省': ['沈阳市', '大连市', '鞍山市', '抚顺市', '本溪市', '丹东市', '锦州市', '营口市', '阜新市', '辽阳市', '盘锦市', '铁岭市', '朝阳市', '葫芦岛市'],
        '吉林省': ['长春市', '吉林市', '四平市', '辽源市', '通化市', '白山市', '松原市', '白城市', '延边朝鲜族自治州'],
        '黑龙江省': ['哈尔滨市', '齐齐哈尔市', '鸡西市', '鹤岗市', '双鸭山市', '大庆市', '伊春市', '佳木斯市', '七台河市', '牡丹江市', '黑河市', '绥化市', '大兴安岭地区'],
        '上海市': ['上海市'],
        '江苏省': ['南京市', '无锡市', '徐州市', '常州市', '苏州市', '南通市', '连云港市', '淮安市', '盐城市', '扬州市', '镇江市', '泰州市', '宿迁市'],
        '浙江省': ['杭州市', '宁波市', '温州市', '嘉兴市', '湖州市', '绍兴市', '金华市', '衢州市', '舟山市', '台州市', '丽水市'],
        '安徽省': ['合肥市', '芜湖市', '蚌埠市', '淮南市', '马鞍山市', '淮北市', '铜陵市', '安庆市', '黄山市', '滁州市', '阜阳市', '宿州市', '六安市', '亳州市', '池州市', '宣城市'],
        '福建省': ['福州市', '厦门市', '莆田市', '三明市', '泉州市', '漳州市', '南平市', '龙岩市', '宁德市'],
        '江西省': ['南昌市', '景德镇市', '萍乡市', '九江市', '新余市', '鹰潭市', '赣州市', '吉安市', '宜春市' , '抚州市', '上饶市'],
        '山东省': ['济南市', '青岛市', '淄博市', '枣庄市', '东营市', '烟台市', '潍坊市', '济宁市', '泰安市', '威海市', '日照市', '临沂市', '德州市', '聊城市', '滨州市', '菏泽市'],
        '河南省': ['郑州市', '开封市', '洛阳市', '平顶山市', '安阳市', '鹤壁市', '新乡市', '焦作市', '濮阳市', '许昌市', '漯河市', '三门峡市', '南阳市', '商丘市', '信阳市', '周口市', '驻马店市'],
        '湖北省': ['武汉市', '黄石市', '十堰市', '宜昌市', '襄阳市', '鄂州市', '荆门市', '孝感市', '荆州市', '黄冈市', '咸宁市', '随州市', '恩施土家族苗族自治州'],
        '湖南省': ['长沙市', '株洲市', '湘潭市', '衡阳市', '邵阳市', '岳阳市', '常德市', '张家界市', '益阳市', '郴州市', '永州市', '怀化市', '娄底市', '湘西土家族苗族自治州'],
        '广东省': ['广州市', '韶关市', '深圳市', '珠海市', '汕头市', '佛山市', '江门市', '湛江市', '茂名市', '肇庆市', '惠州市', '梅州市', '汕尾市', '河源市', '阳江市', '清远市', '东莞市', '中山市', '潮州市' ,'揭阳市', '云浮市'],
        '广西壮族自治区': ['南宁市', '柳州市', '桂林市', '梧州市', '北海市', '防城港市', '钦州市', '贵港市', '玉林市', '百色市', '贺州市', '河池市', '来宾市', '崇左市'],
        '海南省': ['海口市', '三亚市', '三沙市', '儋州市'],
        '重庆市': ['重庆市'],
        '四川省': ['成都市', '自贡市', '攀枝花市', '泸州市', '德阳市', '绵阳市', '广元市', '遂宁市', '内江市', '乐山市', '南充市', '眉山市', '宜宾市', '广安市', '达州市', '雅安市', '巴中市', '资阳市', '阿坝藏族羌族自治州', '甘孜藏族自治州', '凉山彝族自治州'],
        '贵州省': ['贵阳市', '六盘水市', '遵义市', '安顺市', '毕节市', '铜仁市', '黔西南布依族苗族自治州', '黔东南苗族侗族自治州', '黔南布依族苗族自治州'],
        '云南省': ['昆明市', '曲靖市', '玉溪市', '保山市', '昭通市', '丽江市', '普洱市', '临沧市', '楚雄彝族自治州', '红河哈尼族彝族自治州', '文山壮族苗族自治州', '西双版纳傣族自治州', '大理白族自治州', '德宏傣族景颇族自治州', '怒江傈僳族自治州', '迪庆藏族自治州'],
        '西藏自治区': ['拉萨市', '日喀则市', '昌都市', '林芝市', '山南市', '那曲市', '阿里地区'],
        '陕西省': ['西安市', '铜川市', '宝鸡市', '咸阳市', '渭南市', '延安市', '汉中市', '榆林市', '安康市', '商洛市'],
        '甘肃省': ['兰州市', '嘉峪关市', '金昌市', '白银市', '天水市', '武威市', '张掖市', '平凉市', '酒泉市', '庆阳市', '定西市', '陇南市', '临夏回族自治州', '甘南藏族自治州'],
        '青海省': ['西宁市', '海东市', '海北藏族自治州', '黄南藏族自治州', '海南藏族自治州', '果洛藏族自治州', '玉树藏族自治州', '海西蒙古族藏族自治州'],
        '宁夏回族自治区': ['银川市', '石嘴山市', '吴忠市', '固原市', '中卫市'],
        '新疆维吾尔自治区': ['乌鲁木齐市', '克拉玛依市', '吐鲁番市', '哈密市', '昌吉回族自治州', '博尔塔拉蒙古自治州', '巴音郭楞蒙古自治州', '阿克苏地区', '克孜勒苏柯尔克孜自治州', '喀什地区', '和田地区', '伊犁哈萨克自治州', '城地区', '阿勒泰地区']
        }
    area_keys = list(area.keys())
    # 省份
    province = random.choice(area_keys)
    # 城市
    city = random.choice(area.get(province))
    return province, city

# province, city = get_random_city()
# print(province + city)


#得到音乐信息的子集，将每个用户的听歌记录缩减至30首
def get_min_song_info():
    # 文件路径名
    song_info_file_name = './dataset/new_song_info.txt'
    record_file_name = './dataset/user_record.txt'

    # 歌曲中id列表
    song_id_list = []
    # 歌曲音乐信息，内容唯一
    song_lines = []
    user_id = []
    i = 0
    print('读播放记录文件')
    with open(record_file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if line.split('\t')[0] not in user_id:
                user_id.append(line.split('\t')[0])
                i = 0
            # 获取播放次数最多的前30首
            print('前30首')
            if i < 30 and line.split('\t')[0] in user_id:
                song_id_list.append(line.split('\t')[1])
                i = i + 1
    f.close()

    # 筛选数据
    print('读音乐信息文件')
    with open(song_info_file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if line.split('\t')[0] in song_id_list:
                song_lines.append(line)
    f.close()

    # 将筛选之后的音乐数据覆盖掉原来的音乐数据
    print('生成新的音乐信息文件')
    with open('dataset/min_song_info.txt', 'a', encoding='utf-8') as f:
        for line in song_lines:
            f.write(line)
            f.flush()
    f.close()

# get_min_song_info()

#减少用户播放记录，每个用户30首
def get_min_user_record():
    record_file_name = './dataset/user_record.txt'
    min_record_file_name = './dataset/min_user_record.txt'
    user_id = []
    user_record_line = []
    print('读播放记录文件')
    with open(record_file_name, 'r', encoding='utf-8') as f, open(min_record_file_name, 'a', encoding='utf-8') as o_f:
        for line in f:
            if line.split('\t')[0] not in user_id:
                user_id.append(line.split('\t')[0])
                i = 0
            # 获取播放次数最多的前30首
            print(line.split('\t')[0] + '的前30首')
            if i < 15 and line.split('\t')[0] in user_id:
                o_f.write(line)
                o_f.flush()
                i = i + 1
    f.close()
    o_f.close()

# get_min_user_record()

