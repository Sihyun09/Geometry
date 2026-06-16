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

        scale = 0.7

        for i in range(0, len(x), 8):

            x0 = x[i]
            y0 = y[i]

            x1 = x0 + scale * Fx[i]
            y1 = y0 + scale * Fy[i]

            fig.add_trace(
                go.Scatter(
                    x=[x0, x1],
                    y=[y0, y1],
                    mode="lines",
                    showlegend=False
                )
            )

            fig.add_annotation(
                x=x1,
                y=y1,
                ax=x0,
                ay=y0,
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