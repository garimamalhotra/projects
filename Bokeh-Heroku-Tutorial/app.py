import pandas as pd
from bokeh.plotting import figure, show, output_file, output_notebook
from bokeh.palettes import Spectral11, colorblind, Inferno, BuGn, brewer
from bokeh.models import HoverTool, value, LabelSet, Legend, ColumnDataSource,\
LinearColorMapper,BasicTicker, PrintfTickFormatter, ColorBar, Dropdown, Select, CustomJS,RadioGroup 
from bokeh.io import curdoc
from bokeh.layouts import column, gridplot 
from bokeh.embed import components 
from bokeh.themes import Theme
import yaml

import datetime as dt
import time
from flask import Flask, render_template

#Connect the app
app = Flask(__name__)


def get_plot():
    TOOLS = 'crosshair,save,pan,box_zoom,reset,wheel_zoom'
    p = figure(title="Employees on Linkedin through Time", y_axis_type="log",x_axis_type='datetime', tools = TOOLS)

    #Selecting Apple for this EDA since it has largest number of followers and employees on linkedin
    df_select=pd.read_csv('df_common.csv')
    common_companies=df_select.company_name.unique()
    df_comp=df_select[df_select['company_name']=='Apple']
    print(df_comp)
    df_comp=df_comp.sort_values(by='as_of_date')

    source = ColumnDataSource(data={'x': df_comp['as_of_date'], 'y': df_comp['employees_on_platform']})
    source2 = ColumnDataSource(data={'x': df_comp['as_of_date'], 'y': df_comp['followers_count']})

    #p.line(df_comp['as_of_date'], df_comp['employees_on_platform'], legend=icomp, line_color="purple", line_width = 3)
    p.line(x='x',y='y',source=source,line_width=3,line_color="#f46d43",legend='Employees')
    p.line(x='x',y='y',source=source2,line_width=3,line_color="blue",line_alpha=0.3,legend='Followers')

    p.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=\
                          [('Date', '@x{%F}'),('Employees', '@y')],\
                         formatters={'@x': 'datetime'}))
    p.plot_width =800

    def callback(attr, old, new):
        df_comp=df_select[df_select['company_name']==new]
        df_comp=df_comp.sort_values(by='as_of_date')
        y_val=df_comp['employees_on_platform']
        y_val2=df_comp['followers_count']
        df_new=pd.DataFrame({'x':df_comp['as_of_date'],'y':y_val})
        df_new2=pd.DataFrame({'x':df_comp['as_of_date'],'y':y_val2})
        source.data=ColumnDataSource.from_df(df_new)
        source2.data=ColumnDataSource.from_df(df_new2)

    menu= Select(options=list(common_companies), value='Apple', title='Distribution')
    menu.on_change('value', callback) 

    curdoc().add_root(column(menu, p))
    curdoc().theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#DDDDDD"
                outline_line_color: white
                toolbar_location: above
                height: 500
                width: 800
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: white
    """, Loader=yaml.FullLoader))
    
    return p

@app.route('/')
def homepage():

    #Get the data, from somewhere
    #df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', 
    #                 names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class'])

    #Setup plot    
    p = get_plot()
    script, div = components(p)

    #Give some text for the bottom of the page 
    example_string = 'Example web app built using python, Flask, and Bokeh.'

    #Render the page
    return render_template('home.html', script=script, div=div, example_string=example_string)    

if __name__ == '__main__':
    app.run(debug=False)

