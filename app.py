import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# read in some data
data = pd.read_csv("metals.csv", 
                   usecols=[
                       "DateTime", 
                       "Platinum",
                       "Gold", 
                       "Silver",
                       "Palladium",
                       "Rhodium",
                       "Iridium",
                       "Ruthenium",
                       ])

# create a figure
fig = px.line(data, 
              x="DateTime", 
              y=["Gold", "Silver", "Palladium", "Rhodium", "Iridium", "Ruthenium"],
              title="Gold Prices 2018 to 2021", 
              color_discrete_map={"Gold": "gold", "Silver": "silver",
                                  "Palladium": "lightblue", "Rhodium": "darkblue",
                                  "Iridium": "purple", "Ruthenium": "orange"
                                }
)

app = dash.Dash(__name__, suppress_callback_exceptions=True)  # Added suppress_callback_exceptions=True
app.title = "Metal Prices 2018 to 2021"

app.layout = html.Div(
    id="root",
    style={"backgroundColor": "black", "color": "white", "fontFamily": "Verdana, sans-serif"},
    children=[
        dcc.Location(id='url', refresh=False),
        html.Div(
            id="header",
            style={"backgroundColor": "black"},
            children=[
                html.H1(
                    id="header-title",
                    style={"color": "white", "fontFamily": "Verdana, sans-serif"},
                    children="Precious Metals Prices"
                ),
                html.P(
                    id="header-description",
                    style={"color": "white", "fontFamily": "Verdana, sans-serif"},
                    children=("Metal prices", html.Br(), "from 2018 to 2021")
                ),
                html.Div(
                    id="navbar",
                    children=[
                        dcc.Link('Home', href='/', style={"margin-right": "20px"}),
                        dcc.Link('About', href='/about')
                    ],
                    style={"padding": "10px", "backgroundColor": "#333"}
                ),
            ]
        ),
        html.Div(id='page-content', children=[])
    ]
)

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/about':
        return html.Div([
            html.H2("About This App"),
            html.P("This app visualizes the prices of precious metals from 2018 to 2021."),
            html.P("You can select different metals and date ranges to see how prices have fluctuated over time.")
        ])
    else:
        return html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="menu-area",
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    className="menu-title",
                                    children="Select Metal"
                                ),
                                dcc.Dropdown(
                                    id="metal-filter",
                                    className="dropdown",
                                    options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
                                    clearable=False,
                                    value="Gold",
                                )
                            ],
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    className="menu-title",
                                    children="Date Range"
                                ),
                                dcc.DatePickerRange(
                                    id="date-range",
                                    min_date_allowed=data["DateTime"].min(),
                                    max_date_allowed=data["DateTime"].max(),
                                    start_date=data["DateTime"].min(),
                                    end_date=data["DateTime"].max(),
                                    display_format="MMM YY"
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    id="graph-container",
                    children=dcc.Graph(
                        id="price-chart",
                        figure=fig,
                        config={"displayModeBar": False}
                    )
                )
            ]
        )

@app.callback(
    Output("price-chart", "figure"),
    Input("metal-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)
def update_chart(metal, start_date, end_date):
    filtered_data = data.loc[(data["DateTime"] >= start_date) & (data["DateTime"] <= end_date)]
    fig = px.line(
        filtered_data, 
        x="DateTime", 
        y=[metal],
        title=f"{metal} Prices 2018 to 2021", 
        color_discrete_map={
            "Platinum": "#E5E4E2",
            "Gold": "gold",
            "Silver": "silver",
            "Palladium": "#ced0dd",
            "Rhodium": "#e2e7e1",
            "Iridium": "#3d3c3a",
            "Ruthenium": "#c9cbc8"}
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Price (USD) / oz",
        font=dict(
            family="Verdana",
            size=18,
            color="white"
        )
    )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)


