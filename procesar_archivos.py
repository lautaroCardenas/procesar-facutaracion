from datetime import datetime
from helpers import es_dni_valido, formatear_fecha, formatear_importe   
 
def procesar_clinica(fila):  # Excel
    dni = str(fila["DNI"]).strip().replace(".", "")
    if not es_dni_valido(dni):
        return None, "DNI inválido"
    fecha = formatear_fecha(fila["Fecha"], "%d/%m/%Y")
    importe = formatear_importe(fila["Importe"])
    return {"dni": dni, "fecha": fecha, "codigo": fila["Cod_Practica"], "importe": importe}, None
 
def procesar_laboratorio(linea):  # TXT de ancho fijo
    dni = linea[0:8].strip().replace(".", "")
    if not es_dni_valido(dni):
        return None, "DNI inválido"
    fecha = formatear_fecha(linea[8:16], "%Y%m%d")
    importe = formatear_importe(linea[24:34], divisor=100)
    return {"dni": dni, "fecha": fecha, "codigo": linea[16:24].strip(), "importe": importe}, None
 
def procesar_imagenes(fila):  # CSV separado por ";"
    dni = fila[1].strip().replace(".", "")
    if not es_dni_valido(dni):
        return None, "DNI inválido"
    fecha = formatear_fecha(fila[0], "%d-%m-%Y")
    importe = formatear_importe(fila[3])
    return {"dni": dni, "fecha": fecha, "codigo": fila[2], "importe": importe}, None
