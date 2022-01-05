import webapp2
import requests
import re
import json
import cgi
import sys
import wsgiref.handlers
import  urllib2
import datetime
import os
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import taskqueue
from bs4 import BeautifulSoup
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()
from scraper import PlayStoreScraper
from models import Collection, App
import json

# Show the top charts page
class ShowTopCharts(webapp2.RequestHandler):
    def get(self):
        scraper = PlayStoreScraper()
        data = scraper.show_top_charts()

        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers.add_header('Access-Control-Allow-Headers','Origin, X-Requested-With, Content-Type, Accept')

        self.response.out.write(json.dumps(data))

# Show single collection page
class ShowCollectionApps(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('name')
        temp = name.split('-')
        collection_name = ' '.join(temp).capitalize()

        scraper = PlayStoreScraper()
        collection_data = scraper.show_collection_apps(collection_name)

        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers.add_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

        self.response.out.write(json.dumps(collection_data))

# Rescrape the top charts page
class ScrapeTopCharts(webapp2.RequestHandler):
    def get(self):
        scraper = PlayStoreScraper()
        scraper.scrape_top_charts()
        data = scraper.show_top_charts()

        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers.add_header('Access-Control-Allow-Headers','Origin, X-Requested-With, Content-Type, Accept')

        self.response.out.write(json.dumps(data))

# Single app page details
class GetAppDetails(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('id')

        scraper = PlayStoreScraper()
        app_data = scraper.get_app_details(id)

        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers.add_header('Access-Control-Allow-Headers','Origin, X-Requested-With, Content-Type, Accept')

        self.response.out.write(json.dumps(app_data))

application = webapp2.WSGIApplication([
    ('/', ShowTopCharts),
    ('/scrape', ScrapeTopCharts),
    ('/appdetails', GetAppDetails),
    ('/collection', ShowCollectionApps)
], debug=True)

