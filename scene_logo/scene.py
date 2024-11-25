from os.path import join, dirname
import numpy as np
import Sofa

from SimRender.sofa import Viewer


class Simulation(Sofa.Core.Controller):

    def __init__(self, root: Sofa.Core.Node, *args, **kwargs):
        """
        Simulation of the SOFA logo.
        Forces and constraints can be manually defined using the 'select_constraints.py' script.
        """

        Sofa.Core.Controller.__init__(self, name='PyController', *args, **kwargs)
        data_dir = join(dirname(__file__), 'data')
        self.root = root
        self.animate_event_fnc = lambda: None
        self.viewer = None

        # Root
        self.root.dt.value = 0.1
        with open(join(data_dir, 'plugins.txt'), 'r') as f:
            required_plugins = [plugin[:-1] if plugin.endswith('\n') else plugin for plugin in f.readlines()
                                if plugin != '\n']
        self.root.addObject('RequiredPlugin', pluginName=required_plugins)
        self.root.addObject('VisualStyle', displayFlags='showVisualModels showBehaviorModels showForceFields')
        self.root.addObject('DefaultAnimationLoop')
        self.root.addObject('GenericConstraintSolver', maxIterations=20, tolerance=1e-6)

        self.root.addChild('logo')
        self.root.logo.addObject('EulerImplicitSolver', firstOrder=False, rayleighMass=1e-3, rayleighStiffness=1e-3)
        self.root.logo.addObject('CGLinearSolver', iterations=25, tolerance=1e-9, threshold=1e-9)
        self.root.logo.addObject('MeshVTKLoader', name='mesh', filename=join(data_dir, 'volume.vtk'), rotation=[90, 0, 0])
        self.root.logo.addObject('TetrahedronSetTopologyContainer', name='topology', src='@mesh')
        self.root.logo.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
        self.root.logo.addObject('MechanicalObject', name='state', src='@topology')
        self.root.logo.addObject('TetrahedronFEMForceField', youngModulus=5000, poissonRatio=0.45, method='svd')
        self.root.logo.addObject('UniformMass', totalMass=0.1)
        self.root.logo.addObject('FixedConstraint', name='constraints', indices=np.load(join(data_dir, 'constraints.npy')))

        self.root.logo.addChild('visual')
        self.root.logo.visual.addObject('MeshOBJLoader', name='mesh', filename=join(data_dir, 'surface.obj'), rotation=[90, 0, 0])
        self.root.logo.visual.addObject('OglModel', name='ogl', color='0.85 .3 0.1 0.9', src='@mesh')
        self.root.logo.visual.addObject('BarycentricMapping')

    def init_viewer(self):

        self.viewer = Viewer(root_node=self.root, sync=False)
        self.viewer.objects.add_scene_graph(visual_models=True,
                                            behavior_models=True,
                                            force_fields=False,
                                            collision_models=False)
        self.viewer.launch()
        self.animate_event_fnc = self.viewer.render

    def close_viewer(self):

        self.viewer.shutdown()

    def onAnimateEndEvent(self, event):

        self.animate_event_fnc()

    def __default_animate(self):
        pass
