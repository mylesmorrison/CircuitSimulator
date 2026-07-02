import pytest
from core.components import Resistor, VoltageSource
from core.solver import solve
from ui.circuits import CIRCUITS

def test_voltage_divider():
    components = [
        VoltageSource("V1", 5.0, ["N1", "GND"]),
        Resistor("R1", 2.0, ["N1", "N2"]),
        Resistor("R2", 4.0, ["N2", "GND"]),
    ]
    voltages, currents = solve(components)

    assert voltages["N1"] == pytest.approx(5.0)
    assert voltages["N2"] == pytest.approx(5.0 * 4 / (2 + 4))  # 3.333V
    assert currents["V1"] == pytest.approx(-5.0 / 6)           # 0.833A drawn

def test_busy_node():
    # The 4-component circuit with three resistors meeting at N1
    components = [
        VoltageSource("V1", 5.0, ["N1", "GND"]),
        Resistor("R1", 2.0, ["N1", "N2"]),
        Resistor("R2", 4.0, ["N1", "N3"]),
        Resistor("R3", 10.0, ["N1", "GND"]),
    ]
    voltages, currents = solve(components)
    assert voltages["N1"] == pytest.approx(5.0)
    # N2 and N3 dangle (no path to ground except back through N1),
    # so no current flows through R1/R2 → same voltage as N1
    assert voltages["N2"] == pytest.approx(5.0)
    assert voltages["N3"] == pytest.approx(5.0)

def test_two_source_ladder():
    components = [
        VoltageSource("V1", 10.0, ["N1", "GND"]),
        VoltageSource("V2",  5.0, ["N4", "GND"]),
        Resistor("R1", 2.0, ["N1", "N2"]),
        Resistor("R2", 4.0, ["N2", "GND"]),
        Resistor("R3", 4.0, ["N2", "N3"]),
        Resistor("R4", 8.0, ["N3", "GND"]),
        Resistor("R5", 4.0, ["N3", "N4"]),
    ]
    voltages, currents = solve(components)

    assert voltages["N1"] == pytest.approx(10.0)
    assert voltages["N2"] == pytest.approx(55 / 9)
    assert voltages["N3"] == pytest.approx(40 / 9)
    assert voltages["N4"] == pytest.approx(5.0)
    assert abs(currents["V1"]) == pytest.approx(35 / 18)
    assert abs(currents["V2"]) == pytest.approx(5 / 36)

def test_parallel_resistors():
    # Two 4Ω in parallel = 2Ω, divider with another 2Ω → N2 should be 2.5V
    components = [
        VoltageSource("V1", 5.0, ["N1", "GND"]),
        Resistor("R1", 2.0, ["N1", "N2"]),
        Resistor("R2", 4.0, ["N2", "GND"]),
        Resistor("R3", 4.0, ["N2", "GND"]),   # same nodes as R2!
    ]
    voltages, _ = solve(components)
    assert voltages["N2"] == pytest.approx(2.5)

def test_floating_node_raises():
    components = [
        VoltageSource("V1", 5.0, ["N1", "GND"]),
        Resistor("R1", 2.0, ["N1", "N2"]),
        Resistor("R2", 4.0, ["N3", "N4"]),   # island — not connected to anything
    ]
    with pytest.raises(ValueError):
        solve(components)

def test_stress_circuit():
    voltages, currents = solve(CIRCUITS["Stress Test (5V, 10R)"]["components"])
    assert voltages["N2"] == pytest.approx(8.2869, abs=1e-3)
    assert voltages["N4"] == pytest.approx(8.3352, abs=1e-3)
    assert voltages["N5"] - voltages["N6"] == pytest.approx(5.0)
    assert voltages["N8"] - voltages["N2"] == pytest.approx(6.0)