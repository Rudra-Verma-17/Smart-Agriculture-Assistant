import os

import requests
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

st.set_page_config(page_title="Rudra | Weather & Advisory", layout="centered")

# --- API Config ---
weather_api_key = os.getenv("OPENWEATHER_API_KEY")
if not weather_api_key:
    try:
        weather_api_key = st.secrets["OPENWEATHER_API_KEY"]
    except StreamlitSecretNotFoundError:
        weather_api_key = None
    except KeyError:
        weather_api_key = None
if not weather_api_key:
    st.error("OpenWeather API key is not configured. Set OPENWEATHER_API_KEY in the environment or Streamlit secrets.")
    st.stop()

base_url = "http://api.openweathermap.org/data/2.5/weather"

# --- State to City Mapping ---
state_city_map = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore"],
    "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat"],
    "Assam": ["Guwahati", "Dibrugarh", "Silchar"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama"],
    "Gujarat": ["Ahmedabad", "Surat", "Rajkot", "Vadodara"],
    "Haryana": ["Chandigarh", "Gurugram", "Faridabad", "Panipat"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubli"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Manipur": ["Imphal", "Thoubal"],
    "Meghalaya": ["Shillong", "Tura"],
    "Mizoram": ["Aizawl", "Lunglei"],
    "Nagaland": ["Kohima", "Dimapur"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Puri", "Rourkela"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jodhpur", "Kota"],
    "Sikkim": ["Gangtok", "Namchi"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
    "Tripura": ["Agartala", "Udaipur"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Nainital"],
    "West Bengal": ["Kolkata", "Siliguri", "Asansol", "Durgapur"],
    "Andaman and Nicobar Islands": ["Port Blair"],
    "Chandigarh": ["Chandigarh"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Silvassa"],
    "Delhi": ["New Delhi", "Delhi"],
    "Jammu and Kashmir": ["Srinagar", "Jammu"],
    "Ladakh": ["Leh", "Kargil"],
    "Lakshadweep": ["Kavaratti"],
    "Puducherry": ["Puducherry", "Karaikal", "Mahe"]
}

# --- Advisory Function ---
def get_weather_advice(temperature, humidity, weather_description, wind_speed):
    advice = []

    # Temperature
    if temperature > 38:
        advice.append("⚠️ High temperature! Irrigate in early morning or late evening.")
    elif temperature < 15:
        advice.append("🌡️ Low temperature. Delay sowing heat-loving crops.")

    # Humidity
    if humidity < 20:
        advice.append("💧 Very low humidity. Increase irrigation frequency.")
    elif humidity > 80:
        advice.append("🌫️ High humidity. Monitor for fungal diseases.")

    # Weather description
    if "rain" in weather_description.lower():
        advice.append("🌧️ Rain expected. Avoid irrigation.")
    elif "clear" in weather_description.lower():
        advice.append("☀️ Clear sky. Ideal for spraying or harvesting.")

    # Wind speed
    if wind_speed > 10:
        advice.append("💨 Windy! Avoid pesticide/fertilizer spraying.")
    elif wind_speed < 2:
        advice.append("🌬️ Low wind speed. Safe for spraying.")

    return advice

# --- UI ---
st.title("🌦️ Rudra Weather & Advisory")

selected_state = st.selectbox("Select State", list(state_city_map.keys()))
selected_city = st.selectbox("Select City", state_city_map[selected_state])
show_advice = st.checkbox("Show Agricultural Advisory")

if st.button("Get Weather"):
    params = {
        "q": selected_city,
        "appid": weather_api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        weather_desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        st.success(f"Weather in {selected_city}, {selected_state}")
        st.write(f"🌡️ Temperature: **{temperature}°C**")
        st.write(f"🌥️ Description: **{weather_desc.title()}**")
        st.write(f"💧 Humidity: **{humidity}%**")
        st.write(f"💨 Wind Speed: **{wind_speed} m/s**")

        if show_advice:
            st.subheader("📋 Agricultural Advisory")
            advice_list = get_weather_advice(temperature, humidity, weather_desc, wind_speed)
            for tip in advice_list:
                st.markdown(f"- {tip}")
    else:
        st.error("❌ Failed to fetch weather. Please try again later.")
