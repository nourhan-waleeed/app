import pandas as pd
from dash import Dash, html, dcc, Output, Input
import plotly.express as px

booking = pd.read_csv('bookingtest.csv')

repeated_guests = booking[booking['repeated'] == 1]

app = Dash(__name__)
app=app.server

app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px', 'background-color': '#F0F3F5'}, children=[
    html.H1(children='Hotel Booking & Reservation Report', style={'color': '#333', 'font-weight': 'bold'}),
    html.Hr(style={'border-top': '2px solid #999'}),
    dcc.RadioItems(
        options=[
            {'label': 'Total Nights vs. Average Price On Booking Status', 'value': 'total_nights'},
            {'label': 'Total Nights vs. Lead Time On Booking Status', 'value': 'lead time'},
            {'label': 'Average Price vs. Lead Time On Booking Status', 'value': 'avg_price_per_night'},
            {'label': 'Booking count in each Year', 'value': 'year'},
            {'label': 'Repeated Guests by Hotel Segment', 'value': 'repeated'},
            {'label': 'The children effect on parents decision with selecting the meal type and room type', 'value': 'number of children'},
            {'label': 'The relation between having children and to be repeated customer', 'value': 'rep&no_of_children'}


        ],
        value='rep&no_of_children', 
        id='controls-and-radio-item',
        labelStyle={'display': 'block', 'margin-bottom': '10px', 'font-weight': 'bold', 'color': '#353'}
    ),
    
    html.Div([
        
        dcc.Graph(figure={}, id='controls-and-graph'),
        
        dcc.Graph(figure = px.histogram(
            booking,
            x='market segment type',
            color='booking status',
            barmode='stack',
            color_discrete_sequence=px.colors.sequential.Viridis
        ).update_layout(title='What is the most used booking segment'))
    ], style={'display': 'flex', 'flex-direction': 'row'}),
        
    
    html.Div([ 
        
        dcc.Graph(figure = px.histogram(
            booking,
            x='number of weekend nights',
            color='booking status',
            color_discrete_sequence=px.colors.sequential.Viridis,
            facet_col='booking status'
            ).update_layout(title='Number of Weekends by Booking Status'), id='weekendplot'),
        
       dcc.Graph(figure = px.histogram(
            booking,
            x='number of week nights',
            color='booking status',
            color_discrete_sequence=px.colors.sequential.Viridis,
            facet_col='booking status'
            ).update_layout(title='Number of Week days by Booking Status'), id='weekplot'),
    ], style={'display': 'flex', 'flex-direction': 'row'}),
  
])
            
    
@app.callback(
    Output(component_id = 'controls-and-graph', component_property='figure'),
    Input(component_id = 'controls-and-radio-item', component_property='value')
    )

def update_graph(chosen_col):
    if chosen_col=='avg_price_per_night':
        figure = px.histogram(
            booking,
            x='lead time',
            y='avg_price_per_night',
            color='booking status',
            barmode='stack',
            title='Lead Time Vs.The average price per night',
            labels={'avg_price_per_night': 'Average Price Per Night', 'booking status': 'Booking Status'},
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        
    elif chosen_col=='lead time':
        figure = px.histogram(
            booking,
            x='total_nights',
            y='lead time',
            color='booking status',
            title='Distribution of Lead Time & total number of nights by Booking Status',
            barmode='stack',
            color_discrete_sequence=px.colors.sequential.Viridis

        )
    elif chosen_col == 'repeated':
        figure = px.bar(
            repeated_guests,
            x='market segment type',
            title='Number of Repeated Guests by Hotel Segment',
            labels={'market_segment': 'Hotel Segment', 'count': 'Count of Repeated Guests'}
           ,color_discrete_sequence=px.colors.sequential.Viridis
        )
        
    elif chosen_col == 'year':
        figure = px.histogram(
            booking,
            x='reservation year',
            color='booking status',
            barmode='stack',
            title = 'Booking Count of each Year',
            color_discrete_sequence=px.colors.sequential.Viridis
                
                )
    elif chosen_col == 'number of children':
        figure = px.histogram(
            booking,
            x='number of children',
            y='room type',
            color='type of meal',
            title='The children effect on parents decision with selecting the meal type and room typee',
            labels={'booking_meals': 'Booking Meals', 'number_of_children': 'Average Number of Children'},
            color_discrete_sequence=px.colors.sequential.Viridis

        )        

    elif chosen_col =='rep&no_of_children':
        figure = px.violin(
            booking,
            x='repeated',
            y='number of children',
            title='Distribution of Number of Children for Repeated and Non-Repeated Guests',
            labels={'repeated_guest': 'Repeated Guest', 'number_of_children': 'Number of Children'},
            color_discrete_sequence=px.colors.sequential.Viridis

        )        

        
        
    else:
        figure = px.histogram(
            booking,
            x='total_nights',
            y='avg_price_per_night',
            color='booking status',

            title='Distribution of Price Per Night & total number of nights by Booking Status',
            barmode='stack',
            color_discrete_sequence=px.colors.sequential.Viridis)

      
    return figure

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
