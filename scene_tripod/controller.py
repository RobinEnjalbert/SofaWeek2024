import Sofa
from splib3.animation import animate
from splib3.constants import Key
from splib3.numerics import RigidDof


def reset_animation(actuators, step, angular_step, factor):

    for actuator in actuators:
        rigid = RigidDof(actuator.ServoMotor.ServoBody.dofs)
        rigid.setPosition(rigid.rest_position + rigid.forward * step * factor)
        actuator.angleIn = angular_step * factor


class Controller(Sofa.Core.Controller):

    def __init__(self, root, actuators, step_size=0.1,  *args, **kwargs):

        Sofa.Core.Controller.__init__(self, *args, **kwargs)
        self.name = "TripodController"
        self.step_size = step_size
        self.actuators = actuators

        self.root = root

    def onSimulationInitDoneEvent(self, event):

        animate(reset_animation, {"actuators": self.actuators, "step": 35.0, "angular_step": -1.4965},
                duration=0.2)

    def onKeypressedEvent(self, event):

        self.__animate_tripod(event['key'])

    def __animate_tripod(self, key):

        if key == Key.uparrow:
            self.actuators[0].ServoMotor.angleIn = self.actuators[0].ServoMotor.angleOut.value + self.step_size
        elif key == Key.downarrow:
            self.actuators[0].ServoMotor.angleIn = self.actuators[0].ServoMotor.angleOut.value - self.step_size

        if key == Key.leftarrow:
            self.actuators[1].ServoMotor.angleIn = self.actuators[1].ServoMotor.angleOut.value + self.step_size
        elif key == Key.rightarrow:
            self.actuators[1].ServoMotor.angleIn = self.actuators[1].ServoMotor.angleOut.value - self.step_size

        if key == Key.plus:
            self.actuators[2].ServoMotor.angleIn = self.actuators[2].ServoMotor.angleOut.value + self.step_size
        elif key == Key.minus:
            self.actuators[2].ServoMotor.angleIn = self.actuators[2].ServoMotor.angleOut.value - self.step_size
