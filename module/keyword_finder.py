## keyword finder ##

# EX pattern : Supreme®/Nike® Air Max Dn, Small Box Hooded Sweatshirt, Futura Sweater

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
    print('\033[1;33mFetch data..', end='\r')
    link_Stock = []
    title_stock = []
    r = HTMLSession()

    base = r.get('https://eu.supreme.com/collections/new')
    base.html.render()
    
    soup = BeautifulSoup(base.html.html, 'html.parser')
    el = soup.find('div', {'class', 'scroll-content'})
    a = el.find('ul')
    prep = a.find_all('li')

    for i in prep:
        h = i.find_all('a')
        for title in h:
                t = title.get('data-cy-title')
                #print('title : ' + title.get('data-cy-title'), 'href : ' + title.get('href'))
                if keyword.lower() in t.lower():
                    titles = title.get('data-cy-title')    
                    href = title.get('href')
                    url = f'https://eu.supreme.com{href}' 

                    ## list lien ##

                    title_stock.append(titles)
                    link_Stock.append(url)
                    break


    if title_stock == [] or title_stock == '[]':
        print('\033[1;31mProduct Not found')
        exit()


    if link_Stock:
        print(f'\033[1;32mProduct found : {titles}')       
        for i in link_Stock:
            stock = []
            r = requests.Session()
    
            base = r.get(i)
            soup = BeautifulSoup(base.text, 'lxml')
            id = soup.find("script", {'class', 'js-product-json'})
            data = json.loads(id.text)

            product_color = data['product']['tags'][0].replace('color:','')
            in_stock = data['product']['available']

            if product_color == form :
                print(f'\033[1;32mColor found : {form}')
                stock.append(i)

                return stock[0]
            else :
                if in_stock == True:
                    stock.append(i)
                    print(f'\033[1;32mRandom color : {product_color}')

                    return stock[0]
                elif in_stock == False and product_color == form:
                    stock.append(i)
                    print(f'\033[1;32mColor found : {product_color}')

                    return stock[0]
                elif in_stock == False:
                    stock.append(i)

                    return stock[0]
                
                     
if __name__ == "__main__":
    pass
