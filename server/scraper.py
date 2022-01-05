import requests
from bs4 import BeautifulSoup
from google.appengine.ext import db
from models import Collection, App
import logging

class PlayStoreScraper:
    url = ''
    def __init__(self):
        self.url = 'https://play.google.com/store/apps/top?gl=in&hl=en'

    def show_top_charts(self):
        try:

            collection_data = {}
            collections = Collection.all()
            # print(Collection.get_by_key_name('Top Free Apps').app_pkgs)

            for collection in collections:
                apps_data = []
                apps = collection.app_pkgs
                for app_pkg in apps:
                    AppEntity = App.get_by_key_name(app_pkg)

                    if(AppEntity):
                        data = {}
                        data['id'] = app_pkg
                        data['title'] = AppEntity.title
                        data['icon_url'] = AppEntity.icon_url
                        data['developer'] = AppEntity.developer_id
                        data['app_star_count'] = AppEntity.app_star_count
                        apps_data.append(data)

                collection_data[collection.title] = apps_data
        except:
            logging.error('error occurred while in show top charts')

        return collection_data

    def show_collection_apps(self, collection_name):
        try:
            data = []
            CollectionEntity = Collection.get_by_key_name(collection_name)

            apps = CollectionEntity.app_pkgs
            for app_pkg in apps:
                AppEntity = App.get_by_key_name(app_pkg)

                app_data = {}
                app_data['id'] = app_pkg
                app_data['title'] = AppEntity.title
                app_data['icon_url'] = AppEntity.icon_url
                app_data['developer'] = AppEntity.developer_id
                app_data['app_star_count'] = AppEntity.app_star_count
                data.append(app_data)
        except:
            logging.error('error occurred in show collection apps')

        return data

    def scrape_top_charts(self):
        try:
            res = requests.get(self.url)
            htmlContent = res.content

            # parse the html
            soup = BeautifulSoup(htmlContent, 'html.parser')
            # print(soup)

            # title
            title = soup.title.text

            # App Links
            iconLinks = soup.find_all('div', {"class": "Vpfmgd"})

            # collections
            collections = soup.find_all('h2')

            # App packages
            packages = soup.find_all('div', {'class': 'wXUyZd'})

            # App names
            apps = soup.find_all('div', class_="WsMG1c nnK0zc")

            # Developer names
            developersList = soup.find_all('div', class_="KoLSrc")
            developersList = developersList[::2]

            # Ratings of apps
            ratings = soup.find_all('div', class_="pf5lIe")


            obj = {}
            listInd = 0

            for collection in collections:
                collection_name = collection.get_text().encode('ascii', 'ignore')
                CollectionEntity = Collection.get_by_key_name(collection_name)

                if not CollectionEntity:
                    CollectionEntity = Collection(key_name=collection_name, title=collection_name)
                    CollectionEntity.put()

                app_packages = []

                for i in range(listInd, listInd+10):
                    pkg_id = packages[i].find('a', {'class': 'poRVub'})['href'].split('=')[1].encode('ascii', 'ignore')

                    AppEntity = App.get_by_key_name(pkg_id)
                    if not AppEntity:
                        AppEntity = App(key_name=pkg_id)

                    AppEntity.title = apps[i].text.encode('ascii', 'ignore')
                    AppEntity.icon_url = iconLinks[i].find('span', {'class': 'kJ9uy'}).find("img").get('data-src').encode('ascii', 'ignore')
                    AppEntity.developer_id = developersList[i].text.encode('ascii', 'ignore')
                    AppEntity.app_star_count = ratings[i].div.get("aria-label")[6:9].encode('ascii', 'ignore')
                    AppEntity.put()

                    app_packages.append(pkg_id)

                CollectionEntity.app_pkgs = app_packages
                CollectionEntity.put()
                listInd = listInd + 10
        except:
            logging.error('error occurred in scrape top charts')

    def get_app_details(self, pkg_id):
        try:
            AppEntity = App.get_by_key_name(pkg_id)
            if not AppEntity:
                AppEntity = App(key_name=pkg_id)

            if AppEntity.is_scraped == False:

                # scrape and store data
                url = "https://play.google.com/store/apps/details?gl=IN&hl=en&id=" + pkg_id

                res = requests.get(url)
                htmlContent = res.content

                soup = BeautifulSoup(htmlContent, 'html.parser')

                # Playstore url
                AppEntity.playstore_url = url

                # Icon url
                icon_soup = soup.find('img', class_="T75of sHb2Xb")
                if icon_soup:
                    AppEntity.icon_url = soup.find('img', class_="T75of sHb2Xb").get('src').encode('ascii', 'ignore')

                # App name
                title_soup = soup.find('h1', class_="AHFaub")
                if title_soup:
                    AppEntity.title= title_soup.get_text().encode('ascii', 'ignore')

                # Developer id and category
                developer_and_category = soup.find_all('a', class_="hrTbp R8zArc")
                if developer_and_category[0]:
                    AppEntity.developer_id = developer_and_category[0].text.encode('ascii', 'ignore')

                if developer_and_category[1]:
                    AppEntity.category = developer_and_category[1].text.encode('ascii', 'ignore')


                # Age group
                age_group_settings = soup.find('img', class_="T75of E1GfKc")
                if age_group_settings:
                    AppEntity.age_group = age_group_settings.get('alt').encode('ascii', 'ignore')

                # Ads Settings
                in_app_soup = soup.find('div', class_="bSIuKf")
                if (in_app_soup):
                    AppEntity.in_app = in_app_soup.text.encode('ascii', 'ignore')


                # Ratings
                rating_soup = soup.find('div', class_="pf5lIe")
                if rating_soup:
                    AppEntity.app_star_count = rating_soup.div.get('aria-label')[6:9].encode('ascii', 'ignore')

                # No of ratings
                no_of_ratings_soup = soup.find('span', class_="AYi5wd TBRnV")
                if (no_of_ratings_soup):
                    no_of_ratings = no_of_ratings_soup.span.text.encode('ascii', 'ignore').split(',')
                    no_of_ratings = ''.join(no_of_ratings)
                    AppEntity.ratings_count = no_of_ratings


                # Video Trailer
                video_trailer = soup.find('div', class_="TdqJUe")
                if (video_trailer):
                    video_trailer = video_trailer.button.get("data-trailer-url").encode('ascii', 'ignore')
                    AppEntity.video_trailer_url = video_trailer


                # Cost
                cost = soup.find('button', class_="LkLjZd ScJHi HPiPcc IfEcue")
                if cost:
                    cost = cost.get('aria-label').encode('ascii', 'ignore')
                    if (cost == "Install"):
                        cost = "FREE"
                    AppEntity.price = cost


                # Screenshots
                screenshots_soup = soup.find_all('img', class_="T75of DYfLw")
                screenshots = []

                for ss in screenshots_soup:
                    url_present_in_src = ss.get('src').encode('ascii', 'ignore')
                    if (url_present_in_src and url_present_in_src[0:5] == "https"):
                        screenshots.append(url_present_in_src)
                    else:
                        screenshots.append(ss.get('data-src'))

                AppEntity.screenshots = screenshots

                description = soup.find("div", {"jsname": "sngebd"})
                if description:
                    AppEntity.description = description.get_text().encode('ascii', 'ignore')


                app_meta_data_soup = soup.find_all("div", {"class": "hAyfc"})
                for meta_data in app_meta_data_soup:
                    meta_info = meta_data.find("div", {'class': 'BgcNfc'}).get_text().encode('ascii', 'ignore')

                    if meta_info == "Updated":
                        AppEntity.updated_on = meta_data.find("span", {"class", "htlgb"}).get_text().encode('ascii', 'ignore')
                    elif meta_info == "Size":
                        AppEntity.size = meta_data.find("span", {"class", "htlgb"}).get_text().encode('ascii', 'ignore')
                    elif meta_info == "Installs":
                        no_of_installs = meta_data.find("span", {"class", "htlgb"}).get_text().encode('ascii', 'ignore')[:-1].split(',')
                        AppEntity.installs = ''.join(no_of_installs)
                    elif meta_info == "Current Version":
                        AppEntity.app_version = meta_data.find("span", {"class", "htlgb"}).get_text().encode('ascii', 'ignore')
                    elif meta_info == "Requires Android":
                        AppEntity.requires = meta_data.find("span", {"class", "htlgb"}).get_text().encode('ascii', 'ignore')
                    elif meta_info == "Content Rating":
                        AppEntity.content_rating = meta_data.find("span", {"class", "htlgb"}).get_text().encode('ascii', 'ignore')
                    elif meta_info == "Offered By":
                        AppEntity.offered_by = meta_data.find("span", {"class", "htlgb"}).get_text().encode('ascii', 'ignore')
                    elif meta_info == "Developer":
                        dev_soup = meta_data.find("span", {"class", "htlgb"}).find("span", {"class": "htlgb"}).find_all("div")

                        for div_element in dev_soup:
                            if 'Visit website' in div_element.get_text():
                                AppEntity.dev_website = div_element.a['href'].encode('ascii', 'ignore')
                            elif '@' in div_element.get_text():
                                AppEntity.dev_email = div_element.get_text().encode('ascii', 'ignore')
                            elif 'Privacy Policy' in div_element.get_text():
                                pass
                            else:
                                AppEntity.dev_address = div_element.get_text().encode('ascii', 'ignore')


                AppEntity.is_scraped = True
                AppEntity.put()

            app_data = {
                'is_scraped' : AppEntity.is_scraped,
                'title' : AppEntity.title,
                'description' : AppEntity.description,
                'developer_id' : AppEntity.developer_id,
                'app_star_count' : AppEntity.app_star_count,
                'icon_url' : AppEntity.icon_url,
                'playstore_url' : AppEntity.playstore_url,
                'category' : AppEntity.category,
                'age_group' : AppEntity.age_group,
                'in_app' : AppEntity.in_app,
                'ratings_count' : AppEntity.ratings_count,
                'price' : AppEntity.price,
                'video_trailer_url' : AppEntity.video_trailer_url,
                'screenshots' : AppEntity.screenshots,
                'updated_on' : AppEntity.updated_on,
                'size' : AppEntity.size,
                'installs' : AppEntity.installs,
                'app_version' : AppEntity.app_version,
                'requires' : AppEntity.requires,
                'content_rating' : AppEntity.content_rating,
                'offered_by' : AppEntity.offered_by,
                'dev_website' : AppEntity.dev_website,
                'dev_email' : AppEntity.dev_email,
                'dev_address' : AppEntity.dev_address
            }
        except:
            logging.error('error occurred in get_app_details')

        return app_data




