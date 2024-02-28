import requests
import json
from bs4 import BeautifulSoup

def checkout(checkout_url):
    card_fields_url = ' https://deposit.us.shopifycs.com/sessions'
