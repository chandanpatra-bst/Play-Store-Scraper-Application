from google.appengine.ext import db

class Collection(db.Model):
    title = db.StringProperty()
    app_pkgs = db.StringListProperty([])

class Review(db.Model):
    review = db.StringProperty()
    reviewer = db.StringProperty()
    review_date = db.StringProperty()
    review_rating = db.StringProperty()

class App(db.Model):
    is_scraped = db.BooleanProperty(default=False)
    title = db.StringProperty()
    description = db.TextProperty()
    developer_id = db.StringProperty()
    app_star_count = db.StringProperty()
    playstore_url = db.StringProperty()
    icon_url = db.StringProperty()
    category = db.StringProperty()
    age_group = db.StringProperty()
    in_app = db.StringProperty()
    ratings_count = db.StringProperty()
    price = db.StringProperty()
    video_trailer_url = db.StringProperty()
    screenshots = db.StringListProperty()
    price = db.StringProperty()
    updated_on = db.StringProperty()
    size = db.StringProperty()
    installs = db.StringProperty()
    app_version = db.StringProperty()
    requires = db.StringProperty()
    content_rating = db.StringProperty()
    offered_by = db.StringProperty()
    dev_website = db.StringProperty()
    dev_email = db.StringProperty()
    dev_address = db.TextProperty()

