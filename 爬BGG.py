import time
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials   #導入module

def upload_to_gs(items):
    scopes = ["https://spreadsheets.google.com/feeds"]    #GS網址
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)   #取得驗證檔
    client = gspread.authorize(credentials)   #比對驗證
    sheet = client.open_by_key("").sheet1  #取得第一個工作表的網址跟名稱
    sheet.append_rows(items)

r = requests.get('https://boardgamegeek.com/browse/boardgame', verify = False)    #連線網站
if r.status_code == requests.codes.ok:  #如果連線成功，則取得網站資料
    soup = BeautifulSoup(r.text, 'html.parser')

    items = soup.find_all('tr', id = 'row_')    #用row_為名的tr分段
    
    bgs = []
    n = 0
    for s in items:
        results_item = s.find('div', id = 'results_objectname' + str(n+1))   #用results為名的div分段

        a_item = results_item.select_one('a')
        name = a_item.text   #找出a底下的字
        href_item = a_item.get('href')   #找出文章連結

        bgs.append([n+1, name, 'https://boardgamegeek.com' + href_item])
        
        n += 1
        #if n > 3:
        #    break;

upload_to_gs(bgs)