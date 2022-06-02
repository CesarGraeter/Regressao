import streamlit as st
import pandas as pd
import datetime
#import joblib
import sklearn
from sklearn.externals import joblib

def celsius(f):
	celcius = 5*(((f*100) - 32)/9)
	return celcius

def fahr(c):
	fahr = (9*((32/9)+(c/5))) / 100
	return fahr

# escrevendo um título na página
st.title(':bike:')
st.write('Aplicativo de previsão de aluguel de bicicletas')

bike = pd.read_csv('bike.csv')

# datas = pd.date_range(start='1/1/2013', end='31/12/2013')
Weathersit = bike['weathersit'].unique()
MaxTemp = bike['temp'].max()
MinTemp = bike['temp'].min()
AvgTemp = bike['temp'].mean()
MaxaTemp = bike['atemp'].max()
MinaTemp = bike['atemp'].min()
AvgaTemp = bike['atemp'].mean()
MaxHum = bike['hum'].max()
MinHum = bike['hum'].min()
AvgHum = bike['hum'].mean()
MaxWspeed = bike['windspeed'].max()
MinWspeed = bike['windspeed'].min()
AvgWspeed = bike['windspeed'].mean()

d = st.date_input("escolha a data para previsão", datetime.date(2013, 1, 1), min_value=datetime.date(2013, 1, 1), max_value=datetime.date(2013, 12, 31),)

hd = st.checkbox('É feriado ?')
if hd:
   h = 1
   workingday = 0
else:
   h = 0
   workingday = 1

if d.weekday() >=5:
   workingday = 0

ws = st.selectbox('Situação do tempo',
     ('1: Clear, Few clouds, Partly cloudy, Partly cloudy', '2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist', '3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds','4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'))

if ws == '1: Clear, Few clouds, Partly cloudy, Partly cloudy':
   ws = 1
if ws == '2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist':
   ws = 2
if ws == '3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds':
   ws = 3
if ws == '4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog':
   ws = 4

t = st.slider('Temperatura em graus celsius', celsius(MinTemp), celsius(MaxTemp), celsius(AvgTemp))
t = fahr(t)

at = st.slider('Sensação térmica em graus celsius', celsius(MinaTemp), celsius(MaxaTemp), celsius(AvgaTemp))
at = fahr(at)

h = st.slider('Humidade relativa %', MinHum * 100, MaxHum * 100, AvgHum * 100)
h = h / 100

s = st.slider('Velocidade do vento km/h', MinWspeed * 67, MaxWspeed * 67, AvgWspeed * 67)
s = s / 67

# 1 de 21-12 ate 20-03
if (d.month == 12 and d.day >= 21) or (d.month >= 1 and d.month <=2) or (d.month == 3 and d.day <=20):
	season = 1

# 2 de 21-03 ate 20-06
if (d.month == 3 and d.day >= 21) or (d.month >= 4 and d.month <=5) or (d.month == 6 and d.day <=20):
	season = 2

# 3 de 21-06 ate 22-09
if (d.month == 6 and d.day >= 21) or (d.month >= 7 and d.month <=8) or (d.month == 9 and d.day <=22):
	season = 3

# 4 de 23-09 ate 20-12
if (d.month == 9 and d.day >= 23) or (d.month >= 10 and d.month <=11) or (d.month == 12 and d.day <=20):
	season = 4

weekday = d.weekday()

# holiday : weather day is holiday or not
# weekday : day of the week
# workingday : if day is neither weekend nor holiday is 1, otherwise is 0.
# weathersit :
# 1: Clear, Few clouds, Partly cloudy, Partly cloudy
# 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
# 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
# 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
# temp : Normalized temperature in Celsius. The values are derived via (t-t_min)/(t_max-t_min), t_min=-8, # t_max=+39 (only in hourly scale)
# atemp: Normalized feeling temperature in Celsius. The values are derived via (t-t_min)/(t_max-t_min), t_min=-# 16, t_max=+50 (only in hourly scale)
# hum: Normalized humidity. The values are divided to 100 (max)
# windspeed: Normalized wind speed. The values are divided to 67 (max)
# season 
# 1 de 21-12 ate 20-03
# 2 de 21-03 ate 20-06
# 3 de 21-06 ate 22-09
# 4 de 23-09 ate 20-12

modelo_arquivo = joblib.load('mod_01.pkl')
# 'day','mnth','year','season','holiday','weekday','workingday','weathersit','temp','atemp','hum','windspeed'
x = [[d.day,d.month,d.year,season,h,d.weekday(),workingday,ws,t,at,h,s]]
val = modelo_arquivo.predict(x)
st.write('A previsão de aluguel é de ', int(val[0]), ' bicicletas')

