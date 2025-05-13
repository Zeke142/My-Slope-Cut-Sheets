import streamlit as st
import pandas as pd
import numpy as np

# --- Page Title ---
st.title("Slope Cut Sheet Generator")

# --- Input Section ---
st.header("Input Parameters")

col1, col2 = st.columns(2)
with col1:
    begin_station = st.number_input("Begin Station (ft)", value=0.00)
    begin_elev = st.number_input("Begin Elevation (ft)", value=100.00)
with col2:
    end_station = st.number_input("End Station (ft)", value=100.00)
    end_elev = st.number_input("End Elevation (ft)", value=110.00)

increment = st.number_input("Station Interval (ft)", min_value=0.01, value=10.00, step=1.0)

custom_input = st.text_input(
    "Optional: Custom Stations (comma-separated)", 
    value="25,45,85"
)

# --- Slope Calculation ---
if end_station != begin_station:
    slope = (end_elev - begin_elev) / (end_station - begin_station)
    st.success(f"Slope = {slope:.3f} ft/station")
else:
    st.error("Begin and End Station cannot be the same.")
    st.stop()

# --- Generate Main Table ---
main_stations = np.arange(begin_station, end_station + increment, increment)
main_elevations = begin_elev + slope * (main_stations - begin_station)

df_main = pd.DataFrame({
    "Station": main_stations,
    "Elevation (ft)": np.round(main_elevations, 3),
    "Formula": [f"{begin_elev:.2f} + {slope:.3f} × ({s:.2f} - {begin_station:.2f})"
                for s in main_stations]
})

# --- Handle Custom Stations ---
df_custom = None
if custom_input.strip():
    try:
        custom_stations = sorted({float(s.strip()) for s in custom_input.split(",")})
        custom_elevs = begin_elev + slope * (np.array(custom_stations) - begin_station)

        df_custom = pd.DataFrame({
            "Station": custom_stations,
            "Elevation (ft)": np.round(custom_elevs, 3),
            "Formula": [f"{begin_elev:.2f} + {slope:.3f} × ({s:.2f} - {begin_station:.2f})"
                        for s in custom_stations]
        })
    except:
        st.error("Invalid input in custom station list. Use numbers separated by commas.")

# --- Display Results ---
st.subheader("Incremental Stations")
st.dataframe(df_main)

if df_custom is not None:
    st.subheader("Custom Stations")
    st.dataframe(df_custom)

# --- Download Results ---
st.subheader("Export Results")

combined = pd.concat([df_main, df_custom]) if df_custom is not None else df_main
combined = combined.sort_values("Station").reset_index(drop=True)

csv_data = combined.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv_data, file_name="slope_cut_sheet.csv", mime="text/csv")