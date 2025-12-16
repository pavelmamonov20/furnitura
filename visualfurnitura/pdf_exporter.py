"""
PDF exporter module for VisualFurnitura
Generates PDF reports with hardware layout and specifications
"""
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from typing import Dict, List
import os
from datetime import datetime


class PDFExporter:
    def __init__(self):
        # Register a Cyrillic font if available, otherwise use built-in
        try:
            # Try to register a Cyrillic font (like DejaVu or Arial Unicode)
            pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
            self.default_font = 'DejaVu'
        except:
            # Fallback to built-in fonts that support Cyrillic
            self.default_font = 'Helvetica'

        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Center alignment
            fontName=self.default_font
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            fontSize=14,
            spaceAfter=12,
            fontName=self.default_font
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            fontSize=10,
            spaceAfter=6,
            fontName=self.default_font
        ))

    def export_visualization_report(self, output_path: str, order_data: Dict, hardware_list: List[Dict], 
                                   window_image_path: str = None):
        """
        Export a complete visualization report to PDF
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []

        # Title
        title = Paragraph("Схема установки фурнитуры", self.styles['CustomTitle'])
        story.append(title)

        # Order information
        order_info = [
            ["Информация о заказе"],
            [f"Название: {order_data.get('name', 'N/A')}"],
            [f"Описание: {order_data.get('description', 'N/A')}"],
            [f"Размеры окна: {order_data.get('window_width', 'N/A')} x {order_data.get('window_height', 'N/A')} мм"],
            [f"Дата создания: {datetime.now().strftime('%d.%m.%Y %H:%M')}"]
        ]

        order_table = Table(order_info, colWidths=[400])
        order_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(order_table)
        story.append(Spacer(1, 12))

        # Add window visualization image if available
        if window_image_path and os.path.exists(window_image_path):
            story.append(Paragraph("Схема расположения фурнитуры", self.styles['CustomHeading']))
            img = Image(window_image_path, width=6*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 12))

        # Hardware list table
        story.append(Paragraph("Перечень компонентов", self.styles['CustomHeading']))
        
        # Prepare table data
        hardware_headers = ["Артикул", "Название", "Количество", "Часть изделия", "Координаты", "Примечания"]
        hardware_data = [hardware_headers]

        for hw in hardware_list:
            row = [
                hw.get('article_number', hw.get('article', 'N/A')),
                hw.get('name', 'N/A'),
                str(hw.get('quantity', 1)),
                hw.get('part', 'N/A'),
                f"X:{hw.get('x_position', 0)}, Y:{hw.get('y_position', 0)}",
                hw.get('notes', '')
            ]
            hardware_data.append(row)

        # Create table
        hardware_table = Table(hardware_data)
        hardware_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), self.default_font),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(hardware_table)
        story.append(Spacer(1, 12))

        # Technical specifications
        story.append(Paragraph("Технические характеристики", self.styles['CustomHeading']))
        
        if 'profile_system' in order_data:
            profile_info = [
                ["Характеристика", "Значение"],
                ["Система профиля", order_data['profile_system'].get('name', 'N/A')],
                ["Описание", order_data['profile_system'].get('description', 'N/A')],
                ["Смещение оси", f"{order_data['profile_system'].get('axis_offset', 'N/A')} мм"],
                ["Толщина створки", f"{order_data['profile_system'].get('sash_thickness', 'N/A')} мм"],
                ["Ширина рамы", f"{order_data['profile_system'].get('frame_width', 'N/A')} мм"],
                ["Ширина створки", f"{order_data['profile_system'].get('sash_width', 'N/A')} мм"]
            ]
            
            profile_table = Table(profile_info)
            profile_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), self.default_font),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            story.append(profile_table)

        # Build PDF
        doc.build(story)

    def export_simple_hardware_list(self, output_path: str, hardware_list: List[Dict], 
                                   title: str = "Перечень фурнитуры"):
        """
        Export a simple list of hardware components to PDF
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []

        # Title
        title_para = Paragraph(title, self.styles['CustomTitle'])
        story.append(title_para)

        # Hardware list table
        hardware_headers = ["#", "Артикул", "Название", "Категория", "Количество", "Ед.изм.", "Примечания"]
        hardware_data = [hardware_headers]

        for idx, hw in enumerate(hardware_list, 1):
            row = [
                str(idx),
                hw.get('article_number', hw.get('article', 'N/A')),
                hw.get('name', 'N/A'),
                hw.get('category', 'N/A'),
                str(hw.get('quantity', 1)),
                "шт",  # Units
                hw.get('notes', '')
            ]
            hardware_data.append(row)

        # Create table
        hardware_table = Table(hardware_data)
        hardware_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), self.default_font),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        story.append(hardware_table)

        # Build PDF
        doc.build(story)

    def export_measurement_report(self, output_path: str, order_data: Dict, measurements: List[Dict]):
        """
        Export a measurement report with precise coordinates
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []

        # Title
        title = Paragraph("Отчет по замерам и координатам установки", self.styles['CustomTitle'])
        story.append(title)

        # Order information
        story.append(Paragraph(f"Заказ: {order_data.get('name', 'N/A')}", self.styles['CustomNormal']))
        story.append(Paragraph(f"Размеры: {order_data.get('window_width', 'N/A')} x {order_data.get('window_height', 'N/A')} мм", 
                              self.styles['CustomNormal']))
        story.append(Spacer(1, 12))

        # Measurements table
        story.append(Paragraph("Координаты установки компонентов", self.styles['CustomHeading']))

        measurement_headers = ["Артикул", "Название", "X (мм)", "Y (мм)", "Поворот (град)", "Примечания"]
        measurement_data = [measurement_headers]

        for meas in measurements:
            row = [
                meas.get('article_number', meas.get('article', 'N/A')),
                meas.get('name', 'N/A'),
                f"{meas.get('x_position', 0):.1f}",
                f"{meas.get('y_position', 0):.1f}",
                f"{meas.get('rotation', 0):.1f}",
                meas.get('notes', '')
            ]
            measurement_data.append(row)

        measurement_table = Table(measurement_data)
        measurement_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), self.default_font),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        story.append(measurement_table)

        # Build PDF
        doc.build(story)

    def create_visualization_image(self, canvas_scene, output_path: str, width: int = 800, height: int = 600):
        """
        Create an image from the visualization canvas for inclusion in PDF
        Note: This requires the actual canvas scene to be passed
        """
        # This is a placeholder - in a real implementation, this would render
        # the canvas to an image file
        pass