import requests
from bs4 import BeautifulSoup   #module檔入
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

article = ['adate':[], 'content':[], 'link':[]]
recipes_num = 0 #食譜數量
wn = 3850   #網址

def to_csv():   #寫入csv
    itr = pd.DataFrame(article)
    itr.to_csv('recipe.csv', encoding= 'utf_8_sig', index = False)

while recipes_num < 100:  #至少找到5個食譜
    r = requests.get('https://www.ptt.cc/bbs/cookclub/index' + str(wn) +'.html')    #連線網站
    if r.status_code == requests.codes.ok:  #如果連線成功，則取得網站資料
        soup = BeautifulSoup(r.text, 'html.parser')

        items = soup.find_all('div', class_='r-ent')    #用r-ent為名的class分段

        for s in items:
            titles = s.select('div.title')
            for title in titles:    #輸入標題是心得跟食譜的文章
                if '[心得]' in title.text:
                    article['content'].append(title.text)
                    recipes_num += 1
                elif '[食譜]' in title.text:
                    article['content'].append(title.text)
                    recipes_num += 1
                else :
                    break

                links = title.select('a')
                for link in links:
                    article['link'].append('https://www.ptt.cc' + link.get('href'))

                dates = s.select('div.date')    #輸入日期
                for date in dates:
                    article['adate'].append(date.text)
    wn -= 1
to_csv()