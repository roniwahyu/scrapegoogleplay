import json
import pandas as pd
from tqdm import tqdm

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

from google_play_scraper import Sort, reviews, app

# %matplotlib inline
# %config InlineBackend.figure_format='retina'

app_packages = [
  'com.alloapp.yump', #allo bank
  'com.jago.digitalBanking', #bank jago
  # 'com.senyumkubank.rekeningonline', #amarbank
  # 'id.aladinbank.mobile',
  'id.co.bankbkemobile.digitalbank', #seabank
  'com.btpn.dc', #btpn jenius
  'com.bcadigital.blu', #bank bca
  'id.co.bankraya.apps', #rayabank
  'com.bnc.finance' #neobank
#   'com.supercell.brawlstars',
#   'jp.pokemon.pokemonunite',
]

app_infos = []

for ap in tqdm(app_packages):
  info = app(ap, lang='id', country='id')
 # del info['comments']
  app_infos.append(info)

df=pd.DataFrame(app_infos)
df.head(10)

def print_json(json_object):
  json_str = json.dumps(
    json_object, 
    indent=2, 
    sort_keys=True, 
    default=str
  )
  print(highlight(json_str, JsonLexer(), TerminalFormatter()))

print_json(app_infos[0])
df.to_csv('BankDigital/dataset/info_BANK_MOBILE_GOOGLE_PLAY_Update21092024.csv', index=None, header=True)

app_reviews = []

for ap in tqdm(app_packages):
  for score in list(range(1, 6)):
    for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
      rvs, _ = reviews(
        ap,
        lang='id',
        country='id',
        sort=sort_order,
        count= 3000 if score == 3 else 1500,
        filter_score_with=score
      )
      for r in rvs:
        r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
        r['appId'] = ap
      app_reviews.extend(rvs)
