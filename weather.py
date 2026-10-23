
import requests

def get_weather(city):
    # Step 1: Find city coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_response = requests.get(
        geo_url,
        params={"name": city, "count": 1, "language": "en"},
        timeout=10
    )
    geo_response.raise_for_status()
    locations = geo_response.json().get("results", [])

    if not locations:
        print("City not found!")
        return

    place = locations[0]
    latitude = place["latitude"]
    longitude = place["longitude"]

    # Step 2: Get weather forecast
    weather_url = "https://api.open-meteo.com/v1/forecast"

    response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto",
            "forecast_days": 3
        },
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    # Step 3: Display current conditions
    current = data["current"]
    print(f"\nWeather in {place['name']}, {place.get('country', '')}")
    print("-" * 35)
    print(f"Temperature: {current['temperature_2m']} °C")
    print(f"Humidity: {current['relative_humidity_2m']}%")
    print(f"Wind speed: {current['wind_speed_10m']} km/h")

    # Step 4: Display daily forecast
    daily = data["daily"]
    print("\n3-Day Forecast")

    for i, date in enumerate(daily["time"]):
        print(
            f"{date}: Min {daily['temperature_2m_min'][i]} °C, "
            f"Max {daily['temperature_2m_max'][i]} °C"
        )

if __name__ == "__main__":
    city = input("Enter city name: ").strip()

    try:
        get_weather(city)
    except requests.RequestException as error:
        print("Unable to fetch weather:", error)
