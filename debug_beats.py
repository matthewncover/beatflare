import plotly.express as px

def plot_stream_clip(df, beat_midpoints):

    fig = px.line(df, x="timestep", y="db")

    for i in beat_midpoints:
        fig.add_vline(i, line_color="red", opacity=0.2)

    fig.show()