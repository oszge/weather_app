CREATE TABLE weather_data (id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, temperature NUMERIC(5, 2) NOT NULL, feels_like NUMERIC(5, 2), humidity INTEGER, weather varchar(50), wind_speed NUMERIC(6, 2), air_pressure INTEGER, date_timestamp TIMESTAMP WITH TIME ZONE);
SELECT * FROM weather_data;
INSERT INTO weather_data (id, temperature, feels_like, humidity, weather, wind_speed, air_pressure, date_timestamp) VALUES();

UPDATE weather_data