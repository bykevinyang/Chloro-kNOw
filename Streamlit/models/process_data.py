import pandas as pd
# import streamlit as st
from matplotlib import pyplot as plt


def cleanChlData():

    df = pd.read_csv('data\chl.csv')
    df["Time"] = pd.to_datetime(df['Time'])
    geometry = [list(map(float, x.split(','))) for x in df.AOI]
    lat = pd.Series([x[0] for x in geometry])
    lon = pd.Series([x[1] for x in geometry])
    df['latitude'] = lat
    df['longitude'] = lon
    df['latitude']=pd.to_numeric(df['latitude'])
    df['longitude']=pd.to_numeric(df['longitude'])
    df['Measurement Value']=pd.to_numeric(df['Measurement Value'])
    df = df[df['Measurement Value'].notna()]
    # df.rename(columns = {'Measurement Value':'Measurement Value'}, inplace = True)
    df = df[['Time', 'Country', 'Region', 'Measurement Value', 'latitude', 'longitude', 'City']]
    return df


def cleanAirQualityData():
    df = pd.read_csv('data/tokyo_air_quality.csv')
    df["time"] = pd.to_datetime(df['time'])
    df['measurement']=pd.to_numeric(df['measurement'])
    df = df[df['measurement'].notna()]
    df = df[['time', 'measurement', 'eoSensor', 'inputData', 'colorCode']]
    return df

def cleanActivityData():
    japan_ac = pd.read_csv('data/japan_activity.csv')
    japan_ac["time"] = pd.to_datetime(japan_ac['time'])
    japan_ac['measurement']=pd.to_numeric(japan_ac['measurement'])
    japan_ac = japan_ac[['time', 'measurement', 'colorCode']]
    japan_ac = japan_ac.reset_index(drop=True)
    return japan_ac

def veniceData():
    df = cleanChlData()
    venice_df = df.loc[df['Country'] == "IT"]
    venice_chl = venice_df.loc[venice_df['City'] == "Venice, Chl-a"]
    venice_tsm = venice_df.loc[venice_df['City'] == "Venice, TSM"]
    venice_df = venice_df.reset_index(drop=True)
    return venice_chl, venice_tsm, venice_df

def tokyoData():
    df = cleanChlData()
    tokyo_df = df.loc[df['Country'] == "JP"]
    tokyo_chl = tokyo_df.loc[tokyo_df['City'] == "Tokyo, Chl-a"]
    tokyo_tsm = tokyo_df.loc[tokyo_df['City'] == "Tokyo, TSM"]
    tokyo_df = tokyo_df.reset_index(drop=True)

    tokyo_air = cleanAirQualityData()
    tokyo_air = tokyo_air.reset_index(drop=True)

    japan_activity = cleanActivityData()
    return tokyo_chl, tokyo_air, japan_activity, tokyo_df

def newYorkData():
    df = cleanChlData()
    newyork_df = df.loc[df['Country'] == "US"]
    newyork_chl = newyork_df.loc[newyork_df['City'] == "New York, Chl-a"]
    newyork_tsm = newyork_df.loc[newyork_df['City'] == "New York, TSM"]
    newyork_df = newyork_df.reset_index(drop=True)
    return newyork_chl, newyork_tsm, newyork_df

def movingAverage():
    LAGTIME = 5 # In months

    output = []

    df_venice = veniceData()[0]
    df_newYork = newYorkData()[0]
    df_tokyo = tokyoData()[0]

    mapping = {
        "Venice" : df_venice,
        "New York" : df_newYork,
        "Tokyo" : df_tokyo
        }

    cities = [("Venice", df_venice['Measurement Value']), ("New York", df_newYork['Measurement Value']), ("Tokyo", df_tokyo['Measurement Value'])]

    for city in cities:
        measurements = city[1].tolist()
        ema = calculate_ema(measurements, LAGTIME, 4)
        df = mapping[city[0]]
        df["Smoothed"] = ema
        output.append(("Venice", df))


    # Ouputs tuple in the form of [(City Name, Data Frame),(City Name, Data Frame),(City Name, Data Frame)]
    return df


    # for p in smoothedValues:
    #     plt.plot(p[1], label=p[0])

    # plt.show()

def calculate_ema(data, LAGTIME, smoothing=2):
    ema = [sum(data[:LAGTIME]) / LAGTIME]

    for mes in data[1:]:
        ema.append((mes * (smoothing / (1 + LAGTIME))) + ema[-1] * (1 - (smoothing / (1 + LAGTIME))))

    return ema
