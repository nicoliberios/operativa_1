from flask import Blueprint, request, jsonify, render_template
import os
import matplotlib.pyplot as plt
from datetime import datetime
from inventario.inventario_solver import (
    calcular_eoq,
    calcular_rop,
    calcular_stock_seguridad,
    calcular_costo_total,
    calcular_poq
)

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/inventario', methods=['GET', 'POST'])
def inventario():
    if request.method == 'POST':
        try:
            # 📌 Recibir datos del formulario
            operacion = request.form.get('operacion')

            # 📌 Ejecutar la operación seleccionada
            resultado = {}
            if operacion == "eoq":
                demanda_anual = float(request.form.get('demanda_anual'))
                costo_pedido = float(request.form.get('costo_pedido'))
                costo_mantenimiento = float(request.form.get('costo_mantenimiento'))
                resultado = calcular_eoq(demanda_anual, costo_pedido, costo_mantenimiento)

            elif operacion == "rop":
                demanda_diaria = float(request.form.get('demanda_diaria'))
                tiempo_entrega = float(request.form.get('tiempo_entrega'))
                resultado = calcular_rop(demanda_diaria, tiempo_entrega)

            elif operacion == "stock_seguridad":
                nivel_servicio = float(request.form.get('nivel_servicio'))
                desviacion_demanda = float(request.form.get('desviacion_demanda'))
                tiempo_entrega = float(request.form.get('tiempo_entrega'))
                resultado = calcular_stock_seguridad(nivel_servicio, desviacion_demanda, tiempo_entrega)

            elif operacion == "costo_total":
                demanda_anual = float(request.form.get('demanda_anual'))
                costo_pedido = float(request.form.get('costo_pedido'))
                costo_mantenimiento = float(request.form.get('costo_mantenimiento'))
                eoq = float(request.form.get('eoq'))
                resultado = calcular_costo_total(demanda_anual, costo_pedido, costo_mantenimiento, eoq)

            elif operacion == "poq":
                demanda_anual = float(request.form.get('demanda_anual'))
                costo_pedido = float(request.form.get('costo_pedido'))
                costo_mantenimiento = float(request.form.get('costo_mantenimiento'))
                tasa_produccion = float(request.form.get('tasa_produccion'))
                tasa_demanda = float(request.form.get('tasa_demanda'))
                resultado = calcular_poq(demanda_anual, costo_pedido, costo_mantenimiento, tasa_produccion, tasa_demanda)

            else:
                return jsonify({"error": "Operación no válida"}), 400

            # 📌 Generar y guardar gráfico en app/static/graphs/
            img_path = os.path.join("app", "static", "graphs", "inventario.png")
            os.makedirs(os.path.dirname(img_path), exist_ok=True)

            fig, ax = plt.subplots()
            ax.bar([operacion.upper()], [list(resultado.values())[0]], color='blue')
            ax.set_ylabel("Valor Calculado")
            ax.set_title(f"Resultado de {operacion.upper()}")

            plt.savefig(img_path)
            plt.close()

            return render_template("resultado_inventario.html", resultado=resultado, now=datetime.now())

        except Exception as e:
            return jsonify({"error": str(e)})

    return render_template('inventario.html')
