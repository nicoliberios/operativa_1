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

def calcular_rop(demanda_diaria, tiempo_entrega):
    """
    Calcula el Punto de Reorden (ROP).
    
    :param demanda_diaria: Demanda promedio diaria
    :param tiempo_entrega: Tiempo de entrega en días
    :return: ROP (Punto de Reorden)
    """
    try:
        rop = demanda_diaria * tiempo_entrega
        return {"rop": round(rop, 2)}
    except Exception as e:
        return {"error": str(e)}

def calcular_stock_seguridad(nivel_servicio, desviacion_demanda, tiempo_entrega):
    """
    Calcula el Stock de Seguridad basado en nivel de servicio y variabilidad de la demanda.
    
    :param nivel_servicio: Factor Z de nivel de servicio (ej. 1.65 para 95%)
    :param desviacion_demanda: Desviación estándar de la demanda
    :param tiempo_entrega: Tiempo de entrega en días
    :return: Stock de Seguridad
    """
    try:
        stock_seguridad = nivel_servicio * desviacion_demanda * math.sqrt(tiempo_entrega)
        return {"stock_seguridad": round(stock_seguridad, 2)}
    except Exception as e:
        return {"error": str(e)}

def calcular_costo_total(demanda_anual, costo_pedido, costo_mantenimiento, eoq):
    """
    Calcula el Costo Total de Inventario (Costo de pedidos + Costo de mantenimiento).
    
    :param demanda_anual: Demanda anual del producto
    :param costo_pedido: Costo de realizar un pedido
    :param costo_mantenimiento: Costo de mantenimiento por unidad por año
    :param eoq: Cantidad Económica de Pedido (EOQ)
    :return: Costo Total de Inventario
    """
    try:
        num_pedidos = demanda_anual / eoq
        costo_pedidos = num_pedidos * costo_pedido
        costo_mantenimiento_total = (eoq / 2) * costo_mantenimiento
        costo_total = costo_pedidos + costo_mantenimiento_total
        return {"costo_total": round(costo_total, 2)}
    except Exception as e:
        return {"error": str(e)}

def calcular_poq(demanda_anual, costo_pedido, costo_mantenimiento, tasa_produccion, tasa_demanda):
    """
    Calcula la Cantidad Óptima de Producción (POQ).
    
    :param demanda_anual: Demanda anual del producto
    :param costo_pedido: Costo de realizar un pedido
    :param costo_mantenimiento: Costo de mantenimiento por unidad por año
    :param tasa_produccion: Tasa de producción diaria
    :param tasa_demanda: Tasa de demanda diaria
    :return: POQ (Cantidad Óptima de Producción)
    """
    try:
        poq = math.sqrt((2 * demanda_anual * costo_pedido) / (costo_mantenimiento * (1 - (tasa_demanda / tasa_produccion))))
        return {"poq": round(poq, 2)}
    except ZeroDivisionError:
        return {"error": "La tasa de producción debe ser mayor que la tasa de demanda"}
    except Exception as e:
        return {"error": str(e)}

# ✅ Pruebas rápidas
if __name__ == "__main__":
    print("🔹 Prueba de EOQ:", calcular_eoq(demanda_anual=5000, costo_pedido=100, costo_mantenimiento=5))
    print("🔹 Prueba de ROP:", calcular_rop(demanda_diaria=50, tiempo_entrega=5))
    print("🔹 Prueba de Stock de Seguridad:", calcular_stock_seguridad(nivel_servicio=1.65, desviacion_demanda=20, tiempo_entrega=5))
    print("🔹 Prueba de Costo Total:", calcular_costo_total(demanda_anual=5000, costo_pedido=100, costo_mantenimiento=5, eoq=200))
    print("🔹 Prueba de POQ:", calcular_poq(demanda_anual=5000, costo_pedido=100, costo_mantenimiento=5, tasa_produccion=100, tasa_demanda=50))
