import sys
from math import *
import numpy as np
user_information = []
food_information=[]
recipe_information=[]
user_info_dict={}
food_info_dict={}
recipe_info_dict={}

with open('./database/user_info.txt',encoding='utf-8') as fp:
    user_information = fp.readlines()
with open('./database/food_info.txt',encoding='utf-8') as fp:
    food_information = fp.readlines()
with open('./database/recipe_info.txt', encoding='utf-8') as fp:
    recipe_information = fp.readlines()

def processFile(info_dict,typeOfInfo):
    temp_dict = {}
    if(typeOfInfo==1):
        # 将用户、评分、和食物写入字典data
        for line in info_dict:
            line = line.strip().split(',')
            # 如果字典中没有某位用户，则使用用户ID来创建这位用户
            if not line[0] in temp_dict.keys():
                temp_dict[line[0]] = {line[1]: line[2]}
            else:
                temp_dict[line[0]][line[1]] = line[2]
    elif(typeOfInfo==2):
        for line in info_dict:
            line = line.strip().split(',')
            # 如果字典中没有某位用户，则使用用户ID来创建这位用户
            temp_dict[line[0]] = {line[1]}
    return  temp_dict

def Euclid(user1, user2):
    # 取出两位用户购买过的手机和评分
    user1_data = user_info_dict[user1]
    user2_data = user_info_dict[user2]
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
    for userid in user_info_dict.keys():
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
        food_list.append(user_info_dict[top_sim_user])
    BN_sim_user_and_value=(Normalization(sim_user_and_value,recommend_user_num))
    recommendations = []
    for n in range(recommend_user_num):
        for food in food_list[n].keys():
            if food not in user_info_dict[user].keys():
                if(float(food_list[n][food])>=4.0):
                    recommendations.append((food,float(food_list[n][food]) +BN_sim_user_and_value[n]))
                    # 按照评分排序
    recommendations.sort(key=lambda val: val[1], reverse=True)
    recommendations_list=[]
    for i in range(len(recommendations)):
        recommendations_list.append(list(recommendations[i]))
        temp=recommendations_list[i][0]
        recommendations_list[i][0]=str(food_info_dict.get(temp))
        recommendations_list[i].append(str(recipe_info_dict.get(temp)))
    return recommendations_list,recommendations

if __name__ == "__main__":
    user_info_dict = processFile(user_information,1)
    food_info_dict = processFile(food_information,2)
    recipe_info_dict=processFile(recipe_information,2)
    recommendationslist,recommendations=recommend('1',2)
    print("recommendations",recommendations)
    print("recommendationslist",recommendationslist)
