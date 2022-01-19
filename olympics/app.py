import numpy as np
import pandas as pd
from .clusteringData import Kmean_Olympics
from .cleaningIndicators import cleaning_economics
from .cleaningOlympics import cleaning_olympics
from .data_exploration import creating_data
# for sqlalchemy
#from config import db_password
import sqlalchemy
from sqlalchemy import create_engine, func
# for plotting
import plotly.express as px
#for flask
from flask import Flask, render_template, redirect, url_for, request

# --- Setup FLASK ----
# create a new flask app
print('setup FLASK')
app = Flask(__name__)

#setup the database
print('setup the database')
#db_string = f"postgresql://postgres:{db_password}@127.0.0.1:5432/OlympicAnalysis_FP"
db_string = 'sqlite:///db.sqlite'

#Create the database engine
print('create engine')
engine = create_engine(db_string, echo=True)

# create the first route
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/loading')
def loading_data():
    print('creating database...')
    cleaning_economics(engine)
    print('indicators table created')
    cleaning_olympics(engine)
    print('olympic table created')
    creating_data(engine)
    return render_template("index.html")

@app.route('/clustering')
def plot_kmeans():
    city_names = {1992:'Barcelona', 1996:'Atlanta', 2000:'Sydney', 2004:'Athens', 
                  2008:'Beijing', 2012:'London', 2016:'Rio', 2020:'Tokyo'}
    print('running kmeans')
    year = int(request.args.get('years'))
    print(year)
    plot_indsc, plot_map = Kmean_Olympics(engine,year)
    game_name = f"{city_names[year]}, {year}"
    plot_indsc.write_html(f"olympics/static/images/clustering-{year}.html")
    # return redirect('/', code=302)
    plot_map.write_html(f"olympics/static/images/map-{year}.html")
    return render_template("index.html", years=year, game_name=game_name)
    
if __name__=='__main__':
    app.run(debug=True)
