import pandas as pd
import requests as req
import streamlit as st
import datetime 

import db
import codes

LIMIT = 1
API_KEY = st.secrets["openweather"]["api_key"]

def submit():
        
        selected_country_code = CODE.split("—")[-1].strip()
        

        geocode_api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={CITY},,{CODE}&limit={LIMIT}&appid={API_KEY}"
        geocode_data = db.fetch_coords_from_url(geocode_api_url)

        city_country_code = geocode_data[0]["country"]

        LATITUDE = geocode_data[0]["lat"]
        LONGTITUDE = geocode_data[0]["lon"]

        weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGTITUDE}&units=metric&appid={API_KEY}"
        weather_data =  db.fetch_data_from_url(weather_api_url)

        if city_country_code != selected_country_code:
            st.error( f"The selected country code does not match the city's country code")
            return

        if weather_data and geocode_data is not None:

                    st.header(
                          f"{CITY}, {CODE}", 
                          text_alignment="center", 
                          width='stretch'
                    )

                    outer_container = st.container(
                    horizontal=True,
                    horizontal_alignment="center",
                    border=True
                    )

                    metrics_container = outer_container.container(
                        width=800,
                        horizontal=True,
                        horizontal_alignment="distribute",
                        vertical_alignment="center",
                        gap="large",
                    )

                    metrics_container.metric(
                        "Temperature",
                        f"{weather_data['main']['temp']:.2f} °C",
                        width="content",
                    )

                    metrics_container.metric(
                        "Feels like",
                        f"{weather_data['main']['feels_like']:.2f} °C",
                        width="content",
                    )

                    metrics_container.metric(
                        "Humidity",
                        f"{weather_data['main']['humidity']}%",
                        width="content",
                    )


                    timezone_offset = weather_data["timezone"]

                    local_timezone = datetime.timezone(
                        datetime.timedelta(seconds=timezone_offset)
                    )
                    measure_date = datetime.datetime.fromtimestamp(
                        weather_data["dt"],
                        tz=local_timezone
                    )
                    sunrise = datetime.datetime.fromtimestamp(
                        weather_data["sys"]["sunrise"],
                        tz=local_timezone
                    )
                    sunset = datetime.datetime.fromtimestamp(
                        weather_data["sys"]["sunset"],
                        tz=local_timezone
                    )

                    st.write(f"Actual weather: {weather_data['weather'][0]['description'].capitalize()}")
                    st.write(f"Wind speed: {weather_data["wind"]["speed"]}(m/s)")
                    st.write(f"Air pressure: {weather_data["main"]["pressure"]}(hPa)")
                    st.write(f"Sunrise:  "f"{sunrise.strftime('%H:%M')}")
                    st.write(f"Sunset:   "f"{sunset.strftime('%H:%M')}")
                    st.write(f"Date of Measure:   "f"{measure_date.strftime('%Y.%m.%d. - %H:%M:%S')}")
                    
                    with st.expander("API response_1"):
                        st.json(weather_data)

                    with st.expander("API response_2"):
                        st.json(geocode_data)
        else:
            st.error("Couldnt fetch data from API")


st.set_page_config(
     page_title="Weather",
     layout="centered"
)
st.title(
     "Simple Forecast",
     text_alignment="center"
)


left_column, center_column, right_column = st.columns([2, 6, 2])

with center_column:
        CITY = st.text_input(
            label="The city you are looking for", placeholder="For example: Budapest",
            width="stretch"
        )
        if any(character.isdigit() for character in CITY):
            st.error("The city field cannot contain numbers.")

        CODE = st.selectbox("Country Code ",["Hungary — HU"] + codes.clean_codes_list,
                             width="stretch")
        if any(character.isdigit() for character in CODE):
            st.error("The code field cannot contain numbers.")

        get_weather_button = st.button(
            "Get weather data",
            width="stretch"
        )
        
        
if get_weather_button:
     submit()