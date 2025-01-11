import pandas as pd
from core import methods as m1
from core import HelperTools as ht

from config import pdict


@ht.timer
def main():
    """Main: Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""
    # Load geographic data for postal codes
    df_postal_codes = pd.read_csv("datasets/" + pdict["file_geodat_plz"], delimiter=";")

    # Load and preprocess location station data
    df_location_stations = pd.read_csv("datasets/" + pdict["file_lstations"], delimiter=",")
    df_preprocessed_stations = m1.preprop_lstat(df_location_stations, df_postal_codes, pdict)
    gdf_station_occurrences_by_plz = m1.count_plz_occurrences(df_preprocessed_stations)

    # Load and preprocess resident data
    df_resident_data = pd.read_csv("datasets/" + pdict["file_residents"], delimiter=",")
    gdf_preprocessed_residents = m1.preprop_resid(df_resident_data, df_postal_codes, pdict)

    # Generate Streamlit visualization for electric charging and residents
    m1.make_streamlit_electric_Charging_resid(gdf_station_occurrences_by_plz, gdf_preprocessed_residents)


if __name__ == "__main__":
    main()
