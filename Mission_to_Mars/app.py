from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = pymongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scrape():

    mars_data = mongo.db.mars_data
    mars_data = scrape_mars.news_scrape()
    mars_data = scrape_mars.featured_image_scrape()
    mars_data = scrape_mars.facts_scrape()
    mars_data = scrape_mars.hemisphere_url_scrape()

    mars_info.update({}, mars_data, upsert=True)


    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
