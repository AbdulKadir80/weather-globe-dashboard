import streamlit as st
import requests
import plotly.graph_objs as go

API_KEY = ""  # Api Key here 

example_cities = [
    "New York, United States",
    "London, United Kingdom",
    "Paris, France",
    "Dubai, UAE",
    "Mumbai, India"
]

st.set_page_config(page_title="Weather Globe", layout="wide")

st.title("🌍 Global Weather Dashboard")

# Sidebar input
st.sidebar.header("City Search")
city_input = st.sidebar.text_input(
    "Enter city name",
    placeholder="Example: London, United Kingdom"
)

add_city = st.sidebar.button("Add City")

# Session state to store cities
if "cities" not in st.session_state:
    st.session_state.cities = []

if add_city and city_input:
    st.session_state.cities.append(city_input)


def get_weather(city):

    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()

            return {
                "city": city,
                "lat": data['location']['lat'],
                "lon": data['location']['lon'],
                "temp": data['current']['temp_c'],
                "desc": data['current']['condition']['text'],
                "humidity": data['current']['humidity'],
                "wind": data['current']['wind_kph']
            }

    except:
        return None


weather_data = []

with st.spinner("Fetching weather..."):
    for city in st.session_state.cities:
        data = get_weather(city)
        if data:
            weather_data.append(data)

# ---------------- GLOBE ----------------

fig = go.Figure()

for city in weather_data:

    fig.add_trace(go.Scattergeo(
        lon=[city["lon"]],
        lat=[city["lat"]],
        text=[f"{city['city']}<br>{city['temp']}°C<br>{city['desc']}"],
        mode='markers+text',
        marker=dict(
            size=12,
            color=city["temp"],
            colorscale="Turbo",
            colorbar=dict(title="Temp °C")
        )
    ))

fig.update_geos(
    projection_type="orthographic",
    showcountries=True,
    showocean=True,
    showland=True,
    landcolor="lightgreen",
    oceancolor="lightblue"
)

fig.update_layout(
    height=600,
    margin={"r":0,"t":40,"l":0,"b":0}
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- WEATHER CARDS ----------------

st.subheader("City Weather Details")

cols = st.columns(3)

for i, city in enumerate(weather_data):

    with cols[i % 3]:

        st.metric(
            label=city["city"],
            value=f"{city['temp']}°C",
            delta=city["desc"]
        )

        st.write(f"💧 Humidity: {city['humidity']}%")
        st.write(f"💨 Wind: {city['wind']} km/h")

# Example cities

st.sidebar.markdown("### Example Cities")

for city in example_cities:
    st.sidebar.write(city)
