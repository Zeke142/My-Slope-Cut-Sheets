import streamlit as st
import pandas as pd
import numpy as np

# Optional: Match style with vertical curve app
# Uncomment this if you have a style.css file
# with open("style.css") as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Slope Cut Sheet", layout="centered")

st.title("Slope Cut Sheet Generator")

# --- User Input Section ---
st.header("1. Input Parameters")

col1, col2 = st.columns(2)

with col1:
    begin_station = st.number_input("Begin Station", value=0.0, step=10.0)
    begin_elev = st.number_input("Begin Elevation", value=100.0, step=0.1)

with col2:
    end_station = st.number_input("End Station", value=100.0, step=10.0)
    end_elev = st.number_input("End Elevation", value=110.0, step=0.1)

increment = st.number_input("Station Increment", value=20.0, min_value=0.1)

# --- Custom Stations (Odd or Specific) ---
st.header("2. Add Custom Stations")

if "odd_stations" not in st.session_state:
    st.session_state.odd_stations = []

new_odd = st.number_input("Enter a custom station (e.g. 25, 45.5)", key="new_odd")

col3, col4 = st.columns([1, 1])
with col3:
    if st.button("Add Station"):
        if new_odd not in st.session_state.odd_stations:
            st.session_state.odd_stations.append(new_odd)
            st.success(f"Added station: {new_odd}")
        else:
            st.warning("That station is already added.")

with col4:
    if st.button("Clear Custom Stations"):
        st.session_state.odd_stations.clear()
        st.info("Custom stations cleared.")

# --- Validation and Calculation ---
if end_station == begin_station:
    st.error("Begin and end stations cannot be the same.")
    st.stop()

slope = (end_elev - begin_elev) / (end_station - begin_station)
slope_pct = slope * 100

st.markdown(f"### Slope: **{slope_pct:.2f}%**")

# Generate station/elevation data
station_range = np.arange(begin_station, end_station + increment, increment)
elevations_main = begin_elev + slope * (station_range - begin_station)

df_main = pd.DataFrame({
    "Station": station_range,
    "Elevation (ft)": np.round(elevations_main, 3)
})

# Custom station processing
odd_stations = sorted(set(st.session_state.odd_stations))
if odd_stations:
    odd_elevs = begin_elev + slope * (np.array(odd_stations) - begin_station)
    df_odd = pd.DataFrame({
        "Station": odd_stations,
        "Elevation (ft)": np.round(odd_elevs, 3)
    })
    df_combined = pd.concat([df_main, df_odd])
else:
    df_combined = df_main

# Final combined, sorted, clean result
df_combined = df_combined.drop_duplicates().sort_values(by="Station").reset_index(drop=True)

# --- Output Table ---
st.header("3. Cut Sheet Output")
st.dataframe(df_combined, use_container_width=True)

# --- Export Option ---
csv = df_combined.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", data=csv, file_name="slope_cut_sheet.csv", mime="text/csv")