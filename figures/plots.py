import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
from plotly.graph_objects import Figure, Bar

def create_grid(
        df:             pd.DataFrame)->dag.AgGrid:
    '''
    Create an AgGrid component
    '''

    grid = dag.AgGrid(
                id              = {"type": "grid", "index": "main_grid"},
                rowData         = df.to_dict("records"),
                columnDefs      = [{"field": i, 'filter': True, 'sortable': True} for i in df.columns],
                dashGridOptions = {"pagination": True},
                columnSize      = "sizeToFit")

    return grid


def create_choropleth(
        df:             pd.DataFrame,
        color_column:   str,
        color_scale:    str,
        title:          str)->Figure:
    '''
    Create a Choropleth plot
    '''

    choropleth_fig      = px.choropleth(
                        data_frame      = df,
                        locations       = "State",
                        locationmode    = "USA-states",
                        scope           = "usa",
                        color           = color_column,
                        hover_name      = "State",
                        color_continuous_scale  = color_scale,
                        hover_data      = {"State": True, color_column: True},
                        title=title)

    # Remove state borders
    choropleth_fig.update_geos(
                    showlakes       = False,
                    showland        = True,
                    showcountries   = True,
                    showframe       = False,
                    visible         = False)
    
    choropleth_fig.update_traces(marker_line_width=0)

    return choropleth_fig


def create_bar(
        df:             pd.DataFrame,
        color_column:   str,
        color_scale:    str,
        title:          str)->Figure:
    '''
    Create a Choropleth plot
    '''

    sorted_df = df.sort_values(by=color_column)
    fig = px.bar(sorted_df, 
                       x='State', 
                       y=color_column, 
                       color=color_column, 
                       color_continuous_scale=color_scale,
                       title=title)
    
    fig.update_layout(xaxis=dict(tickangle=-45, tickfont=dict(size=9)), plot_bgcolor="white")
    fig.update_coloraxes(showscale=False)

    return fig