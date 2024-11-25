from os.path import join
import subprocess
import webbrowser
import qrcode
import Sofa, Sofa.Gui

from SimExporter.sofa import Exporter
from scene_tripod.scene import Simulation


def publish():

    # Github
    subprocess.run(['git', 'add', 'html/tripod.html'])
    subprocess.run(['git', 'commit', '-m', 'Update html.'])
    subprocess.run(['git', 'push'])

    # Generate url
    com = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8')[:-1]
    url = f'https://htmlpreview.github.io/?https://github.com/RobinEnjalbert/SofaWeek2024/blob/{com}/html/tripod.html'
    webbrowser.open(url)

    # Generate qr-code
    img = qrcode.make(url)
    img.show()


if __name__ == '__main__':

    # Create the SOFA simulation
    node = Sofa.Core.Node()
    node.addObject(Simulation(root=node))

    # Create the Exporter and add objects
    exporter = Exporter(root=node, dt=0.01, animation=True, fps=80)
    exporter.objects.add_sofa_mesh(positions_data=node.Modelling.Tripod.ElasticBody.VisualModel.renderer.position,
                                   cells=node.Modelling.Tripod.ElasticBody.VisualModel.renderer.triangles.value,
                                   color='#ff7800', alpha=0.9)
    for i in range(3):
        exporter.objects.add_sofa_mesh(positions_data=node.Modelling.Tripod.getChild(f'ActuatedArm{i}').ServoMotor.Articulation.ServoWheel.ServoArm.VisualModel.OglModel.position,
                                       cells=node.Modelling.Tripod.getChild(f'ActuatedArm{i}').ServoMotor.Articulation.ServoWheel.ServoArm.VisualModel.OglModel.triangles.value,
                                       color='#ffffff', alpha=0.1)

    # Init the SOFA simulation AFTER creating the exporter (otherwise, callbacks will not work)
    Sofa.Simulation.init(node)

    # Launch the SOFA Gui, run a few time steps
    Sofa.Gui.GUIManager.Init(program_name="main", gui_name="qglviewer")
    Sofa.Gui.GUIManager.createGUI(node, __file__)
    Sofa.Gui.GUIManager.SetDimension(1200, 900)
    Sofa.Gui.GUIManager.MainLoop(node)
    Sofa.Gui.GUIManager.closeGUI()

    # Export to HTML file
    exporter.set_camera(factor=1.2)
    exporter.to_html(filename=join('html', 'tripod.html'), background_color='#fedfbe', grid_visible=False,
                     menu_visible=True, frame_visible=True)

    # Publish
    publish()
