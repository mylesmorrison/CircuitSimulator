# Circuit Simulator

A circuit simulator built from scratch in Python using Modified Nodal Analysis (MNA).

![Circuit simulator GUI showing a solved voltage divider](gui-divider.png)

## How it works

Each component stamps its contribution into a conductance matrix,
then numpy solves the resulting system:

![MNA pipeline diagram](mna-pipeline.png)
