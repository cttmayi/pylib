import pandas as pd
import plotly
import plotly.graph_objects as go
from flytekit import Deck, task, workflow, Resources


@task(requests=Resources(mem="1Gi"))
def clean_data() -> pd.DataFrame:
    """Clean the dataset."""
    df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    filled_df = (
        df.sort_values(["people_vaccinated"], ascending=False)
        .groupby("location")
        .first()
        .reset_index()
    )[["location", "people_vaccinated", "population", "date"]]
    return filled_df

@task(disable_deck=False)
def plot(df: pd.DataFrame):
    """Render a Choropleth map."""
    df["text"] = df["location"] + "<br>" + "Last updated on: " + df["date"]
    fig = go.Figure(
        data=go.Choropleth(
            locations=df["location"],
            z=df["people_vaccinated"].astype(float) / df["population"].astype(float),
            text=df["text"],
            locationmode="country names",
            colorscale="Blues",
            autocolorscale=False,
            reversescale=False,
            marker_line_color="darkgray",
            marker_line_width=0.5,
            zmax=1,
            zmin=0,
        )
    )

    fig.update_layout(
        title_text=(
          "Percent population with at least one dose of COVID-19 vaccine"
        ),
        geo_scope="world",
        geo=dict(
            showframe=False, showcoastlines=False, projection_type="equirectangular"
        ),
    )
    Deck("Choropleth Map", plotly.io.to_html(fig))


@workflow
def analytics_workflow():
    """Prepare a data analytics workflow."""
    plot(df=clean_data())