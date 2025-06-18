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
dates:          list            = [''.join(list(date)[:10]) for date in df['Issue Date']]
months:         list            = [datetime.strptime(day, "%Y-%m-%d").strftime("%B") for day in dates]
days_of_week:   list            = [datetime.strptime(day, "%Y-%m-%d").strftime("%A") for day in dates]
df['Day of the Week']           = days_of_week
df['Month']                     = months

day_orders:     dict            = {'Day of the Week': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
month_orders:   dict            = {"Month": ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]}
options:        list            = list (df.columns)


state_cols:     list            = []

for state in sorted(set(list(df['State']))):

    current_df: pd.DataFrame    = df[df['State'] == state]

    violations_amount           = len(current_df)
    total_fine_amount           = current_df['Fine Amount'].sum()
    mean_fine_amount            = current_df['Fine Amount'].mean()
    total_penalty_amount        = current_df['Penalty Amount'].sum()
    mean_penalty_amount         = current_df['Penalty Amount'].mean()
    total_interest_amount       = current_df['Interest Amount'].sum()
    mean_interest_amount        = current_df['Interest Amount'].mean()
    total_reduction_amount      = current_df['Reduction Amount'].sum()
    mean_reduction_amount       = current_df['Reduction Amount'].mean()
    total_payment_amount        = current_df['Payment Amount'].sum()
    mean_payment_amount         = current_df['Payment Amount'].mean()

    state_cols.append({ 'State': state, 
                        'Violations Amount':        violations_amount,
                        'Total Fine Amount':        total_fine_amount, 
                        'Mean Fine Amount':         mean_fine_amount,
                        'Total Penalty Amount':     total_penalty_amount, 
                        'Mean Penalty Amount':      mean_penalty_amount,
                        'Total Interest Amount':    total_interest_amount, 
                        'Mean Interest Amount':     mean_interest_amount,
                        'Total Reduction Amount':   total_reduction_amount, 
                        'Mean Reduction Amount':    mean_reduction_amount,
                        'Total Payment Amount':     total_payment_amount, 
                        'Mean Payment Amount':      mean_payment_amount})
    
state_df:       pd.DataFrame    = pd.DataFrame(state_cols)

colors_lst:     list            = ['red', 'blue', 'green', 'black', 'gray', "#00FF98", "#00E1FF", "#C8FF00", "#0021FF", "#E600FF", "#FF002E", "#FFF300", "#37FF00", "#00FFFA"]

grid            = plots.create_grid(df)

choropleth_1    = plots.create_choropleth(state_df, "Mean Fine Amount", px.colors.sequential.Cividis, "State Mean Fine Amount")
bar_1           = plots.create_bar(state_df, "Mean Fine Amount", px.colors.sequential.Cividis, "State Mean Fine Amount")

choropleth_2    = plots.create_choropleth(state_df, "Mean Penalty Amount", px.colors.sequential.Viridis, "State Mean Penalty Amount")
bar_2           = plots.create_bar(state_df, "Mean Penalty Amount", px.colors.sequential.Viridis, "State Mean Penalty Amount")

choropleth_3    = plots.create_choropleth(state_df, "Mean Interest Amount", px.colors.sequential.Inferno, "State Mean Interest Amount")
bar_3           = plots.create_bar(state_df, "Mean Interest Amount", px.colors.sequential.Inferno, "State Mean Interest Amount")

choropleth_4    = plots.create_choropleth(state_df, "Mean Reduction Amount", px.colors.sequential.Plasma, "State Mean Reduction Amount")
bar_4           = plots.create_bar(state_df, "Mean Reduction Amount", px.colors.sequential.Plasma, "State Mean Reduction Amount")

choropleth_5    = plots.create_choropleth(state_df, "Mean Payment Amount", px.colors.sequential.Turbo, "State Mean Payment Amount")
bar_5           = plots.create_bar(state_df, "Mean Payment Amount", px.colors.sequential.Turbo, "State Mean Payment Amount")


app = Dash ("Figure Friday 2025 week 24", external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                            className   = "col-6 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "choropleth_1", 
                                                  figure = px.histogram(  df,
                                                                    x='Day of the Week',
                                                                    y='Fine Amount',
                                                                    color='Violation',
                                                                    title="Fine Amount per Day and Violation",
                                                                    category_orders=day_orders,
                                                                    color_discrete_sequence=colors_lst).update_layout(plot_bgcolor="white", bargap=0.05, yaxis_title='Fine Amount')),
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
                                        dcc.Graph(id = "choropleth_1", 
                                                  figure = px.histogram(  df,
                                                                    x='Month',
                                                                    y='Fine Amount',
                                                                    color='Violation',
                                                                    histfunc='avg',
                                                                    title="Fine Amount per Month and Violation",
                                                                    category_orders=month_orders,
                                                                    color_discrete_sequence=colors_lst).update_layout(plot_bgcolor="white", bargap=0.05, yaxis_title='Fine Amount')),
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
                                        dcc.Graph(id = "choropleth_1", 
                                                  figure = px.histogram(  df,
                                                                    x='Day of the Week',
                                                                    y='Fine Amount',
                                                                    color='License Type',
                                                                    title="Fine Amount per Day and Licence Type",
                                                                    category_orders=day_orders,
                                                                    color_discrete_sequence=colors_lst).update_layout(plot_bgcolor="white", bargap=0.05, yaxis_title='Fine Amount')),
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
                                        dcc.Graph(id = "choropleth_1", 
                                                  figure = px.histogram(  df,
                                                                    x='Day of the Week',
                                                                    y='Fine Amount',
                                                                    color='Issuing Agency',
                                                                    title="Fine Amount per Day and Issuing Agency",
                                                                    category_orders=day_orders,
                                                                    color_discrete_sequence=colors_lst).update_layout(plot_bgcolor="white", bargap=0.05, yaxis_title='Fine Amount')),
                                    ]
                                )
                            ]
                        ),

                        

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
                            className   = "col-5 m-0 p-0",
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
                            className   = "col-7 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "bar_2", figure = bar_2),
                                    ]
                                )
                            ]
                        ),

                        html.Div(
                            className   = "col-5 m-0 p-0",
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
                            className   = "col-7 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "bar_3", figure = bar_3),
                                    ]
                                )
                            ]
                        ),

                        html.Div(
                            className   = "col-5 m-0 p-0",
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
                            className   = "col-7 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "bar_4", figure = bar_4),
                                    ]
                                )
                            ]
                        ),

                        html.Div(
                            className   = "col-5 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "choropleth_5", figure = choropleth_5),
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
                                        dcc.Graph(id = "bar_5", figure = bar_5),
                                    ]
                                )
                            ]
                        ),
                        
                    ]
                ),
            ])

    ])


if __name__ == "__main__":
    app.run(debug=False)