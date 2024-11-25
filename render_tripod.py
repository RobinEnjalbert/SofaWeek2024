import Sofa, Sofa.Gui

from scene_tripod.scene import Simulation


if __name__ == '__main__':

    # Create the SOFA simulation
    root = Sofa.Core.Node()
    simu = root.addObject(Simulation(root=root))
    Sofa.Simulation.init(root)
    simu.init_viewer()

    # Launch the SOFA Gui, run a few time steps
    Sofa.Gui.GUIManager.Init(program_name="main", gui_name="qglviewer")
    Sofa.Gui.GUIManager.createGUI(root, __file__)
    Sofa.Gui.GUIManager.SetDimension(1200, 900)
    Sofa.Gui.GUIManager.MainLoop(root)
    Sofa.Gui.GUIManager.closeGUI()

    # Publish
    simu.close_viewer()
