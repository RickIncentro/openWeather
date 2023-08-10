import pyowm
from pyowm.utils import config
from pyowm import OWM
from pyowm.utils import timestamps
from streamlit.connections import ExperimentalBaseConnection
import streamlit as st


#1. Create a new connection class that extends Streamlit's ExperimentalBaseConnection.
# It also needs the type of the underlying connection object to be specified.
class OWMConnection(ExperimentalBaseConnection[OWM]):
        
#2.Add a _connect() method that sets up and returns the underlying connection object. 
#It can pull secrets specific to the connection from the self._secrets property.
    def _connect(self, **kwargs) -> OWM:
        if 'api_key' in kwargs:
            api_key = kwargs.pop('api_key')
        else:
            api_key = self._secrets['api_key']
        return OWM(api_key= api_key, **kwargs)
    
    
#3. Add a way to get the underlying connection object. ExperimentalBaseConnection has a _instance property that does this by default. 
# Most connections will want some domain-specific property or method that exposes this.
    def cursor(self) -> OWM:
        return self._instance.weather_manager()
    
#4. Add any convenience read / getter methods. These should be wrapped with @st.cache_data by default, 
# and conform to the st.experimental_connection best practices.
    def query(self, query: str, ttl: int = 3600, **kwargs) -> str:
        @st.cache_data(ttl=ttl)
        def _query(query: str, **kwargs) -> str:
            cursor = self.cursor()
            cursor.execute(query, **kwargs)
            return cursor.df()

        return _query(query, **kwargs)