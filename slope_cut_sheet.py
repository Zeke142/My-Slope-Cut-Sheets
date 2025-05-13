import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Slope Cut Sheet", layout="centered")

# --- Title ---
st.title("Slope Cut Sheet Generator")
st.markdown("Enter basic data to generate a cut sheet with calculated elevations.")

# --- Input Section ---
st.header("1. Input Parameters")

col1, col2 = st.columns(2)

with col1:
    begin_station = st.number_input("Begin Station", value=0.0)
    begin_elev = st.number_input("Begin Elevation", value=100.0)

with col2:
    end_station = st.number_input("End Station", value=100.0)
    end_elev = st.number_input("End Elevation", value=110.0)

increment = st.number_input("Station Increment", value=20.0, min_value=0.1)

# --- Custom Stations Section ---
st.header("2. Add Custom Stations")

if "custom_stations" not in st.session_state:
    st.session_state.custom_stations = []

new_station = st.number_input("Enter Custom Station", value=0.0, key="new_station")

col3, col4 = st.columns([1, 1])
with col3:
    if st.button("Add Station"):
        if new_station not in st.session_state.custom_stations:
            st.session_state.custom_stations.append(new_station)
            st.success(f"Station {new_station:.2f} added.")
        else:
            st.warning("Station already added.")

with col4:
    if st.button("Clear All Custom Stations"):
        st.session_state.custom_stations.clear()

if st.session_state.custom_stations:
    st.markdown("**Current Custom Stations:**")
    st.write(sorted(st.session_state.custom_stations))

# --- Calculation ---
if end_station != begin_station:
    slope = (end_elev - begin_elev) / (end_station - begin_station)
    slope_percent = slope * 100
else:
    st.error("Begin and end stations cannot be the same.")
    slope = 0
    slope_percent = 0

st.markdown(f"### Slope: {slope_percent:.2f}%")

# Generate main incremental stations
station_range = np.arange(begin_station, end_station + increment, increment)
elevations_main = begin_elev + slope * (station_range - begin_station)

df_main = pd.DataFrame({
    "Station": station_range,
    "Elevation (ft)": np.round(elevations_main, 3)
})

# Custom stations
custom_stations = sorted(set(st.session_state.custom_stations))
if custom_stations:
    custom_elevs = begin_elev + slope * (np.array(custom_stations) - begin_station)
    df_custom = pd.DataFrame({
        "Station": custom_stations,
        "Elevation (ft)": np.round(custom_elevs, 3)
    })
else:
    df_custom = None

# Merge & Sort
if df_custom is not None:
    df_combined = pd.concat([df_main, df_custom])
else:
    df_combined = df_main

df_combined = df_combined.drop_duplicates().sort_values("Station").reset_index(drop=True)

# --- Output Section ---
st.header("3. Results")

st.dataframe(df_combined, use_container_width=True)

csv = df_combined.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", data=csv, file_name="slope_cut_sheet.csv", mime="text/csv")