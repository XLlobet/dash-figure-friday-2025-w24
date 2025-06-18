from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd
import copy
from figures import plots
import numpy as np
from datetime import datetime


df:             pd.DataFrame    = pd.read_csv("./Open_Parking_and_Camera_Violations.csv")
dates:    list            = [list(date)[:10] for date in df['Issue Date']]
print(dates)
options:        list            = list (df.columns)

colors:         list            = ["#00FF98", "#00E1FF", "#4600CF", "#C8FF00", "#0021FF", "#E600FF", "#FF002E", "#FFF300", "#37FF00", "#00FFFA"]

# Expand division counts to states
expanded_rows       = []

for state in sorted(set(list(df['State']))):
    current_df: pd.DataFrame = df[df['State'] == state]
    violations_amount = len(current_df)
    total_fine_amount = current_df['Fine Amount'].sum()
    mean_fine_amount = current_df['Fine Amount'].mean()
    total_penalty_amount = current_df['Penalty Amount'].sum()
    mean_penalty_amount = current_df['Penalty Amount'].mean()
    total_interest_amount = current_df['Interest Amount'].sum()
    mean_interest_amount = current_df['Interest Amount'].mean()
    total_reduction_amount = current_df['Reduction Amount'].sum()
    mean_reduction_amount = current_df['Reduction Amount'].mean()
    total_payment_amount = current_df['Payment Amount'].sum()
    mean_payment_amount = current_df['Payment Amount'].mean()
    expanded_rows.append({'State': state, 
                          'Violations Amount': violations_amount,
                          'Total Fine Amount': total_fine_amount, 
                          'Mean Fine Amount': mean_fine_amount,
                          'Total Penalty Amount': total_penalty_amount, 
                          'Mean Penalty Amount': mean_penalty_amount,
                          'Total Interest Amount': total_interest_amount, 
                          'Mean Interest Amount': mean_interest_amount,
                          'Total Reduction Amount': total_reduction_amount, 
                          'Mean Reduction Amount': mean_reduction_amount,
                          'Total Payment Amount': total_payment_amount, 
                          'Mean Payment Amount': mean_payment_amount})
    
state_df            = pd.DataFrame(expanded_rows)

N = len(state_df)
c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]
colors = [c[i] for i in range(int(N))]



grid            = plots.create_grid(df)
choropleth_1    = plots.create_choropleth(state_df, "Mean Fine Amount", px.colors.sequential.Cividis, "State Mean Fine Amount")
bar_1           = plots.create_bar(state_df, "Mean Fine Amount", px.colors.sequential.Cividis, "State Mean Fine Amount")
choropleth_2    = plots.create_choropleth(state_df, "Mean Penalty Amount", px.colors.sequential.Viridis, "State Mean Penalty Amount")
choropleth_3    = plots.create_choropleth(state_df, "Mean Interest Amount", px.colors.sequential.Inferno, "State Mean Interest Amount")
choropleth_4    = plots.create_choropleth(state_df, "Mean Reduction Amount", px.colors.sequential.Plasma, "State Mean Reduction Amount")
choropleth_5    = plots.create_choropleth(state_df, "Mean Payment Amount", px.colors.sequential.Turbo, "State Mean Payment Amount")

app = Dash ("Figure Friday week 23", external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div(
    id       = "main_container",
    style    = {"minHeight": "100vh"},
    children = [

        html.H1("Open Parking and Camera Violation", className="p-4 bg-light text-primary mb-0"),

        html.Div(
            id          = "main_div",
            className   = "m-0 p-2 w-100",
            children    = [
                html.Div(
                    className   = "row m-0 p-0",
                    children    = [
                        html.Div(
                            className   = "col-5 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "choropleth_1", figure = choropleth_1),
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className   = "col-7 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "bar_1", figure = bar_1),
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className   = "col-6 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "choropleth_2", figure = choropleth_2),
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className   = "col-6 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "choropleth_3", figure = choropleth_3),
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className   = "col-6 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "choropleth_4", figure = choropleth_4),
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className   = "col-6 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "choropleth_5", figure = choropleth_5),
                                    ]
                                )
                            ]
                        ),
                        
                    ]
                ),
                html.Div(
                    className   = "col-12 m-0 p-0",
                    children    = [
                        dcc.Dropdown(
                            className   = "text-dark",
                            id          = "variable_1",
                            options     = options[0:8],
                            value       = options[0],
                        ),
                        dcc.Dropdown(
                            className   = "text-dark",
                            id          = "variable_2",
                            options     = options[7:],
                            value       = options[8],
                        ),
                        dcc.Loading(
                            type        = 'cube',
                            children    = [
                                dcc.Graph(id = "figure_1")
                            ]
                        )
                    ]
                )
            ])

    ])

@app.callback(
    Output("figure_1",      'figure'),
    Output("choropleth_1",  "figure"),
    Output("choropleth_2",  "figure"),
    Input('variable_1',     'value'),
    Input('variable_2',     'value'),
    Input("bg_color",       "value"),
    Input("text_color",     "value"),
    Input("font_type",      "value"),
)
def two_variable_corssfiltering(variable_1, 
                                variable_2, 
                                bg_color, 
                                text_color, 
                                font_type):

    filtered_df:    pd.DataFrame    = df[[variable_1, variable_2]].dropna(how="any")

    options_lst:    list            = [variable_1, variable_2]
    cat_orders:     dict            = {cat:sorted(set(list(filtered_df[cat]))) for cat in options_lst}

    figure:         Figure          = px.histogram(
                                            data_frame                = filtered_df, 
                                            x                         = variable_2, 
                                            facet_row                 = variable_1, 
                                            color                     = variable_2, 
                                            color_discrete_sequence   = colors,
                                            category_orders           = cat_orders,
                                            title                     = variable_1)
    
    figure.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]) if "=" in a.text else a.update(text=a.text))

    figure.update_layout(
        paper_bgcolor   = bg_color,
        plot_bgcolor    = bg_color,
        font_family     = font_type,
        font_color      = text_color,
        height          = 500,
        bargap          = 0.01
    )

    figure.update_xaxes(showline            = True,
                        showgrid            = False,
                        linewidth           = 0.5,
                        linecolor           = "#E7E7E7",
                        mirror              = True,
                        zeroline            = False)
    figure.update_yaxes(showline            = False,
                        showgrid            = False,
                        linewidth           = 0.5,
                        linecolor           = "#E7E7E7",
                        mirror              = False,
                        zeroline            = False)
    
    choro_1 = copy.deepcopy(choropleth_2)
    choro_2 = copy.deepcopy(choropleth_1)

    choro_1.update_layout(  paper_bgcolor   = bg_color,
                            font_family     = font_type,
                            font_color      = text_color)
    choro_1.update_geos(    bgcolor         = bg_color)

    choro_2.update_layout(  paper_bgcolor   = bg_color,
                            font_family     = font_type,
                            font_color      = text_color)
    choro_2.update_geos(    bgcolor         = bg_color)

    return figure, choro_1, choro_2

if __name__ == "__main__":
    app.run(debug=True)