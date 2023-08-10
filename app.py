import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

from weather import OWMConnection
import streamlit as st
from streamlit.connections import ExperimentalBaseConnection

#define secret
api_key = st.secrets.API_KEY

#establish connection
conn= st.experimental_connection("pyowm.OWM", type=OWMConnection, api_key=api_key)
conn

#create cursor
c = conn.cursor()

#create observation of Amsterdam
observation = c.weather_at_place('Amsterdam')
w = observation.weather

#write the detailed status of weather in Amsterdam (In later version this could be an input field)
st.write(f"""
# Insights into weather in beautiful Amsterdam
## {datetime.now(tz=ZoneInfo("Europe/Amsterdam")).strftime("%d-%m-%Y :  %H:%M:%S")}
---
      {w.detailed_status}  """
      )