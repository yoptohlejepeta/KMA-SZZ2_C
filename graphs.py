import pandas as pd
import plotly.express as px
import streamlit as st

gpgi_long = pd.read_csv("data/gpgi_long.csv")


def create_bubble_lifeexp():
    pop = pd.read_csv("init_data/Total_population.csv")
    pop = pop.loc[pop["Indicator"] == "Total population (thousands)"][
        ["LOCATION", "TIME", "Value"]
    ]
    new_ind = pd.read_csv("init_data/Life_expectancy.csv")
    new_ind = new_ind.loc[
        new_ind["Indicator"] == "Life expectancy at birth, total (years)"
    ][["Indicator", "LOCATION", "TIME", "Value"]]
    gpgi = pd.read_csv("data/gpgi_long.csv")

    df = gpgi.merge(pop, left_on=["iso3", "year"], right_on=["LOCATION", "TIME"])
    df.rename(columns={"Value": "pop_thousands"}, inplace=True)
    df.drop(columns=["TIME", "LOCATION"], inplace=True)

    df = df.merge(new_ind, left_on=["iso3", "year"], right_on=["LOCATION", "TIME"])
    df.rename(columns={"Value": "life_expectancy"}, inplace=True)
    df.drop(columns=["TIME", "LOCATION"], inplace=True)

    df["pop_thousands"] = df["pop_thousands"] * 1000
    df = df[["life_expectancy", "gpgi", "pop_thousands", "region", "country", "year"]]
    df.columns = [
        "Očekávaná průměrná délka života",
        "GPGI",
        "Populace",
        "Region",
        "Země",
        "Rok",
    ]

    fig = px.scatter(
        df,
        x="Očekávaná průměrná délka života",
        y="GPGI",
        size="Populace",
        color="Region",
        hover_name="Země",
        template="none",
        labels={
            "Očekávaná průměrná délka života": "Očekávaná průměrná délka života (log)",
            "GPGI": "GPGI",
        },
        size_max=60,
        log_x=True,
        animation_frame="Rok",
        animation_group="Země",
    )

    fig.update_layout(
        title={
            "text": "GPGI vs Očekávaná průměrná délka života",
        },
        font=dict(
            # family="Poppins, sans-serif",
            color="Black"
        ),
        hoverlabel=dict(
            font_size=16,
        ),
    )

    # fig.update_layout(transition = {'duration': 3000})
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500

    return fig


def create_bubble_gdp():
    pop = pd.read_csv("init_data/Total_population.csv")
    pop = pop.loc[pop["Indicator"] == "Total population (thousands)"][
        ["LOCATION", "TIME", "Value"]
    ]
    new_ind = pd.read_csv("init_data/GDP_per_capita.csv")
    new_ind = new_ind.loc[
        new_ind["Indicator"] == "GDP per capita, PPP (current international $)"
    ][["Indicator", "LOCATION", "TIME", "Value"]]
    gpgi = pd.read_csv("data/gpgi_long.csv")

    df = gpgi.merge(pop, left_on=["iso3", "year"], right_on=["LOCATION", "TIME"])
    df.rename(columns={"Value": "pop_thousands"}, inplace=True)
    df.drop(columns=["TIME", "LOCATION"], inplace=True)

    df = df.merge(new_ind, left_on=["iso3", "year"], right_on=["LOCATION", "TIME"])
    df.rename(columns={"Value": "gdp"}, inplace=True)
    df.drop(columns=["TIME", "LOCATION"], inplace=True)

    df["pop_thousands"] = df["pop_thousands"] * 1000
    df = df[["gdp", "gpgi", "pop_thousands", "region", "country", "year"]]
    df.columns = ["HDP", "GPGI", "Populace", "Region", "Země", "Rok"]

    fig = px.scatter(
        df,
        x="HDP",
        y="GPGI",
        size="Populace",
        color="Region",
        hover_name="Země",
        template="none",
        labels={
            "Očekávaná průměrná délka života": "Očekávaná průměrná délka života (log)",
            "GPGI": "GPGI",
        },
        size_max=60,
        log_x=True,
        animation_frame="Rok",
        animation_group="Země",
    )

    fig.update_layout(
        title={
            "text": "GPGI vs HDP",
        },
        font=dict(
            # family="Poppins, sans-serif",
            color="Black"
        ),
        hoverlabel=dict(
            font_size=16,
        ),
    )

    # fig.update_layout(transition = {'duration': 3000})
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

    return fig


def bubble_school_exp_female():
    pop = pd.read_csv("init_data/Total_population.csv")
    pop = pop.loc[pop["Indicator"] == "Total population (thousands)"][
        ["LOCATION", "TIME", "Value"]
    ]
    gpgi = pd.read_csv("data/gpgi_long.csv")

    df = gpgi.merge(pop, left_on=["iso3", "year"], right_on=["LOCATION", "TIME"])
    df.rename(columns={"Value": "pop_thousands"}, inplace=True)
    df.drop(columns=["TIME", "LOCATION"], inplace=True)
    # Load the school life expectancy data for both males and females
    school_male = pd.read_csv("init_data/School_life_expectancy_male.csv")
    school_female = pd.read_csv("init_data/School_life_expectancy_female.csv")

    # Filter and rename for consistency
    school_male = school_male.loc[
        school_male["Indicator"]
        == "School life expectancy, primary to tertiary, male (years)"
    ][["LOCATION", "TIME", "Value"]]
    school_female = school_female.loc[
        school_female["Indicator"]
        == "School life expectancy, primary to tertiary, female (years)"
    ][["LOCATION", "TIME", "Value"]]

    school_male.rename(columns={"Value": "School_Expectancy_Male"}, inplace=True)
    school_female.rename(columns={"Value": "School_Expectancy_Female"}, inplace=True)

    # Merge the datasets
    df = df.merge(
        school_male, left_on=["iso3", "year"], right_on=["LOCATION", "TIME"], how="left"
    )
    df = df.merge(
        school_female,
        left_on=["iso3", "year"],
        right_on=["LOCATION", "TIME"],
        how="left",
    )
    # df.drop(columns=["TIME", "LOCATION"], inplace=True)

    # Visualize the data
    fig = px.scatter(
        df,
        x="School_Expectancy_Female",
        y="gpgi",
        size="pop_thousands",
        color="region",
        hover_name="country",
        template="none",
        labels={"HDP": "HDP (log)"},
        size_max=60,
        log_x=True,
        animation_frame="year",
        animation_group="country",
    )

    fig.update_layout(
        title="GDPI vs Průměrná délka školní docházky - Ženy",
        xaxis_title="Průměrná délka školní docházky - Ženy (log)",
        yaxis_title="GPGI",
    )

    return fig


def bubble_school_exp_male():
    pop = pd.read_csv("init_data/Total_population.csv")
    pop = pop.loc[pop["Indicator"] == "Total population (thousands)"][
        ["LOCATION", "TIME", "Value"]
    ]
    gpgi = pd.read_csv("data/gpgi_long.csv")

    df = gpgi.merge(pop, left_on=["iso3", "year"], right_on=["LOCATION", "TIME"])
    df.rename(columns={"Value": "pop_thousands"}, inplace=True)
    df.drop(columns=["TIME", "LOCATION"], inplace=True)
    # Load the school life expectancy data for both males and females
    school_male = pd.read_csv("init_data/School_life_expectancy_male.csv")
    school_female = pd.read_csv("init_data/School_life_expectancy_female.csv")

    # Filter and rename for consistency
    school_male = school_male.loc[
        school_male["Indicator"]
        == "School life expectancy, primary to tertiary, male (years)"
    ][["LOCATION", "TIME", "Value"]]
    school_female = school_female.loc[
        school_female["Indicator"]
        == "School life expectancy, primary to tertiary, female (years)"
    ][["LOCATION", "TIME", "Value"]]

    school_male.rename(columns={"Value": "School_Expectancy_Male"}, inplace=True)
    school_female.rename(columns={"Value": "School_Expectancy_Female"}, inplace=True)

    # Merge the datasets
    df = df.merge(
        school_male, left_on=["iso3", "year"], right_on=["LOCATION", "TIME"], how="left"
    )
    df = df.merge(
        school_female,
        left_on=["iso3", "year"],
        right_on=["LOCATION", "TIME"],
        how="left",
    )
    # df.drop(columns=["TIME", "LOCATION"], inplace=True)

    # Visualize the data
    fig = px.scatter(
        df,
        x="School_Expectancy_Male",
        y="gpgi",
        size="pop_thousands",
        color="region",
        hover_name="country",
        template="none",
        labels={"HDP": "HDP (log)"},
        size_max=60,
        log_x=True,
        animation_frame="year",
        animation_group="country",
    )

    fig.update_layout(
        title="GDPI vs Průměrná délka školní docházky - Muži",
        xaxis_title="Průměrná délka školní docházky - Muži (log)",
        yaxis_title="GPGI",
    )

    return fig


def dem_vyvoj_hdp(country):
    df = pd.read_csv("init_data/GDP_per_capita.csv")
    df = df.loc[df["Indicator"] == "GDP per capita, PPP (current international $)"][
        ["Indicator", "LOCATION", "TIME", "Value", "Country"]
    ]

    df = df.loc[df["Country"] == country]
    fig = px.line(
        df,
        x="TIME",
        y="Value",
        title=f"GDP per capita - {country}",
        template="none",
        labels={"TIME": "Rok", "Value": "HDP"},
    )

    return fig


def top_10graph():
    gpgi_sorted = gpgi_long.sort_values(by="year", ascending=True)
    gpgi_sorted = gpgi_long.sort_values(by="rank", ascending=True)[
        ["gpgi", "country", "region", "year"]
    ]
    gpgi_sorted.dropna(subset=["gpgi"], inplace=True)

    fig = px.bar(
        gpgi_sorted,
        x="gpgi",
        y="country",
        orientation="h",
        range_y=[0, 20],
        animation_frame="year",
        animation_group="country",
        labels="",
    )

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500

    return fig


def cz_hdp(year, country):
    gpgi_sorted = gpgi_long.loc[(gpgi_long["year"] == year)].sort_values(
        by="rank", ascending=True
    )[["rank", "country", "region"]]
    gpgi_sorted.dropna(subset=["rank"], inplace=True)

    df = pd.read_csv("init_data/GDP_per_capita.csv")
    df = df.loc[df["Indicator"] == "GDP per capita, PPP (current international $)"][
        ["Indicator", "LOCATION", "TIME", "Value", "Country"]
    ]
    df.columns = ["Indicator", "LOCATION", "TIME", "Value", "Země"]

    df = df.loc[(df["Země"].isin([country, "Czechia"]))]

    fig = px.line(
        df,
        x="TIME",
        y="Value",
        title=f"HDP - {country}",
        template="none",
        color="Země",
        labels={"TIME": "Rok", "Value": "HDP"},
    )

    return fig


def cz_rural(year, country):
    gpgi_sorted = gpgi_long.loc[(gpgi_long["year"] == year)].sort_values(
        by="rank", ascending=True
    )[["rank", "country", "region"]]
    gpgi_sorted.dropna(subset=["rank"], inplace=True)

    top10 = gpgi_sorted.head(10).country

    top10

    df = pd.read_csv("init_data/Rural_population.csv")
    df = df.loc[df["Indicator"] == "Rural population (% of total population)"][
        ["Indicator", "LOCATION", "TIME", "Value", "Country"]
    ]

    df = df.loc[(df["Country"].isin([country, "Czechia"]))]

    fig = px.line(
        df,
        x="TIME",
        y="Value",
        title=f"Rural population",
        template="none",
        color="Country",
        labels={"Value": "Podíl obyvatelstva, žijícího na venkově (%)", "TIME": "Rok"},
    )

    return fig
