"""
Hardware administration module for VisualFurnitura
Provides GUI for managing hardware components
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QDialog, QTableWidget, QTableWidgetItem, QHeaderView,
                            QLineEdit, QTextEdit, QPushButton, QComboBox, 
                            QDoubleSpinBox, QSpinBox, QFileDialog, QMessageBox,
                            QTabWidget, QGroupBox, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import json
import os
from ..db_manager import DBManager


class HardwareAdminDialog(QDialog):
    def __init__(self, db_manager: DBManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Администрирование фурнитуры")
        self.setGeometry(200, 200, 1000, 700)
        
        self.layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Hardware management tab
        self.hardware_tab = self.create_hardware_tab()
        self.tab_widget.addTab(self.hardware_tab, "Фурнитура")
        
        # Profile systems tab
        self.profiles_tab = self.create_profiles_tab()
        self.tab_widget.addTab(self.profiles_tab, "Системы профиля")
        
        self.layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("Обновить")
        self.btn_close = QPushButton("Закрыть")
        
        self.btn_refresh.clicked.connect(self.refresh_tables)
        self.btn_close.clicked.connect(self.accept)
        
        button_layout.addWidget(self.btn_refresh)
        button_layout.addWidget(self.btn_close)
        
        self.layout.addLayout(button_layout)
        
        # Load initial data
        self.refresh_tables()

    def create_hardware_tab(self):
        """Create the hardware management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Create form for adding/editing hardware
        form_group = QGroupBox("Добавить/Редактировать компонент")
        form_layout = QFormLayout(form_group)
        
        # Form fields
        self.le_article = QLineEdit()
        self.le_name = QLineEdit()
        self.cb_category = QComboBox()
        self.cb_category.addItems(["Петли", "Ручки", "Замки", "Углы", "Отливы", "Микролифты", "Прочее"])
        self.te_description = QTextEdit()
        self.le_image_path = QLineEdit()
        self.btn_browse_image = QPushButton("Обзор...")
        
        self.sb_width = QDoubleSpinBox()
        self.sb_width.setRange(0, 10000)
        self.sb_width.setSuffix(" мм")
        
        self.sb_height = QDoubleSpinBox()
        self.sb_height.setRange(0, 10000)
        self.sb_height.setSuffix(" мм")
        
        self.sb_depth = QDoubleSpinBox()
        self.sb_depth.setRange(0, 10000)
        self.sb_depth.setSuffix(" мм")
        
        self.le_mounting_points = QLineEdit()
        self.le_mounting_schemes = QLineEdit()
        self.le_manufacturer = QLineEdit()
        self.le_supplier = QLineEdit()
        
        self.sb_price = QDoubleSpinBox()
        self.sb_price.setRange(0, 1000000)
        self.sb_price.setPrefix("руб. ")
        
        # Add fields to form
        form_layout.addRow("Артикул:", self.le_article)
        form_layout.addRow("Название:", self.le_name)
        form_layout.addRow("Категория:", self.cb_category)
        form_layout.addRow("Описание:", self.te_description)
        
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.le_image_path)
        image_layout.addWidget(self.btn_browse_image)
        form_layout.addRow("Изображение:", image_layout)
        
        form_layout.addRow("Ширина:", self.sb_width)
        form_layout.addRow("Высота:", self.sb_height)
        form_layout.addRow("Глубина:", self.sb_depth)
        form_layout.addRow("Точки крепления (JSON):", self.le_mounting_points)
        form_layout.addRow("Схемы монтажа (JSON):", self.le_mounting_schemes)
        form_layout.addRow("Производитель:", self.le_manufacturer)
        form_layout.addRow("Поставщик:", self.le_supplier)
        form_layout.addRow("Цена:", self.sb_price)
        
        # Connect browse button
        self.btn_browse_image.clicked.connect(self.browse_image)
        
        layout.addWidget(form_group)
        
        # Buttons for form actions
        form_button_layout = QHBoxLayout()
        self.btn_add_update = QPushButton("Добавить/Обновить")
        self.btn_cancel = QPushButton("Отмена")
        self.btn_delete = QPushButton("Удалить")
        
        self.btn_add_update.clicked.connect(self.add_update_hardware)
        self.btn_cancel.clicked.connect(self.clear_form)
        self.btn_delete.clicked.connect(self.delete_hardware)
        
        form_button_layout.addWidget(self.btn_add_update)
        form_button_layout.addWidget(self.btn_cancel)
        form_button_layout.addWidget(self.btn_delete)
        form_button_layout.addStretch()
        
        layout.addLayout(form_button_layout)
        
        # Table for displaying hardware
        self.hw_table = QTableWidget()
        self.hw_table.setColumnCount(12)
        self.hw_table.setHorizontalHeaderLabels([
            "ID", "Артикул", "Название", "Категория", "Ширина", "Высота", 
            "Глубина", "Производитель", "Поставщик", "Цена", "Изображение", "Описание"
        ])
        
        # Set header properties
        header = self.hw_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Connect table selection change
        self.hw_table.itemSelectionChanged.connect(self.on_hw_selection_changed)
        
        layout.addWidget(self.hw_table)
        
        return tab

    def create_profiles_tab(self):
        """Create the profile systems management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Form for profile systems
        form_group = QGroupBox("Добавить/Редактировать систему профиля")
        form_layout = QFormLayout(form_group)
        
        self.le_profile_name = QLineEdit()
        self.te_profile_desc = QTextEdit()
        
        self.sb_axis_offset = QDoubleSpinBox()
        self.sb_axis_offset.setRange(-100, 100)
        self.sb_axis_offset.setSuffix(" мм")
        
        self.sb_sash_thickness = QDoubleSpinBox()
        self.sb_sash_thickness.setRange(0, 100)
        self.sb_sash_thickness.setSuffix(" мм")
        
        self.sb_frame_width = QDoubleSpinBox()
        self.sb_frame_width.setRange(0, 200)
        self.sb_frame_width.setSuffix(" мм")
        
        self.sb_sash_width = QDoubleSpinBox()
        self.sb_sash_width.setRange(0, 200)
        self.sb_sash_width.setSuffix(" мм")
        
        form_layout.addRow("Название:", self.le_profile_name)
        form_layout.addRow("Описание:", self.te_profile_desc)
        form_layout.addRow("Смещение оси:", self.sb_axis_offset)
        form_layout.addRow("Толщина створки:", self.sb_sash_thickness)
        form_layout.addRow("Ширина рамы:", self.sb_frame_width)
        form_layout.addRow("Ширина створки:", self.sb_sash_width)
        
        layout.addWidget(form_group)
        
        # Profile form buttons
        profile_button_layout = QHBoxLayout()
        self.btn_add_update_profile = QPushButton("Добавить/Обновить")
        self.btn_cancel_profile = QPushButton("Отмена")
        self.btn_delete_profile = QPushButton("Удалить")
        
        self.btn_add_update_profile.clicked.connect(self.add_update_profile)
        self.btn_cancel_profile.clicked.connect(self.clear_profile_form)
        self.btn_delete_profile.clicked.connect(self.delete_profile)
        
        profile_button_layout.addWidget(self.btn_add_update_profile)
        profile_button_layout.addWidget(self.btn_cancel_profile)
        profile_button_layout.addWidget(self.btn_delete_profile)
        profile_button_layout.addStretch()
        
        layout.addLayout(profile_button_layout)
        
        # Table for profile systems
        self.profile_table = QTableWidget()
        self.profile_table.setColumnCount(7)
        self.profile_table.setHorizontalHeaderLabels([
            "ID", "Название", "Описание", "Смещение оси", "Толщина створки", 
            "Ширина рамы", "Ширина створки"
        ])
        
        header = self.profile_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.profile_table.itemSelectionChanged.connect(self.on_profile_selection_changed)
        
        layout.addWidget(self.profile_table)
        
        return tab

    def refresh_tables(self):
        """Refresh both hardware and profile tables"""
        self.load_hardware_data()
        self.load_profile_data()

    def load_hardware_data(self):
        """Load hardware data into the table"""
        hardware_list = self.db_manager.get_all_hardware()
        
        self.hw_table.setRowCount(len(hardware_list))
        
        for row_idx, hw in enumerate(hardware_list):
            self.hw_table.setItem(row_idx, 0, QTableWidgetItem(str(hw['id'])))
            self.hw_table.setItem(row_idx, 1, QTableWidgetItem(hw['article_number']))
            self.hw_table.setItem(row_idx, 2, QTableWidgetItem(hw['name']))
            self.hw_table.setItem(row_idx, 3, QTableWidgetItem(hw['category'] or ""))
            self.hw_table.setItem(row_idx, 4, QTableWidgetItem(f"{hw['width'] or 0:.1f}"))
            self.hw_table.setItem(row_idx, 5, QTableWidgetItem(f"{hw['height'] or 0:.1f}"))
            self.hw_table.setItem(row_idx, 6, QTableWidgetItem(f"{hw['depth'] or 0:.1f}"))
            self.hw_table.setItem(row_idx, 7, QTableWidgetItem(hw['manufacturer'] or ""))
            self.hw_table.setItem(row_idx, 8, QTableWidgetItem(hw['supplier'] or ""))
            self.hw_table.setItem(row_idx, 9, QTableWidgetItem(f"{hw['price'] or 0:.2f}"))
            self.hw_table.setItem(row_idx, 10, QTableWidgetItem(hw['image_path'] or ""))
            self.hw_table.setItem(row_idx, 11, QTableWidgetItem(hw['description'] or ""))

    def load_profile_data(self):
        """Load profile system data into the table"""
        profiles = self.db_manager.get_all_profile_systems()
        
        self.profile_table.setRowCount(len(profiles))
        
        for row_idx, profile in enumerate(profiles):
            self.profile_table.setItem(row_idx, 0, QTableWidgetItem(str(profile['id'])))
            self.profile_table.setItem(row_idx, 1, QTableWidgetItem(profile['name']))
            self.profile_table.setItem(row_idx, 2, QTableWidgetItem(profile['description'] or ""))
            self.profile_table.setItem(row_idx, 3, QTableWidgetItem(f"{profile['axis_offset'] or 0:.1f}"))
            self.profile_table.setItem(row_idx, 4, QTableWidgetItem(f"{profile['sash_thickness'] or 0:.1f}"))
            self.profile_table.setItem(row_idx, 5, QTableWidgetItem(f"{profile['frame_width'] or 0:.1f}"))
            self.profile_table.setItem(row_idx, 6, QTableWidgetItem(f"{profile['sash_width'] or 0:.1f}"))

    def browse_image(self):
        """Browse for an image file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать изображение", "", 
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.le_image_path.setText(file_path)

    def add_update_hardware(self):
        """Add or update hardware component"""
        # Validate required fields
        if not self.le_article.text().strip():
            QMessageBox.warning(self, "Ошибка", "Артикул обязателен для заполнения!")
            return

        if not self.le_name.text().strip():
            QMessageBox.warning(self, "Ошибка", "Название обязательно для заполнения!")
            return

        # Prepare data
        data = {
            'article_number': self.le_article.text().strip(),
            'name': self.le_name.text().strip(),
            'category': self.cb_category.currentText(),
            'description': self.te_description.toPlainText(),
            'image_path': self.le_image_path.text(),
            'width': self.sb_width.value() if self.sb_width.value() > 0 else None,
            'height': self.sb_height.value() if self.sb_height.value() > 0 else None,
            'depth': self.sb_depth.value() if self.sb_depth.value() > 0 else None,
            'mounting_points': self.le_mounting_points.text() or None,
            'mounting_schemes': self.le_mounting_schemes.text() or None,
            'manufacturer': self.le_manufacturer.text() or None,
            'supplier': self.le_supplier.text() or None,
            'price': self.sb_price.value() if self.sb_price.value() > 0 else None
        }

        # Check if we're updating existing hardware
        selected_items = self.hw_table.selectedItems()
        if selected_items:
            # Get ID from selected row
            row = selected_items[0].row()
            id_item = self.hw_table.item(row, 0)
            if id_item:
                component_id = int(id_item.text())
                
                # Update existing component
                try:
                    self.db_manager.update_hardware_component(component_id, data)
                    QMessageBox.information(self, "Успех", "Компонент успешно обновлен!")
                    self.refresh_tables()
                    self.clear_form()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении компонента: {str(e)}")
                return

        # Add new component
        try:
            component_id = self.db_manager.add_hardware_component(data)
            QMessageBox.information(self, "Успех", f"Компонент успешно добавлен! ID: {component_id}")
            self.refresh_tables()
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении компонента: {str(e)}")

    def delete_hardware(self):
        """Delete selected hardware component"""
        selected_items = self.hw_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Выберите компонент для удаления!")
            return

        row = selected_items[0].row()
        id_item = self.hw_table.item(row, 0)
        if not id_item:
            return

        component_id = int(id_item.text())
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Вы действительно хотите удалить компонент с ID {component_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db_manager.delete_hardware_component(component_id)
                QMessageBox.information(self, "Успех", "Компонент успешно удален!")
                self.refresh_tables()
                self.clear_form()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении компонента: {str(e)}")

    def on_hw_selection_changed(self):
        """Handle hardware table selection change"""
        selected_items = self.hw_table.selectedItems()
        if not selected_items:
            return

        row = selected_items[0].row()
        
        # Fill form with selected data
        self.le_article.setText(self.hw_table.item(row, 1).text())
        self.le_name.setText(self.hw_table.item(row, 2).text())
        
        category = self.hw_table.item(row, 3).text()
        index = self.cb_category.findText(category)
        if index >= 0:
            self.cb_category.setCurrentIndex(index)
        
        self.te_description.setPlainText(self.hw_table.item(row, 11).text())
        self.le_image_path.setText(self.hw_table.item(row, 10).text())
        
        try:
            width = float(self.hw_table.item(row, 4).text())
            self.sb_width.setValue(width)
        except:
            self.sb_width.setValue(0)
        
        try:
            height = float(self.hw_table.item(row, 5).text())
            self.sb_height.setValue(height)
        except:
            self.sb_height.setValue(0)
        
        try:
            depth = float(self.hw_table.item(row, 6).text())
            self.sb_depth.setValue(depth)
        except:
            self.sb_depth.setValue(0)
        
        self.le_manufacturer.setText(self.hw_table.item(row, 7).text())
        self.le_supplier.setText(self.hw_table.item(row, 8).text())
        
        try:
            price = float(self.hw_table.item(row, 9).text())
            self.sb_price.setValue(price)
        except:
            self.sb_price.setValue(0)

    def clear_form(self):
        """Clear the hardware form"""
        self.le_article.clear()
        self.le_name.clear()
        self.cb_category.setCurrentIndex(0)
        self.te_description.clear()
        self.le_image_path.clear()
        self.sb_width.setValue(0)
        self.sb_height.setValue(0)
        self.sb_depth.setValue(0)
        self.le_mounting_points.clear()
        self.le_mounting_schemes.clear()
        self.le_manufacturer.clear()
        self.le_supplier.clear()
        self.sb_price.setValue(0)

    def add_update_profile(self):
        """Add or update profile system"""
        if not self.le_profile_name.text().strip():
            QMessageBox.warning(self, "Ошибка", "Название системы профиля обязательно!")
            return

        data = {
            'name': self.le_profile_name.text().strip(),
            'description': self.te_profile_desc.toPlainText(),
            'axis_offset': self.sb_axis_offset.value() if self.sb_axis_offset.value() != 0 else None,
            'sash_thickness': self.sb_sash_thickness.value() if self.sb_sash_thickness.value() != 0 else None,
            'frame_width': self.sb_frame_width.value() if self.sb_frame_width.value() != 0 else None,
            'sash_width': self.sb_sash_width.value() if self.sb_sash_width.value() != 0 else None
        }

        # Check if updating existing profile
        selected_items = self.profile_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            id_item = self.profile_table.item(row, 0)
            if id_item:
                profile_id = int(id_item.text())
                
                # In a real implementation, we'd have an update method for profiles
                # For now, we'll recreate the profile
                try:
                    # We'll remove the old one and add a new one since our DB manager doesn't have update method for profiles
                    # Actually, let's implement this properly - first we'll modify the DB manager to include update functionality
                    # But for now, we'll just show a message that it's not implemented
                    QMessageBox.information(self, "Информация", "Обновление профильных систем будет реализовано в следующей версии.")
                    return
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении системы: {str(e)}")
                return

        # Add new profile
        try:
            profile_id = self.db_manager.add_profile_system(data)
            QMessageBox.information(self, "Успех", f"Система профиля добавлена! ID: {profile_id}")
            self.refresh_tables()
            self.clear_profile_form()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении системы: {str(e)}")

    def delete_profile(self):
        """Delete selected profile system"""
        QMessageBox.information(self, "Информация", "Удаление систем профиля будет реализовано в следующей версии.")

    def on_profile_selection_changed(self):
        """Handle profile table selection change"""
        selected_items = self.profile_table.selectedItems()
        if not selected_items:
            return

        row = selected_items[0].row()
        
        # Fill form with selected data
        self.le_profile_name.setText(self.profile_table.item(row, 1).text())
        self.te_profile_desc.setPlainText(self.profile_table.item(row, 2).text())
        
        try:
            offset = float(self.profile_table.item(row, 3).text())
            self.sb_axis_offset.setValue(offset)
        except:
            self.sb_axis_offset.setValue(0)
        
        try:
            thickness = float(self.profile_table.item(row, 4).text())
            self.sb_sash_thickness.setValue(thickness)
        except:
            self.sb_sash_thickness.setValue(0)
        
        try:
            frame_w = float(self.profile_table.item(row, 5).text())
            self.sb_frame_width.setValue(frame_w)
        except:
            self.sb_frame_width.setValue(0)
        
        try:
            sash_w = float(self.profile_table.item(row, 6).text())
            self.sb_sash_width.setValue(sash_w)
        except:
            self.sb_sash_width.setValue(0)

    def clear_profile_form(self):
        """Clear the profile form"""
        self.le_profile_name.clear()
        self.te_profile_desc.clear()
        self.sb_axis_offset.setValue(0)
        self.sb_sash_thickness.setValue(0)
        self.sb_frame_width.setValue(0)
        self.sb_sash_width.setValue(0)