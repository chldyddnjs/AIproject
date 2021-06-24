import requests
url = "http://www.kric.go.kr/jsp/industry/rss/citystapassList.jsp?q_org_cd=A010010021&q_fdate=2020"

html_text = requests.get(url).text

#parsing 
#태그들을 하나하나 찾아서 연결해주는 것을 파싱이라한다.
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_text,"html.parser")

#Manipulation
#table 가져오기
tab = soup.find("table",{"class":"listtbl_c100"})
trs = tab.find('tbody').find_all('tr')

tdcols = trs[1].find("td",{"class":"tdcol"})
tds = trs[1].find_all('td')

print(tds[0].text)
print(tds[2].text)

stationpassengers = []
for tr in trs[1:]:
    dic = {}
    tds = tr.find_all('td')
    dic['station'] = tds[0].text
    dic['ride'] = tds[2].text
    dic['alight'] = tds[3].text
    stationpassengers.append(dic)

print(stationpassengers)