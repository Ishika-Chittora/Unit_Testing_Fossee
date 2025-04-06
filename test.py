import pytest
from bolted_lap_joint_design import design_lap_joint
from is800_2007 import IS800_2007

# Dummy functions to override functions in IS800_2007
def dummy_bolt_shear_capacity(bolt_fy, A_bolt1, A_bolt2, x, y, mode):
    # Return a nonzero positive shear capacity (in Newtons)
    return 1000.0

def dummy_bolt_bearing_capacity(fu_plate, bolt_fy, total_thickness, d, e, p, mode, field):
    # Return a nonzero positive bearing capacity (in Newtons)
    return 1500.0

# Parameterize over a range of loads (P in kN) and thicknesses (t1 and t2 in mm)
# Here, P=0 is included and it will be handled separately.
@pytest.mark.parametrize("P", range(0, 101, 10))  # 0, 10, 20, ..., 100 kN
@pytest.mark.parametrize("t1", [6, 8, 10, 12, 16, 20, 24])
@pytest.mark.parametrize("t2", [6, 8, 10, 12, 16, 20, 24])
def test_bolted_lap_joint(monkeypatch, P, t1, t2):
    """
    Test that design_lap_joint returns a design with at least 2 bolts for loads > 0.
    For P=0, we expect a ValueError (if the design code deems a zero load invalid).
    """
    # Override the functions using monkeypatch
    monkeypatch.setattr(IS800_2007, "cl_10_3_3_bolt_shear_capacity", dummy_bolt_shear_capacity)
    monkeypatch.setattr(IS800_2007, "cl_10_3_4_bolt_bearing_capacity", dummy_bolt_bearing_capacity)

    w = 150  # Fixed plate width in mm is 150 

    if P == 0:
        # For a zero load, we expect the design function to raise ValueError.
        with pytest.raises(ValueError):
            design_lap_joint(P, w, t1, t2)
    else:
        # For nonzero load, the design should return a design with at least 2 bolts.
        design = design_lap_joint(P, w, t1, t2)
        assert design["number_of_bolts"] >= 2, (
            f"Design returned {design['number_of_bolts']} bolts for P={P}, t1={t1}, t2={t2}"
        )

if __name__ == "__main__":
    pytest.main()
