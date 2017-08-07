import jieba.analyse


def getkeystr(content):
    sep = jieba.analyse.extract_tags(content, topK=10, withWeight=True)
    keylist = []
    for a, b in sep:
        # if ord(a[0]) > 127:   #去掉英文
        keylist.append(a)
    keystr = ''.join(keylist)
    return keystr


content = '''李聿仁 :李聿仁，专业画家，号晟煜，昊宸，纳海阁主人。山东淄博人，大学学历，现居北京。  中国长城书画家协会理事，中国美术家协会河北省分会会员，中国收藏家协会会员，山东淄博职业学院艺术设计系大写意花鸟画客座教授。'''
a = getkeystr(content)
print(a)