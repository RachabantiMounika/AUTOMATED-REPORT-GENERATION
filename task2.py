import requests
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# Your OpenWeather API key
API_KEY = '33bada5fc0173bd5a4c2fc2c0be5faf5'
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CITY = "London"  # You can change this to any city you want

# Function to fetch weather data from OpenWeather API
def get_weather_data(city, api_key):
    # API parameters
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',  # Get temperature in Celsius
    }
    
    try:
        # Make API request
        response = requests.get(BASE_URL, params=params)
        
        # Check for errors in the request
        if response.status_code != 200:
            print(f"Error: Unable to fetch data. HTTP Status Code: {response.status_code}")
            return None
        
        # Parse response JSON
        data = response.json()
        
        # Extract relevant data from the response
        weather_data = {
            "City": city,
            "Temperature": data["main"]["temp"],
            "Humidity": data["main"]["humidity"],
            "Pressure": data["main"]["pressure"],
            "Weather": data["weather"][0]["description"],
            "Wind Speed": data["wind"]["speed"],
            "Date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return weather_data
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to generate a PDF report
def generate_pdf_report(weather_data, filename="weather_report.pdf"):
    if weather_data:
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica", 12)
        
        # Title
        c.drawString(200, 750, f"Weather Report for {weather_data['City']}")
        c.drawString(200, 730, f"Date: {weather_data['Date']}")
        
        # Weather data
        c.drawString(50, 700, f"Temperature: {weather_data['Temperature']} °C")
        c.drawString(50, 680, f"Humidity: {weather_data['Humidity']} %")
        c.drawString(50, 660, f"Pressure: {weather_data['Pressure']} hPa")
        c.drawString(50, 640, f"Weather: {weather_data['Weather']}")
        c.drawString(50, 620, f"Wind Speed: {weather_data['Wind Speed']} m/s")
        
        # Save the PDF
        c.save()
        print(f"Report saved as {filename}")
    else:
        print("No data to generate report.")

# Fetch weather data for the city
weather_data = get_weather_data(CITY, API_KEY)

# Generate PDF report
generate_pdf_report(weather_data)
