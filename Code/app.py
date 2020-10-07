# <-------------------------- TERRORISM ANALYSIS------------------------------>
# Importing required libraries
import pandas as pd
import dash 
import dash_html_components as html
import webbrowser
import dash_core_components as dcc
from dash.dependencies import Input,Output
import plotly.graph_objects as go
import plotly.express as px   
from dash.exceptions import PreventUpdate

# Creating a global Dash type object 
app=dash.Dash()

# Defining required variables
def load_data():
    dataset_name = "global_terror.csv"
    global df
    df=pd.read_csv(dataset_name)
    
    month={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
    global month_list
    month_list=[{'label':key,'value':values} for key,values in month.items()]
    
    global region_list
    region_list=[{'label':str(i),'value':str(i)} for i in sorted(df['region_txt'].unique().tolist())]
    
    global country_data
    country_data=df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
    
    global state_data
    state_data=df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
    
    global city_data
    city_data=df.groupby("provstate")["city"].unique().apply(list).to_dict()
    
    global attack_list
    attack_list=[{'label':str(i),'value':str(i)} for i in sorted(df['attacktype1_txt'].unique().tolist())]  
    
    global year_list
    year_list=sorted(df['iyear'].unique().tolist())
    global year_dict
    year_dict={str(year):str(year) for year in year_list}
    
    global chart_dropdown_data,chart_dropdown_values
    chart_dropdown_data={'Terrorist Organisation':'gname','Target Nationality':'natlty1_txt','Target Type':'targtype1_txt','Attack Type':'attacktype1_txt','Weapon Type':'weaptype1_txt','Region':'region_txt','Country Attacked':'country_txt'}
    chart_dropdown_values=[{'label':key,'value':val} for key,val in chart_dropdown_data.items()]

# Creating a UI having 2 tabs ie Map Tool and Chart Tool
# Both the tabs have respective subtabs for world and india scenario
def create_app_ui():
    main_layout=html.Div(
    [
     html.H1(children="Terrorism Analysis with Insights",id='Main_heading',style={'textAlign':'center'}),      
     
     html.Hr(),
     html.Br(),  
     
     dcc.Tabs(id='Tabs', value='map', children=[
         dcc.Tab(label='Map Tool',id='MapT', value='map', children=[
         dcc.Tabs(id='Subtabs_map',value='worldmap',children=[
                 dcc.Tab(label='World Map',id='WorldM',value='worldmap'),
                 dcc.Tab(label='India Map',id='IndiaM',value='indiamap')
                 ]
                 )]),
         
         dcc.Tab(label='Chart Tool',id='ChartT',value='chart',children=[
         dcc.Tabs(id='Subtabs_chart',value='worldchart',children=[
                 dcc.Tab(label='World Chart',id='WorldC',value='worldchart'),
                 dcc.Tab(label='India Chart',id='IndiaC',value='indiachart')]),
                 ])        
     ]),
     html.Div(id='dropdowns') # Here the screen will fill with either map-specifications or the chart-specifications as returned by update_data callback
    ])
    return main_layout

@app.callback(
Output('dropdowns','children'),
[Input('Tabs','value')]
)
def update_data(tab): # To show dropdowns based on id='Tabs' value
    data=None
    if tab=='map':  # When user selects Map Tool tab
        data=html.Div([
        dcc.Dropdown(
        id='dropdown-month',
        options=month_list,
        placeholder='Select Month',
        multi=True       
        ),
     
        dcc.Dropdown(
        id='dropdown-date',
        placeholder='Select Date',      
        multi=True
        ),
     
        dcc.Dropdown(
        id='dropdown-region',
        options=region_list,
        placeholder='Select Region',        
        multi=True
        ),
            
        dcc.Dropdown(id='dropdown-country',   
        options=[{'label':'All','value':'All'}],   
        placeholder='Select Country',
        multi=True
        ),
                  
        dcc.Dropdown(
        id='dropdown-state',
        options=[{'label':'All','value':'All'}],
        placeholder='Select State',        
        multi=True
        ),
             
        dcc.Dropdown(
        id='dropdown-city',
        options=[{'label':'All','value':'All'}],
        placeholder='Select City',        
        multi=True
        ),
             
        dcc.Dropdown(
        id='dropdown-attack',
        options=attack_list,
        placeholder='Select Attack Type',        
        multi=True
        ),
             
        html.Br(),
        html.H4("Select Year", id='year-title'),
     
        dcc.RangeSlider(
        id='year-slider',
        min=min(year_list),
        max=max(year_list),
        value=[min(year_list),max(year_list)],
        marks=year_dict        
        ),
             
        html.Br(),
     
        html.Div(id='map-initials',children=["World map loading..."])
        ])
    else:  # When user selects Chart Tool tab
        data=html.Div([
        html.Br(),
        html.Br(),
        
        dcc.Dropdown(
        id='dropdown-chart',
        options=chart_dropdown_values,
        placeholder='Select Your Option',
        value='region_txt'
        ),
                
        html.Br(),
        html.Br(),
        
        dcc.Input(id='search-box',placeholder='Search Filter'),
        
        html.Br(),
        html.Br(),
        
        dcc.RangeSlider(
        id='chart-year-slider',
        min=min(year_list),
        max=max(year_list),
        value=[min(year_list),max(year_list)],
        marks=year_dict,
        step=None        
        ),
        
        html.Br(),
        
        html.Div(id='chart-initials',children=["World chart loading..."])
        ])
    return data

# To update the map(world map or india map) according to user selected values
@app.callback(
        dash.dependencies.Output('map-initials','children'),
        [
        dash.dependencies.Input('dropdown-month','value'),
        dash.dependencies.Input('dropdown-date','value'),
        dash.dependencies.Input('dropdown-region','value'),
        dash.dependencies.Input('dropdown-country','value'),
        dash.dependencies.Input('dropdown-state','value'),
        dash.dependencies.Input('dropdown-city','value'),
        dash.dependencies.Input('dropdown-attack','value'),
        dash.dependencies.Input('year-slider','value'),
        dash.dependencies.Input('Tabs','value')
        ]
        )
def update_app_ui_map(month_value,date_value,region_value,country_value,state_value,city_value,attack_value,year_value,tab):
    # Printing is just for debugging purpose
    print(type(month_value))
    print(month_value)
    print(type(date_value))
    print(date_value)
    print(type(region_value))
    print(region_value)
    print(type(country_value))
    print(country_value)
    print(type(state_value))
    print(state_value)
    print(type(city_value))
    print(city_value)
    print(type(attack_value))
    print(attack_value)
    print(type(year_value))
    print(year_value)
   
    figure_map=go.Figure()  
        
    if tab=='map':  # When map is to be implemented
        year_range=range(year_value[0],year_value[1]+1)
        map_df=df[df['iyear'].isin(year_range)]
    
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                map_df=map_df[map_df["imonth"].isin(month_value)]
            else:
                map_df=map_df[map_df['imonth'].isin(month_value) & map_df['iday'].isin(date_value)]  # here () not needed for expressions on either side of &
        
        if region_value==[] or region_value is None:
            pass
        else: 
            if country_value==[] or country_value is None: 
                map_df=map_df[map_df['region_txt'].isin(region_value)]
            else: 
                if state_value==[] or state_value is None:
                    map_df=map_df[map_df['region_txt'].isin(region_value) & map_df['country_txt'].isin(country_value)]
                else: 
                    if city_value==[] or city_value is None:
                        map_df=map_df[map_df['region_txt'].isin(region_value) & map_df['country_txt'].isin(country_value) & map_df['provstate'].isin(state_value)]
                    else:
                        map_df=map_df[map_df['region_txt'].isin(region_value) & map_df['country_txt'].isin(country_value) & map_df['provstate'].isin(state_value) & map_df['city'].isin(city_value)]
    
        if attack_value==[] or attack_value is None:
            pass
        else:
            map_df=map_df[map_df['attacktype1_txt'].isin(attack_value)]
    
        if map_df.shape[0]:
            pass
        else: 
            map_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate', 'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            map_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
    
        figure_map=px.scatter_mapbox(
            map_df,
            lat='latitude',
            lon='longitude',
            color='attacktype1_txt',  
            hover_name="city",
            hover_data=['region_txt','country_txt','provstate','city','attacktype1_txt','nkill','iyear'],
            zoom=1  
            )
    
        figure_map.update_layout(
            mapbox_style='open-street-map',
            autosize=True,  
            margin=dict(l=0,r=0,t=25,b=20)                     
            )
    
        return dcc.Graph(figure=figure_map)
    else:
        pass
    
# To update the chart(world chart/india chart) according to user selected values
@app.callback(
        dash.dependencies.Output('chart-initials','children'),
        [
        dash.dependencies.Input('dropdown-chart','value'),
        dash.dependencies.Input('search-box','value'),
        dash.dependencies.Input('chart-year-slider','value'),
        dash.dependencies.Input('Tabs','value'),
        dash.dependencies.Input('Subtabs_chart','value')
        ]
        )
def update_app_ui_chart(chart_value,search_value,chart_year_value,tab,subtab): 
    figure_chart=go.Figure() 
        
    if tab=='chart':   # When chart is to be implemented
        year_range=range(chart_year_value[0],chart_year_value[1]+1)
        chart_df=df[df['iyear'].isin(year_range)]
        
        # Following if-else block would filter the output according to world chart or india chart
        if subtab=='worldchart':  
            pass
        else:  
            chart_df=chart_df[(chart_df["region_txt"]=="South Asia") & (chart_df["country_txt"]=="India")]
        
        if chart_value is not None:
            if search_value is not None:
                chart_df=chart_df=chart_df.groupby('iyear')[chart_value].value_counts().reset_index(name='count')
                chart_df=chart_df[chart_df[chart_value].str.contains(search_value,case=False)]
            else:
                chart_df=chart_df.groupby('iyear')[chart_value].value_counts().reset_index(name='count')
        else:
            raise PreventUpdate
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['count', 'iyear','chart_value'])
            chart_df.loc[0] = [0, 0, "No Data"]
        
        figure_chart=px.area(chart_df,x='iyear',y='count',color=chart_value)
        
        return dcc.Graph(figure=figure_chart)
    else:
        pass

# Updating the date dropdown options according to the value selected from month dropdown
@app.callback(
Output('dropdown-date','options'),
[Input('dropdown-month','value')]        
)
def update_date_options_acc_to_month_selected(month_value):
    dates=[x for x in range(1,32)]
    options=[]
    if month_value:
        options=[{'label':m,'value':m} for m in dates]
    return options
    
# 'dropdown_update_acc_to_world_or_india_map' callback is for providing india map tool facility (here we need to fix the values for region and country dropdowns)
@app.callback(
[
Output('dropdown-region','value'),
Output('dropdown-region','disabled'),
Output('dropdown-country','value'),
Output('dropdown-country','disabled')
],
[Input('Subtabs_map','value')]        
)
def dropdown_update_acc_to_world_or_india_map(subtab):
    region=None
    disable_region=False
    country=None
    disable_country=False
    if subtab=='worldmap':
        pass
    else:
        region=['South Asia']
        disable_region=True
        country=['India']
        disable_country=True
    return region, disable_region, country, disable_country

# Chained callbacks to filter country,state,city options based on region,country,state values respectively
@app.callback(
Output('dropdown-country','options'),
[Input('dropdown-region','value')]     
)
def update_country_options_acc_to_region_selected(region_value):
    options=[]
    if region_value is None:
        raise PreventUpdate
    else: 
        for reg in region_value:
            if reg in country_data.keys():
                options.extend(country_data[reg])
    return [{'label':country,'value':country} for country in options]
@app.callback(
Output('dropdown-state','options'),
[Input('dropdown-country','value')]        
)
def update_state_options_acc_to_region_country_selected(country_value):
    options=[]
    if country_value is None:
        raise PreventUpdate
    else:
        for country in country_value:
            if country in state_data.keys():
                options.extend(state_data[country])
    return [{'label':state,'value':state} for state in options]
@app.callback(
Output('dropdown-city','options'),
[Input('dropdown-state','value')]         
)
def update_city_options_acc_to_region_country_state_selected(state_value):
    options=[]
    if state_value is None:
        raise PreventUpdate
    else:
        for state in state_value:
            if state in city_data.keys():
                options.extend(city_data[state])
    return [{'label':city,'value':city} for city in options]

# Automatically opening the web app on running the script
def open_browser():
    url='http://127.0.0.1:8050/'
    webbrowser.open_new(url)

# Program flow
def main():
    load_data()
    open_browser() 
    global app,df 
    app.layout=create_app_ui()
    app.title="Terrorism Analysis"
    app.run_server()
    df=None
    app=None
    
if __name__=='__main__':
    print('Project starting ... ')
    main()
    print('Project ended!!')
