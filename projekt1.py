
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from itables import show
import geopandas as gpd


# Wczytanie danych
data = pd.read_excel("./who_aap_2021_v9_11august2022.xlsx", "AAP_2022_city_v9")
d = pd.read_excel("./who_aap_2021_v9_11august2022.xlsx", "2020")
shapefile = r'C:\Users\user\Downloads\swiat\swiat.shp'      



# Funkcja do analizy danych na poziomie kraju lub miasta
def analyze_data(location, level):
    if level == 'Kraj':
        # Analiza na poziomie kraju
        country_data = data[data['WHO Country Name'] == location]
        
        # Podsumowanie statystyk dla wybranego kraju
        st.write("Statystyki dla", location, ":")
        st.write(country_data.describe())
        show(country_data.describe())

        
        # Wykresy dla PM2.5, PM10 i NO2
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        sns.boxplot(y=country_data['PM2.5 (μg/m3)'], ax=axes[0])
        axes[0].set_title('PM2.5')
        sns.boxplot(y=country_data['PM10 (μg/m3)'], ax=axes[1])
        axes[1].set_title('PM10')
        sns.boxplot(y=country_data['NO2 (μg/m3)'], ax=axes[2])
        axes[2].set_title('NO2')
        st.pyplot(fig)
        
        
    elif level == 'Miasto':
        # Analiza na poziomie miasta
        city_data = data[data['City or Locality'] == location]
        
        # Podsumowanie statystyk dla wybranego miasta
        st.write("Statystyki dla", location, ":")
        st.write(city_data.describe())
        show(city_data.describe())

        
        # Wykresy dla PM2.5, PM10 i NO2
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        sns.boxplot(y=city_data['PM2.5 (μg/m3)'], ax=axes[0])
        axes[0].set_title('PM2.5')
        sns.boxplot(y=city_data['PM10 (μg/m3)'], ax=axes[1])
        axes[1].set_title('PM10')
        sns.boxplot(y=city_data['NO2 (μg/m3)'], ax=axes[2])
        axes[2].set_title('NO2')
        st.pyplot(fig)

    elif level == 'Region':
        # Analiza na poziomie regionu
        region_data = data[data['WHO Region'] == location]
        
        # Podsumowanie statystyk dla wybranego regionu
        st.write("Statystyki dla regionu", location, ":")
        st.write(region_data.describe())
        show(region_data.describe())


        # Wykresy dla PM2.5, PM10 i NO2
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        sns.boxplot(y=region_data['PM2.5 (μg/m3)'], ax=axes[0])
        axes[0].set_title('PM2.5')
        sns.boxplot(y=region_data['PM10 (μg/m3)'], ax=axes[1])
        axes[1].set_title('PM10')
        sns.boxplot(y=region_data['NO2 (μg/m3)'], ax=axes[2])
        axes[2].set_title('NO2')
        st.pyplot(fig)


def map(data, shapefile):
    st.subheader("Średnie roczne stężenie dla konkretnych zanieczyszczeń dla 2020 r.")

    excel = pd.read_excel("./who_aap_2021_v9_11august2022.xlsx", "2020")
    shapefile_path = r'C:\Users\user\Downloads\swiat\swiat.shp'      
    shapefile = gpd.read_file(shapefile_path)


    selected_column = st.selectbox("Wybierz zanieczyszczenie:", excel.columns[5:8], key='map1')

    # Zmienna gdf_merged
    gdf_merged = None

    # Łączenie danych po kolumnie ISO3_CODE
    gdf_merged = shapefile.merge(excel, on="ISO3_CODE", how="left")

    # Przekształcenie na wartości float
    gdf_merged[selected_column] = gdf_merged[selected_column].replace(',', '.')
    gdf_merged[selected_column] = gdf_merged[selected_column].astype(float)


    if gdf_merged is not None:
        # Dobierz lepszy schemat kolorów
        cmap = 'OrRd'

        # Ustaw niestandardowe limity wartości kolorów
        vmin = gdf_merged[selected_column].min()
        vmax = gdf_merged[selected_column].max()

        # Wyświetlenie kartogramu
        fig, ax = plt.subplots()
        gdf_merged.plot(column=selected_column, cmap=cmap, legend=True, ax=ax, vmin=vmin, vmax=vmax)

        # Pobierz obiekt ScalarMappable
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))

        plt.title('Średnie roczne stężenie ' + selected_column)
        st.pyplot(fig)

    else:
        st.write("Brak danych")
    

def main():

    st.header("Projekt 1")
    st.subheader("EDA Z UWZGLĘDNIENIEM CZYNNIKA PRZESTRZENNEGO")

    # Lista rozwijana z możliwością wyboru kraju lub miasta
    level = st.selectbox('Wybierz poziom:', ['Region', 'Kraj', 'Miasto', 'Mapa'])

    # Lista rozwijana z dostępnymi lokalizacjami
    if level == 'Region':
        location_options = data['WHO Region'].unique()
        

    elif level == 'Kraj':
        location_options = data['WHO Country Name'].unique()
    elif level == 'Miasto':
        location_options = data['City or Locality'].unique()
    else:
        location_options = []

    location = st.selectbox('Wybierz lokalizację:', location_options)


    if level == 'Mapa':
        map(d, shapefile)
    else:
        # Analiza danych na podstawie wybranego poziomu i lokalizacji
        analyze_data(location, level)


if __name__ == "__main__":
    main()
