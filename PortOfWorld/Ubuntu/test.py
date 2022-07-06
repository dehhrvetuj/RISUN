from bs4 import BeautifulSoup
import requests, json

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

html = requests.get('https://www.google.com/search?q=ice cream', headers=headers)
soup = BeautifulSoup(html.text, 'lxml')

print(soup.text)
# collect data
data = []

result_div = soup.find_all('div', attrs={'class': 'yuRUbf'})

print(result_div)

# for result in soup.select('.tF2Cxc'):
#   title = result.select_one('.DKV0Md').text
#   link = result.select_one('.yuRUbf a')['href']
#   snippet = result.select_one('#rso .lyLwlc').text
#
#   print(title,'-')
#   print(link,'-')
#   print(snippet)
#
#   # appending data to an array
#   data.append({
#       'title': title,
#       'link': link,
#       'snippet': snippet,
#   })
#
# print(json.dumps(data, indent=2, ensure_ascii=False))