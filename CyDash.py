import json
import dash
from dash import dcc, html, Input, Output, ctx
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Load configuration from file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Load and preprocess data
file_path = 'Cyber Events Database - Records thru June 2024.xlsx'
data = pd.read_excel(file_path, sheet_name="Sheet 1").dropna(subset=["event_date", "actor_type", "country", "industry"])

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'static/css/style.css'])

# Dynamically generate filter components
def generate_filters():
    filters = []
    for filter_config in config["filters"]:
        filters.append(html.Label(filter_config["label"]))
        filters.append(dcc.Dropdown(
            id=filter_config["id"],
            options=[{"label": str(value), "value": value} for value in sorted(data[filter_config["column"]].unique())],
            #optionHeight= 105,
            value=None,
            className="wide-dropdown",
            placeholder=filter_config["placeholder"]
        ))
    filters.append(html.Button("Reset Filters", id="reset-filters-button", n_clicks=0, style={"marginTop": "10px"}))
    return html.Div(filters, style={"padding": "10px"})

# Dynamically generate visualizations layout
def generate_visualizations():
    rows = []
    row = []
    current_width = 0

    for viz_config in config["visualizations"]:
        col_width = viz_config.get("width", 6)
        if current_width + col_width > 12:
            # Append the current row and reset
            rows.append(dbc.Row(row, className="mb-4"))
            row = []
            current_width = 0
        row.append(dbc.Col(dcc.Graph(id=viz_config["id"]), width=col_width))
        current_width += col_width

    if row:
        rows.append(dbc.Row(row, className="mb-4"))  # Append the last row
    return html.Div(rows)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("CyDash: The Cyber-Events Dashboard", style={"textAlign": "center"}),

    # Filters Panel
    generate_filters(),

    # Visualizations
    generate_visualizations()
])

# Fallback visualization for empty or invalid data
def create_fallback_figure(title):
    return px.bar(
        title=title,
        x=[],
        y=[],
        labels={"x": "No Data Available", "y": "No Data Available"}
    ).update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{
            "text": "No Data Available",
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "font": {"size": 20}
        }]
    )


# Helper function to truncate labels
def truncate_labels(labels, max_length=10):
    return [label[:max_length] + "..." if len(label) > max_length else label for label in labels]

# Callback for interactivity
@app.callback(
    [Output(filter_config["id"], "value") for filter_config in config["filters"]] +
    [Output(viz_config["id"], "figure") for viz_config in config["visualizations"]],
    [Input(filter_config["id"], "value") for filter_config in config["filters"]] +
    [Input(viz_config["id"], "clickData") for viz_config in config["visualizations"]] +
    [Input("reset-filters-button", "n_clicks")]
)
def update_dashboard(*inputs):
    reset_clicks = inputs[-1]
    filter_values = list(inputs[:len(config["filters"])])  # Convert tuple to list
    click_data = inputs[len(config["filters"]):-1]

    # Reset logic
    if ctx.triggered_id == "reset-filters-button":
        filter_values = [None] * len(config["filters"])

    # Handle click interactions for filters
    for idx, viz_config in enumerate(config["visualizations"]):
        if ctx.triggered_id == viz_config["id"] and click_data[idx]:
            if viz_config["type"] == "choropleth":
                clicked_location = click_data[idx]["points"][0]["location"]  # Extract the clicked country
                filter_index = next(
                    (i for i, f in enumerate(config["filters"]) if f["column"] == viz_config["location"]), None)
                if filter_index is not None:
                    filter_values[filter_index] = None if filter_values[
                                                              filter_index] == clicked_location else clicked_location
            elif viz_config["type"] == "heatmap":
                x_value = click_data[idx]["points"][0]["y"]
                y_value = click_data[idx]["points"][0]["x"]
                x_filter_index = next((i for i, f in enumerate(config["filters"]) if f["column"] == viz_config["x"]),
                                      None)
                y_filter_index = next((i for i, f in enumerate(config["filters"]) if f["column"] == viz_config["y"]),
                                      None)
                if x_filter_index is not None:
                    filter_values[x_filter_index] = None if filter_values[x_filter_index] == x_value else x_value
                if y_filter_index is not None:
                    filter_values[y_filter_index] = None if filter_values[y_filter_index] == y_value else y_value
            else:
                column = viz_config.get("names", viz_config.get("x", viz_config.get("column")))
                clicked_value = click_data[idx]["points"][0].get("label", click_data[idx]["points"][0].get("x"))
                filter_index = next((i for i, f in enumerate(config["filters"]) if f["column"] == column), None)
                if filter_index is not None:
                    filter_values[filter_index] = None if filter_values[
                                                              filter_index] == clicked_value else clicked_value

    # Filter data
    filtered_data = data.copy()
    for idx, filter_config in enumerate(config["filters"]):
        if filter_values[idx]:
            filtered_data = filtered_data[filtered_data[filter_config["column"]] == filter_values[idx]]

    # Generate figures
    figures = []
    for viz_config in config["visualizations"]:
        try:
            if viz_config["type"] == "line":
                chart_data = filtered_data.groupby(viz_config["x"]).size().reset_index(name="count")
                figures.append(px.line(chart_data, x=viz_config["x"], y=viz_config["y"], title=viz_config["title"]))
            elif viz_config["type"] == "stacked_bar":
                chart_data = filtered_data.groupby([viz_config["x"], viz_config["color"]]).size().reset_index(name="count")
                figures.append(px.bar(chart_data, x=viz_config["x"], y=viz_config["y"], color=viz_config["color"], title=viz_config["title"]))
            elif viz_config["type"] == "choropleth":
                chart_data = filtered_data.groupby(viz_config["location"]).size().reset_index(name="count")
                figures.append(px.choropleth(chart_data, locations=viz_config["location"], color="count", title=viz_config["title"]))
            elif viz_config["type"] == "choropleth2":
                chart_data = filtered_data.groupby(viz_config["location"]).size().reset_index(name="count")
                figures.append(px.choropleth(
                    chart_data,
                    locations=viz_config["location"],  # Column with country names
                    locationmode='country names',  # Ensure it maps to country names
                    color="count",  # Use 'count' to determine color intensity
                    color_continuous_scale="Reds",  # Use a color scale that intensifies with count
                    title=viz_config["title"]
                ).update_layout(
                    geo=dict(
                        showframe=False,
                        showcoastlines=True,
                        projection_type="equirectangular"
                    ),
                    coloraxis_colorbar=dict(
                        title="Event Count",
                        tickvals=[min(chart_data["count"]), max(chart_data["count"])],
                        ticktext=["Low", "High"]
                    )
                ))

            elif viz_config["type"] == "treemap":
                figures.append(px.treemap(filtered_data, path=viz_config["path"], values=viz_config["values"], title=viz_config["title"]))
            elif viz_config["type"] == "bar":
                chart_data = filtered_data.groupby(viz_config["x"]).size().reset_index(name="count")
                figures.append(px.bar(chart_data, x=viz_config["x"], y=viz_config["y"], title=viz_config["title"]))
            elif viz_config["type"] == "pie":
                chart_data = filtered_data[viz_config["names"]].value_counts().reset_index(name="count")
                chart_data.rename(columns={"index": viz_config["names"]}, inplace=True)
                figures.append(px.pie(chart_data, names=viz_config["names"], values="count", title=viz_config["title"]))
            elif viz_config["type"] == "horizontal_bar":
                chart_data = filtered_data[viz_config["column"]].value_counts().head(10).reset_index(name="count")
                chart_data.rename(columns={"index": viz_config["column"]}, inplace=True)
                figures.append(px.bar(chart_data, x="count", y=viz_config["column"], orientation=viz_config["orientation"], title=viz_config["title"]))
            elif viz_config["type"] == "heatmap":
                matrix = filtered_data.pivot_table(index=viz_config["x"], columns=viz_config["y"], aggfunc='size', fill_value=0)
                if not matrix.empty:
                    # Apply label truncation
                    truncated_x_labels = truncate_labels(matrix.columns.tolist())
                    figures.append(px.imshow(
                        matrix,
                        title=viz_config["title"]
                    ).update_layout(
                        xaxis=dict(
                            tickvals=matrix.columns.tolist(),
                            ticktext=truncated_x_labels
                        )
                    ))
                else:
                    figures.append(create_fallback_figure(viz_config["title"]))
        except Exception as e:
            print(f"Error generating {viz_config['id']}: {e}")
            figures.append(create_fallback_figure(viz_config["title"]))

    return filter_values + figures


# Layout of the dashboard
app.layout = html.Div([
    dbc.Row([
        # Sidebar (Filter Pane)
        dbc.Col(
            html.Div([
                html.Button(
                    "☰", id="toggle-sidebar-button", n_clicks=0,
                    style={"marginBottom": "10px", "width": "100%", "padding": "10px"}
                ),
                dbc.Collapse(
                    id="sidebar",
                    is_open=True,
                    children=generate_filters(),
                    style={
                        "backgroundColor": "#f8f9fa",
                        "padding": "10px",
                        "height": "100vh",
                        "overflowY": "auto",
                        "position": "fixed",
                        "top": 0,
                        "left": 0,
                        "zIndex": 1000,
                        "width": "20%"
                    }
                )
            ]),
            width=2, style={"padding": "0px"}
        ),
        # Main Content (Visualizations)
        dbc.Col(
            html.Div([
                html.H1("CyDash: The Cyber-Events Dashboard", style={"textAlign": "center"}),
                generate_visualizations()
            ]),
            width={"size": 10, "offset": 2}, style={"padding": "20px"}
        )
    ])
])

# Layout of the dashboard
app.layout = html.Div([
    dbc.Row([
        # Sidebar (Filter Pane)
        dbc.Col(
            html.Div([
                dbc.Collapse(
                    id="sidebar",
                    is_open=True,
                    children=generate_filters(),
                    style={
                        "backgroundColor": "#f8f9fa",
                        "padding": "10px",
                        "height": "100vh",
                        "overflowY": "auto",
                        "position": "fixed",
                        "top": 0,
                        "left": 0,
                        "zIndex": 1000,
                        "width": "16%"
                    }
                )
            ]),
            width=2, style={"padding": "0px"}
        ),
        # Main Content (Visualizations)
        dbc.Col(
            html.Div([
                html.H1("CyDash: The Cyber-Events Dashboard", style={"textAlign": "center"}),
                generate_visualizations()
            ]),
            width={"size": 10, "offset": 2}, style={"padding": "20px"}
        )
    ])
])

'''
# Callback for toggling the sidebar
@app.callback(
    Output("sidebar", "is_open"),
    [Input("toggle-sidebar-button", "n_clicks")],
    [Input("sidebar", "is_open")]
)
def toggle_sidebar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
'''

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
