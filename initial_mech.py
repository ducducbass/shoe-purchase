__author__ = 'rcs'
from bs4 import BeautifulSoup
import requests


# goto proudct page
# get product info using bs4 (sku, model#, requestkey, etc..)
# form id="product_form" action = "/catalog/addToCart" method="post" ...>
# <input name="requestKey" id="requestKey"
#footlocker id="product_attributes"/ id="product_Form"
# get requestKey... via bs4? then input the rest of the values

# with requests.Session() as session:

def main():

    URL = "http://www.footlocker.com/product/model:266161/"
    sesh = "http://footlocker.com/session"
    # create session
    session = requests.Session()
    return addToCart(URL)

def addToCart(url):
    base_url = "http://www.footlocker.com/"
    resp_headers = {
        'Accept': '*/*',
        'Connection': "keep-alive",
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': base_url,
        'Referer': url,
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    }
    with requests.Session() as session:
        session.headers.update({ # soething about this changed it...
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': '1'
        })
        r = session.get(url)
        print r.headers
        # cookies = dict(r.cookies) #
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
                 'requestKey': requestKey,#requestKey,
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

        print 'requestKey: {0}'.format(requestKey)
        response = session.post('http://www.footlocker.com/catalog/miniAddToCart.cfm?secure=0&', headers=resp_headers, data=load)
        response_text = BeautifulSoup(response.text, "html.parser")
        print "Status Code: {0}".format(response.status_code)
        if response.status_code == 500:
            print "ERROR: {0}".format([err.string.encode("utf8") for err in response_text.find_all("span", class_='error')])
            print response.request.headers
        elif response.status_code == 200:
            # print response_text
            print "{0} - successfully added to cart".format(name)
        else:
            print response.status_code
            print response_text
    return 1

main()