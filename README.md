# Self-Driving Car ANN Simulation

A Pygame simulation of a car detecting obstacles with five ray sensors and making steering decisions using a hand-coded Artificial Neural Network.

## Architecture

```text
5 obstacle sensors
       |
       v
6 hidden neurons
       |
       v
2 output neurons
 LEFT / RIGHT
       |
       v
Car steering
```

No TensorFlow, PyTorch, Keras, or other ANN library is used.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/main.py
```

Press `R` to restart after a crash.

## Run with Docker

The Docker image runs Pygame in headless mode so it can be built and executed without requiring a graphical display inside the container.

```bash
docker build -t self-driving-car-ann .
docker run --rm self-driving-car-ann
```

Or:

```bash
docker compose up --build
```

## ANN

The network is deliberately small:

- 5 inputs: normalized sensor distances
- 6 hidden neurons
- `tanh` activation
- 2 outputs: left and right
- hard-coded weights

The next development step would be replacing the fixed weights with a training algorithm such as gradient descent or neuroevolution.
