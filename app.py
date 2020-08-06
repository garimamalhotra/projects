import pandas as pd
from bokeh.plotting import figure, show, output_file, output_notebook
from bokeh.palettes import Spectral11, colorblind, Inferno, BuGn, brewer
from bokeh.models import HoverTool, value, LabelSet, Legend, ColumnDataSource,\
LinearColorMapper,BasicTicker, PrintfTickFormatter, ColorBar, Dropdown, Select, CustomJS,RadioGroup 
from bokeh.io import curdoc
from bokeh.layouts import column, gridplot,row 
from bokeh.embed import components 
from bokeh.themes import Theme
import yaml

import datetime as dt
import time
from flask import Flask, render_template


TOOLS = 'crosshair,save,pan,box_zoom,reset,wheel_zoom'
p = figure(title="Employees on Linkedin through Time", y_axis_type="log",x_axis_type='datetime', tools = TOOLS)

#Selecting Apple for this EDA since it has largest number of followers and employees on linkedin
df_select=pd.read_csv('df_common.csv')
df_select['as_of_date']=pd.to_datetime(df_select['as_of_date'])
df_stocks_cut=pd.read_csv('df_stocks_cut.csv')
df_stocks_cut['date']=pd.to_datetime(df_stocks_cut['date'])

common_companies=df_select.company_name.unique()
df_comp=df_select[df_select['company_name']=='Apple']

df_comp=df_comp.sort_values(by='as_of_date')
source = ColumnDataSource(data={'x': df_comp['as_of_date'].values, 'y': df_comp['employees_on_platform'].values})
source2 = ColumnDataSource(data={'x': df_comp['as_of_date'], 'y': df_comp['followers_count']})

p.line(x='x',y='y',source=source,line_width=3,line_color="#f46d43",legend='Employees')
p.line(x='x',y='y',source=source2,line_width=3,line_color="blue",line_alpha=0.3,legend='Followers')

p.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=\
                      [('Date', '@x{%F}'),('Employees', '@y')],\
                     formatters={'@x': 'datetime'}))
#p.plot_width =400


def callback(attr, old, new):
    df_comp=df_select[df_select['company_name']==new]
    df_comp=df_comp.sort_values(by='as_of_date')
    y_val=df_comp['employees_on_platform']
    y_val2=df_comp['followers_count']
    df_new=pd.DataFrame({'x':df_comp['as_of_date'],'y':y_val})
    df_new2=pd.DataFrame({'x':df_comp['as_of_date'],'y':y_val2})
    source.data=ColumnDataSource.from_df(df_new)
    source2.data=ColumnDataSource.from_df(df_new2)

    sym_click=df_comp['Sym'].unique()[0]
    df_stock_new=df_stocks_cut[df_stocks_cut['Name']==sym_click]
    df_stock_new=df_stock_new.sort_values(by='date')
    yval=df_stock_new['high']
    df_new3=pd.DataFrame({'x':df_stock_new['date'],'y':yval})
    source3.data=ColumnDataSource.from_df(df_new3)

#Figure 2
#apple_sym='APL'
p2 = figure(title="Stocks of the company through Time", y_axis_type="log",x_axis_type='datetime', tools = TOOLS)
#p2.line(x=[1,2,3],y=[6,7,9])

sym=df_select[df_select['company_name']=='Apple']['Sym'].unique()[0]
df_stocks_comp=df_stocks_cut[df_stocks_cut['Name']==sym]
df_stocks_comp=df_stocks_comp.sort_values(by='date')

source3=ColumnDataSource(data={'x': df_stocks_comp['date'], 'y': df_stocks_comp['high']})
p2.line(x='x',y='y',source=source3,line_width=3,line_color="#f46d43")

p2.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=\
                          [('Date', '@x{%F}'),('High', '@y')],\
                         formatters={'@x': 'datetime'}))

menu= Select(options=list(common_companies), value='Apple', title='Distribution')
menu.on_change('value', callback) 
    
ph=row(p,p2)
curdoc().add_root(column(menu,ph))

curdoc().theme = Theme(json=yaml.load("""
    attrs:
        Figure:
            background_fill_color: "white"
            outline_line_color: white
            toolbar_location: above
            height: 500
            width: 700
        Grid:
            grid_line_dash: [6, 4]
            grid_line_color: "#DDDDDD"
""", Loader=yaml.FullLoader))


