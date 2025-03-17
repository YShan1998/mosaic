import streamlit

from core.simulator import Simulator
from ui import GridDesignerUI, SimulationInputUI, SimulationPreparationUI


def main():
    streamlit.title("Mosaic App")

    grid_designer_ui = GridDesignerUI()
    is_grid_designer_ui_success = grid_designer_ui.show()

    simulation_input_ui = SimulationInputUI()
    is_simulation_input_ui_success = simulation_input_ui.show()

    if not is_grid_designer_ui_success or not is_simulation_input_ui_success:
        return

    simulation_preparation_ui = SimulationPreparationUI(
        grid_designer_ui=grid_designer_ui, simulation_input_ui=simulation_input_ui
    )
    simulation_preparation_ui.show()

    simulator = Simulator(simulation_preparation_ui=simulation_preparation_ui)

    is_start_simulation = streamlit.button("Start Simulation", type="primary")
    is_stop_simulation = streamlit.button("Stop Simulation")
    if is_start_simulation:
        simulator.run()

    if is_stop_simulation:
        simulator.stop()


if __name__ == "__main__":
    main()
