from flask import Blueprint, request, jsonify, render_template
import os
import matplotlib.pyplot as plt
from datetime import datetime
from inventario.inventario_solver import calcular_eoq

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/inventario', methods=['GET', 'POST'])
def inventario():
    if request.method == 'POST':
        try:
            # 📌 Recibir datos del formulario
            demanda_anual = float(request.form.get('demanda_anual'))
            costo_pedido = float(request.form.get('costo_pedido'))
            costo_mantenimiento = float(request.form.get('costo_mantenimiento'))

            # 📌 Calcular EOQ
            resultado = calcular_eoq(demanda_anual, costo_pedido, costo_mantenimiento)

            # 📌 Generar y guardar gráfico en app/static/graphs/
            img_path = os.path.join("app", "static", "graphs", "inventario.png")
            os.makedirs(os.path.dirname(img_path), exist_ok=True)

            fig, ax = plt.subplots()
            ax.bar(["EOQ"], [resultado.get("eoq", 0)], color='blue')
            ax.set_ylabel("Cantidad Óptima de Pedido (EOQ)")
            ax.set_title("Optimización de Inventario")

            plt.savefig(img_path)
            plt.close()

            return render_template("resultado_inventario.html", resultado=resultado, now=datetime.now())

        except Exception as e:
            return jsonify({"error": str(e)})

    return render_template('inventario.html')
