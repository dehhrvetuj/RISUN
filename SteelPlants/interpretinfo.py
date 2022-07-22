import re
import pandas as pd


def None2Null(x):
    return '' if pd.isnull(x) or x is None else x


def list2str(x):
    return None if len(x) == 0 else ' '.join(x)


def str2num(text):
    return max([float(x.strip()) for x in text.strip().split() if x]) if text else None


def add(*x):
    assert len(x) > 0
    num = len(x)
    y = [x[i] for i in range(0, num) if not pd.isnull(x[i])]
    return sum(y) if y else None


def Convert(x):
    if pd.isnull(x) or x == 0:
        return None
    else:
        return x / 10.0


def RemoveBrackets(text):
    return None if text is None or pd.isnull(text) else re.sub(r"\[.*?\]", "", text).strip()


def RemoveRedundantSpace(text):
    return re.sub(r"\s{2,}", " ", text if text is not None else "")


def GPSCoord(text):
    if pd.isnull(text):
        return pd.Series([None, None])

    text = re.sub(r"[\(\[].*?[\)\]]", "", text).strip()

    try:
        coord = [float(x.strip()) for x in text.split(',') if x]
        assert len(coord) == 2
        return pd.Series(coord)
    except:
        return pd.Series([None, None])


def Country(text):
    if pd.isnull(text):
        return None

    text = re.sub(r"\[.*?\]", "", text)  # Remove all brackets
    text = re.sub(r"-", " ", text)
    text = re.sub(r"[a-zA-Z]*?\d+[a-zA-Z]*", "", text).strip()  # Remove all numbers and number-associated
    text = next(iter(re.findall(r"[,.;]\s?([a-zA-Zé ]*?)[,.;]?$", text)), None)
    if text is not None and re.search(r"Province", text, flags=re.I):
        text = "China"  # + " " + text

    return None2Null(text).strip()


def DropChina(text):
    if re.search(r"[\u4e00-\u9fa5]{4:}", text, flags=re.I):
        return False
    else:
        return True


def Equipment(text):
    if pd.isnull(text):
        return None

    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\(.*?\)", "", text)

    text = re.sub(r"blast furnace[s]? ", "BF", text, flags=re.I)
    text = re.sub(r"basic oxygen furnace[s]? ", "BOF", text, flags=re.I)
    text = re.sub(r"electric arc furnace[s]? ", "EAF", text, flags=re.I)
    text = re.sub(r"direct reduced iron", "DRI", text, flags=re.I)
    text = re.sub(r"argon[- ]oxygen decarburization", "AOD", text, flags=re.I)
    text = re.sub(r"coking plant[s]?", "CP", text, flags=re.I)
    text = re.sub(r"coke oven[s]?|coking over[s]?", "CO", text, flags=re.I)
    text = re.sub(r"sinter plant[s]?|sintering plant[s]?", "SP", text, flags=re.I)
    text = re.sub(r"pellet plant[s]?|pelletizing plant[s]?]", "PP", text, flags=re.I)

    text = re.sub(r"\(BF.*?\)|\(BOF.*?\)|\(EAF.*?\)|\(DRI.*?\)|\(AOD.*?\)", "", text)
    text = re.sub(r"\(.*?unknown\)", "", text, re.I)

    return RemoveRedundantSpace(text)


# print(Equipment("sinter plant ;  coke ovens  (# unknown); 2  blast furnaces (BF) ; \
#                 3  basic oxygen furnaces (BOF) ,  direct reduced iron (DRI) plant [2] [5] [6]"))

def MainEquip(text):
    if pd.isnull(text):
        return None

    equip = list()

    if re.search(r"BF", text):
        equip.append("高炉(BF)")
    if re.search(r"BOF", text):
        equip.append("氧气顶吹转炉(BOF)")
    if re.search(r"EAF", text):
        equip.append("电弧炉(EAF)")
    if re.search(r"AOD", text):
        equip.append("AOD炉")
    if re.search(r"DRI", text):
        equip.append("直接还原铁(DRI)")
    if re.search(r"CP|CO", text):
        equip.append("炼焦炉")
    if re.search(r"PP", text):
        equip.append("球团")
    if re.search(r"SP", text):
        equip.append("烧结")

    return "、".join(equip)


def Status(text):
    if pd.isnull(text):
        return None

    text = re.sub(r"[\[].*?[\]]", "", text).strip()

    # r"(?<!\()\boperating\b(?![\w\s]*[\)])"
    text = re.sub(r"operating", "运营", text, flags=re.I)
    text = re.sub(r"closed", "关闭", text, flags=re.I)
    text = re.sub(r"construction", "在建", text, flags=re.I)
    text = re.sub(r"mothballed", "封存", text, flags=re.I)
    text = re.sub(r"proposed", "提议", text, flags=re.I)
    text = re.sub(r"idled", "闲置", text, flags=re.I)

    years = re.findall(r"in (.*?[0-9][0-9][]0-9][0-9])", text)
    for year in years:
        text = re.sub(f"in {year}", f"({year})", text)

    return text


def IsCoking(text):
    if pd.isnull(text) or not text:
        return None

    return "是" if re.search(r"coking plant|coking oven", text.strip(), flags=re.I) else "否"


def IsShort(text):
    if pd.isnull(text) or not text:
        return None
    if re.search(r"blast furnace|basic oxygen furnace|BF|BOF", text, flags=re.I):
        return "长"
    elif re.search(r"electric arc furnace|EAF", text, flags=re.I):
        return "短"
    else:
        return None


def Production(text):
    if pd.isnull(text):
        return pd.Series([None] * 10)

    total = list()
    crude_steel = list()
    crude_steel_bof = list()
    crude_steel_eaf = list()
    crude_iron = list()
    crude_iron_bf = list()
    crude_iron_dri = list()
    steel_prod = list()
    coking_plant = list()
    other = list()

    entries = [entry.strip() for entry in RemoveBrackets(text).split('\n') if len(entry) > 0]
    entries = [entry for entry in entries if entry != '2020' or entry != '2019']

    for entry in entries:
        # Extract numbers from the entry
        num = re.findall(r"(\d+\.?\d*)", re.sub(r"[\(\（].*?[\)\）]", "", entry), flags=re.I)
        if len(num) == 0:  # if no number exists, proceed to next entry
            continue
        else:
            num = num[0]

        if re.search(r"Basic oxygen furnace|BOF/BF|BOF", entry, flags=re.I):
            crude_steel_bof.append(num)
        elif re.search(r"electric arc furnace|EAF", entry, flags=re.I):
            crude_steel_eaf.append(next(iter(re.findall(r"(\d+\.?\d*)", entry, flags=re.I)), ''))
        elif re.search(r"crude steel", entry, flags=re.I):
            crude_steel.append(num)
        elif re.search(r"Blast furnace|BF", entry, flags=re.I):
            crude_iron_bf.append(num)
        elif re.search(r"direct reduced iron|DRI", entry, flags=re.I):
            crude_iron_dri.append(num)
        elif re.search(r"crude iron|pig iron|iron|hot metal", entry, flags=re.I):
            crude_iron.append(num)
        elif re.search(r"steel product", entry, flags=re.I):
            steel_prod.append(num)
        elif re.search(r"coking plant|coking|coke", entry, flags=re.I):
            coking_plant.append(num)
        elif re.search(r"^\s*(\d+\.?\d*)", entry, flags=re.I):
            total.append(num)
        elif re.search(r"(\d+\.?\d*)", entry, flags=re.I):  # [^0-9]*?\s(\d+\.?\d*)
            other.append(num)

    # crude_steel = max(crude_steel, max(crude_steel_bof) + max(crude_steel_eaf))
    # crude_iron = max(crude_iron, max(crude_iron_bf) + max(crude_iron_dri))

    return pd.Series(
        [list2str(total),
         list2str(crude_steel), list2str(crude_steel_eaf), list2str(crude_steel_bof),
         list2str(crude_iron), list2str(crude_iron_bf), list2str(crude_iron_dri),
         list2str(steel_prod),
         list2str(coking_plant),
         list2str(other)])  # '@'.join(entries),

    # return pd.Series(
    #     [' '.join(total),
    #      ' '.join(crude_steel),  ' '.join(crude_steel_eaf), ' '.join(crude_steel_bof),
    #      ' '.join(crude_iron), ' '.join(crude_iron_bf), ' '.join(crude_iron_dri),
    #      ' '.join(steel_prod),
    #      ' '.join(coking_plant),
    #      ' '.join(other)])  # '@'.join(entries),

    # return pd.Series(
    #     ['\n'.join(entries), total,
    #      crude_steel,  crude_steel_eaf, crude_steel_bof,
    #      crude_iron, crude_iron_bf, crude_iron_dri,
    #      steel_prod,
    #      coking_plant,
    #      other]
    # )  # '@'.join(entries),


def Capacity(text):
    if pd.isnull(text):
        return pd.Series([None] * 11)

    total = list()
    crude_steel = list()
    crude_steel_bof = list()
    crude_steel_eaf = list()
    crude_iron = list()
    crude_iron_bf = list()
    crude_iron_dri = list()
    coking_plant = list()
    sinter = list()
    pellet = list()
    other = list()

    entries = [entry.strip() for entry in RemoveBrackets(text).split('\n') if len(entry) > 0]
    entries = [entry for entry in entries if entry != '2020' or entry != '2019']

    for entry in entries:
        # Extract numbers from the entry
        num = re.findall(r"(\d+\.?\d*)", re.sub(r"[\(\（].*?[\)\）]", "", entry), flags=re.I)
        if len(num) == 0:  # if no number exists, proceed to next entry
            continue
        else:
            num = num[0]

        if re.search(r"Basic oxygen furnace|BOF/BF|BOF", entry, flags=re.I):
            crude_steel_bof.append(num)
        elif re.search(r"electric arc furnace|EAF", entry, flags=re.I):
            crude_steel_eaf.append(next(iter(re.findall(r"(\d+\.?\d*)", entry, flags=re.I)), ''))
        elif re.search(r"crude steel", entry, flags=re.I):
            crude_steel.append(num)
        elif re.search(r"Blast furnace|BF", entry, flags=re.I):
            crude_iron_bf.append(num)
        elif re.search(r"direct reduced iron|DRI", entry, flags=re.I):
            crude_iron_dri.append(num)
        elif re.search(r"crude iron|pig iron|iron|hot metal", entry, flags=re.I):
            crude_iron.append(num)
        elif re.search(r"coke|coking", entry, flags=re.I):
            coking_plant.append(num)
        elif re.search(r"sinter", entry, flags=re.I):
            sinter.append(num)
        elif re.search(r"pellet", entry, flags=re.I):
            pellet.append(num)
        elif re.search(r"^\s*(\d+\.?\d*)", entry, flags=re.I):
            total.append(num)
        elif re.search(r"(\d+\.?\d*)", entry, flags=re.I):  # [^0-9]*?\s(\d+\.?\d*)
            other.append(num)

    return pd.Series(
        [list2str(total),
         list2str(crude_steel), list2str(crude_steel_eaf), list2str(crude_steel_bof),
         list2str(crude_iron), list2str(crude_iron_bf), list2str(crude_iron_dri),
         list2str(coking_plant), list2str(sinter), list2str(pellet),
         list2str(other)])  # '@'.join(entries),

    # return pd.Series(
    #     [' '.join(total),
    #      ' '.join(crude_steel),  ' '.join(crude_steel_eaf), ' '.join(crude_steel_bof),
    #      ' '.join(crude_iron), ' '.join(crude_iron_bf), ' '.join(crude_iron_dri),
    #      ' '.join(coking_plant), ' '.join(sinter), ' '.join(pellet),
    #      ' '.join(other)])  # '@'.join(entries),


# def fillnull():
#
#
#
#     pass

if __name__ == "__main__":
    # test = pd.read_excel('production.xlsx', index_col=0)
    #
    # test[['original', 'total', 'steel', 'eaf', 'bof', 'iron', 'bf', 'dri', 'product', 'coking', 'other']] = test['production'].apply(lambda x: Production(x))
    #
    # # print(test['production'].apply(lambda x: Production(x)).head(20))
    #
    # test.to_excel('production3.xlsx')

    # test = pd.read_excel('iron_cap.xlsx', index_col=0)
    #
    # test[['total', 'steel', 'eaf', 'bof', 'iron', 'bf', 'dri', 'coking', 'sinter', 'pellet', 'other']] = test['iron_cap'].apply(lambda x: IronCap(x))
    #
    # # print(test['production'].apply(lambda x: Production(x)).head(20))
    #
    # test.to_excel('iron_cap.xlsx')

    test = pd.read_excel('steel_cap.xlsx', index_col=0)

    test[['total', 'steel', 'eaf', 'bof', 'iron', 'bf', 'dri', 'coking', 'sinter', 'pellet', 'other']] = test[
        'steel_cap'].apply(lambda x: IronCap(x))

    # print(test['production'].apply(lambda x: Production(x)).head(20))

    test.to_excel('steel_cap.xlsx')
