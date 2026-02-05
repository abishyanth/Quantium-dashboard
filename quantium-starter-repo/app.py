import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go


df = pd.read_csv("pink_morsels_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
daily_sales = (
    df.groupby("Date", as_index=False)["Sales"]
    .sum()
    .sort_values("Date")
)

# Derive unique regions for the region picker if the column exists
if "Region" in df.columns:
    regions = sorted(df["Region"].dropna().unique())
else:
    regions = []

price_increase_date = pd.to_datetime("2021-01-15")
price_increase_str = "2021-01-15"
before_increase = daily_sales[daily_sales["Date"] < price_increase_date]["Sales"].sum()
after_increase = daily_sales[daily_sales["Date"] >= price_increase_date]["Sales"].sum()
total_sales = daily_sales["Sales"].sum()

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=daily_sales["Date"],
        y=daily_sales["Sales"],
        mode="lines",
        line=dict(width=2.5, color="#0ea5e9"),
        fill="tozeroy",
        fillcolor="rgba(14, 165, 233, 0.12)",
    )
)
fig.add_vline(
    x=price_increase_str,
    line_width=2,
    line_dash="dash",
    line_color="#94a3b8"
)
fig.add_annotation(
    x=price_increase_str,
    y=1,
    yref="paper",
    text="Price Increase (15 Jan 2021)",
    showarrow=False,
    yanchor="bottom",
    font=dict(size=11, color="#64748b", family="Inter, sans-serif"),
    bgcolor="rgba(255,255,255,0.9)",
    borderpad=6,
    borderwidth=1,
    bordercolor="#e2e8f0"
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#334155", size=12),
    title=dict(
        text="Sales Performance Over Time",
        font=dict(size=18, color="#0f172a"),
        x=0.02,
        xanchor="left"
    ),
    xaxis=dict(
        title="",
        gridcolor="#f1f5f9",
        zeroline=False,
        showline=True,
        linecolor="#e2e8f0",
        tickfont=dict(color="#64748b", size=11),
    ),
    yaxis=dict(
        title=dict(text="Total Sales ($)", font=dict(size=12, color="#64748b")),
        gridcolor="#f1f5f9",
        zeroline=False,
        showline=False,
        tickfont=dict(color="#64748b", size=11),
        tickformat=",.0f",
    ),
    margin=dict(l=60, r=24, t=56, b=48),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Inter, sans-serif",
        bordercolor="#e2e8f0",
    ),
)

app = Dash(__name__, suppress_callback_exceptions=True)

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    </head>
    <body>
        {%app_entry%}
        <footer>{%config%}{%scripts%}{%renderer%}</footer>
    </body>
</html>
"""

kpi_style = {
    "flex": 1,
    "minWidth": "180px",
    "padding": "24px",
    "backgroundColor": "white",
    "borderRadius": "12px",
    "boxShadow": "0 1px 3px rgba(0,0,0,0.06)",
    "border": "1px solid #f1f5f9",
}
kpi_value_style = {"fontSize": "28px", "fontWeight": "700", "color": "#0f172a", "marginBottom": "4px"}
kpi_label_style = {"fontSize": "13px", "color": "#64748b", "fontWeight": "500"}

app.layout = html.Div(
    style={
        "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
        "backgroundColor": "#f8fafc",
        "minHeight": "100vh",
        "padding": "48px 24px",
    },
    children=[
        html.Div(
            style={"maxWidth": "1200px", "margin": "0 auto"},
            children=[
                html.Header(
                    style={
                        "marginBottom": "40px",
                        "paddingBottom": "32px",
                        "borderBottom": "1px solid #e2e8f0",
                    },
                    children=[
                        html.H1(
                            "Soul Foods · Pink Morsels",
                            id="main-header",
                            style={
                                "fontSize": "28px",
                                "fontWeight": "700",
                                "color": "#0f172a",
                                "letterSpacing": "-0.02em",
                                "marginBottom": "8px",
                            }
                        ),
                        html.P(
                            "Sales performance analysis to evaluate the impact of the January 15th, 2021 price increase.",
                            style={"fontSize": "15px", "color": "#64748b", "lineHeight": 1.6}
                        ),
                    ]
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "gap": "20px",
                        "marginBottom": "32px",
                        "flexWrap": "wrap",
                    },
                    children=[
                        html.Div(
                            [html.Div(f"${total_sales:,.0f}", style=kpi_value_style), html.Div("Total Sales", style=kpi_label_style)],
                            style=kpi_style
                        ),
                        html.Div(
                            [html.Div(f"${before_increase:,.0f}", style=kpi_value_style), html.Div("Pre–Price Increase", style=kpi_label_style)],
                            style=kpi_style
                        ),
                        html.Div(
                            [html.Div(f"${after_increase:,.0f}", style=kpi_value_style), html.Div("Post–Price Increase", style=kpi_label_style)],
                            style=kpi_style
                        ),
                    ]
                ),
                html.Div(
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "16px",
                        "padding": "28px",
                        "boxShadow": "0 1px 3px rgba(0,0,0,0.06)",
                        "border": "1px solid #f1f5f9",
                        "marginBottom": "32px",
                    },
                    children=[
                        html.Div(
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                                "marginBottom": "16px",
                                "gap": "12px",
                                "flexWrap": "wrap",
                            },
                            children=[
                                html.H2(
                                    "Sales over time",
                                    style={
                                        "fontSize": "18px",
                                        "fontWeight": "600",
                                        "color": "#0f172a",
                                        "margin": 0,
                                    },
                                ),
                                dcc.Dropdown(
                                    id="region-picker",
                                    options=(
                                        [
                                            {"label": region, "value": region}
                                            for region in regions
                                        ]
                                        if regions
                                        else [
                                            {"label": "All regions", "value": "ALL"}
                                        ]
                                    ),
                                    value=regions[0] if regions else "ALL",
                                    clearable=False,
                                    style={
                                        "minWidth": "220px",
                                        "fontSize": "13px",
                                    },
                                ),
                            ],
                        ),
                        dcc.Graph(
                            id="sales-graph",
                            figure=fig,
                            config={"displayModeBar": True, "displaylogo": False},
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.H3(
                            "Key Insight",
                            style={"fontSize": "16px", "fontWeight": "600", "color": "#0f172a", "marginBottom": "12px"}
                        ),
                        html.P(
                            "The change in sales volume before and after the price increase is clearly visible in the trend. "
                            "This visual evidence allows Soul Foods to confidently assess the pricing decision.",
                            style={"fontSize": "14px", "color": "#475569", "lineHeight": 1.7, "margin": 0}
                        )
                    ],
                    style={
                        "padding": "24px 28px",
                        "backgroundColor": "white",
                        "borderRadius": "16px",
                        "boxShadow": "0 1px 3px rgba(0,0,0,0.06)",
                        "border": "1px solid #f1f5f9",
                        "borderLeft": "4px solid #0ea5e9",
                    }
                )
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
