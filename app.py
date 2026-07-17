import pandas as pd
import requests as req
import streamlit as st
import datetime 
import db

def submit():
        
        st.header(
        f"{CITY}",
        text_alignment="center",
        width='stretch'
        )

        geocode_api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={CITY}&limit={LIMIT}&appid={API_KEY}"
        geocode_data = db.fetch_coords_from_url(geocode_api_url)

        LATITUDE = geocode_data[0]["lat"]
        LONGTITUDE = geocode_data[0]["lon"]

        weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGTITUDE}&units=metric&appid={API_KEY}"
        weather_data =  db.fetch_data_from_url(weather_api_url)


        if weather_data and geocode_data is not None:
        
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

            st.write(f"Actual weather: {weather_data['weather'][0]['description'].capitalize()}")
            st.write(f"Wind speed: {weather_data["wind"]["speed"]}(m/s)")
            st.write(f"Air pressure: {weather_data["main"]["pressure"]}(hPa)")

            timezone_offset = weather_data["timezone"]

            local_timezone = datetime.timezone(
                datetime.timedelta(seconds=timezone_offset)
            )

            measure_date = datetime.datetime.fromtimestamp(
                weather_data["dt"],
                tz=local_timezone
            )

            st.write(
                f"Data timestamp: "
                f"{measure_date.strftime('%Y.%m.%d. %H:%M:%S')}"
            )
            
            with st.expander("API response_1"):
                st.json(weather_data)

            with st.expander("API response_2"):
                st.json(geocode_data)
        else:
            st.error("Couldnt fetch data from API")

LIMIT = 1
API_KEY = st.secrets["openweather"]["api_key"]

st.set_page_config(
     page_title="Weather",
     layout="centered"
)
st.title(
     "Weather Forecast",
     text_alignment="center"
)


left_column, center_column, right_column = st.columns([2, 6, 2])

with center_column:
        CITY = st.text_input(
            label="The city you are looking for:", placeholder="For example: Budapest",
            width="stretch"
        )
        if any(character.isdigit() for character in CITY):
            st.error("The city field cannot contain numbers.")

        get_weather_button = st.button(
            "Get weather data of the chosen city",
            width="stretch"
    )
        
if get_weather_button:
     submit()