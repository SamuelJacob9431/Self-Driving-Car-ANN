import math


def tanh(x):
    return math.tanh(x)


class NeuralNetwork:
    """
    Hand-coded Artificial Neural Network.

    Architecture:

        5 sensor inputs
              ↓
        6 hidden neurons
              ↓
        2 output neurons

    Sensor inputs represent CLEARANCE:

        0.0 = obstacle is very close
        1.0 = path is clear

    Outputs:

        output[0] = LEFT
        output[1] = RIGHT
    """

    def __init__(self):

      
        self.weights_input_hidden = [

            # Left danger
            [-6.0, -3.0, 0.0, 0.0, 0.0],

            # Left/front danger
            [0.0, -5.0, -4.0, 0.0, 0.0],

            # Front danger
            [0.0, 0.0, -7.0, 0.0, 0.0],

            # Right/front danger
            [0.0, 0.0, -4.0, -5.0, 0.0],

            # Right danger
            [0.0, 0.0, 0.0, -3.0, -6.0],

            # Overall danger
            [-2.0, -2.0, -3.0, -2.0, -2.0],
        ]

        self.bias_hidden = [
            4.5,
            4.5,
            4.0,
            4.5,
            4.5,
            4.0,
        ]


        self.weights_hidden_output = [

            # LEFT
            [
                -2.5,   # left danger -> don't turn left
                -1.5,
                0.5,    # front danger
                1.5,
                2.5,    # right danger -> turn left
                0.0,
            ],

            # RIGHT
            [
                2.5,    # left danger -> turn right
                1.5,
                0.5,    # front danger
                -1.5,
                -2.5,   # right danger -> don't turn right
                0.0,
            ],
        ]

        self.bias_output = [0.0, 0.0]

    def forward(self, inputs):

        hidden = []

     

        for neuron_weights, bias in zip(
            self.weights_input_hidden,
            self.bias_hidden
        ):

            weighted_sum = 0.0

            for input_value, weight in zip(
                inputs,
                neuron_weights
            ):
                weighted_sum += input_value * weight

            weighted_sum += bias

            hidden.append(tanh(weighted_sum))

        

        outputs = []

        for neuron_weights, bias in zip(
            self.weights_hidden_output,
            self.bias_output
        ):

            weighted_sum = 0.0

            for hidden_value, weight in zip(
                hidden,
                neuron_weights
            ):
                weighted_sum += hidden_value * weight

            weighted_sum += bias

            outputs.append(tanh(weighted_sum))

        return outputs, hidden