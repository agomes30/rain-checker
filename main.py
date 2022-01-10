import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

owm_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ID")
auth_token = os.environ.get("AUTH_TOKEN")

# Silver Spring, MD
MY_LAT = 38.997662
MY_LONG = -77.027023

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(owm_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]  # next 12 hours

will_rain = False
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_='+13165308650',
        to='YOUR_NUMBER',
    )

    print(message.status)



