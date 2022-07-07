import re
# import unidecode
# word = unidecode.unidecode(word)

def SearchForCountry(content):
    if content is None:
        return None

    if not [x for x in content if 'Country' in x]:
        return None

    content = [x.strip() for x in content if x]
    content = ' '.join(content)

    output = re.findall(r"Country\s+([a-zA-Z ]+)$", content)

    return ''.join(output).strip()


def SearchForCoordinates(content, flag='lattitude'):
    if content is None:
        return None

    if not [x for x in content if 'Coordinates' in x]:
        return None

    content = [x.strip() for x in content if x]
    content = ' '.join(content)

    if flag == 'lattitude':
        output = re.findall(r"\-?\d+\°\d+\′\d+\″\s?[NS]", content)
    else:
        output = re.findall(r"\-?\d+\°\d+\′\d+\″\s?[EW]", content)

    if output:
        return output[0]
    else:
        return None


def SearchForCargo(content):
    if content is None:
        return None

    content = [x.strip() for x in content if x]
    content = ' '.join(content)

    if re.search(r"annual cargo tonnage", content, re.I) is not None:
        return re.sub(r"[\[].*?[\]]", " ", content).strip()
    else:
        return None

def SearchForContainer(content):
    if content is None:
        return None

    content = [x.strip() for x in content if x]
    content = ' '.join(content)


    if re.search(r"annual[\s]+container[\s]+volume", content, re.I) is not None:
        return re.sub(r"[\[].*?[\]]", " ", content).strip()
    else:
        return None


def SearchForLocation(content):
    if content is None:
        return None
    if not [x for x in content if 'Location' in x]:
        return None
    if len(content) <= 1:
        return None

    content = [x.strip() for x in content if x]
    content = ' '.join(content)

    output = re.findall(r"Location\s+([a-zA-Z ]+)$", content)

    return ''.join(output).strip()