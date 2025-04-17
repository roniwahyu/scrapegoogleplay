import json
import pandas as pd
from tqdm import tqdm
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from google_play_scraper import Sort, reviews, app
from flask import Flask, render_template

app = Flask(__name__)

app_packages = [
    'com.alloapp.yump',  # allo bank
    'com.jago.digitalBanking',  # bank jago
    'id.co.bankbkemobile.digitalbank',  # seabank
    'com.btpn.dc',  # btpn jenius
    'com.bcadigital.blu',  # bank bca
    'id.co.bankraya.apps',  # rayabank
    'com.bnc.finance'  # neobank
]

def get_app_data():
    """Collects app information and returns a DataFrame."""
    app_infos = []
    for ap in tqdm(app_packages):
        info = app(ap, lang='id', country='id')
        app_infos.append(info)
    df = pd.DataFrame(app_infos)
    return df

def get_app_reviews():
    """Collects app reviews and returns a list of dictionaries."""
    app_reviews = []
    for ap in tqdm(app_packages):
        for score in list(range(1, 6)):
            for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
                rvs, _ = reviews(
                    ap,
                    lang='id',
                    country='id',
                    sort=sort_order,
                    count=3000 if score == 3 else 1500,
                    filter_score_with=score
                )
                for r in rvs:
                    r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
                    r['appId'] = ap
                app_reviews.extend(rvs)
    return app_reviews

# Home route
@app.route("/")
def index():
    """Renders the index page with app information."""
    df = get_app_data()
    app_data = df.to_dict("records")
    return render_template("index.html", app_data=app_data)

@app.route("/reviews")
def reviews_page():
    """Renders the reviews page with reviews."""
    reviews_data = get_app_reviews()
    return render_template("reviews.html", reviews_data=reviews_data)

if __name__ == "__main__":
    app.run(debug=True)
