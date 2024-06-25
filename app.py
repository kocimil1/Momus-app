from flask import Flask, render_template, jsonify, request
import quantumFunctions

app = Flask(__name__)

#filename = 'data/h2o.xyz'
#filename = 'data/hydrogen_molecule.xyz'
filename = 'data/paracetamol.xyz'


@app.route('/startComputing', methods=['POST', 'GET', 'HEAD', 'OPTIONS'])
def startComputing():
    E, mu, qubit_number = quantumFunctions.startComputing()
    E = round(E, 3)
    # Předpokládáme, že mu je ve formátu [(0.0,0.0,0.0)]
    mu_tuple = mu[0]  # Extrahujeme tuple
    # Zaokrouhlíme každé číslo v tuple
    mu_rounded = tuple(round(num, 3) for num in mu_tuple)
    # Převedeme zaokrouhlený tuple na řetězec
    mu_str = f"({mu_rounded[0]},{mu_rounded[1]},{mu_rounded[2]})"
    return jsonify({"E": str(E), "mu": mu_str, "qubit_number": qubit_number})


@app.route('/loadFile', methods=['POST', 'GET', 'HEAD', 'OPTIONS'])
def loadFile():
    
    # Získání JSON dat z POST requestu
    data = request.get_json()
    quantumFunctions.loadFile("data/"+data)
    E = "-"  # Příklad hodnoty energie
    mu = "-"  # Příklad hodnoty dipólového momentu
    filename = "data/"+data
    with open(filename, 'r') as file:
        xyz_data = file.read()
    molecule_html = quantumFunctions.get_molecule_html(xyz_data)
    return (render_template('index.html', molecule_html=molecule_html, E=E, mu=mu))



@app.route('/')
def index():
    with open(filename, 'r') as file:
        xyz_data = file.read()
    
    E = "-"  # Příklad hodnoty energie
    mu = "-"  # Příklad hodnoty dipólového momentu
    qubit_number = '-'

    molecule_html = quantumFunctions.get_molecule_html(xyz_data)

    return render_template('index.html', molecule_html=molecule_html, E=E, mu=mu, qubit_number=qubit_number)


if __name__ == '__main__':
    app.run(debug=True)