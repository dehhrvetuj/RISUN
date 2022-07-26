import re
import pandas as pd


data = pd.read_excel("中国以外世界钢厂列表(产量产能单位为万吨).xlsx", index_col=0)

def BF(x):
    x = "" if pd.isnull(x) else x
    if re.search(r"高炉", x) or re.search(r"BF", x) or re.search(r"blast", x, flags=re.I):
        return True
    else:
        return False


# long_process = data[data['设备类型'].apply(lambda x: BF(x))].copy()
long_process = data[data['设备类型'].apply(lambda x: BF(x)) | data['设备详细'].apply(lambda x: BF(x))].copy()
long_process.reset_index(inplace=True, drop=True)
long_process.index += 1

long_process.to_excel('长流程钢厂.xlsx')