import math
import numpy as np
import pandas as pd

from bokeh.embed import components
from bokeh.layouts import column, gridplot, layout, row
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure

from flask import Flask, render_template, request

df = pd.read_csv('data/iris.csv')

df_Setosa = df.loc[df.iris_class=='Setosa'].copy()
df_Setosa['color'] = 'firebrick'
df_Versicolor = df.loc[df.iris_class=='Versicolor'].copy()
df_Versicolor['color'] = 'limegreen'
df_Virginica = df.loc[df.iris_class=='Virginica'].copy()
df_Virginica['color'] = 'deepskyblue'


def sepal_dim(df):
    def sepal_dim_plot(df_class):
        source = ColumnDataSource(df_class)
        hover = HoverTool(tooltips=[('sepal length','@sepal_length'), ('sepal width','@sepal_width')])
        p = figure(
            title=df_class.iris_class.unique().tolist().pop(),
            x_axis_label='sepal length',
            y_axis_label='sepal width',
            plot_width=380,
            plot_height=380,
        )
        p.circle(
            x='sepal_length',
            y='sepal_width',
            color='color',
            alpha=0.7,
            hover_alpha=0,
            source=source
            )
        p.add_tools(hover)

        return p

    p_Setosa = sepal_dim_plot(df_Setosa)
    p_Versicolor = sepal_dim_plot(df_Versicolor)
    p_Virginica = sepal_dim_plot(df_Virginica)

    p_Setosa.x_range = p_Versicolor.x_range = p_Virginica.x_range
    p_Setosa.y_range = p_Versicolor.y_range = p_Virginica.y_range

    layout = row(p_Setosa, p_Versicolor, p_Virginica)

    return layout


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    sepal_dim_chart = sepal_dim(df)
    script, div = components(sepal_dim_chart)

    return render_template('index.html', script=script,  div=div)


if __name__ == '__main__':
    app.run()
