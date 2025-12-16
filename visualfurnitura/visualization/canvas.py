"""
Visualization canvas for VisualFurnitura
Handles 2D rendering of window hardware layout
"""
from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsPixmapItem, QFrame
from PyQt6.QtCore import Qt, QPointF, QRectF, QPoint
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen, QFont, QPixmap
from typing import List, Dict, Optional


class VisualizationCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        
        # Set up the graphics scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Set view properties
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # Enable panning by holding mouse
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Initialize scale and translation
        self.scale_factor = 1.0
        self.translation_x = 0
        self.translation_y = 0
        
        # Store hardware items
        self.hardware_items = []
        self.window_outline = None
        
        # Initialize sample scene
        self.setup_default_scene()

    def setup_default_scene(self):
        """Set up a default scene with a window outline"""
        # Clear existing items
        self.scene.clear()
        
        # Draw a default window outline (1500x1000 mm scaled down)
        window_width = 1500  # mm
        window_height = 1000  # mm
        
        # Scale down for display (1 unit = 1 mm initially)
        scale_factor = 0.2  # 1 pixel = 5 mm
        display_width = window_width * scale_factor
        display_height = window_height * scale_factor
        
        # Create window outline
        self.window_outline = self.scene.addRect(
            0, 0, 
            display_width, 
            display_height,
            QPen(QColor(0, 0, 0), 2),
            QBrush(QColor(240, 240, 240, 100))
        )
        
        # Add title
        title = self.scene.addText("Схема установки фурнитуры", QFont("Arial", 14))
        title.setPos(10, 10)
        
        # Add dimensions text
        dims_text = self.scene.addText(f"Размеры: {window_width}x{window_height} мм", QFont("Arial", 10))
        dims_text.setPos(10, 40)

    def load_sample_data(self):
        """Load sample hardware data for demonstration"""
        # Clear existing hardware items
        for item in self.hardware_items:
            self.scene.removeItem(item)
        self.hardware_items = []
        
        # Sample hardware positions (in mm from top-left corner)
        sample_hardware = [
            {"name": "Петля верхняя", "article": "H-001", "x": 50, "y": 50, "width": 30, "height": 100, "color": QColor(255, 0, 0)},
            {"name": "Петля нижняя", "article": "H-002", "x": 50, "y": 950, "width": 30, "height": 100, "color": QColor(255, 0, 0)},
            {"name": "Ручка", "article": "H-003", "x": 700, "y": 500, "width": 120, "height": 40, "color": QColor(0, 0, 255)},
            {"name": "Замок", "article": "H-004", "x": 1400, "y": 500, "width": 80, "height": 80, "color": QColor(0, 128, 0)},
            {"name": "Микролифт", "article": "H-005", "x": 700, "y": 100, "width": 60, "height": 20, "color": QColor(255, 165, 0)},
            {"name": "Отлив", "article": "H-006", "x": 0, "y": 980, "width": 1500, "height": 20, "color": QColor(139, 69, 19)},  # Brown
        ]
        
        # Add sample hardware to scene
        scale_factor = 0.2  # Convert mm to pixels
        
        for hw in sample_hardware:
            # Calculate display position and size
            x_pos = hw["x"] * scale_factor
            y_pos = hw["y"] * scale_factor
            width = hw["width"] * scale_factor
            height = hw["height"] * scale_factor
            
            # Create rectangle for hardware component
            rect_item = self.scene.addRect(
                x_pos, y_pos, 
                width, height,
                QPen(hw["color"], 1),
                QBrush(hw["color"].lighter(150))
            )
            
            # Add label
            label = self.scene.addText(f"{hw['name']} ({hw['article']})", QFont("Arial", 8))
            label.setDefaultTextColor(QColor(0, 0, 0))
            label.setPos(x_pos, y_pos - 15)  # Position above the rectangle
            
            # Store references to manage these items
            self.hardware_items.append(rect_item)
            self.hardware_items.append(label)
            
            # Add tooltip with detailed information
            rect_item.setToolTip(f"Артикул: {hw['article']}\nНазвание: {hw['name']}\nКоординаты: ({hw['x']}, {hw['y']}) мм")

    def clear_scene(self):
        """Clear all items from the scene"""
        self.scene.clear()
        self.setup_default_scene()

    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming"""
        # Get the current mouse position in scene coordinates
        mouse_pos_before = self.mapToScene(event.position().toPoint())
        
        # Determine zoom factor
        zoom_factor = 1.2 if event.angleDelta().y() > 0 else 1/1.2
        
        # Apply zoom
        self.scale(zoom_factor, zoom_factor)
        
        # Adjust scroll bars to keep mouse position fixed
        mouse_pos_after = self.mapToScene(event.position().toPoint())
        delta = mouse_pos_after - mouse_pos_before
        
        self.translate(delta.x(), delta.y())
        
        # Update scale factor
        self.scale_factor *= zoom_factor
        self.update()

    def set_scale(self, scale: float):
        """Set the scale of the view"""
        # Calculate the scale factor needed to reach the target scale
        current_transform = self.transform()
        current_scale = current_transform.m11()  # Assuming uniform scaling
        
        target_scale = scale
        scale_factor = target_scale / current_scale
        
        self.scale(scale_factor, scale_factor)
        self.scale_factor = scale

    def zoom_in(self):
        """Zoom in on the canvas"""
        self.scale(1.2, 1.2)
        self.scale_factor *= 1.2

    def zoom_out(self):
        """Zoom out on the canvas"""
        self.scale(1/1.2, 1/1.2)
        self.scale_factor /= 1.2

    def reset_zoom(self):
        """Reset zoom to default"""
        # Reset transform
        self.resetTransform()
        self.scale_factor = 1.0
        self.setup_default_scene()
        self.load_sample_data()