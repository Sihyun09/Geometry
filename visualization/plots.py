import plotly.graph_objects as go

def vessel_plot(
    x,
    y,
    Fx=None,
    Fy=None
):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            line=dict(width=6)
        )
    )

    if Fx is not None:

        for i in range(
            0,
            len(x),
            8
        ):

            fig.add_annotation(
                x=x[i] + 0.4 * Fx[i],
                y=y[i] + 0.4 * Fy[i],

                ax=x[i],
                ay=y[i],

                showarrow=True,
                arrowhead=3
            )

    fig.update_layout(
        height=600,
        showlegend=False
    )

    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1
    )

    return fig