__author__ = 'rcs'
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import urllib2

# goto proudct page
# get product info using bs4 (sku, model#, requestkey, etc..)
# form id="product_form" action = "/catalog/addToCart" method="post" ...>
# <input name="requestKey" id="requestKey"
#footlocker id="product_attributes"/ id="product_Form"
# get requestKey... via bs4? then input the rest of the values

# with requests.Session() as session:

def main():
    base_url = "http://www.footlocker.com/"
    URL = "http://www.footlocker.com/product/model:266161/"
    sesh = "http://footlocker.com/session"
    # create session
    session = requests.Session()
    return addToCart(session, URL)

def addToCart(sesh, url):
    session = sesh
    r = session.get(url)
    html = r.text
    referer = r.url
    soup = BeautifulSoup(html,"html.parser")

    qty = '1'
    size = '13.0'

    #add to cart payload
    # form id="product_form"
    # get VALUE

    model = soup.find("input", id='pdp_model')['value'].encode("utf8") # id="pdp_model"
    name = soup.find("input", id='model_name')['value'].encode("utf8") # id="model_name"
    requestKey = soup.find("input", id='requestKey')['value'].encode("utf8") # id="requestKey"
    sku = soup.find("input", id='pdp_selectedSKU')['value'].encode("utf8") # id="pdp_selectedSKU"
    price = soup.find("input", attrs={'name':'selectedPrice', 'type':'hidden'})['value'].encode("utf8") # id="selectedPrice"

    load = { # need to set default values/ variables
             'storeCostOfGoods':'0.00',
             'lineItemId':'',
             'model': model,
             'requestKey': 'F28D6gBB28EE28FE',#requestKey,
             'hasXYPromo':'false',
             'sameDayDeliveryConfig':'false',
             'sku':sku,
             'the_model_nbr': model,
             'model_name': name,
             'skipISA':'no',
             'selectedPrice': price,
             'qty': qty,
             'size':size,
             'fulfillmentType':'SHIP_TO_HOME',
             'storeNumber':'00000',
             'coreMetricsDo':'true',
             'coreMetricsCategory':'Add to Wish List - PDP',
             'quantity': qty,
             'inlineAddToCart':'1'
             }
    # headers = {
    #     'Accept': '*/*',
    #     'Origin': base_url,
    #     'X-Requested-With': 'XMLHttpRequest',
    #     'Referer': referer,
    #     'Accept-Encoding': 'gzip, deflate',
    # }
    print r.request.headers
    print requestKey
    response = requests.post('http://www.footlocker.com/catalog/miniAddToCart.cfm?secure=0&', data=load)
    response_text = BeautifulSoup(response.text, "html.parser")
    if response.status_code == 500:
        print "ERROR: {0}".format([err.string.encode("utf8") for err in response_text.find_all("span", class_='error')])
        # print response.headers
    else:
        print response_text

print main()