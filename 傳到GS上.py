import gspread
from oauth2client.service_account import ServiceAccountCredentials   #導入module

def upload_to_gs(items):
    scopes = ["https://spreadsheets.google.com/feeds"]    #GS網址
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)   #取得驗證檔
    client = gspread.authorize(credentials)   #比對驗證
    sheet = client.open_by_key("1e8bhnsW13AmfJwYB3hlUUX35pPHQruzXLJvOa1QVaaw").sheet1  #取得第一個工作表的網址跟名稱
    for i in items:
	    sheet.append_row(i)   #一次新增一行到sheet上

article = [('1', '2', '3'), ('1', '2', '3'), ('1', '2', '3')]   #只有list可以上傳
upload_to_gs(article)