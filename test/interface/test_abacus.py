"""Tests for ABACUS calculater interface."""
import os

import numpy as np

from phonopy.interface.abacus import read_abacus
from phonopy.interface.phonopy_yaml import read_cell_yaml
from phonopy.structure import cells

data_dir = os.path.dirname(os.path.abspath(__file__))


def test_read_abacus():
    """Test of read_ABACUS."""
    cell, pps, orbitals, abfs = read_abacus(os.path.join(data_dir, "NaCl-abacus.stru"))
    filename = os.path.join(data_dir, "NaCl-abinit-pwscf.yaml")
    cell_ref = read_cell_yaml(filename)
    # assert (np.abs(cell.cell - cell_ref.cell) < 1e-5).all()
    assert cells.isclose(cell, cell_ref)
    diff_pos = cell.scaled_positions - cell_ref.scaled_positions
    diff_pos -= np.rint(diff_pos)
    assert (np.abs(diff_pos) < 1e-5).all()
    for s, s_r in zip(cell.symbols, cell_ref.symbols):
        assert s == s_r
    assert pps["Na"] == "Na_ONCV_PBE-1.0.upf"
    assert pps["Cl"] == "Cl_ONCV_PBE-1.0.upf"
    assert orbitals["Na"] == "Na_gga_9au_100Ry_4s2p1d.orb"
    assert orbitals["Cl"] == "Cl_gga_8au_100Ry_2s2p1d.orb"

    print(pps, orbitals)
