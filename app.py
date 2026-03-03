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
        "background": "linear-gradient(-45deg, #1e1e1e, #2b1055, #0f2027, #203a43)",
        "backgroundSize": "400% 400%",
        "animation": "gradientBG 15s ease infinite",
        "minHeight": "100vh",
        "padding": "40px",
        "fontFamily": "Arial"
    },
    children=[
        html.H1(
            "Soul Foods Sales Dashboard",
            style={
                "letter-spacing": "5px",
                "textAlign": "center",
                "color": "#3de281",
                "textShadow": "0 0 20px #3de281, 0 0 20px #3de281",
                "marginBottom": "30px",
                "animation": "fadeInUp 1s ease"
            }
        ),

        # 🔹 Region Filter
        html.Div(
            style={"textAlign": "center", "marginBottom": "20px"},
            children=[
                html.Div(
                    className="region-bar",
                    children=[
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "ALL", "value": "all"},
                                {"label": "NORTH", "value": "north"},
                                {"label": "EAST", "value": "east"},
                                {"label": "SOUTH", "value": "south"},
                                {"label": "WEST", "value": "west"},
                            ],
                            value="all",
                            inputClassName="region-radio",
                            labelClassName="region-label"
                        )
                    ]
                )
            ]
        ),

        html.Div(
            className="glass-card",
            children=[
                dcc.Graph(
                    id="sales-graph",
                    config={
                        "displayModeBar": True,
                        "modeBarButtonsToRemove": ["select2d", "lasso2d"]
                    }
                )
            ],
            style={
                "background": "rgba(255, 255, 255, 0.05)",
                "backdropFilter": "blur(15px)",
                "borderRadius": "20px",
                "padding": "20px",
                "boxShadow": "0 8px 32px rgba(0, 0, 0, 0.37)",
                "border": "1px solid rgba(255, 255, 255, 0.18)"
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
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
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)"
        )
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)