import math

def calcular_eoq(demanda_anual, costo_pedido, costo_mantenimiento):
    """
    Calcula la Cantidad Económica de Pedido (EOQ).
    
    :param demanda_anual: Demanda anual del producto
    :param costo_pedido: Costo de realizar un pedido
    :param costo_mantenimiento: Costo de mantenimiento por unidad por año
    :return: EOQ (Cantidad óptima de pedido)
    """
    try:
        eoq = math.sqrt((2 * demanda_anual * costo_pedido) / costo_mantenimiento)
        return {"eoq": round(eoq, 2)}
    except ZeroDivisionError:
        return {"error": "El costo de mantenimiento no puede ser cero"}
    except Exception as e:
        return {"error": str(e)}

# ✅ Prueba rápida
if __name__ == "__main__":
    resultado = calcular_eoq(demanda_anual=5000, costo_pedido=100, costo_mantenimiento=5)
    print("🔹 Resultado de prueba:", resultado)
