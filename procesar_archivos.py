from datetime import datetime
 
def procesar_clinica(fila):  # Excel
    dni = str(fila["DNI"]).strip().replace(".", "")
    if len(dni) < 7 or len(dni) > 8 or not dni.isdigit():
        return None, "DNI inválido"
    fecha = datetime.strptime(fila["Fecha"], "%d/%m/%Y")
    importe = float(fila["Importe"].replace("$", "").replace(".", "").replace(",", "."))
    return {"dni": dni, "fecha": fecha, "codigo": fila["Cod_Practica"], "importe": importe}, None
 
def procesar_laboratorio(linea):  # TXT de ancho fijo
    dni = linea[0:8].strip().replace(".", "")
    if len(dni) < 7 or len(dni) > 8 or not dni.isdigit():
        return None, "DNI inválido"
    fecha = datetime.strptime(linea[8:16], "%Y%m%d")
    importe = float(linea[24:34]) / 100
    return {"dni": dni, "fecha": fecha, "codigo": linea[16:24].strip(), "importe": importe}, None
 
def procesar_imagenes(fila):  # CSV separado por ";"
    dni = fila[1].strip().replace(".", "")
    if len(dni) < 8 or not dni.isdigit():
        return None, "DNI inválido"
    fecha = datetime.strptime(fila[0], "%d-%m-%Y")
    importe = float(fila[3].replace(",", "."))
    return {"dni": dni, "fecha": fecha, "codigo": fila[2], "importe": importe}, None
