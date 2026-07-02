# ui/circuits.py
from core.components import Resistor, VoltageSource

CIRCUITS = {
    "Voltage Divider": {
        "components": [
            VoltageSource("V1", 5.0, ["N1", "GND"]),
            Resistor("R1", 2.0, ["N1", "N2"]),
            Resistor("R2", 4.0, ["N2", "GND"]),
        ],
        "positions": {
            "N1": (100, 80), "N2": (400, 80), "GND": (250, 280),
        },
    },
    "Two-Source Ladder": {
        "components": [
            VoltageSource("V1", 10.0, ["N1", "GND"]),
            VoltageSource("V2", 5.0, ["N4", "GND"]),
            Resistor("R1", 2.0, ["N1", "N2"]),
            Resistor("R2", 4.0, ["N2", "GND"]),
            Resistor("R3", 4.0, ["N2", "N3"]),
            Resistor("R4", 8.0, ["N3", "GND"]),
            Resistor("R5", 4.0, ["N3", "N4"]),
        ],
        "positions": {
            "N1": (80, 80), "N2": (220, 80), "N3": (360, 80),
            "N4": (500, 80), "GND": (290, 280),
        },
    },
    "Stress Test (5V, 10R)": {
        "components": [
            VoltageSource("V1", 12.0, ["N1", "GND"]),
            VoltageSource("V2",  9.0, ["N3", "GND"]),
            VoltageSource("V3",  5.0, ["N5", "N6"]),   # floating!
            VoltageSource("V4",  3.3, ["N7", "GND"]),
            VoltageSource("V5",  6.0, ["N8", "N2"]),   # floating!
            Resistor("R1",   100.0, ["N1", "N2"]),
            Resistor("R2",   220.0, ["N2", "N3"]),
            Resistor("R3",   330.0, ["N2", "GND"]),
            Resistor("R4",   470.0, ["N3", "N4"]),
            Resistor("R5",  1000.0, ["N4", "GND"]),
            Resistor("R6",   150.0, ["N4", "N5"]),
            Resistor("R7",   680.0, ["N6", "GND"]),
            Resistor("R8",   560.0, ["N5", "N7"]),
            Resistor("R9",   820.0, ["N6", "N7"]),
            Resistor("R10",  390.0, ["N8", "N4"]),
        ],
        "positions": {
            "N1": (60, 60),   "N2": (200, 60),  "N3": (340, 60),
            "N4": (340, 180), "N5": (480, 180), "N6": (480, 300),
            "N7": (200, 300), "N8": (60, 180),  "GND": (60, 300),
        },
},
}