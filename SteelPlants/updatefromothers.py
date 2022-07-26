import re
import pandas as pd
from one2one import one2one


def GetChinese(text):
    return ''.join(re.findall(r"[\u4e00-\u9fa5].*[\u4e00-\u9fa50-9%]", '' if pd.isnull(text) else text))


def BFInfo(text):
    if pd.isnull(text) or text == "":
        return None
    info_lst = text.split(';')
    output = ''.join([info for info in info_lst if re.search(r"BF|blast", info, flags=re.I)])
    return re.sub(r"blast furnace[s]? ", "BF", output, flags=re.I).strip()


def CokeInfo(text):
    if pd.isnull(text) or text == "":
        return None
    info_lst = text.split(';')
    return ''.join([info for info in info_lst if re.search(r"coking|coke", info, flags=re.I)]).strip()


mines = pd.read_excel("中国以外世界长流程钢厂.xlsx", index_col=0, sheet_name='Sheet1')
other = pd.read_excel("中国以外世界长流程钢厂.xlsx", sheet_name='Sheet2')

mines['高炉信息'] = mines['设备详细'].apply(lambda x: BFInfo(x))
mines['焦炉信息'] = mines['设备详细'].apply(lambda x: CokeInfo(x))

for i, j in enumerate(one2one):
    if not j:
        # mines = pd.concat([mines, pd.DataFrame({'国家(中文)': other.loc[i, '国家'], '客户名称': other.loc[i, '客户'],
        #                                         '高炉信息': other.loc[i, '高炉信息（座）'], '焦炉信息': other.loc[i, '焦炉信息（座）'],
        #                                         '焦炭缺口(万吨)': other.loc[i, '焦炭缺口（万吨）'], '基本情况': other.loc[i, '基本情况']},
        #                                         index=[0])],
        #                   ignore_index=True)
        continue

    if type(j) is not list:
        j = [j]

    for k in j:
        mines.loc[k, "客户名称"] = other.loc[i, '客户']
        mines.loc[k, "焦炭缺口(万吨)"] = other.loc[i, '焦炭缺口（万吨）']
        mines.loc[k, "基本情况"] = other.loc[i, '基本情况']

        if pd.notnull(other.loc[i, '焦炉信息（座）']):
            mines.loc[k, "焦炉信息"] = other.loc[i, '焦炉信息（座）']
            num = re.findall(r"([0-9]+)[ ]*?万吨", str(other.loc[i, '焦炉信息（座）']))
            if len(num) > 0:
                mines.loc[k, "焦化产能(万吨)"] = num[0]

        if pd.notnull(other.loc[i, '高炉信息（座）']):
            mines.loc[k, "高炉信息"] = other.loc[i, '高炉信息（座）']
        if pd.notnull(other.loc[i, '粗钢产能(万吨)']):
            mines.loc[k, '粗钢总产能(万吨)'] = other.loc[i, '粗钢产能(万吨)']

        # mines.loc[k, ["客户名称", "高炉信息", "焦炉信息", "焦炭缺口（万吨）", "基本情况"]] \
        #         = other.loc[i, ['客户', '高炉信息（座）', '焦炉信息（座）', '焦炭缺口（万吨）', '基本情况']]

mines['客户名称'] = mines['客户名称'].apply(lambda x: GetChinese(x))

for i, j in enumerate(one2one):
    if not j:
        mines = pd.concat([mines, pd.DataFrame({'国家(中文)': other.loc[i, '国家'], '客户名称': other.loc[i, '客户'],
                                                '高炉信息': other.loc[i, '高炉信息（座）'], '焦炉信息': other.loc[i, '焦炉信息（座）'],
                                                '焦炭缺口(万吨)': other.loc[i, '焦炭缺口（万吨）'], '基本情况': other.loc[i, '基本情况']},
                                               index=[0])],
                          ignore_index=True)

mines.reset_index(inplace=True, drop=True)

mines.index += 1
mines[['国家(中文)', '客户名称', '工厂名称(英文)', '设备类型', '高炉信息', '粗钢总产能(万吨)', '焦炉信息', '焦化产能(万吨)', '焦炭缺口(万吨)', '状态', \
       "基本情况", '位置', '纬度坐标', '经度坐标', '所有者', '母公司']].to_excel("update_test.xlsx")
