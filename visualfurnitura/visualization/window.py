"""
Main visualization window for VisualFurnitura
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QMenuBar, QStatusBar, QToolBar, QDockWidget, 
                            QTreeWidget, QTreeWidgetItem, QLabel, QSpinBox,
                            QPushButton, QComboBox, QGroupBox, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon
from .canvas import VisualizationCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisualFurnitura - Программа визуализации установки фурнитуры")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create visualization canvas
        self.canvas = VisualizationCanvas()
        
        # Create left sidebar for controls
        self.sidebar = self.create_sidebar()
        
        # Create right panel for properties
        self.properties_panel = self.create_properties_panel()
        
        # Add widgets to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.canvas, stretch=1)
        main_layout.addWidget(self.properties_panel)
        
        # Create menus and toolbars
        self.create_menus()
        self.create_toolbar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово")

    def create_sidebar(self):
        """Create the left sidebar with controls"""
        sidebar = QFrame()
        sidebar.setMinimumWidth(250)
        sidebar.setMaximumWidth(300)
        layout = QVBoxLayout(sidebar)
        
        # Layers group
        layers_group = QGroupBox("Слои")
        layers_layout = QVBoxLayout(layers_group)
        
        self.layers_tree = QTreeWidget()
        self.layers_tree.setHeaderLabel("Отображаемые элементы")
        self.layers_tree.addTopLevelItem(QTreeWidgetItem(["Фурнитура"]))
        self.layers_tree.addTopLevelItem(QTreeWidgetItem(["Крепления"]))
        self.layers_tree.addTopLevelItem(QTreeWidgetItem(["Габариты"]))
        self.layers_tree.addTopLevelItem(QTreeWidgetItem(["Текст"]))
        
        layers_layout.addWidget(self.layers_tree)
        
        # Zoom controls
        zoom_group = QGroupBox("Масштаб")
        zoom_layout = QVBoxLayout(zoom_group)
        
        self.zoom_spinbox = QSpinBox()
        self.zoom_spinbox.setRange(10, 500)
        self.zoom_spinbox.setValue(100)
        self.zoom_spinbox.setSuffix("%")
        self.zoom_spinbox.valueChanged.connect(self.on_zoom_changed)
        
        zoom_layout.addWidget(QLabel("Масштаб:"))
        zoom_layout.addWidget(self.zoom_spinbox)
        
        # Add buttons
        btn_load_pdf = QPushButton("Загрузить PDF задание")
        btn_load_pdf.clicked.connect(self.load_pdf_task)
        
        btn_export_pdf = QPushButton("Экспортировать в PDF")
        btn_export_pdf.clicked.connect(self.export_to_pdf)
        
        layout.addWidget(layers_group)
        layout.addWidget(zoom_group)
        layout.addWidget(btn_load_pdf)
        layout.addWidget(btn_export_pdf)
        layout.addStretch()
        
        return sidebar

    def create_properties_panel(self):
        """Create the right properties panel"""
        panel = QFrame()
        panel.setMinimumWidth(250)
        panel.setMaximumWidth(300)
        layout = QVBoxLayout(panel)
        
        # Component properties group
        props_group = QGroupBox("Свойства компонента")
        props_layout = QVBoxLayout(props_group)
        
        self.component_info = QLabel("Выберите компонент для просмотра свойств")
        self.component_info.setWordWrap(True)
        self.component_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        props_layout.addWidget(self.component_info)
        
        # Profile system selection
        profile_group = QGroupBox("Система профиля")
        profile_layout = QVBoxLayout(profile_group)
        
        self.profile_combo = QComboBox()
        self.profile_combo.addItem("Выберите систему профиля")
        self.profile_combo.addItem("Aluplast Ideal-2000")
        self.profile_combo.addItem("Rehau Geneva")
        self.profile_combo.addItem("KBE Evolution")
        self.profile_combo.currentTextChanged.connect(self.on_profile_changed)
        
        profile_layout.addWidget(self.profile_combo)
        
        layout.addWidget(props_group)
        layout.addWidget(profile_group)
        layout.addStretch()
        
        return panel

    def create_menus(self):
        """Create application menus"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("Файл")
        
        action_new = QAction("Новый проект", self)
        action_new.setShortcut("Ctrl+N")
        action_new.triggered.connect(self.new_project)
        file_menu.addAction(action_new)
        
        action_open = QAction("Открыть проект", self)
        action_open.setShortcut("Ctrl+O")
        action_open.triggered.connect(self.open_project)
        file_menu.addAction(action_open)
        
        action_save = QAction("Сохранить проект", self)
        action_save.setShortcut("Ctrl+S")
        action_save.triggered.connect(self.save_project)
        file_menu.addAction(action_save)
        
        file_menu.addSeparator()
        
        action_exit = QAction("Выход", self)
        action_exit.setShortcut("Ctrl+Q")
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)
        
        # View menu
        view_menu = menu_bar.addMenu("Вид")
        
        action_zoom_in = QAction("Увеличить", self)
        action_zoom_in.setShortcut("Ctrl++")
        action_zoom_in.triggered.connect(self.canvas.zoom_in)
        view_menu.addAction(action_zoom_in)
        
        action_zoom_out = QAction("Уменьшить", self)
        action_zoom_out.setShortcut("Ctrl+-")
        action_zoom_out.triggered.connect(self.canvas.zoom_out)
        view_menu.addAction(action_zoom_out)
        
        action_reset_zoom = QAction("Сбросить масштаб", self)
        action_reset_zoom.setShortcut("Ctrl+0")
        action_reset_zoom.triggered.connect(self.canvas.reset_zoom)
        view_menu.addAction(action_reset_zoom)

    def create_toolbar(self):
        """Create application toolbar"""
        toolbar = self.addToolBar("Основная панель инструментов")
        
        # Add actions to toolbar
        action_zoom_in = QAction("Увеличить", self)
        action_zoom_in.triggered.connect(self.canvas.zoom_in)
        toolbar.addAction(action_zoom_in)
        
        action_zoom_out = QAction("Уменьшить", self)
        action_zoom_out.triggered.connect(self.canvas.zoom_out)
        toolbar.addAction(action_zoom_out)
        
        action_reset_zoom = QAction("Сброс", self)
        action_reset_zoom.triggered.connect(self.canvas.reset_zoom)
        toolbar.addAction(action_reset_zoom)

    def on_zoom_changed(self, value):
        """Handle zoom level changes"""
        self.canvas.set_scale(value / 100.0)
        self.status_bar.showMessage(f"Масштаб: {value}%")

    def load_pdf_task(self):
        """Load PDF task and visualize hardware placement"""
        # This would normally open a file dialog and load a PDF
        self.status_bar.showMessage("Загрузка PDF задания...")
        # For now, just simulate loading
        self.canvas.load_sample_data()
        self.status_bar.showMessage("PDF задание загружено")

    def export_to_pdf(self):
        """Export visualization to PDF"""
        self.status_bar.showMessage("Экспорт в PDF...")

    def on_profile_changed(self, text):
        """Handle profile system changes"""
        if text != "Выберите систему профиля":
            self.status_bar.showMessage(f"Выбрана система профиля: {text}")

    def new_project(self):
        """Create a new project"""
        self.canvas.clear_scene()
        self.status_bar.showMessage("Новый проект создан")

    def open_project(self):
        """Open an existing project"""
        self.status_bar.showMessage("Открытие проекта...")

    def save_project(self):
        """Save the current project"""
        self.status_bar.showMessage("Проект сохранен")