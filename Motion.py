import math
from Component import *


class Motion(Component):
    def __init__(self, hardware, identifiers):
        super().__init__(hardware, identifiers)

        # ===========CONSTANTS========

        self.PWMNORMAL = 305
        self.PWMMAXCW = 470
        self.PWMMAXCCW = 140

        self.PWMRANGE = 165

        # =========VARIABLES==========
        self._motors = {}
        self._setMyDevicesToDefaults()

    def _calculateHorizontalMotors(self):
        left_front_thruster_value = self.PWMNORMAL + self.PWMRANGE * ((self._valueMap['x'] * self._valueMap['x'] + self._valueMap['y'] * self._valueMap['y'] + self._valueMap['r'] * self._valueMap['r']) / 10000) * (100 / (self._valueMap['x'] + self._valueMap['y'] + self._valueMap['r']))
        right_front_thruster_value = self.PWMNORMAL + self.PWMRANGE * ((-1 * self._valueMap['x'] * self._valueMap['x'] + self._valueMap['y'] * self._valueMap['y'] + -1 * self._valueMap['r'] * self._valueMap['r']) / 10000) * (100 / (self._valueMap['x'] + self._valueMap['y'] + self._valueMap['r']))
        left_rear_thruster_value = self.PWMNORMAL + self.PWMRANGE * ((-1 * self._valueMap['x'] * self._valueMap['x'] + self._valueMap['y'] * self._valueMap['y'] + self._valueMap['r'] * self._valueMap['r']) / 10000) * (100 / (self._valueMap['x'] + self._valueMap['y'] + self._valueMap['r']))
        right_rear_thruster_value = self.PWMNORMAL + self.PWMRANGE * ((self._valueMap['x'] * self._valueMap['x'] + self._valueMap['y'] * self._valueMap['y'] + -1 * self._valueMap['r'] * self._valueMap['r']) / 10000) * (100 / (self._valueMap['x'] + self._valueMap['y'] + self._valueMap['r']))

        self._motors["right_front_thruster"] = right_front_thruster_value
        self._motors["left_front_thruster"] = left_front_thruster_value
        self._motors["right_rear_thruster"] = right_rear_thruster_value
        self._motors["left_rear_thruster"] = left_rear_thruster_value

    def _calculateVerticalMotors(self):
        top_front_thruster_value = int(self.MOTORS_BASE_PWM + (self._valueMap['z'] * self.FULL_PWM_RANGE_COEFFICIENT))
        top_rear_thruster_value = int(self.MOTORS_BASE_PWM + (self._valueMap['z'] * self.FULL_PWM_RANGE_COEFFICIENT))

        self._motors["top_front_thruster"] = top_front_thruster_value
        self._motors["top_rear_thruster"] = top_rear_thruster_value


    def _setMyDevicesToDefaults(self):
        self._motors["right_front_thruster"] = self.PWMNORMAL
        self._motors["left_front_thruster"] = self.PWMNORMAL
        self._motors["right_rear_thruster"] = self.PWMNORMAL
        self._motors["left_rear_thruster"] = self.PWMNORMAL
        self._motors["top_front_thruster"] = self.PWMNORMAL
        self._motors["top_rear_thruster"] = self.PWMNORMAL

        print("set to default")

        self._hardware.setDeviceValue("right_front_thruster", self._hardware.getDeviceBaseValue("right_front_thruster"))
        self._hardware.setDeviceValue("left_front_thruster", self._hardware.getDeviceBaseValue("left_front_thruster"))
        self._hardware.setDeviceValue("right_rear_thruster", self._hardware.getDeviceBaseValue("right_rear_thruster"))
        self._hardware.setDeviceValue("left_rear_thruster", self._hardware.getDeviceBaseValue("left_rear_thruster"))
        self._hardware.setDeviceValue("top_front_thruster", self._hardware.getDeviceBaseValue("top_front_thruster"))
        self._hardware.setDeviceValue("top_rear_thruster", self._hardware.getDeviceBaseValue("top_rear_thruster"))

    def _setFromMyLocalToDevice(self):
        # print("right_front_thruster pwm: ", self._motors["right_front_thruster"])
        # print("left_front_thruster pwm: ", self._motors["left_front_thruster"])
        # print("right_rear_thruster pwm: ", self._motors["right_rear_thruster"])
        # print("left_rear_thruster pwm: ", self._motors["left_rear_thruster"])
        # print("top_front_thruster pwm: ", self._motors["top_front_thruster"])
        # print("top_rear_thruster pwm: ", self._motors["top_rear_thruster"])

        self._hardware.setDeviceValue("right_front_thruster", self._motors["right_front_thruster"])
        self._hardware.setDeviceValue("left_front_thruster", self._motors["left_front_thruster"])
        self._hardware.setDeviceValue("right_rear_thruster", self._motors["right_rear_thruster"])
        self._hardware.setDeviceValue("left_rear_thruster", self._motors["left_rear_thruster"])
        self._hardware.setDeviceValue("top_front_thruster", self._motors["top_front_thruster"])
        self._hardware.setDeviceValue("top_rear_thruster", self._motors["top_rear_thruster"])

        print(self._motors)

    def update(self, event, mail_map=None):
        if event == "TCP ERROR":
            self._setMyDevicesToDefaults()
        if event is "TCP":

            print("TCP Event")
            if super().mail(event, mail_map):
                # change values to floats
                for key in self._valueMap:
                    self._valueMap[key] = float(self._valueMap[key])

                #                if self._valueMap["currentmode"] > 0:
                #                   self._valueMap["x"] = 0

                self._calculateHorizontalMotors()
                # self._calculateVerticalMotors()
                # self._hardware.setDeviceValue("right_front_thruster", self._motors["right_front_thruster"])
                # self._hardware.setDeviceValue("left_front_thruster", (self._motors["left_front_thruster"]))
                # self._hardware.setDeviceValue("right_rear_thruster", self._motors["right_rear_thruster"])
                # self._hardware.setDeviceValue("left_rear_thruster", self._inverse(self._motors["left_rear_thruster"]))
                # self._hardware.setDeviceValue("top_front_thruster", self._motors["top_front_thruster"])
                # self._hardware.setDeviceValue("top_rear_thruster", (self._motors["top_rear_thruster"]))

        if event == "I2C":
            #            print("PWM UPDATE")
            self._setFromMyLocalToDevice()


