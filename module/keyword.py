## keyword finder ##

# EX title pattern : Supreme®/Nike® Air Max Dn, Small Box Hooded Sweatshirt, Futura Sweater
# EX Size pattern : US7.5/UK6.5, US7.5/UK6.5

from requests_html import HTMLSession
import requests
import json
from bs4 import BeautifulSoup

with open('info.json', 'r') as rd:
        j = json.load(rd)
        d_keyword = j['Product']['keyword']
        form = j['Product']['Color']
        d_color = [form]


header = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type' : 'application/json; text/plain',
        'Accept' : '*/*',    
        'Origin' : 'https://eu.supreme.com',
        'Referer' : 'https://eu.supreme.com/cart',
    }    



def keyword_finder(keyword):
    r = HTMLSession()
    base = r.get('https://eu.supreme.com/collections/new')
    print('\033[1;33mFetch data..', end='\r')

    base.html.render()
    soup = BeautifulSoup(base.html.html, 'html.parser')
    el = soup.find('div', {'class', 'scroll-content'})
    a = el.find('ul')
    prep = a.find_all('li')

    stock = []
    for i in prep:
        h = i.find_all('a')
        for title in h:
                title_all = title.get('data-cy-title')
                link_all = title.get('href')

                stock.append([title_all, link_all])
    target_keyword(keyword, stock)


def target_keyword(keyword, stock) :
    stock_url = []
    for value in stock :
            if keyword in value :
                ## title = value[0] href = value[1] ##
                url = f'https://eu.supreme.com{value[1]}'
                stock_url.append(url)   
    color_finder(stock_url)
    

def color_finder(link):
    stock = []
    for i in link :
        r = requests.Session()

        base = r.get(i)
        soup = BeautifulSoup(base.text, 'lxml')
        id = soup.find("script", {'class', 'js-product-json'})
        data = json.loads(id.text)

        product_color = data['product']['tags'][0].replace('color:','')
        in_stock = data['product']['available']

        stock.append([i, product_color, in_stock])
        print(f'found : Link : {stock[0]} Color : {stock[1]} Available : {stock[2]}')
        

if __name__ == "__main__":
    pass


keyword_finder('Cashmere Sweater')