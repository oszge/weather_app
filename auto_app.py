import datetime
import streamlit as st

import db
import codes


LIMIT = 1
API_KEY = st.secrets["openweather"]["api_key"]


st.set_page_config(
    page_title="Weather",
    layout="centered",
)

st.title(
    "Simple Forecast",
    text_alignment="center",
)


def get_coordinates(CITY, CODE):
    geocode_api_url = (f"http://api.openweathermap.org/geo/1.0/direct?q={CITY},,{CODE}&limit={LIMIT}&appid={API_KEY}")

    geocode_data = db.fetch_coords_from_url(geocode_api_url)

    if not geocode_data:
        return None

    return geocode_data[0]


def get_weather_data(LATITUDE, LONGTITUDE):
    weather_api_url = (f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGTITUDE}&units=metric&appid={API_KEY}")

    return db.fetch_data_from_url(weather_api_url)


def display_weather(weather_data):
    
    city = st.session_state["weather_city"]
    country_code = st.session_state["weather_country_code"]

    st.header(
        f"{city}, {country_code}",
        text_alignment="center",
        width="stretch",
    )

    outer_container = st.container(
        horizontal=True,
        horizontal_alignment="center",
        border=True,
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
        tz=local_timezone,
    )

    sunrise = datetime.datetime.fromtimestamp(
        weather_data["sys"]["sunrise"],
        tz=local_timezone,
    )

    sunset = datetime.datetime.fromtimestamp(
        weather_data["sys"]["sunset"],
        tz=local_timezone,
    )

    st.write("Actual weather: " f"{weather_data['weather'][0]['description'].capitalize()}")
    st.write(f"Wind speed: {weather_data['wind']['speed']} m/s")
    st.write(f"Air pressure: {weather_data['main']['pressure']} hPa")
    st.write(f"Sunrise: {sunrise:%H:%M}")
    st.write(f"Sunset: {sunset:%H:%M}")
    #st.write(f"Date of measure: {measure_date:%Y.%m.%d. - %H:%M:%S}")

    current_refresh_time = datetime.datetime.now(tz=local_timezone)
    st.caption(
        f"Last update at {current_refresh_time:%H:%M:%S}"
    )

    with st.expander("Weather API response"):
        st.json(weather_data)


@st.fragment(run_every="10m")
def auto_display():

    latitude = st.session_state.get("weather_latitude")
    longitude = st.session_state.get("weather_longitude")

    if latitude is None or longitude is None:
        return

    weather_data = get_weather_data(latitude, longitude)

    if not weather_data:
        st.error("Couldn't fetch weather data from the API.")
        return

    display_weather(weather_data)


left_column, center_column, right_column = st.columns([2, 6, 2])

with center_column:
    city = st.text_input(
        label="The city you are looking for",
        placeholder="For example: Budapest",
        width="stretch",
    )

    selected_code = st.selectbox(
        "Country Code",
        ["Hungary — HU"] + codes.clean_codes_list,
        width="stretch",
    )

    get_weather_button = st.button(
        "Get weather data",
        width="stretch",
    )


if get_weather_button:

    cleaned_city = city.strip()
    country_code = selected_code.split("—")[-1].strip()

    if not cleaned_city:
        st.error("Please enter a city.")
    elif any(character.isdigit() for character in cleaned_city):
        st.error("The city field cannot contain numbers.")
    else:
        geocode_result = get_coordinates(cleaned_city, country_code)

        if geocode_result is None:
            st.error("The city could not be found.")
        elif geocode_result.get("country") != country_code:
            st.error(
                "The selected country code does not match "
                "the city's country code."
            )
        else:
            # Az adatokat eltesszük, így automatikus frissítéskor
            # nem kell újra meghívni a geokód API-t.
            st.session_state["weather_city"] = cleaned_city
            st.session_state["weather_country_code"] = country_code
            st.session_state["weather_latitude"] = geocode_result["lat"]
            st.session_state["weather_longitude"] = geocode_result["lon"]


auto_display()