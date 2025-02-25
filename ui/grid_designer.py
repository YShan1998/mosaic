import numpy
import pandas
import plotly.graph_objects as go
import streamlit

EXCEL_OPTIONS = [0, 1, 2, 3]
MAX_SIZE = 50


class GridDesignerUI:
    """
    The UI for grid designer.
    """

    def __init__(self):
        pass

    def show(self) -> bool:
        streamlit.write("## Grid Design")

        grid_excel_file = streamlit.file_uploader("Upload grid excel.")
        grid_data = pandas.read_excel(grid_excel_file, header=0, index_col=0, dtype=str)

        grid_data = grid_data.dropna(how="all", axis=0)  # Drop rows
        grid_data = grid_data.dropna(how="all", axis=1)  # Drop columns

        streamlit.write(grid_data)

        discrete_colourscale = [
            [0.0, "#47b39d"],
            [0.25, "#47b39d"],
            [0.25, "#ffc153"],
            [0.5, "#ffc153"],
            [0.5, "#b05f6d"],
            [0.75, "#b05f6d"],
            [0.75, "#462446"],
            [1.0, "#462446"],
        ]

        grid_data_display = grid_data.copy()

        streamlit.write(grid_data_display)

        grid_data_display = pandas.DataFrame(
            numpy.where(
                grid_data_display.map(lambda x: str(x).startswith("P")),
                1,
                numpy.where(
                    grid_data_display.map(lambda x: str(x).isdigit()),
                    0,
                    numpy.where(
                        grid_data_display.map(lambda x: pandas.isna(x)), 3, 2
                    ),
                ),
            ),
            index=grid_data_display.index,
            columns=grid_data_display.columns,
        )

        streamlit.write(grid_data_display)

        fig = go.Figure(
            data=go.Heatmap(
                z=grid_data_display.values,
                x=list(grid_data_display.columns),
                y=list(grid_data_display.index),
                colorscale=discrete_colourscale,
                colorbar=dict(
                    tickvals=[0, 1, 2, 3],
                    ticktext=[
                        "Free",
                        "Stations",
                        "Others",
                        "Unavailable",
                    ],
                    title="Legend",
                ),
                zmin=-0.5,
                zmax=3.5,
            )
        )

        for col in range(grid_data_display.shape[1] + 1):
            fig.add_shape(
                type="line",
                x0=col + 0.5,
                x1=col + 0.5,
                y0=0.5,
                y1=grid_data_display.shape[0] + 0.5,
                line=dict(color="gray", width=1),
            )

        for row in range(grid_data_display.shape[0] + 1):
            fig.add_shape(
                type="line",
                x0=0.5,
                x1=grid_data_display.shape[1] + 0.5,
                y0=row + 0.5,
                y1=row + 0.5,
                line=dict(color="gray", width=1),
            )

        fig.update_layout(
            title="Grid Layout",
            xaxis=dict(
                title="X",
                tickvals=list(grid_data_display.columns),
                scaleanchor="y",
                showgrid=False,
            ),
            yaxis=dict(
                title="Y",
                tickvals=list(grid_data_display.index),
                autorange="reversed",
                scaleanchor="x",
                showgrid=False,
            ),
        )
        fig.update_traces(hovertemplate="X: %{x}<br>Y: %{y}<extra></extra>")

        streamlit.plotly_chart(fig)

        streamlit.divider()

