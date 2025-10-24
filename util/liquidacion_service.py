# util/liquidacion_service.py
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import os

class LiquidacionService:
    """Servicio para generar PDFs de liquidaciones"""
    
    @staticmethod
    def generar_pdf(liquidaciones, filename=None):
        """
        Genera un PDF con las liquidaciones proporcionadas
        """
        if not filename:
            filename = f"liquidaciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = os.path.join("temp", filename)
        
        # Crear directorio temp si no existe
        os.makedirs("temp", exist_ok=True)
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#21808d'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Título
        title = Paragraph("Liquidaciones de Sueldo - Finantel Group", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Fecha
        fecha_texto = f"Fecha de emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        fecha_style = ParagraphStyle(
            'FechaStyle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(fecha_texto, fecha_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Preparar datos para la tabla
        data = [['Nombre', 'RUT', 'Cargo', 'Sueldo Base', 'Horas Extras', 'Total']]
        
        for liq in liquidaciones:
            data.append([
                liq.nombre,
                liq.rut,
                liq.cargo,
                f"${liq.sueldo_base:,.0f}",
                f"${liq.horas_extras:,.0f}",
                f"${liq.total:,.0f}"
            ])
        
        # Crear tabla
        table = Table(data, colWidths=[2*inch, 1.2*inch, 1.3*inch, 1*inch, 1*inch, 1*inch])
        
        # Estilo de la tabla
        table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#21808d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Cuerpo
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        
        # Construir PDF
        doc.build(elements)
        
        return filepath
