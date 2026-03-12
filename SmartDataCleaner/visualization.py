import plotly.express as px 
def histogram(df, column):
    fig=px.histogram(
        df,
        x=column,
        title=f"Distributation of {column}"
    )
    return fig
def bar_chart(df, x_col, y_col):
    fig=px.bar(
        df,
        x=x_col,
        y=y_col,
        title=f"{y_col} by {x_col}"
    )
    return fig
def scatter_plot(df,x_col,y_col):
    fig=px.scatter(
        df,
        x=x_col,
        y=y_col,
        title=f"{x_col} vs {y_col}"
    )
    return fig
def correlation_heatmap(df):
    corr=df.corr(numeric_only=True)
    fig=px.imshow(
        corr,
        text_auto=True,
        title="Correlation Heartmap"
    )
    return fig