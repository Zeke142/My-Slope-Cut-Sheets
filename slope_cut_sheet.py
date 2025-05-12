import streamlit as st
import pandas as pd
import numpy as np

st.title("Slope Cut Sheet Generator")

# --- User Inputs ---
st.header("Enter Basic Parameters")

begin_station = st.number_input("Begin Station", value=0.0)
end_station = st.number_input("End Station", value=100.0)
begin_elev = st.number_input("Elevation at Begin Station", value=100.0)
end_elev = st.number_input("Elevation at End Station", value=110.0)
increment = st.number_input("Station Increment", value=10.0)

custom_stations_input = st.text_input(
    "Optional: Enter custom (odd or specific) stations separated by commas",
    value="25,45,85"
)

# --- Data Preparation ---
station_range = np.arange(begin_station, end_station + increment, increment)
slope = (end_elev - begin_elev) / (end_station - begin_station)

elevations = begin_elev + slope * (station_range - begin_station)

df_main = pd.DataFrame({
    "Station": station_range,
    "Elevation": np.round(elevations, 3),
    "Formula": [f"{begin_elev} + {slope:.3f} * ({s:.2f} - {begin_station})" for s in station_range]
})

# Handle custom (odd or specific) stations
if custom_stations_input.strip():
    try:
        custom_stations = [float(s.strip()) for s in custom_stations_input.split(',')]
        custom_elevs = begin_elev + slope * (np.array(custom_stations) - begin_station)

        df_custom = pd.DataFrame({
            "Station": custom_stations,
            "Elevation": np.round(custom_elevs, 3),
            "Formula": [f"{begin_elev} + {slope:.3f} * ({s:.2f} - {begin_station})" for s in custom_stations]
        })
    except:
        st.error("Check your custom station input format.")
        df_custom = None
else:
    df_custom = None

# --- Display Results ---
st.subheader("Incremental Stations")
st.dataframe(df_main)

if df_custom is not None:
    st.subheader("Custom Stations")
    st.dataframe(df_custom)

# --- Export Option ---
combined_df = pd.concat([df_main, df_custom]) if df_custom is not None else df_main
csv = combined_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Results as CSV", csv, "slope_cut_sheet.csv", "text/csv")
