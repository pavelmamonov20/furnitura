"""
Profile administration module for VisualFurnitura
Provides GUI for managing profile systems
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QDialog, QTableWidget, QTableWidgetItem, QHeaderView,
                            QLineEdit, QTextEdit, QPushButton, QDoubleSpinBox,
                            QFileDialog, QMessageBox, QTabWidget, QGroupBox, QLabel)
from PyQt6.QtCore import Qt
import json
import os
from ..db_manager import DBManager


class ProfileAdminDialog(QDialog):
    def __init__(self, db_manager: DBManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Администрирование профильных систем")
        self.setGeometry(200, 200, 800, 600)
        
        self.layout = QVBoxLayout(self)
        
        # Create form for profile systems
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
        
        self.layout.addWidget(form_group)
        
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
        
        self.layout.addLayout(profile_button_layout)
        
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
        
        self.layout.addWidget(self.profile_table)
        
        # Load initial data
        self.load_profile_data()

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
                
                try:
                    self.db_manager.update_profile_system(profile_id, data)
                    QMessageBox.information(self, "Успех", "Система профиля успешно обновлена!")
                    self.load_profile_data()
                    self.clear_profile_form()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении системы: {str(e)}")
                return

        # Add new profile
        try:
            profile_id = self.db_manager.add_profile_system(data)
            QMessageBox.information(self, "Успех", f"Система профиля добавлена! ID: {profile_id}")
            self.load_profile_data()
            self.clear_profile_form()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении системы: {str(e)}")

    def delete_profile(self):
        """Delete selected profile system"""
        selected_items = self.profile_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Выберите систему профиля для удаления!")
            return

        row = selected_items[0].row()
        id_item = self.profile_table.item(row, 0)
        if not id_item:
            return

        profile_id = int(id_item.text())
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Вы действительно хотите удалить систему профиля с ID {profile_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db_manager.delete_profile_system(profile_id)
                QMessageBox.information(self, "Успех", "Система профиля успешно удалена!")
                self.load_profile_data()
                self.clear_profile_form()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении системы: {str(e)}")

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