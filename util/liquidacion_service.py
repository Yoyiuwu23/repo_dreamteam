# util/liquidacion_service.py
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

class LiquidacionService:
    """Servicio para generar PDFs de liquidaciones"""
    
    @staticmethod
    def generar_pdf(liquidaciones, filename=None):
        """
        Genera un PDF con la liquidación de sueldo en formato chileno
        """
        if not filename:
            filename = f"liquidaciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = os.path.join("temp", filename)
        os.makedirs("temp", exist_ok=True)
        
        # Configuración del documento
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        titulo_style = ParagraphStyle(
            'TituloStyle',
            parent=styles['Heading1'],
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        subtitulo_style = ParagraphStyle(
            'SubtituloStyle',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        seccion_style = ParagraphStyle(
            'SeccionStyle',
            parent=styles['Heading2'],
            fontSize=10,
            alignment=TA_LEFT,
            spaceBefore=15,
            spaceAfter=8
        )
        
        # Datos de ejemplo para una liquidación (usar el primero de la lista)
        liq = liquidaciones[0]
        
        # Encabezado con logo y datos de la empresa
        datos_header = [
            ['', 'Finantel Group'],
            ['', 'RUT: 76.XXX.XXX-X'],
            ['', 'Av. Ejemplo 123, Santiago']
        ]
        # Obtener la ruta absoluta del logo
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'assets', 'img', 'logo.png')
        if os.path.exists(logo_path):
            from reportlab.platypus import Image
            logo = Image(logo_path, width=2*cm, height=2*cm)
            datos_header[0][0] = logo
        
        tabla_header = Table(datos_header, colWidths=[3*cm, 15*cm])
        tabla_header.setStyle(TableStyle([
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (1, 0), 14),  # Nombre de empresa más grande
            ('FONTSIZE', (1, 1), (1, -1), 10),  # Resto del texto más pequeño
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),  # Centrar logo verticalmente
            ('SPAN', (0, 0), (0, -1)),  # Fusionar celdas del logo
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
        ]))
        elements.append(tabla_header)
        elements.append(Spacer(1, 0.2*inch))
        
        # Información del trabajador
        elements.append(Paragraph("ANTECEDENTES DEL EMPLEADO", seccion_style))
        datos_trabajador = [
            ['Nombre', f"{liq.nombre}"],
            ['RUT', f"{liq.rut}"],
            ['Cargo', f"{liq.cargo}"],
            ['Días Trabajados', f"{getattr(liq, 'dias_trabajados', 30)}"]
        ]
        tabla_trabajador = Table(datos_trabajador, colWidths=[4*cm, 14*cm])
        tabla_trabajador.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ]))
        elements.append(tabla_trabajador)
        
        # Detalle de remuneración
        elements.append(Paragraph("HABERES", seccion_style))
        haberes = [
            ['CONCEPTO', 'MONTO'],
            ['Sueldo Base', f"${liq.sueldo_base:,.0f}"],
            ['Horas Extras', f"${getattr(liq, 'horas_extras_monto', 0.0):,.0f}"],
            ['Gratificación', f"${getattr(liq, 'gratificacion', 0.0):,.0f}"]
        ]
        tabla_haberes = Table(haberes, colWidths=[12*cm, 6*cm])
        tabla_haberes.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(tabla_haberes)
        
        # Descuentos previsionales
        elements.append(Paragraph("DESCUENTOS PREVISIONALES", seccion_style))
        descuentos = [
            ['CONCEPTO', 'MONTO'],
            ['AFP', f"${getattr(liq, 'afp_monto', 0.0):,.0f}"],
            ['AFC', f"${getattr(liq, 'afc_monto', 0.0):,.0f}"],
            ['Salud', f"${getattr(liq, 'salud_monto', 0.0):,.0f}"]
            
        ]
        tabla_descuentos = Table(descuentos, colWidths=[12*cm, 6*cm])
        tabla_descuentos.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(tabla_descuentos)
        
        # Total y líquido
        total_imponible = getattr(liq, 'total_imponible', round(liq.sueldo_base + getattr(liq, 'horas_extras_monto', 0.0), 2))
        total_descuentos = getattr(liq, 'total_descuentos', round(getattr(liq, 'afp_monto', 0.0) + getattr(liq, 'salud_monto', 0.0) + getattr(liq, 'afc_monto', 0.0), 2))
        liquido = getattr(liq, 'liquido', round(total_imponible - total_descuentos, 2))

        totales = [
            ['TOTAL IMPONIBLE', f"${total_imponible:,.0f}"],
            ['TOTAL DESCUENTOS', f"${total_descuentos:,.0f}"],
            ['ALCANCE LÍQUIDO', f"${liquido:,.0f}"]
        ]
        tabla_totales = Table(totales, colWidths=[12*cm, 6*cm])
        tabla_totales.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
        ]))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(tabla_totales)
        
        
        # Construir PDF
        doc.build(elements)
        return filepath
