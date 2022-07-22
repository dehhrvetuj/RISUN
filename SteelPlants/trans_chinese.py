#-*- coding:utf-8 -*-
import re

import numpy as np

coun_en = ["Oman", "Comoros", "Papua New Guinea", "Bolivia", "Sierra Leone", "Angola", "Slovakia",
           "France", "Benin", "Tunisia", "Liberia", "United Kingdom", "Argentina", "Ghana", "Finland",
           "Turkmenistan", "Norway", "Seychelles", "Western Sahara", "Viet Nam", "Equatorial Guinea",
           "Bangladesh", "Saint Vincent and the Grenadines", "Poland", "Gambia", "Kyrgyzstan",
           "Bosnia and Herzegovina", "Morocco", "Moldova", "Montenegro", "Nicaragua", "Peru",
           "Belgium", "Maldives", "Korea, South", "Libya", "Jordan", "Chile", "Cambodia", "Barbados",
           "Netherlands", "USA", "Togo", "Switzerland", "Cote D Ivoire", "Singapore", "Slovenia",
           "Indonesia", "Spain", "Mauritius", "Samoa", "Greece", "Kiribati", "Mongolia", "South Sudan",
           "Djibouti", "Venezuela", "Jamaica", "Korea, North", "Romania", "Croatia", "Albania",
           "Solomon Islands", "Tonga", "Madagascar", "Italy", "Bulgaria", "Democratic Republic of the Congo",
           "Panama", "Japan", "Israel", "Qatar", "Cook Islands", "Burkina Faso", "Armenia", "Honduras", "Turkey",
           "Uganda", "Bahrain", "East Timor", "Tajikistan", "Micronesia", "Saint Kitts and Nevis", "Myanmar",
           "New Zealand", "Latvia", "Lithuania", "Pakistan", "Austria", "Marshall Islands", "Thailand", "Brazil",
           "Georgia", "Estonia", "Laos", "Mexico", "Niger", "Gabon", "Antigua and Barbuda", "Cameroon", "Denmark",
           "Mauritania", "Germany", "Serbia", "South Africa", "Lesotho", "The Central African Republic", "Saint Lucia",
           "Eritrea", "Malawi", "Brunei", "Afghanistan", "Iran", "Lebanon", "Grenada", "Canada", "Haiti", "Ecuador",
           "Trinidad and Tobago", "Macedonia", "Mali", "India", "Sudan", "Ireland", "Egypt", "Fiji", "Iceland",
           "Andorra", "Iraq", "Burundi", "Sri Lanka", "The Republic of Congo", "Luxembourg", "Philippines", "Guinea",
           "Saudi Arabia", "Ukraine", "Russia", "Kenya", "Namibia", "Zambia", "United Arab Emirates", "Macao,China",
           "Malta", "Chad", "Australia", "Yemen", "China", "Kuwait", "Hong Kong,China", "Sweden", "Malaysia", "Monaco",
           "Nigeria", "Algeria", "Aruba", "American Samoa", "Bahamas", "Belize", "Bermuda", "Cyprus", "Dominica",
           "Dominican Republic", "El Salvador", "French Guiana", "French Polynesia", "Syria", "Taiwan", "Tanzania",
           "Vietnam", "Virgin Islands (U.S.)",
           "Uruguay", "Vanuatu", "United States", "Cuba",
           "Azerbaijan", "Belarus", "Czech Republic", "Ethiopia", "Guatemala", "Hungary", "Uzbekistan",
           "the Netherlands", "State of Qatar", "South Korea", "North Korea", "Republic of Korea", "Slovak Republic", "Portugal",
           "Kazakhstan", "Ethiopia"
           ]
coun_zh = ["阿曼", "科摩罗", "巴布亚新几内亚", "玻利维亚", "塞拉利昂", "安哥拉", "斯洛伐克", "法国", "贝宁", "突尼斯",
           "利比里亚", "英国", "阿根廷", "加纳", "芬兰", "土库曼斯坦", "挪威", "塞舌尔", "西撒哈拉", "越南", "赤道几内亚",
           "孟加拉国", "圣文森特和格林纳丁斯", "波兰", "冈比亚", "吉尔吉斯斯坦", "波黑", "摩洛哥", "摩尔多瓦",
           "黑山", "尼加拉瓜", "秘鲁", "比利时", "马尔代夫",  "韩国", "利比亚", "约旦", "智利", "柬埔寨", "巴巴多斯",
           "荷兰", "美国", "多哥", "瑞士", "科特迪瓦", "新加坡", "斯洛文尼亚", "印度尼西亚", "西班牙", "毛里求斯", "萨摩亚",
           "希腊", "基里巴斯", "蒙古", "南苏丹", "吉布提", "委内瑞拉", "牙买加" , "朝鲜", "罗马尼亚", "克罗地亚",
           "阿尔巴尼亚", "所罗门群岛", "汤加", "马达加斯加", "意大利", "保加利亚", "刚果民主共和国", "巴拿马","日本",
           "以色列", "卡塔尔", "库克群岛", "布基纳法索", "亚美尼亚", "洪都拉斯", "土耳其", "乌格达", "巴林", "东帝汶",
           "塔吉克斯坦", "密克罗尼西亚", "圣基茨和尼维斯", "缅甸", "新西兰", "拉脱维亚", "立陶宛", "巴基斯坦", "奥地利",
           "马绍尔群岛", "泰国", "巴西", "格鲁吉亚", "爱沙尼亚", "老挝", "墨西哥", "尼日尔", "加蓬", "安提瓜和巴布达", "喀麦隆",
           "丹麦", "毛里塔尼亚", "德国", "塞尔维亚", "南非", "莱索托", "中非共和国", "圣卢西亚", "厄立特里亚", "马拉维", "文莱",
           "阿富汗", "伊朗", "黎巴嫩", "格林纳达", "加拿大", "海地", "厄瓜多尔", "特立尼达和多巴哥", "马其顿", "马里", "印度",
           "苏丹", "爱尔兰", "埃及", "斐济", "冰岛", "安道尔", "伊拉克", "布隆迪", "斯里兰卡", "刚果共和国", "卢森堡", "菲律宾",
           "几内亚", "沙特阿拉伯", "乌克兰", "俄罗斯", "肯尼亚", "纳米比亚", "赞比亚", "阿联酋", "中国澳门", "马耳他",
           "乍得", "澳大利亚", "也门", "中国", "科威特", "中国香港", "瑞典", "马来西亚", "摩纳哥", "尼日利亚",
           "阿尔及利亚", "阿鲁巴", "美属萨摩亚", "巴哈马", "伯利兹", "百慕大", "塞浦路斯", "多米尼克", "多米尼加共和国",
           "萨尔瓦多", "法属圭亚那", "法属波利尼西亚", "叙利亚", "台湾", "坦桑尼亚", "越南", "维尔京群岛（美国）",
           "乌拉圭", "瓦努阿图", "美国", "古巴",
           "阿塞拜疆", "白俄罗斯", "捷克共和国", "埃塞俄比亚", "危地马拉", "匈牙利", "乌兹别克斯坦", "荷兰", "卡塔尔", "韩国",
           "朝鲜", "韩国", "斯洛伐克", "葡萄牙", "哈萨克斯坦", "埃塞俄比亚"
           ]

print(len(coun_en), len(coun_zh))


def trans_country(country):
    global coun_en, coun_zh
    coun_en = [x.lower() for x in coun_en]
    country = country.strip().lower()

    if country in coun_en:
        return coun_zh[coun_en.index(country)]
    else:
        return None


import pandas as pd

# input = pd.read_excel('世界钢厂列表.xlsx', index_col=0)
# input.sort_values(by=['国家(中文)', '工厂名称(英文)'], ascending=True, inplace=True, ignore_index=True)
# input.index += 1
# input.to_excel("世界钢厂列表2.xlsx")

#
# from interpretinfo import RemoveBrackets
# input = pd.read_excel('中国以外世界钢厂列表(产量产能单位为万吨).xlsx', index_col=0)
# input['所有者'] = input['所有者'].apply(lambda x: RemoveBrackets(x))
# input['母公司'] = input['母公司'].apply(lambda x: RemoveBrackets(x))
# input.to_excel("世界钢厂列表3.xlsx")
a = ''
a = list()
print(len(a))
print(True if a else False)
if len(a)==0:
    print("is null")
else:
    print("not null")

print(pd.isna(a))