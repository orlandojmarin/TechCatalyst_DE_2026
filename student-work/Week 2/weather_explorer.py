"""Weather Explorer: a small CLI built from the Bonus Lab notebook.

Run it like:
    uv run python weather_explorer.py "Hartford,US" 41.7658 -72.6734

It fetches today's hourly forecast for one location from Open-Meteo (no API
key needed) and prints today's min, max, and current-hour temperature.
"""
import argparse
import time

import httpx

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_hourly_temperature(latitude, longitude, timezone="UTC"):
    """Return a list of (timestamp, temperature_f) tuples for one location."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "forecast_days": 1,
        "timezone": timezone,
        "temperature_unit": "fahrenheit",
    }
    resp = httpx.get(BASE_URL, params=params, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"API error: {resp.status_code} {resp.text}")
    payload = resp.json()
    hourly = payload.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    return list(zip(times, temps))


def get_hourly_temperature_with_retry(latitude, longitude, timezone="UTC", max_tries=3):
    """Same as get_hourly_temperature, but retries transient failures."""
    # TODO: call get_hourly_temperature(latitude, longitude, timezone=timezone)
    # inside a loop of up to max_tries attempts. Catch (httpx.TransportError,
    # RuntimeError). On the last attempt, let the exception raise. Otherwise,
    # print a message and sleep with exponential backoff (1s, 2s, 4s, ...)
    # before trying again.
    pass


def summarize(readings):
    """Return (min_temp, max_temp, current_temp) from a list of (time, temp) tuples."""
    # TODO: compute the minimum temperature, the maximum temperature, and the
    # temperature of the reading closest to right now. For "current," the
    # simplest correct approach for this lab is the first reading in the list
    # if the API returns hours starting from now, or you can compare each
    # timestamp to time.strftime("%Y-%m-%dT%H:00") and pick the closest match.
    pass


def main():
    parser = argparse.ArgumentParser(description="Print today's weather summary for one location.")
    parser.add_argument("city", help="A label for the location, e.g. 'Hartford,US'")
    parser.add_argument("latitude", type=float)
    parser.add_argument("longitude", type=float)
    parser.add_argument("--timezone", default="America/New_York")
    args = parser.parse_args()

    readings = get_hourly_temperature_with_retry(args.latitude, args.longitude, timezone=args.timezone)
    min_temp, max_temp, current_temp = summarize(readings)

    print(f"Weather for {args.city}")
    print(f"  current: {current_temp}F")
    print(f"  today's low:  {min_temp}F")
    print(f"  today's high: {max_temp}F")


if __name__ == "__main__":
    main()
