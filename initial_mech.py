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
    # create session
    with requests.Session() as session:
        session.headers.update({ # soething about this changed it...
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': '1'
        })
        cookies = addToCart(URL, session)
        print "*"*40
        return getCartInfo(session,cookies)


def addToCart(url,session):
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

    r = session.get(url)
    # cookies = dict(r.cookies) #
    html = r.text
    referer = r.url
    soup = BeautifulSoup(html,"html.parser")

    qty = '1'
    size = '11.0'

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

    # print 'requestKey: {0}'.format(requestKey)
    response = session.post('http://www.footlocker.com/catalog/miniAddToCart.cfm?secure=0&', headers=resp_headers, data=load)
    response_text = BeautifulSoup(response.text, "html.parser")
    print "Status: {0}".format(response.status_code)
    if response.status_code == 200:
        # print response_text
        print "{0}: successfully added to cart".format(name)
        cookies = dict(session.cookies)
        return cookies
    else:
        print "ERROR: {0}".format([err.string.encode("utf8") for err in response_text.find_all("span", class_='error')])
        print response.request.headers
        return -1

def getCartInfo(sesh, cookies):
    session = sesh
    response = session.get('http://www.footlocker.com/shoppingcart/default.cfm?sku=', cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    cart = soup.find_all('tr', attrs={'class':'lineitem'})
    for item in cart:
        attribs = item.find('div', attrs={'class':'attributes'}).text
        qty = item.find('input', attrs={'name':'quantity', 'title':'Enter Quantity'})['value']
        print "Atributes: {0}".format(attribs)
        print "Qty: {0}".format(qty)
    return 0
main()