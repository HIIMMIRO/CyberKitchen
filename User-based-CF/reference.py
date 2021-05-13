# date:20210511
# author:lishaodong
import sys
from math import *
content = []
data = {}
with open('./data.txt',encoding='utf-8') as fp:
    content = fp.readlines()

# 将用户、评分、和食物写入字典data
for line in content:
    line = line.strip().split(',')
    #如果字典中没有某位用户，则使用用户ID来创建这位用户
    if not line[0] in data.keys():
        data[line[0]] = {line[1]:line[2]}
    #否则直接添加以该用户ID为key字典中
    else:
        data[line[0]][line[1]] = line[2]
# print(data['1']['水煮牛肉'])

def Euclid(user1, user2):
    # 取出两位用户购买过的手机和评分
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0
    # 找到两位用户都吃过的食物，计算欧式距离
    for key in user1_data.keys():
        if key in user2_data.keys():
            # distance越小表示越相似。
            # distance为0表示无相似性。
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)
    if distance==0:
        return sys.maxsize
    else:
        return distance


#计算某个用户与其他用户的相似度
def top_simliar(userID):
    res = []
    for userid in data.keys():
        #排除与自己计算相似度
        if not userid == userID:
            simliar = Euclid(userID,userid)
            res.append((userid,simliar))
    res.sort(key=lambda val:val[1])
    return res

def recommend(user):
    #相似度最高的用户
    top_sim_user = top_simliar(user)[0][0]
    #相似度最高的用户的购买记录
    items = data[top_sim_user]
    recommendations = []
    #筛选出该用户未购买的手机并添加到列表中
    for item in items.keys():
        if item not in data[user].keys():
            recommendations.append((item,items[item]))
    recommendations.sort(key=lambda val:val[1],reverse=True)#按照评分排序
    return recommendations

print(recommend('1'))