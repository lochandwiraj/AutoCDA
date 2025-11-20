import pytest
from skidl import Part, Net, generate_netlist, reset

def test_skidl_import():
    assert Part is not None

def test_simple_circuit():
    reset()

    # Create voltage source (no library needed)
    v1 = Part(
        name="V",
        tool=None,
        ref="V1",
        value="DC 5V",
        pins=[
            {"name": "p", "num": "1"},
            {"name": "n", "num": "2"}
        ]
    )

    # Create resistor (no library needed)
    r1 = Part(
        name="R",
        tool=None,
        ref="R1",
        value="1k",
        pins=[
            {"name": "1", "num": "1"},
            {"name": "2", "num": "2"}
        ]
    )

    # Nets
    gnd = Net("GND")
    vout = Net("VOUT")

    # Connect circuit
    v1["p"] += r1["1"]
    r1["2"] += vout
    v1["n"] += gnd

    # Generate netlist
    netlist = generate_netlist()

    assert netlist is not None
    assert "V1" in str(netlist)
    assert "R1" in str(netlist)