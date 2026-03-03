import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go

# Load data
df = pd.read_csv("formatted_output.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

app = Dash(__name__)

# ------------------ Layout ------------------
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

        # 🔹 Region Filter
        html.Div(
            style={"textAlign": "center", "marginBottom": "20px"},
            children=[
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": " All", "value": "all"},
                        {"label": " North", "value": "north"},
                        {"label": " East", "value": "east"},
                        {"label": " South", "value": "south"},
                        {"label": " West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    labelStyle={
                        "color": "white",
                        "marginRight": "20px"
                    }
                )
            ]
        ),

        dcc.Graph(
            id="sales-graph",
            # animate=True,  # 👈 Important
            config={
                "displayModeBar": True,
                "modeBarButtonsToRemove": ["select2d", "lasso2d"]
            }
        )
    ]
)

# ------------------ Callback ------------------
@app.callback(
    Output("sales-graph", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):

    # 🔹 Filter data
    if selected_region != "all":
        filtered_df = df[df["Region"].str.lower() == selected_region]
    else:
        filtered_df = df.copy()

    df_daily = (
        filtered_df
        .groupby("Date")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    # 🔹 Create figure
    fig = go.Figure()

    # Main line
    fig.add_trace(
        go.Scatter(
            x=df_daily["Date"],
            y=df_daily["Sales"],
            mode="lines+markers",
            name="Total Sales",
            line=dict(color="#00e676", width=3, shape="spline"),
            marker=dict(size=5, color="#ff6ec7", line=dict(width=1, color="white"))
        )
    )

    # Glow effect
    fig.add_trace(
        go.Scatter(
            x=df_daily["Date"],
            y=df_daily["Sales"],
            mode="lines",
            line=dict(
                color="#00e676",
                width=3,
                shape="spline",
                smoothing=1.3
            ),
            opacity=0.15,
            showlegend=False
        )
    )

    # Price increase vertical line
    price_date = pd.to_datetime("2021-01-15")

    fig.add_trace(
        go.Scatter(
            x=[price_date, price_date],
            y=[df_daily["Sales"].min(), df_daily["Sales"].max()],
            mode="lines",
            name="Price Increase (15 Jan 2021)",
            line=dict(color="red", dash="dash", width=2)
        )
    )

    # 🔥 IMPORTANT: Enable Auto Centering
    # fig.update_xaxes(autorange=True)
    # fig.update_yaxes(autorange=True)

    # Layout styling
    fig.update_layout(
        title="Pink Morsel Sales Trend",
        title_x=0.5,
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#2a2a2a",
        font=dict(color="white"),
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        hovermode="x unified",
        dragmode=False,
        height=600,
        legend=dict(
            x=0.98,
            y=0.98,
            xanchor="right",
            yanchor="top",
            bgcolor="#2a2a1a",
            bordercolor="white",
            borderwidth=1,
            font=dict(color="white")
        ),
        transition=dict(
            duration=600,
            easing="cubic-in-out"
        )
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)