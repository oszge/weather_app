import psycopg2
import streamlit as st
import requests as req

def fetch_coords_from_url(url):
     try:
          response = req.get(url)

          if response.status_code == 200:
               return response.json()
          else:
               print("Error: Unable to fetch data from API")
     except req.exceptions.RequestException as e:
          print("Error: ", e)
          return None

def fetch_data_from_url(url):
    try:
        response = req.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print("Error: Unable to fetch data from API")
    except req.exceptions.RequestException as e:
            print("Error:", e)
            return None

def connect():
    try:
        return psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres",
            password="123",
        )
    except (psycopg2.Error, ConnectionError) as e:
        ("Error: ", e)
        return None
