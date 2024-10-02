from flask import Flask, render_template, flash, jsonify, render_template, redirect, url_for, request
from pymongo import MongoClient

# Create a Flask Instance
app = Flask(__name__)
# Secret Key
app.config['SECRET_KEY'] = "my super secret key"
# Initialize The Database
client = MongoClient('mongodb',
            username='admin',
            password='admin',
            authMechanism='SCRAM-SHA-256')


@app.route('/', methods=['GET','POST'])
def main_page():
    return render_template('index.html')

# Create a route decorator
@app.route('/findPatents', methods=['POST'])
def findPatents():
    # Process the form data here
    search_query = request.form.get('search')
    checked_providers = request.form.getlist('provider')
    
    # Redirect to the results page with the search query and checked providers
    return redirect(url_for('results_page', query=search_query, providers=checked_providers))


@app.route('/results/<query>')
def results_page(query):
    checked_providers = request.args.getlist('providers')
    provlist = {"cipo": "CIPO", "googlepatent": "Google Patent", "uspto": "USPTO", "espacenet": "ESPACENET", "epo": "EPO"}
    checked_provider_names = []
    if len(checked_providers) == 0:
        return redirect(url_for('main_page'))
    providers = {}
    for provider in checked_providers:
        checked_provider_names = [provlist[provider] for provider in checked_providers]
        patentslist = []
        # Render your results page here
        db = client[provider]
        collection = db['data'+provider]
        patents = collection.find({'title': {'$regex': query, '$options': 'i'}})
        data = patents.rewind()
        for document in data:
            patentslist.append(document)
        providers[provider] = patentslist
    flash("You searched for '{}' in '{}'".format(query, ' and '.join(checked_provider_names)))
    return render_template('show_patent2.html', 
                           providers=providers)


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run()
