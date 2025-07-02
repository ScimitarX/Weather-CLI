#!/usr/bin/env python3
import argparse, os, sys
import requests

API_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"

def get_api_key():
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        print("❌ Please set the OPENWEATHER_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)
    return key

def fetch_weather(city, units):
    params = {
        "q": city,
        "appid": get_api_key(),
        "units": units
    }
    resp = requests.get(API_ENDPOINT, params=params)
    if resp.status_code != 200:
        print("❌ Error fetching data:", resp.json().get("message", resp.text), file=sys.stderr)
        sys.exit(1)
    return resp.json()

def format_output(data):
    name = data["name"]
    weather = data["weather"][0]["description"].title()
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    return (
        f"Weather in {name}:\n"
        f"  → Condition: {weather}\n"
        f"  → Temperature: {temp}° (feels like {feels}°)\n"
        f"  → Humidity: {humidity}%\n"
    )

def main():
    parser = argparse.ArgumentParser(description="CLI Weather App")
    parser.add_argument("city", help="City name, e.g. “London,UK” or “Paris”")
    parser.add_argument(
        "-u", "--units",
        choices=["metric","imperial","standard"],
        default="metric",
        help="Units: metric (°C), imperial (°F), or standard (K)"
    )
    args = parser.parse_args()

    data = fetch_weather(args.city, args.units)
    print(format_output(data))

if __name__ == "__main__":
    main()
