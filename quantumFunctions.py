import py3Dmol
import re
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper, ParityMapper, BravyiKitaevMapper
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit.primitives import Estimator
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
import pandas as pd
from flask import Flask, render_template, jsonify, request

atom = ""
#xyz_file = "data/hydrogen_molecule.xyz"
xyz_file = "data/h2o.xyz"

def loadFile(xyz_data):
    pass
    
    
def get_molecule_html(xyz_data):
    view = py3Dmol.view(width=800, height=400)
    view.addModel(xyz_data, 'xyz')
    view.setStyle({'stick': {}, 'sphere': {'radius': 0.5}})
    view.zoomTo()
    return view._make_html()

def startComputing():
    jwmapper = JordanWignerMapper()
    pmapper = ParityMapper()
    bkmapper = BravyiKitaevMapper()
    #xyz_file = gauss_to_xyz("data/Methan_OPTFRE.gjf")
    atom = read_xyz_file(xyz_file)
    print(atom)
    #atom="He 0 0 0; He 0.52 0 0" # @param {type:"string"}
    charge = 0 # @param {type:"number"}
    spin = 0 # @param {type:"number"}

    driver = PySCFDriver(
        atom=atom,
        basis="sto3g",
        charge=charge ,
        spin=spin,
        unit=DistanceUnit.ANGSTROM,
    )

    problem = driver.run()

    q_map = get_mapping(atom, charge, spin)

    ansatz = UCCSD(
        q_map[2].num_spatial_orbitals,
        q_map[2].num_particles,
        q_map[1],
        initial_state=HartreeFock(
            q_map[2].num_spatial_orbitals,
            q_map[2].num_particles,
            q_map[1],
        ),
    )

    vqe_solver = VQE(Estimator(), ansatz, SLSQP())
    vqe_solver.initial_point = [0.0] * ansatz.num_parameters
    print(ansatz.num_qubits, ansatz.num_parameters )
    qubit_number = ansatz.num_qubits
    
    calc = GroundStateEigensolver(q_map[1], vqe_solver)
    res = calc.solve(q_map[2])
    print(calc.solve(q_map[2]))


    groundenergy = res.groundenergy
    mu = res.dipole_moment
    return groundenergy, mu, qubit_number


# @title insert data from Gaussian
def gauss_to_xyz(gjf_file):
    matched_lines = []
    # Open the .gjf file and read lines
    with open(gjf_file, 'r') as file:
        for line in file:
            # If the line matches the regex (contains a number followed by a dot and two numbers)
            if re.search(r'[0-9]\.[0-9][0-9]', line):
                # Add the line to the list
                matched_lines.append(line.strip())

    # Prepare the name for the output .xyz file
    return gjf_file.replace('.gjf', '.xyz')

def read_xyz_file(xyz_file):
    inputfile = open(xyz_file, 'r')

    molecule = pd.read_table(inputfile, skiprows=2, sep='\s+', names=['atom', 'x', 'y', 'z'])

    df = molecule.reset_index()  # make sure indexes pair with number of rows

    temp_atom = ""
    for index, row in df.iterrows():
        temp_atom += str(row['atom']) + " " + str(row['x']) + " "+ str(row['y']) +" "+ str(row['z']) + ";"
    atom = temp_atom[:-1]
    return atom




def get_mapping(atom, charge = 0, spin = 0):


    jwmapper = JordanWignerMapper()
    pmapper = ParityMapper()
    bkmapper = BravyiKitaevMapper()

    driver = PySCFDriver(
        atom=atom,
        basis="sto3g",
        charge=charge ,
        spin=spin,
        unit=DistanceUnit.ANGSTROM,
    )

    problem = driver.run()
    second_q_op = problem.hamiltonian.second_q_op()

    if second_q_op.num_spin_orbitals <= 25:
        mapper = JordanWignerMapper()
        tapered_mapper = problem.get_tapered_mapper(mapper)
        qubit_op = tapered_mapper.map(second_q_op)
        return qubit_op , mapper, problem
    else:
        mapper = BravyiKitaevMapper()
        tapered_mapper = problem.get_tapered_mapper(mapper)
        qubit_op = tapered_mapper.map(second_q_op)

        return qubit_op, mapper, problem
    


