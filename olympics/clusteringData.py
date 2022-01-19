# Import modules 
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans  
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import plotly.express as px

def Kmean_Olympics(engine,year):
    analysis_table = pd.read_sql_table('Analysis', engine)
    df = analysis_table[analysis_table.Year == year]
    df = df.drop(['GNICapita','HDIRank'], axis=1)
    df_n = df.dropna()
    X = df_n.drop(['Year','CountryCode'], axis=1)
    X_scaled = MinMaxScaler().fit_transform(X)
    model = KMeans(n_clusters=3, random_state=0)
    # Fitting model
    model.fit(X_scaled)
    # Get the predictions
    predictions = model.predict(X_scaled)
    df_n['cluster'] = model.labels_
    fig = px.scatter_3d(df_n, x="GDPCapita", y="HDI",z="Top15", color="cluster", hover_name="CountryCode", width=800)
    #fig.update_layout(legend=dict(x=0,y=1))
    fig.update(layout_coloraxis_showscale=False)
    print(f"fig type: {type(fig)}")
    #fig.write_html('clustering1992.html')
    fig1 = px.choropleth(df_n, color="cluster", locations="CountryCode",
                         hover_name="CountryCode", hover_data={"CountryCode":False}, projection="natural earth",
                         width=800)
    fig1.update(layout_coloraxis_showscale=False)
    return fig, fig1
