import pandas as pd
from dash import Dash, html, dcc
import plotly.graph_objects as go

# Load data
df = pd.read_csv("formatted_output.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

df_daily = df.groupby("Date")["Sales"].sum().reset_index()

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df_daily["Date"],
        y=df_daily["Sales"],
        mode="lines+markers",
        line=dict(
            color="#00e676",  # Bright green
            width=3,
            shape="spline"
        ),
        marker=dict(
            size=8,
            color="#ff6ec7",  # Pinkish dots
            line=dict(width=1, color="white")
        ),
        hovertemplate="<b>Date:</b> %{x}<br><b>Sales:</b> $%{y:,.2f}<extra></extra>"
    )
)

# Default zoom (last 4 months)
end_date = df_daily["Date"].max()
start_date = end_date - pd.DateOffset(months=4)
fig.update_xaxes(range=[start_date, end_date])

# Highlight price increase
fig.add_vline(
    x="2021-01-15",
    line_width=2,
    line_dash="dash",
    line_color="red"
)

# Dark theme styling
fig.update_layout(
    title="Pink Morsel Sales Trend",
    title_x=0.5,
    paper_bgcolor="#1e1e1e",     # Outside graph background
    plot_bgcolor="#2a2a2a",      # Plot area background
    font=dict(color="white"),
    xaxis_title="Date",
    yaxis_title="Total Sales ($)",
    hovermode="x unified"
)

# Dash app
app = Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#1e1e1e",
        "padding": "30px",
        "fontFamily": "Arial"
    },
    children=[
        html.H1(
            "Soul Foods Sales Dashboard",
            style={
                "textAlign": "center",
                "color": "#ff6ec7"
            }
        ),
        dcc.Graph(figure=fig)
    ]
)

if __name__ == "__main__":
    app.run(debug=True)