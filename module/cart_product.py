#### GITHUB : LysC0 ####

## import ##

from datetime import datetime
from bs4 import BeautifulSoup
import requests
import time
import json
import re

## my import ##

from module.log_saver import log_csv

## user data ## 

with open('info.json', 'r') as rd:
    j = json.load(rd)
    form = j['Product']['Size']
    d_color = j['Product']['Color']
    d_size = [form]
    d_webhook = j['Webhook']['url']
    d_proxies = j['proxies']['ip:port']
    d_auth = j['proxies']['usr:pwd']

## header set ##

header = {
       'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
       'Content-Type' : 'application/json; text/plain',
       'Accept' : '*/*',    
       'Origin' : 'https://eu.supreme.com',
       'Referer' : 'https://eu.supreme.com/cart',
}

## FUNCTION ##

def Check_response(element):
        try: 
            el = requests.get(element).status_code
           
            if (el == 200):
                pass
            elif (el == 201):
                pass
            elif (el == 202):
                pass           
            elif (el == 401):
                print('Status Unauthorized')
            elif (el == 400):
                print(el,' Status OFF')
            elif (el == 402):
                print(el,' Status OFF')
            elif (el == 403):
                print(el,' Status OFF')
            else:
                print(el, 'Error')
                pass
        except:
                print("Can't Check Status")

def __atc__(url):

    if url == None:
        exit()
    
    r = requests.Session()
    r.headers = header

    ## verif proxy set ## 

    settings_proxy()
    
    ## verif status ##
        
    Check_response(url)

    ## parse html product page ##

    base = r.get(url)
    soup = BeautifulSoup(base.text, 'lxml')
    id = soup.find("script", {'class', 'js-product-json'})
    data = json.loads(id.text)

    ## save info for found product in json ##

    variant = data['product']['variants']
    in_stock = data['product']['available']
    product_title = data['product']['title']
    product_color = data['product']['tags'][0].replace('color:','')
    product_price_calc = data['product']['price']
    product_price = str(product_price_calc)[:-2] + '€'
    product_img = 'https:' + data["product"]['image']

    while True:
        if in_stock == True:
            break
        else :
            bas = r.get(url)
            sou = BeautifulSoup(bas.text, 'lxml')
            id_ = sou.find("script", {'class', 'js-product-json'})
            dat = json.loads(id_.text)
            product_title_w = dat['product']['title']
            in_stock_ = dat['product']['available']
            if in_stock_ == False:
                print(f'\033[1;33mwait restock : {product_title_w.lower()} ..', end='\r')
                time.sleep(0.2)
            elif in_stock_ == True:
                print(f'\033[1;32mfound restock success : {product_title_w.lower()}')
                break

    ## find desired product ##
            

    try :     
        for vr in variant:
            available = vr['available']
            size = vr['options']

            ## unique size exception ##

            if size == ['OS']:
                os_id = vr['id']
                p_os_id = vr['parent_id']
                print(f'\033[1;32mSize found : {size[0].lower()}')
                add_to_cart(os_id, product_color, p_os_id, product_title, product_price, size[0], product_img)
                break

            if size == d_size and available == True :
                ids = vr['id']
                p_ids = vr['parent_id']
                print(f'\033[1;32mSize found : {size[0].lower()}')
                add_to_cart(ids, product_color, p_ids, product_title, product_price, size[0], product_img)
                break

            elif size == d_size and available == False:
                for vr in variant:
                    available_2 = vr['available']
                    size_2 = vr['options']

                    if available_2 == True:
                        ids = vr['id']
                        p_ids = vr['parent_id']
                        print(f'\033[1;32m{form} size not found. random size : {size_2[0].lower()}')
                        add_to_cart(ids, product_color, p_ids, product_title, product_price, size[0], product_img)
                        break
    except :
        print('\033[1;31;40mproduct oos', end='\r')

def add_to_cart(result_id, color, parent_id, title, price, size, img): 
    r = requests.Session() 
    r.headers = header

    post_url_add = 'https://eu.supreme.com/cart/add.json'
    cart_url = 'https://eu.supreme.com/cart.js'
    payload_add =  {'items':[{'id':result_id,'properties':{'_max_style':2,'_max_product':1,"_style":"","Style":color},"quantity":1,"variant_id":result_id,"product_id":parent_id,"handle":None,"requires_shipping":True,"product_type":"","product_title":"","untranslated_product_title":"","product_description":"","variant_title":"","untranslated_variant_title":"","variant_options":[""],"options_with_values":[{"name":"Size","value":""}]}]}
    
    ## post request add to card ##

    r.post(post_url_add, json=payload_add)

    ## Check cart ## 

    rq_check = r.get(cart_url).json()

    if rq_check['item_count'] == 1:
        while True: 
            baseq =  r.head(cart_url, headers=header).request.headers             
            cart_match = re.search(r'cart=([^;]+)', str(baseq))
            cart_value = cart_match.group(1) if cart_match else None
            if (cart_value == None):
                time.sleep(0.2)
            else:
                id_card = str(cart_value)
                _cart_url = 'https://eu.supreme.com/checkouts/c/' +  str(id_card)
                #menu_url = 'Cart link : ' + 'https://eu.supreme.com/checkouts/c/' +  str(id_card)
                print('\033[1;32mSuccess add to card.')
                Webhook(pay_url=_cart_url, title=title, size=size, price=price, color=color, img=img)
                break
    else :
        print('\033[1;31merror on add to Card.')

def Webhook(pay_url, title, size, color, price, img):
    dh = datetime.now()
    form = f'{dh.day}/{dh.month}/{dh.year}'

    embed = {
        "title": "**Supreme_bot**",
        "url" : pay_url,
        "description" : "- Supreme auto Checkout",
        "color": 3801226,
        "fields": [
            {"name": "__Title :__", "value": title, "inline": True},
            {"name": "__Size :__", "value": size, "inline": True},
            {"name": "__Color :__", "value": color, "inline": True},
            {"name": "__Price :__", "value" : price, "inline": True},
            {"name": "__Cart url :__", "value": '||'+ pay_url +'||', "inline": True}       
        ],
        "footer" : {
            "text" : f'dev v0.01 - {form} - {dh.hour}:{dh.minute}'
        },
        "thumbnail" : {
            "url" : img
        }
    }

    payload = {
        "content": "",
        "embeds": [embed]
    }

    response = requests.post(d_webhook, data=json.dumps(payload), headers={"Content-Type": "application/json"})

    if response.status_code == 204:
        print("\033[1;32mWebhook send success.")
        log_csv(title, size, color, pay_url)
        pass
    else:
        print("\033[1;31mWebhook error :", response.status_code)

def settings_proxy():
    r = requests.Session()
    r.headers = header

    check = 'https://www.google.com/'

    proxie = {  
        'http' : 'https://' + d_proxies,
    } 

    try :
        r.proxies.update(proxie)

        if r.get(check, proxies=proxie).status_code == 200 or 201 or 203 :
            return
        else : 
            print('\033[1;31mproxy error #1')
    except IOError:
        print('\033[1;31mproxy error #2')

if __name__ == "__main__": 
    pass

#__atc__('https://eu.supreme.com/products/wgzf0n9t-d-tbdss')