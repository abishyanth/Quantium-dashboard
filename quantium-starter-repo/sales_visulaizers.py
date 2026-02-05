import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import json
import time

df = pd.read_csv("pink_morsels_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])


# #region agent log helper
def _agent_log(hypothesis_id, location, message, data=None, run_id="pre-fix"):
    entry = {
        "sessionId": "debug-session",
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data or {},
        "timestamp": int(time.time() * 1000),
    }
    try:
        with open(r"d:\projects\Quantium_soul_foods_dashboard\.cursor\debug.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        # Logging must never break the app
        pass


# #endregion

price_increase_date = pd.to_datetime("2021-01-15")
price_increase_str = "2021-01-15"

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

kpi_style = {"flex": 1,"minWidth": "180px","padding": "24px","backgroundColor": "white","borderRadius": "12px","boxShadow": "0 1px 3px rgba(0,0,0,0.06)","border": "1px solid #f1f5f9",}
kpi_value_style = {"fontSize": "28px","fontWeight": "700","color": "#0f172a","marginBottom": "4px",}
kpi_label_style = {"fontSize": "13px","color": "#64748b","fontWeight": "500",}

app.layout = html.Div(
    style={"fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif","backgroundColor": "#f8fafc","minHeight": "100vh","padding": "48px 24px",},
    children=[
        html.Div(
            style={"maxWidth": "1200px", "margin": "0 auto"},
            children=[

                html.Header(
                    style={"marginBottom": "40px","paddingBottom": "32px","borderBottom": "1px solid #e2e8f0",},
                    children=[
                        html.H1(
                            "Soul Foods · Pink Morsels",
                            id="main-header",
                            style={"fontSize": "28px","fontWeight": "700","color": "#0f172a","letterSpacing": "-0.02em","marginBottom": "8px",},
                        ),
                        html.P(
                            "Sales performance analysis to evaluate the impact of the January 15th, 2021 price increase.",
                            style={"fontSize": "15px", "color": "#64748b", "lineHeight": 1.6},
                        ),
                    ],
                ),

                html.Div(
                    style={"display": "flex","justifyContent": "space-between","alignItems": "center","marginBottom": "24px","flexWrap": "wrap","gap": "16px",},
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    "Filter by Region",
                                    style={"fontSize": "13px","fontWeight": "600","color": "#475569","marginBottom": "8px",},
                                ),
                                dcc.RadioItems(
                                    id="region-filter",
                                    options=[
                                        {"label": "All", "value": "all"},
                                        {"label": "North", "value": "north"},
                                        {"label": "East", "value": "east"},
                                        {"label": "South", "value": "south"},
                                        {"label": "West", "value": "west"},
                                    ],
                                    value="all",
                                    inline=True,
                                    inputStyle={"marginRight": "6px"},
                                    labelStyle={"marginRight": "16px","fontSize": "14px","color": "#334155","cursor": "pointer",},
                                ),
                            ]
                        )
                    ],
                ),

                # KPI Cards
                html.Div(
                    style={"display": "flex","gap": "20px","marginBottom": "32px","flexWrap": "wrap",},
                    children=[
                        html.Div(
                            [html.Div(id="total-quantity", style=kpi_value_style),
                             html.Div("Total Quantity", style=kpi_label_style)],
                            style=kpi_style,
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(id="before-qty", style={"fontSize": "20px", "fontWeight": "700", "color": "#0f172a"}),
                                        html.Div("Qty Pre–Price Increase", style={"fontSize": "12px", "color": "#64748b", "marginBottom": "10px"}),
                                        html.Div(id="after-qty", style={"fontSize": "20px", "fontWeight": "700", "color": "#0f172a"}),
                                        html.Div("Qty Post–Price Increase", style={"fontSize": "12px", "color": "#64748b"}),
                                    ]
                                ),
                                html.Div("Quantity Split", style={**kpi_label_style, "marginTop": "12px"}),
                            ],
                            style=kpi_style,
                        ),
                        html.Div(
                            [html.Div(id="total-sales", style=kpi_value_style),
                             html.Div("Total Sales", style=kpi_label_style)],
                            style=kpi_style,
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(id="before-sales", style={"fontSize": "20px", "fontWeight": "700", "color": "#0f172a"}),
                                        html.Div("Pre–Price Increase", style={"fontSize": "12px", "color": "#64748b", "marginBottom": "10px"}),
                                        html.Div(id="after-sales", style={"fontSize": "20px", "fontWeight": "700", "color": "#0f172a"}),
                                        html.Div("Post–Price Increase", style={"fontSize": "12px", "color": "#64748b"}),
                                    ]
                                ),
                                html.Div("Sales Split", style={**kpi_label_style, "marginTop": "12px"}),
                            ],
                            style=kpi_style,
                        ),
                    ],
                ),

                # Sales Chart
                html.Div(
                    style={"backgroundColor": "white","borderRadius": "16px","padding": "28px","boxShadow": "0 1px 3px rgba(0,0,0,0.06)","border": "1px solid #f1f5f9","marginBottom": "32px",},
                    children=[
                        dcc.Graph(
                            id="sales-graph",
                            config={"displayModeBar": True, "displaylogo": False},
                        )
                    ],
                ),

                # Price & Quantity Charts row
                html.Div(
                    style={"display": "flex", "gap": "24px", "marginBottom": "32px", "flexWrap": "wrap"},
                    children=[
                        html.Div(
                            style={"flex": 1, "minWidth": "360px", "backgroundColor": "white", "borderRadius": "16px", "padding": "28px", "boxShadow": "0 1px 3px rgba(0,0,0,0.06)", "border": "1px solid #f1f5f9"},
                            children=[
                                dcc.Graph(id="quantity-graph", config={"displayModeBar": True, "displaylogo": False}),
                            ],
                        ),
                    ],
                ),

                # Insight
                html.Div(
                    style={"padding": "24px 28px","backgroundColor": "white","borderRadius": "16px","boxShadow": "0 1px 3px rgba(0,0,0,0.06)","border": "1px solid #f1f5f9","borderLeft": "4px solid #0ea5e9",},
                    children=[
                        html.H3(
                            "Key Insight",
                            style={"fontSize": "16px","fontWeight": "600","color": "#0f172a","marginBottom": "12px",},
                        ),
                        html.P(
                            "The change in sales volume before and after the price increase is clearly visible. "
                            "Filtering by region further highlights how different markets responded to the pricing decision.",
                            style={
                                "fontSize": "14px",
                                "color": "#475569",
                                "lineHeight": 1.7,
                                "margin": 0,
                            },
                        ),
                    ],
                ),
            ],
        )
    ],
)


def _chart_layout(yaxis_overrides=None):
    base_layout = dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#334155", size=12),
        margin=dict(l=60, r=24, t=40, b=48),
        hovermode="x unified",
        xaxis=dict(gridcolor="#f1f5f9", showline=True, linecolor="#e2e8f0"),
        yaxis=dict(gridcolor="#f1f5f9"),
    )
    if yaxis_overrides:
        base_layout["yaxis"].update(yaxis_overrides)
    return base_layout


@app.callback(
    Output("sales-graph", "figure"),
    Output("total-quantity", "children"),
    Output("before-qty", "children"),
    Output("after-qty", "children"),
    Output("total-sales", "children"),
    Output("before-sales", "children"),
    Output("after-sales", "children"),
    Output("quantity-graph", "figure"),
    Input("region-filter", "value"),
)
def update_dashboard(region):
    # #region agent log
    _agent_log(
        hypothesis_id="H1",
        location="sales_visulaizers.update_dashboard:entry",
        message="Callback entry",
        data={"region": region},
    )
    # #endregion

    if region == "all":
        filtered_df = df.copy()
        branch = "all"
    else:
        filtered_df = df[df["Region"].str.lower() == region]
        branch = "filtered"

    # #region agent log
    _agent_log(
        hypothesis_id="H1",
        location="sales_visulaizers.update_dashboard:after_filter",
        message="After region filter",
        data={"branch": branch, "filtered_rows": int(len(filtered_df))},
    )
    # #endregion

    daily_sales = (
        filtered_df.groupby("Date", as_index=False)
        .agg({"Sales": "sum", "Quantity": "sum"})
        .sort_values("Date")
    )

    # #region agent log
    _agent_log(
        hypothesis_id="H2",
        location="sales_visulaizers.update_dashboard:after_groupby",
        message="After groupby",
        data={
            "daily_rows": int(len(daily_sales)),
            "columns": list(daily_sales.columns),
        },
    )
    # #endregion

    before = daily_sales[daily_sales["Date"] < price_increase_date]["Sales"].sum()
    after = daily_sales[daily_sales["Date"] >= price_increase_date]["Sales"].sum()
    total_sales = daily_sales["Sales"].sum()
    total_quantity = int(daily_sales["Quantity"].sum())

    before_qty = int(filtered_df[filtered_df["Date"] < price_increase_date]["Quantity"].sum())
    after_qty = int(filtered_df[filtered_df["Date"] >= price_increase_date]["Quantity"].sum())

    # #region agent log
    _agent_log(
        hypothesis_id="H3",
        location="sales_visulaizers.update_dashboard:before_return",
        message="Computed aggregates",
        data={
            "total_sales": float(total_sales),
            "before_sales": float(before),
            "after_sales": float(after),
            "total_quantity": total_quantity,
            "before_qty": before_qty,
            "after_qty": after_qty,
        },
    )
    # #endregion

    # Sales chart
    fig_sales = go.Figure()
    fig_sales.add_trace(
        go.Scatter(
            x=daily_sales["Date"],
            y=daily_sales["Sales"],
            mode="lines",
            line=dict(width=2.5, color="#0ea5e9"),
            fill="tozeroy",
            fillcolor="rgba(14, 165, 233, 0.12)",
        )
    )
    fig_sales.add_vline(x=price_increase_str, line_width=2, line_dash="dash", line_color="#94a3b8")
    fig_sales.add_annotation(
        x=price_increase_str, y=1, yref="paper",
        text="Price Increase (15 Jan 2021)",
        showarrow=False, yanchor="bottom",
        font=dict(size=11, color="#64748b", family="Inter, sans-serif"),
        bgcolor="rgba(255,255,255,0.9)", borderpad=6, borderwidth=1, bordercolor="#e2e8f0",
    )
    fig_sales.update_layout(**_chart_layout(yaxis_overrides=dict(title="Total Sales ($)", tickformat=",.0f")))

    # Quantity chart
    fig_quantity = go.Figure()
    fig_quantity.add_trace(
        go.Scatter(
            x=daily_sales["Date"],
            y=daily_sales["Quantity"],
            mode="lines",
            line=dict(width=2.5, color="#10b981"),
            fill="tozeroy",
            fillcolor="rgba(16, 185, 129, 0.12)",
        )
    )
    fig_quantity.add_vline(x=price_increase_str, line_width=2, line_dash="dash", line_color="#94a3b8")
    fig_quantity.update_layout(**_chart_layout(yaxis_overrides=dict(title="Quantity", tickformat=",.0f")))

    return (
        fig_sales,
        f"{total_quantity:,}",
        f"{before_qty:,}",
        f"{after_qty:,}",
        f"${total_sales:,.0f}",
        f"${before:,.0f}",
        f"${after:,.0f}",
        fig_quantity,
    )

if __name__ == "__main__":
    app.run(debug=True)