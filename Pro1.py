import requests
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
#import os

API_KEY = 'a482f980da9e92e4fe3aaa9298e52732'
BASE_URL = 'https://api.openweathermap.org/data/2.5/forecast'

def fetch_weather_data(city):
    """Fetch weather forecast data for a given city from OpenWeatherMap API."""
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_weather_data(data):
    """Extract date, temperature, and humidity from API response."""
    if not data or "list" not in data:
        print("Invalid data format received.")
        return [], [], []

    dates, temperatures, humidity = [], [], []
    
    for entry in data["list"]:
        dates.append(datetime.datetime.fromtimestamp(entry["dt"]))
        temperatures.append(entry["main"]["temp"])
        humidity.append(entry["main"]["humidity"])

    return dates, temperatures, humidity

def plot_weather_trend(dates, values, ylabel, title, color):
    """Plot weather trends with improved visualization."""
    plt.figure(figsize=(9, 5))
    plt.plot(dates, values, color=color, marker='o', linestyle='-', linewidth=2, markersize=5)
    #Unique styles
    plt.title(title, fontsize=16, fontweight="bold", color="darkblue", pad=15, loc="left")
    plt.xlabel("Date & Time", fontsize=14, fontweight="medium", color="darkred", labelpad=10)
    plt.ylabel(ylabel, fontsize=14, fontweight="medium", color="darkgreen", labelpad=10)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='-', alpha=0.6)
    plt.tight_layout()
    plt.show()

def main():
    city = "Mumbai"  
    weather_data = fetch_weather_data(city)
    
    if weather_data:
        dates, temperatures, humidity = parse_weather_data(weather_data)
        
        if dates:
            sns.set_theme(style="darkgrid", palette="coolwarm")
            sns.set_context("talk")
            sns.set_style("whitegrid", {"axes.facecolor": "#f0f0f0", "grid.color": "#d3d3d3"})
            plot_weather_trend(dates, temperatures, "Temperature (°C)", f"Temperature Trend for {city}", "red")
            plot_weather_trend(dates, humidity, "Humidity (%)", f"Humidity Trend for {city}", "blue")
        else:
            print("No data available to plot.")
    else:
        print("Failed to retrieve weather data.")

if __name__ == "__main__":
    main()
