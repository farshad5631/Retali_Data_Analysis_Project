import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# 1. Load and prepare the structured dataset
# Render will look for this file in the same directory
df = pd.read_csv("retail_sales_dataset.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year.astype(str)
df["Month_Year"] = df["Date"].dt.to_period("M").astype(str)

# Mock baseline column for profit requirement
df["Estimated_Profit"] = df["Total Amount"] * 0.40  # Assuming a 40% profit margin

# 2. Initialize the Dash App
app = dash.Dash(__name__)
server = app.server  # <--- CRITICAL: Render needs this line to find the Flask server!

# 3. Application Layout Structure (Pure HTML/DCC Style)
app.layout = html.Div(
    children=[
        # Dashboard Header Title
        html.H1(
            "Retail Performance Executive Dashboard",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "fontSize": "36px",
                "fontFamily": "Arial",
                "marginTop": "20px",
            },
        ),
        # Main Control Panel Row (Year Filter + Category Filter + Export Button)
        html.Div(
            [
                # Year Filter Dropdown
                html.Div(
                    [
                        html.Label(
                            "Select Year: ",
                            style={
                                "fontSize": "18px",
                                "fontWeight": "bold",
                                "marginRight": "10px",
                            },
                        ),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[
                                {"label": i, "value": i}
                                for i in sorted(df["Year"].unique())
                            ]
                            + [{"label": "All Years", "value": "All"}],
                            value="All",
                            clearable=False,
                            style={
                                "width": "180px",
                                "display": "inline-block",
                                "verticalAlign": "middle",
                            },
                        ),
                    ],
                    style={"display": "inline-block", "marginRight": "30px"},
                ),
                # Category Filter Dropdown
                html.Div(
                    [
                        html.Label(
                            "Select Category: ",
                            style={
                                "fontSize": "18px",
                                "fontWeight": "bold",
                                "marginRight": "10px",
                            },
                        ),
                        dcc.Dropdown(
                            id="category-dropdown",
                            options=[
                                {"label": i, "value": i}
                                for i in sorted(df["Product Category"].unique())
                            ]
                            + [{"label": "All Categories", "value": "All"}],
                            value="All",
                            clearable=False,
                            style={
                                "width": "180px",
                                "display": "inline-block",
                                "verticalAlign": "middle",
                            },
                        ),
                    ],
                    style={"display": "inline-block", "marginRight": "40px"},
                ),
                # Export Button Group
                html.Div(
                    [
                        html.Button(
                            "📥 Export Filtered Data to CSV",
                            id="btn-export",
                            style={
                                "height": "40px",
                                "fontSize": "16px",
                                "backgroundColor": "#27ae60",
                                "color": "white",
                                "border": "none",
                                "borderRadius": "4px",
                                "cursor": "pointer",
                                "padding": "0 20px",
                            },
                        ),
                        dcc.Download(id="download-dataframe-csv"),
                    ],
                    style={
                        "display": "inline-block",
                        "verticalAlign": "middle",
                    },
                ),
            ],
            style={
                "textAlign": "center",
                "backgroundColor": "#f8f9fa",
                "padding": "20px",
                "borderRadius": "8px",
                "margin": "20px auto",
                "width": "90%",
            },
        ),
        # KPI Highlights Bar
        html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            "Total Revenue",
                            style={
                                "margin": "5px 0",
                                "color": "#7f8c8d",
                                "fontSize": "18px",
                            },
                        ),
                        html.H1(
                            id="kpi-revenue",
                            style={
                                "margin": "5px 0",
                                "color": "#27ae60",
                                "fontSize": "28px",
                            },
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "border": "1px solid #bdc3c7",
                        "borderRadius": "8px",
                        "padding": "15px",
                        "margin": "0 1.5%",
                        "backgroundColor": "#fff",
                        "boxShadow": "2px 2px 5px #e0e0e0",
                    },
                ),
                html.Div(
                    [
                        html.H3(
                            "Estimated Profit (40%)",
                            style={
                                "margin": "5px 0",
                                "color": "#7f8c8d",
                                "fontSize": "18px",
                            },
                        ),
                        html.H1(
                            id="kpi-profit",
                            style={
                                "margin": "5px 0",
                                "color": "#2980b9",
                                "fontSize": "28px",
                            },
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "border": "1px solid #bdc3c7",
                        "borderRadius": "8px",
                        "padding": "15px",
                        "margin": "0 1.5%",
                        "backgroundColor": "#fff",
                        "boxShadow": "2px 2px 5px #e0e0e0",
                    },
                ),
                html.Div(
                    [
                        html.H3(
                            "Avg Transaction Value",
                            style={
                                "margin": "5px 0",
                                "color": "#7f8c8d",
                                "fontSize": "18px",
                            },
                        ),
                        html.H1(
                            id="kpi-avg-value",
                            style={
                                "margin": "5px 0",
                                "color": "#f39c12",
                                "fontSize": "28px",
                            },
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "border": "1px solid #bdc3c7",
                        "borderRadius": "8px",
                        "padding": "15px",
                        "margin": "0 1.5%",
                        "backgroundColor": "#fff",
                        "boxShadow": "2px 2px 5px #e0e0e0",
                    },
                ),
            ],
            style={"textAlign": "center", "margin": "20px auto", "width": "94%"},
        ),
        html.Br(),
        # Top Visualization Row (Line Chart + Pie Chart)
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="trend-line-chart"),
                    style={"width": "60%", "display": "inline-block", "padding": "10px"},
                ),
                html.Div(
                    dcc.Graph(id="share-pie-chart"),
                    style={"width": "38%", "display": "inline-block", "padding": "10px"},
                ),
            ],
            style={"width": "95%", "margin": "auto", "display": "flex"},
        ),
        # Bottom Visualization Row (Bar Chart + Box Plot)
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="sales-bar-chart"),
                    style={"width": "49%", "display": "inline-block", "padding": "10px"},
                ),
                html.Div(
                    dcc.Graph(id="spread-box-plot"),
                    style={"width": "49%", "display": "inline-block", "padding": "10px"},
                ),
            ],
            style={"width": "95%", "margin": "auto", "display": "flex"},
        ),
    ],
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f4f6f7",
        "padding": "20px",
    },
)


# 4. Main App Callback to update all visuals & KPIs based on Year and Category inputs
@app.callback(
    [
        Output(component_id="kpi-revenue", component_property="children"),
        Output(component_id="kpi-profit", component_property="children"),
        Output(component_id="kpi-avg-value", component_property="children"),
        Output(component_id="trend-line-chart", component_property="figure"),
        Output(component_id="share-pie-chart", component_property="figure"),
        Output(component_id="sales-bar-chart", component_property="figure"),
        Output(component_id="spread-box-plot", component_property="figure"),
    ],
    [
        Input(component_id="year-dropdown", component_property="value"),
        Input(component_id="category-dropdown", component_property="value"),
    ],
)
def update_dashboard(selected_year, selected_cat):
    # Filter dataset dynamically based on selections
    filtered_df = df.copy()

    if selected_year != "All":
        filtered_df = filtered_df[filtered_df["Year"] == selected_year]
    if selected_cat != "All":
        filtered_df = filtered_df[
            filtered_df["Product Category"] == selected_cat
        ]

    # Recalculate KPIs
    total_revenue = filtered_df["Total Amount"].sum()
    total_profit = filtered_df["Estimated_Profit"].sum()
    avg_value = (
        filtered_df["Total Amount"].mean() if len(filtered_df) > 0 else 0
    )

    kpi_rev_str = f"${total_revenue:,.2f}"
    kpi_prof_str = f"${total_profit:,.2f}"
    kpi_avg_str = f"${avg_value:,.2f}"

    # Aggregations for charts
    monthly_data = (
        filtered_df.groupby("Month_Year")["Total Amount"]
        .sum()
        .reset_index()
        .sort_values("Month_Year")
    )
    cat_share = (
        filtered_df.groupby("Product Category")["Total Amount"]
        .sum()
        .reset_index()
    )

    # Generate Figures
    fig_line = px.line(
        monthly_data,
        x="Month_Year",
        y="Total Amount",
        markers=True,
        title="Monthly Sales Volumes",
        labels={"Month_Year": "Timeline", "Total Amount": "Sales ($)"},
    )

    fig_pie = px.pie(
        cat_share,
        values="Total Amount",
        names="Product Category",
        hole=0.4,
        title="Revenue Share Breakdown",
    )

    fig_bar = px.bar(
        cat_share.sort_values(by="Total Amount", ascending=False),
        x="Product Category",
        y="Total Amount",
        color="Product Category",
        title="Performance: Category vs Revenue",
        labels={"Total Amount": "Revenue ($)"},
    )
    fig_bar.update_layout(showlegend=False)

    fig_box = px.box(
        filtered_df,
        x="Product Category",
        y="Total Amount",
        color="Product Category",
        title="Transaction Value Spread & Quartiles",
        labels={"Total Amount": "Transaction Value ($)"},
    )
    fig_box.update_layout(showlegend=False)

    return (
        kpi_rev_str,
        kpi_prof_str,
        kpi_avg_str,
        fig_line,
        fig_pie,
        fig_bar,
        fig_box,
    )


# 5. Export Feature Callback (Uses State so dropdown changes NEVER cause automatic downloads)
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-export", "n_clicks"),
    [State("year-dropdown", "value"), State("category-dropdown", "value")],
    prevent_initial_call=True,
)
def export_csv(n_clicks, selected_year, selected_cat):
    filtered_df = df.copy()

    if selected_year != "All":
        filtered_df = filtered_df[filtered_df["Year"] == selected_year]
    if selected_cat != "All":
        filtered_df = filtered_df[
            filtered_df["Product Category"] == selected_cat
        ]

    return dcc.send_data_frame(
        filtered_df.to_csv, "filtered_retail_sales.csv", index=False
    )


# Run application server (using production settings)
if __name__ == "__main__":
    app.run(debug=False)