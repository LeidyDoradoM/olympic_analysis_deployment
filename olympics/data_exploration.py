#import hvplot.pandas 
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2

def creating_data(engine):
    #Tables named 'Olympics' and 'Indicators' will be returned as a dataframe.
    indicators_df = pd.read_sql_table('Indicators', engine)
    olympic_df = pd.read_sql_table('Olympics', engine)
    # doing the merge using sql
    df_merge = pd.read_sql_query("""SELECT
                            ind."Year", ind."CountryCode", ind."GDPCapita", ind."GNICapita", ind."Population", ind."HDI", ind."HDIRank",
                            oly."Top15", oly."Perc", oly."Total"
                            FROM "Indicators" AS ind 
                            INNER JOIN "Olympics" AS oly 
                            ON (ind."CountryCode" = oly."CountryCode" AND ind."Year" = oly."Year");""",
                         engine)
    columns_to_keep = ['Year','CountryCode','GDPCapita','GNICapita','Population','HDI','HDIRank','Top15']
    df_data = df_merge[columns_to_keep]
    ## Add newdf to a SQL db
    df_data.to_sql(name = 'Analysis', con = engine, if_exists = 'replace', index = False) 
    # Add primary keys
    df_data.to_sql(con=engine, name='Analysis', if_exists='replace', index=False)
    #with engine.connect() as con:
    #    con.execute('ALTER TABLE "Analysis" ADD PRIMARY KEY ("CountryCode","Year");')
    
