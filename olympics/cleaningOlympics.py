# importing libraries/modules 
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2

def cleaning_olympics(engine):
    # loading initial dataset to get the actual data needed in the analysis
    df = pd.read_csv('https://github.com/LeidyDoradoM/mockup_finalProject/blob/myfirstbranch/Resources/counts_and_percentages.csv?raw=true', header=[0,1])
    cols = pd.MultiIndex.from_tuples([("Country",""),("CountryCode",""),("Bar92","TotalE"), ("Bar92","Top15"),("Bar92","Perc"), 
                                    ("Atl96","TotalE"),("Atl96","Top15"),("Atl96","Perc"),("Syd00","TotalE"),("Syd00","Top15"),("Syd00","Perc"),
                                    ("Ath04","TotalE"),("Ath04","Top15"),("Ath04","Perc"),("Bei08","TotalE"),("Bei08","Top15"),("Bei08","Perc"),
                                    ("Lon12","TotalE"),("Lon12","Top15"),("Lon12","Perc"),("Rio16","TotalE"),("Rio16", "Top15"),("Rio16","Perc"),
                                    ("Tok00","TotalE"),("Tok00","Top15"),("Tok00","Perc"),("GTotal","Top15"),("GTotal","Perc")])
    # set cols to df.columns
    df.columns = cols
    # get rid off last two rows - donot have info about countries
    df = df.iloc[:-2 , :]
    # get rid off % symbol in all Perc columns
    for i in cols:
        if i[1] == 'Perc':
            df.loc[:,i] = df.loc[:,i].str.replace('--','0%')
            df.loc[:,i] = df.loc[:,i].map(lambda x: x.rstrip('%'))
            # change those columns type to float64
            df.loc[:,i] = df.loc[:,i].astype('float64', copy=False)
    #keep only columns with information about the olympic games
    df = df.iloc[:,0:26] 

    # Reshape the tables such that there is a column for each Top15 events counting and for each olympic game
    df.columns = df.columns.to_flat_index()
    df.rename(columns={ ('Country', ''):'Country', ('CountryCode', ''):'CountryCode', 
                    ("Bar92","TotalE"):'1992_Total',('Bar92', 'Top15'):'1992_Top15',('Bar92', 'Perc'):'1992_Perc',("Atl96","TotalE"):'1996_Total',
                    ('Atl96', 'Top15'):'1996_Top15',('Atl96', 'Perc'):'1996_Perc',("Syd00","TotalE"):'200_Total',('Syd00', 'Top15'):'2000_Top15', 
                    ('Syd00', 'Perc'):'2000_Perc',("Ath04","TotalE"):'2004_Total',('Ath04', 'Top15'):'2004_Top15',('Ath04', 'Perc'):'2004_Perc', 
                    ("Bei08","TotalE"):'2008_Total',('Bei08', 'Top15'):'2008_Top15',('Bei08', 'Perc'):'2008_Perc',("Lon12","TotalE"):'2012_Total',
                    ('Lon12', 'Top15'):'2012_Top15',('Lon12', 'Perc'):'2012_Perc',('Rio16','TotalE'):'2016_Total',('Rio16', 'Top15'):'2016_Top15',
                    ('Rio16', 'Perc'):'2016_Perc',("Tok00","TotalE"):'2020_Total',('Tok00', 'Top15'):'2020_Top15',
                    ('Tok00', 'Perc'):'2020_Perc' }, inplace=True)
    Odf = df.melt(id_vars = ["Country", "CountryCode"], var_name="Year", value_name="Value")
    # new data frame with split value columns. This separates Years of Olympic games from Top15&Perc 
    new = Odf["Year"].str.split("_", n = 1, expand = True)
    # making column with years from "new" data frame
    Odf["Year"]= new[0]  
    # making column with the two metrics: Top15&Perc from "new" data frame
    Odf["metric"]= new[1]
    # Convert metric Rows to Columns using Pivot Table, so Top15 and Perc are at different columns
    df_pivot = Odf.pivot_table('Value',['Country','CountryCode','Year'],'metric')
    # Convert Multindex pivot table to a dataframe.  This is the final table with olympic games information used in this analysis
    olympic_df = pd.DataFrame(df_pivot.to_records())
    olympic_df.Year = olympic_df.Year.astype('float64', copy=False)
    
    ## Add olympics_df to a SQL db
    olympic_df.to_sql(name = 'Olympics', con = engine, if_exists = 'replace', index = False) 
    #with engine.connect() as con:
    #    con.execute('ALTER TABLE "Olympics" ADD PRIMARY KEY ("CountryCode","Year");')
