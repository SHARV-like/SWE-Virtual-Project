import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Load processed data
df = pd.read_csv("formatted_output.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Sort by Date
df = df.sort_values("Date")

# Group by Date (total daily sales)
df_daily = df.groupby("Date")["Sales"].sum().reset_index()

# Create line chart
fig = px.line(
    df_daily,
    x="Date",
    y="Sales",
    title="Pink Morsel Daily Sales Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Sales"
)

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Visualiser"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)