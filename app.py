import math
import numpy as np
import pandas as pd

from bokeh.embed import components
from bokeh.layouts import column, gridplot, layout, row
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

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
            hover_alpha=0.35,
            size=10,
            source=source
            )
        p.add_tools(hover)

        return p

    p_Setosa = sepal_dim_plot(df_Setosa)
    p_Versicolor = sepal_dim_plot(df_Versicolor)
    p_Virginica = sepal_dim_plot(df_Virginica)

    p_Setosa.x_range = p_Versicolor.x_range = p_Virginica.x_range
    p_Setosa.y_range = p_Versicolor.y_range = p_Virginica.y_range

    return row(p_Setosa, p_Versicolor, p_Virginica)


def petal_dim(df):
    def petal_dim_plot(df_class):
        source = ColumnDataSource(df_class)
        hover = HoverTool(tooltips=[('petal length','@petal_length'), ('petal width','@petal_width')])
        p = figure(
            title=df_class.iris_class.unique().tolist().pop(),
            x_axis_label='petal length',
            y_axis_label='petal width',
            plot_width=380,
            plot_height=380,
        )
        p.circle(
            x='petal_length',
            y='petal_width',
            color='color',
            alpha=0.7,
            hover_alpha=0.35,
            size=10,
            source=source
            )
        p.add_tools(hover)

        return p

    p_Setosa = petal_dim_plot(df_Setosa)
    p_Versicolor = petal_dim_plot(df_Versicolor)
    p_Virginica = petal_dim_plot(df_Virginica)

    p_Setosa.x_range = p_Versicolor.x_range = p_Virginica.x_range
    p_Setosa.y_range = p_Versicolor.y_range = p_Virginica.y_range

    return row(p_Setosa, p_Versicolor, p_Virginica)


app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        dim_chart = column(sepal_dim(df), petal_dim(df))
        script, div = components(dim_chart)
        
        return render_template('index.html', script=script,  div=div)


@app.route('/datatable', methods=['GET'])
def iris_datatable():
    if request.method == 'GET':
        return render_template('datatable.html', table=df.to_html(table_id="iris", index=False, classes="display"))


if __name__ == '__main__':
    app.run()
