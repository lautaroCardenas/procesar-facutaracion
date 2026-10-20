from datetime import datetime

def es_dni_valido(dni):
    if len(dni) < 7 or len(dni) > 8 or not dni.isdigit():
        return False
    return True

def formatear_fecha(fecha, formato_origen):
    fechaNueva = datetime.strptime(fecha, formato_origen)
    return fechaNueva

def formatear_importe(importe, divisor=1): # Si el número no viene con ',' o '.' para indicar su parte decimal, se agrega un divisor por 100.
    if importe is None:
        return 0.0
    if isinstance(importe, (int, float)):
        return float(importe) / divisor

    importe_str = str(importe).strip().replace("$", "")
    if not importe_str:
        return 0.0

    if "." in importe_str and "," in importe_str:
        importe_str = importe_str.replace(".", "").replace(",", ".")
    elif "," in importe_str:
        importe_str = importe_str.replace(",", ".")
    return float(importe_str) / divisor    