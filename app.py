from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = int(request.form['idade'])
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        objetivo = request.form['objetivo']

        calorias = 2200 if objetivo == 'emagrecer' else 2600
        proteinas_g = round(peso * 2.2)
        gorduras_g = 70
        carboidratos_g = (calorias - (proteinas_g * 4 + gorduras_g * 9)) // 4

        plano = pd.DataFrame({
            "Refeição": ["Café da manhã", "Almoço", "Jantar"],
            "Alimentos sugeridos": [
                "6 claras + 2 ovos + aveia + banana",
                "Frango + arroz integral + legumes + azeite",
                "Carne magra + legumes variados + azeite"
            ],
            "Objetivo": [
                "Energia e proteína no café",
                "Refeição principal equilibrada",
                "Leve com nutrientes importantes"
            ]
        })

        path = f"./{nome}_plano.xlsx"
        plano.to_excel(path, index=False)

        return render_template('plano.html', nome=nome, calorias=calorias,
                               proteinas=proteinas_g, gorduras=gorduras_g,
                               carboidratos=carboidratos_g, arquivo=path)

    return render_template('cadastro.html')

@app.route('/download/<arquivo>')
def download(arquivo):
    return send_file(arquivo, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
