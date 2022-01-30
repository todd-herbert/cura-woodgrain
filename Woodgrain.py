from ..Script import Script
import random


class Woodgrain(Script):
    """Creates a woodgrain effect by setting random temperature on each layer
    See https://www.reddit.com/r/3Dprinting/comments/gp5vrp/randomly_adjusting_the_print_temp_per_layer_gives/
    """

    def getSettingDataString(self):
        return """{
            "name": "Woodgrain Effect",
            "key": "Woodgrain",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "temp_min":
                {
                    "label": "Min Temp",
                    "description": "Lowest possible random temperature",
                    "type": "int",
                    "value": "200",
                    "minimum_value": "0",
                    "minimum_value_warning": "180",
                    "maximum_value_warning": "250",
                    "unit": "C"
                },
                "temp_max":
                {
                    "label": "Max Temp",
                    "description": "Highest possible random temperature",
                    "type": "int",
                    "value": "220",
                    "minimum_value": "0",
                    "minimum_value_warning": "180",
                    "maximum_value_warning": "250",
                    "unit": "C"
                }
            }
        }"""

    def execute(self, data):
        for layer in data:
            # Check that a layer is being printed
            lines = layer.split("\n")
            for line in lines:
                temp = random.randint( self.getSettingValueByKey("temp_min"), self.getSettingValueByKey("temp_max") )
                command = "M104 S" + str(temp) + " ;Woodgrain Effect\n"
                if ";LAYER:" in line:
                    index = data.index(layer)

                    # First incidence is "number of layers"
                    if index > 0:
                        #change at end of layer, leaving base layer at original temp
                        layer = layer + command

                    data[index] = layer
                    break
        return data