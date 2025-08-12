import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)

# Initialize Dash app
app = dash.Dash(__name__)

# List of years for dropdown
year_list = [i for i in range(1980, 2024)]

# App layout
app.layout = html.Div([
    # Task 2.1: Title
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}
    ),
    
    # Task 2.2: Dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type',
            value='Yearly Statistics',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'}
        )
    ]),
    
    html.Br(),
    
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select year',
            value=year_list[0],
            style={'width': '50%', 'padding': '3px', 'fontSize': '18px', 'textAlignLast': 'center'}
        )
    ]),
    
    html.Br(),
    
    # Task 2.3: Output container for graphs
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flexWrap': 'wrap'})
    ])
])


# Task 2.4: Callback to enable/disable year dropdown based on report type
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_year_dropdown_disabled(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True


# Task 2.4: Callback to update graphs based on report type and year selection
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Average automobile sales fluctuation over recession period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                           title="Average Automobile Sales fluctuation over Recession Period")
        )
        
        # Plot 2: Average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Number of Vehicles Sold by Vehicle Type During Recessions")
        )
        
        # Plot 3: Total advertising expenditure share by vehicle type during recessions (pie chart)
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                          title="Total Advertising Expenditure Share by Vehicle Type During Recessions")
        )
        
        # Plot 4: Effect of unemployment rate on vehicle type and sales (bar chart)
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )
        
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],
                     style={'display': 'flex', 'width': '100%'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],
                     style={'display': 'flex', 'width': '100%'})
        ]
    
    elif selected_statistics == 'Yearly Statistics' and input_year is not None:
        yearly_data = data[data['Year'] == input_year]
        
        # Plot 1: Yearly automobile sales using line chart for whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', title='Average Automobile Sales (Yearly)')
        )
        
        # Plot 2: Total monthly automobile sales for selected year
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales')
        )
        
        # Plot 3: Average vehicles sold by vehicle type in selected year (bar chart)
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                          title=f'Average Vehicles Sold by Vehicle Type in the year {input_year}')
        )
        
        # Plot 4: Total advertisement expenditure for each vehicle type (pie chart)
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                          title='Total Advertisement Expenditure for Each Vehicle Type')
        )
        
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)],
                     style={'display': 'flex', 'width': '100%'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)],
                     style={'display': 'flex', 'width': '100%'})
        ]
    
    else:
        return None


# Run app
if __name__ == '__main__':
    app.run(debug=True)
