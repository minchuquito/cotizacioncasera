from flask import Flask, jsonify
from flask import render_template
from flask import render_template_string
import requests
import json

app = Flask(__name__)

@app.route('/')
def getTemplate():
    return render_template('index.html')


@app.route('/cotizacion/<string:monedas>', methods=['GET'])
def getCotizacion(monedas):
    bandera = False
    if monedas.lower()=='euro':
        bandera = True
        r = requests.get('https://api.cambio.today/v1/quotes/EUR/ARS/json?quantity=1&key=4503|g30ynND6wzAhLV_~6Ekye7xfCngn78gY')

    if monedas.lower()=='dolar':
        bandera = True
        r = requests.get('https://api.cambio.today/v1/quotes/USD/ARS/json?quantity=1&key=4503|g30ynND6wzAhLV_~6Ekye7xfCngn78gY')

    if monedas.lower()=='real':
        bandera = True
        r = requests.get('https://api.cambio.today/v1/quotes/BRL/ARS/json?quantity=1&key=4503|g30ynND6wzAhLV_~6Ekye7xfCngn78gY')

    if(len(monedas)>0 and bandera == False):
        return jsonify({"mensaje": "Moneda no Disponible pruebe con /cotizaciones/todas/ABREVIATURA"})
    else:
        
        r = r.json()
        precio = r['result']['amount']

        cabecera = '''{% extends "layout.html" %}
                        {% block content %}'''
        fin = '''{% endblock %}'''

        cuerpo = '''
                    <table class="table">
                        <thead class="thead-dark">
                            <tr>
                            <th scope="col">Moneda</th>
                            <th scope="col">Precio en ARS</th>    
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td> %1 </td>
                                <td> %2 </td>
                            </tr>
                        </tbody>
                    </table>'''

        cuerpo = cuerpo.replace("%1", str(monedas)) 
        cuerpo = cuerpo.replace("%2", str(precio))    
        
        #return jsonify({"precio": precio, "moneda": monedas})
        return render_template_string(cabecera+cuerpo+fin)
    
    


'''
#   Conseguir cotizaciones que no sean dolar, real o euro
@app.route('/cotizaciones/todas/<string:abreviatura>')
def getTodas(abreviatura):
    r = requests.get('https://api.cambio.today/v1/quotes/'+abreviatura.upper()+'/ARS/json?quantity=1&key=4503|g30ynND6wzAhLV_~6Ekye7xfCngn78gY')
    r = r.json()
    precio = r['result']['amount']
    #moneda = r['result']['source']

    response = [
        #{"abreviatua": moneda, "precio": precio, "moneda": monedas}
        {"precio": precio, "moneda": abreviatura.upper()}
    ]
    return jsonify({"precio": precio, "moneda": abreviatura.upper()})
'''


if __name__ == '__main__':
    app.run(debug=True)