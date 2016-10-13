from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
ceshi = client['ceshi']
url_list = ceshi['url_list3']
item_info = ceshi['item_info3']

#spider 1 爬取商品链接
def get_links_from(channel,pages):   #who_salls为0默认为个人（商家）
    list_view = '{}/pn{}/'.format(channel,str(pages))
   # http://bj.58.com/diannao/pn2/
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text,'lxml')
    if soup.find('td','t'):
        for link in soup.select('td.t a.t'):         #定位商品名称
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url':item_link}) #数据库中插入链接
            print(item_link)
    else:
        pass         # Nothing
#get_links_from('http://bj.58.com/shouji/',2)

#spider 2
def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    no_longer_exist = '404' in soup.find('script', type="text/javascript").get('src').split('/')
    if no_longer_exist:
        pass
    else:
        title = soup.title.text
        price = soup.select('span.price.c_f50')[0].text
        date = soup.select('.time')[0].text
        area = list(soup.select('.c_25d a')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None
        item_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})
        print({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})

#get_item_info('http://zhuanzhuan.58.com/detail/785791497196306436z.shtml')
#url = 'http://bj.58.com/shouji/24605954621114x.shtml'
#wn_data = requests.get(url)
#oup = BeautifulSoup(wb_data.text,'lxml')
#print(soup.prettify)
#过滤404页面