from bokeh.io import curdoc
from bokeh.plotting import figure

p=figure()
p.line(x=[1,3,4],y=[6,7,9])
curdoc().add_root(p)
