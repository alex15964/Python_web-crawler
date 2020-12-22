import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials   #導入module

def upload_to_gs(items):
    scopes = ["https://spreadsheets.google.com/feeds"]    #GS網址
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)   #取得驗證檔
    client = gspread.authorize(credentials)   #比對驗證
    sheet = client.open_by_key("1e8bhnsW13AmfJwYB3hlUUX35pPHQruzXLJvOa1QVaaw").sheet1  #取得第一個工作表的網址跟名稱

    sheet.append_rows(items)    #把list全部新增到GS上

r = requests.get('https://www.ptt.cc/bbs/Chiayi/index.html', verify = False)    #連線網站
if r.status_code == requests.codes.ok:  #如果連線成功，則取得網站資料
    soup = BeautifulSoup(r.text, 'html.parser')

    items = soup.find_all('div', class_='r-ent')    #用r-ent為名的class分段
    articles = []
    for s in items:
        title_item = s.select_one('div.title')   #用title為名的class分段
        title = title_item.text   #找出title底下的字
        if '(本文已被刪除)' in title:    #若文章被刪除，則輸入文章已被刪除的文字
            continue
        else:   #若文章未刪除則輸入文章標題跟連結
            href_item = title_item.select_one('a').get('href')   #找出文章連結並寫入
            author = s.select_one('div.author').text    #找出文章作者並寫入
            articles.append([title, 'https://www.ptt.cc' + href_item, author])

upload_to_gs(articles)