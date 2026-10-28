from datetime import datetime
from .helpers import es_dni_valido, formatear_fecha, formatear_importe

class RepositorioAfiliados: # Consulta estados de cobertura y devuelve el estado y el tope.
    def __init__(self, base_datos):
        self.base_datos = base_datos

    def obtener_datos_cobertura(self, dni):
        afiliado = self.base_datos.buscar(dni)
        cobertura = afiliado.plan.cobertura

        return {
            "estado": cobertura.estado,
            "tope": cobertura.topes[0]
        }

class ServicioNotificaciones: # Se encarga de enviar emails.
    EMAIL_AUDITORIA = "auditoria@obrasocial.com"

    def __init__(self, mail):
       self.mail = mail

    def enviar_reporte(self, cantidad_registros):
       self.mail.enviar(self.EMAIL_AUDITORIA, str(cantidad_registros))


class ServicioPDF: # Genera el PDF.
    def __init__(self, pdf):
        self.pdf = pdf

    def generar_reporte(self, resultados):
        self.pdf.generar(resultados)

class GestorFacturacion: # Aplica las reglas de facturación.

    DIAS_MAXIMOS_ANTIGUEDAD = 60
    ESTADO_AFILIADO_BAJA = 2
    FORMATO_LISTA = 1
    FORMATO_FECHA = "%d/%m/%Y"
    
    def __init__(self, repositorio, notificaciones, servicio_pdf):
        self.repositorio = repositorio
        self.notificaciones = notificaciones
        self.servicio_pdf = servicio_pdf

    def procesar_facturación(self, datos, tipo_formato): # tipo_formato indica cómo estan organizados los datos de entrada de cada afiliado (para acceder a lo necesario). 
        resultados = []

        for registro in datos:
            dni = self.obtener_dni(registro, tipo_formato)

            if not es_dni_valido(dni):
                continue

            fecha = formatear_fecha(registro[0], self.FORMATO_FECHA)
            if self.es_fecha_antigua(fecha):
                continue

            datos_cobertura = self.repositorio.obetener_datos_cobertura(dni)

            if datos_cobertura["estado"] == self.ESTADO_AFILIADO_BAJA:
                continue

            tope = datos_cobertura["tope"]
            importe_facturado = formatear_importe(registro[3])
            
            if importe_facturado < tope:
                importe_reconocido = importe_facturado
            else:
                importe_reconocido = tope

            resultado = [dni, fecha, registro[2], importe_reconocido]
            resultados.append(resultado)

            self.enviar_mail(len(resultados))
            self.generar_pdf(resultados)

    def obtener_dni(self, registro, tipo_formato):
        if tipo_formato == self.FORMATO_LISTA:
            dni = registro[1]
        else:
            dni = registro["DNI"]

        return dni.replace(".", "")

    def es_fecha_antigua(self, fecha):
        return (
            (datetime.now() - fecha).days > self.DIAS_MAXIMOS_ANTIGUEDAD
        )

    def enviar_mail(self, cantidad_registros):
        self.notificaciones.enviar_reporte(cantidad_registros)

    def generar_pdf(self, resultados):
        self.servicio_pdf.generar_reporte(resultados)