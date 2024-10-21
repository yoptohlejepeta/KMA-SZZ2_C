import streamlit as st
import pandas as pd
import plotly.express as px

import graphs

st.set_page_config(page_title="KMA/SZZ2 - C", page_icon="📊", layout="wide")

st.title("📊 Gender pay gap")

data = pd.read_csv("data/data.csv")
gpgi = pd.read_csv("data/gpgi.csv")
gpgi_long = pd.read_csv("data/gpgi_long.csv")
gpgi_cz = gpgi.loc[gpgi["Country"] == "Czech Republic"]

scope_values = {
    "Svět": "world",
    "Evropa": "europe",
    "Severní Amerika": "north america",
    "Jižní Amerika": "south america",
    "Asie": "asia",
    "Afrika": "africa",
}

tab1, tab2, tab3 = st.tabs(["Tabulky", "GPGI", "ČR"])

with tab1:
    st.header("Data")
    st.write("Přehled zpracovaných dat.")

    col1, col2, col3 = st.columns(3)

    st.subheader("GPGI")
    st.write("Gender pay gap index v letech 2016–2023.")

    gpgi_country = st.selectbox("Země", ["Vše"] + gpgi["Country"].unique().tolist())

    if not gpgi_country == "Vše":
        st.dataframe(gpgi.loc[gpgi["Country"] == gpgi_country])
    else:
        st.dataframe(gpgi)

    st.subheader("Demografické ukazatele")

    col1, col2 = st.columns(2)

    data_country = col1.selectbox("Země", ["Vše"] + data["Country"].unique().tolist())
    indicator = col2.selectbox(
        "Ukazatel", ["Vše"] + data["Indicator"].unique().tolist()
    )

    if (data_country == "Vše") and (indicator == "Vše"):
        st.dataframe(data, use_container_width=True)
    elif indicator == "Vše":
        st.dataframe(
            data.loc[data["Country"] == data_country], use_container_width=True
        )
    elif data_country == "Vše":
        st.dataframe(data.loc[data["Indicator"] == indicator], use_container_width=True)
    else:
        st.dataframe(
            data.loc[
                (data["Indicator"] == indicator) & (data["Country"] == data_country)
            ],
            use_container_width=True,
        )

with tab2:
    st.header("Vývoj GPGI v letech 2016 až 2023")
    col1, col2 = st.columns(2)

    year = col1.selectbox("Rok", [year for year in range(2016, 2024)])
    scope = col2.selectbox("Území", scope_values.keys())

    col1, col2, col3 = st.columns([2, 1, 1])

    # Create a choropleth map
    fig = px.choropleth(
        gpgi,
        locations="ISO3",
        locationmode="ISO-3",
        color=f"{year} Rank",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Plasma_r,
        scope=scope_values[scope],
    )
    if scope_values[scope] == "world":
        fig.update_geos(
            projection_type="natural earth",
            # showcoastlines=True, coastlinecolor="RebeccaPurple",
            showland=True,
            landcolor="LightGreen",
            showocean=True,
            oceancolor="LightBlue",
        )

    fig.update_layout(
        title={"y": 0.95, "x": 0.5, "xanchor": "center", "yanchor": "top"},
        font=dict(size=18, color="Black"),
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
    )

    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))

    fig.update_layout(title_text="")
    col1.plotly_chart(fig)

    gpgi_sorted = gpgi_long.loc[(gpgi_long["year"] == year)].sort_values(
        by="rank", ascending=True
    )[["rank", "country", "region"]]
    gpgi_sorted.dropna(subset=["rank"], inplace=True)
    gpgi_sorted.columns = ["Pořadí", "Země", "Region"]

    col2.subheader("Prvních 10")
    col2.dataframe(gpgi_sorted.head(10), hide_index=True)

    col3.subheader(
        "Posledních 10", help="Zobrazeny jsou pouze státy, kde byla dostupná data"
    )
    col3.dataframe(gpgi_sorted.tail(10), hide_index=True)
    
    st.header("Porovnání GPGI s vybranými demografickými ukazateli")
    
    tab_hdp, tab_lifeexp, tab_schoolexpm, tab_schoolexpf = st.tabs(
        [
            "HDP",
            "Očekávaná průměrná délka života",
            "Průměrná délka školní docházky - Muži",
            "Průměrná délka školní docházky - Ženy",
        ]
    )

    with tab_hdp:
        st.plotly_chart(graphs.create_bubble_gdp(), key="gdp")
    with tab_lifeexp:
        st.plotly_chart(graphs.create_bubble_lifeexp(), key="lifeexp")
    with tab_schoolexpm:
        st.plotly_chart(graphs.bubble_school_exp_male(), key="schoolexpm")
    with tab_schoolexpf:
        st.plotly_chart(graphs.bubble_school_exp_female(), key="schoolexpf")

    st.plotly_chart(graphs.top_10graph())

    top10 = gpgi_sorted.head(10)["Země"].unique()

    st.divider()

    st.header("Demografické charakteristiky top 10 států")

    country = st.selectbox("Země", top10)

    st.plotly_chart(graphs.dem_vyvoj_hdp(country))

    st.divider()


    # indicator = st.selectbox("ad",["HDP", "Očekávaná průměrná délka života", "Průměrná délka školní docházky - Ženy", "Průměrná délka školní docházky - Muži"])

with tab3:
    st.header("Čeká Republika")
    st.subheader("Vývoj GPGI v České republice")
    fig = px.line(
        gpgi_long.loc[gpgi_long["country"] == "Czech Republic"],
        x="year",
        y="gpgi",
        template="none",
        labels={"year": "Rok", "gpgi": "GPGI"},
    )

    fig.update_layout(
        font=dict(color="Black"),
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
    )

    st.plotly_chart(fig)

    st.divider()

    st.subheader("Porovnání ČR s ostatními státy")

    gpgi_sorted = gpgi_long.loc[(gpgi_long["year"] == year)].sort_values(
        by="rank", ascending=True
    )[["rank", "country", "region"]]
    gpgi_sorted.dropna(subset=["rank"], inplace=True)

    top10 = gpgi_sorted.head(10).country

    col1, col2 = st.columns(2)

    year = col1.selectbox(
        "Rok",
        [year for year in range(2016, 2024)],
        key="asdakjsdnm",
        help="Rok, který určuje 10 států s nejvyšším GPGI",
    )
    country = col2.selectbox("Země", top10, key="apjsdna")

    col1.plotly_chart(graphs.cz_hdp(year, country))
    col2.plotly_chart(graphs.cz_rural(year, country))
