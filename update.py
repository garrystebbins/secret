### Random Dev Notes ###

# Grab user profile links from page
# soup = BeautifulSoup(br.response().read())

# Remove Cached files from github
# git rm --cached update.py

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# Tutorials
# http://toddhayton.com/2014/12/08/form-handling-with-mechanize-and-beautifulsoup/

# Only works with Python 2

# Creating Virtual Environment #########
# https://packaging.python.org/guides/installing-using-pip-and-virtualenv/
# sudo apt update
# sudo apt install pip
# pip install --user virtualenv
# virtualenv venv
# source venv/bin/activate

# Sign into an admin page with mechanize #########
# https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup

# Reading a CSV
# http://forums.devshed.com/python-programming-11/python-using-excel-csv-file-read-columns-rows-941281.html

## Installing Dependencies
# pip install beautifulsoup4
# pip install mechanize
# pip install requests2

from bs4 import BeautifulSoup
import requests
import mechanize
import urllib2
import cookielib
import csv

# Login to admin area & set cookie
cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open("https://api.dmctools.com/admin/login/")

br.select_form(nr=0)
br.form['username'] = 'marketing@dmctools.com'
br.form['password'] = 'dmcw3bsi+e'
br.submit()

### Sanitize Data First!!
# Make two columns spreadsheet in Excel, change the amount column to numbers formate, save as csv

# Open the sales CSV & save each column
item_column = []
price_column = []

with open('/home/bens-dev-s/Downloads/2019_retail_pricing_online_items.csv') as csv_file:
    rows = csv.reader(csv_file, delimiter=',')
    for row in rows:
        item_column.append(row[0].strip())
        price_column.append(row[1].strip())

# Run a search for each item in column ######
# Select form by ID, Input the search item & get results from search item
page_content = br.open("https://api.dmctools.com/admin/catalogue/product/").read()
br.select_form(nr=0)

for item in item_column:
    br.form['q'] = item
# item = item_column[0]
# br.form['q'] = item
    br.submit()

    ########## Select the last paginated page & open -- TO DO !!!!!!!! ############
    # https://api.dmctools.com/admin/catalogue/product/?p=2&q=AF8

    soup = BeautifulSoup(br.open('https://api.dmctools.com/admin/catalogue/product/?p=2&q=AF8').read())

    # Find correct link and follow url
    # product_link = soup.find_all('a', text='AF8')
    product_link = soup.find_all('a', text=item) # Replace with loop item

    domain = "https://api.dmctools.com"

    just_url = product_link[0].get('href')

    absolute_url = domain + just_url

    open_product_page = BeautifulSoup(br.open(absolute_url).read())

    # open search item page and change input value

    def select_page_form(form):
        return form.attrs.get('id', None) == 'product_form'

    selected_form = br.select_form(predicate=select_page_form)

    # unit_price_value = br.form['unit_price'] = '1325.31'
    for price in price_column:
        unit_price_value = br.form['unit_price'] = price

        br.submit(name='_save')

# def select_form(form):
    # return form.attrs.get('id', None) == 'changelist-search'
# 
# selected_search_form = br.select_form(predicate=select_form)