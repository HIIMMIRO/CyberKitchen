import sys
from math import *
import numpy as np
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
            distance += sqrt(abs(float(user1_data[key]) - float(user2_data[key])))
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


# 归一化
def Normalization(sim_user_and_value,recommend_user_num):
    BN_sim_user_and_value=[]
    for l in range(recommend_user_num):
        BN_sim_user_and_value.append(float(1/sim_user_and_value[l][1]))
    value_max=np.max(BN_sim_user_and_value)
    BN_sim_user_and_value=BN_sim_user_and_value/value_max*5
    return BN_sim_user_and_value

# 求出似度最高得recommend_user_num个的用户
# 对用户优先级和用户给出的评分优先级分别加权
def recommend(user,recommend_user_num):
    top_sim_user_list=[]
    food_list=[]
    sim_user_and_value=top_simliar(user)
    for i in range(recommend_user_num):
        top_sim_user = sim_user_and_value[i][0]
        top_sim_user_list.append(top_sim_user)
        food_list.append(data[top_sim_user])
    BN_sim_user_and_value=(Normalization(sim_user_and_value,recommend_user_num))
    recommendations = []
    for n in range(recommend_user_num):
        for food in food_list[n].keys():
            if food not in data[user].keys():
                if(float(food_list[n][food])>=4.0):
                    recommendations.append((food,float(food_list[n][food]) +BN_sim_user_and_value[n]))
                    # 按照评分排序
    recommendations.sort(key=lambda val: val[1], reverse=True)
    return recommendations

if __name__ == "__main__":
    print(recommend('1',2))