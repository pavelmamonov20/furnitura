#!/usr/bin/env python3
"""
Test script to verify admin functionality in VisualFurnitura
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from db_manager import DBManager

def test_admin_functionality():
    print("Тестирование функционала администратора...")
    
    # Создаем экземпляр DBManager
    db = DBManager()
    
    # Тестируем добавление компонента фурнитуры
    print("\n1. Тестирование добавления компонента фурнитуры...")
    hardware_data = {
        'article_number': 'TEST-001',
        'name': 'Тестовая ручка',
        'category': 'Ручки',
        'description': 'Тестовый компонент для проверки функционала',
        'width': 60.0,
        'height': 120.0,
        'depth': 10.0,
        'manufacturer': 'Test Manufacturer',
        'supplier': 'Test Supplier',
        'price': 500.0
    }
    
    try:
        hw_id = db.add_hardware_component(hardware_data)
        print(f"   ✓ Компонент добавлен с ID: {hw_id}")
    except Exception as e:
        print(f"   ✗ Ошибка при добавлении компонента: {e}")
        return False
    
    # Тестируем получение компонента
    print("\n2. Тестирование получения компонента...")
    try:
        hw = db.get_hardware_component(hw_id)
        if hw and hw['name'] == 'Тестовая ручка':
            print(f"   ✓ Компонент успешно получен: {hw['name']}")
        else:
            print(f"   ✗ Компонент не найден или данные некорректны: {hw}")
            return False
    except Exception as e:
        print(f"   ✗ Ошибка при получении компонента: {e}")
        return False
    
    # Тестируем обновление компонента
    print("\n3. Тестирование обновления компонента...")
    try:
        updated_data = {
            'name': 'Обновленная тестовая ручка',
            'category': 'Ручки',
            'description': 'Обновленное описание',
            'width': 65.0,
            'height': 125.0,
            'depth': 12.0,
            'manufacturer': 'Updated Manufacturer',
            'supplier': 'Updated Supplier',
            'price': 550.0
        }
        
        db.update_hardware_component(hw_id, updated_data)
        updated_hw = db.get_hardware_component(hw_id)
        
        if updated_hw and updated_hw['name'] == 'Обновленная тестовая ручка':
            print(f"   ✓ Компонент успешно обновлен: {updated_hw['name']}")
        else:
            print(f"   ✗ Компонент не обновлен корректно: {updated_hw}")
            return False
    except Exception as e:
        print(f"   ✗ Ошибка при обновлении компонента: {e}")
        return False
    
    # Тестируем добавление профильной системы
    print("\n4. Тестирование добавления профильной системы...")
    profile_data = {
        'name': 'Тестовая система',
        'description': 'Тестовая профильная система для проверки функционала',
        'axis_offset': 15.5,
        'sash_thickness': 68.0,
        'frame_width': 90.0,
        'sash_width': 78.0
    }
    
    try:
        profile_id = db.add_profile_system(profile_data)
        print(f"   ✓ Профильная система добавлена с ID: {profile_id}")
    except Exception as e:
        print(f"   ✗ Ошибка при добавлении профильной системы: {e}")
        return False
    
    # Тестируем получение профильной системы
    print("\n5. Тестирование получения профильной системы...")
    try:
        profiles = db.get_all_profile_systems()
        if profiles and any(p['name'] == 'Тестовая система' for p in profiles):
            print(f"   ✓ Профильная система успешно найдена в списке. Всего систем: {len(profiles)}")
        else:
            print(f"   ✗ Профильная система не найдена в списке: {profiles}")
            return False
    except Exception as e:
        print(f"   ✗ Ошибка при получении профильных систем: {e}")
        return False
    
    # Тестируем обновление профильной системы
    print("\n6. Тестирование обновления профильной системы...")
    try:
        updated_profile_data = {
            'name': 'Обновленная тестовая система',
            'description': 'Обновленное описание тестовой системы',
            'axis_offset': 16.0,
            'sash_thickness': 70.0,
            'frame_width': 95.0,
            'sash_width': 80.0
        }
        
        db.update_profile_system(profile_id, updated_profile_data)
        profiles = db.get_all_profile_systems()
        updated_profile = next((p for p in profiles if p['id'] == profile_id), None)
        
        if updated_profile and updated_profile['name'] == 'Обновленная тестовая система':
            print(f"   ✓ Профильная система успешно обновлена: {updated_profile['name']}")
        else:
            print(f"   ✗ Профильная система не обновлена корректно: {updated_profile}")
            return False
    except Exception as e:
        print(f"   ✗ Ошибка при обновлении профильной системы: {e}")
        return False
    
    # Тестируем удаление компонента
    print("\n7. Тестирование удаления компонента...")
    try:
        db.delete_hardware_component(hw_id)
        deleted_hw = db.get_hardware_component(hw_id)
        if not deleted_hw:
            print("   ✓ Компонент успешно удален")
        else:
            print("   ✗ Компонент не удален")
            return False
    except Exception as e:
        print(f"   ✗ Ошибка при удалении компонента: {e}")
        return False
    
    # Тестируем удаление профильной системы
    print("\n8. Тестирование удаления профильной системы...")
    try:
        db.delete_profile_system(profile_id)
        profiles = db.get_all_profile_systems()
        deleted_profile = next((p for p in profiles if p['id'] == profile_id), None)
        if not deleted_profile:
            print("   ✓ Профильная система успешно удалена")
        else:
            print("   ✗ Профильная система не удалена")
            return False
    except Exception as e:
        print(f"   ✗ Ошибка при удалении профильной системы: {e}")
        return False
    
    print("\n✓ Все тесты административного функционала пройдены успешно!")
    return True

if __name__ == "__main__":
    success = test_admin_functionality()
    if not success:
        sys.exit(1)