"""
Setup script for VisualFurnitura database
Creates the database and adds sample data
"""
from db_manager import DBManager


def setup_database():
    """Setup the database with initial data"""
    print("Setting up VisualFurnitura database...")
    
    # Create database manager instance
    db = DBManager()
    
    # Add sample profile systems
    profile_data = [
        {
            'name': 'Aluplast Ideal-2000',
            'description': 'Трехкамерный профиль, ширина 76 мм',
            'axis_offset': 35.8,
            'sash_thickness': 68,
            'frame_width': 76,
            'sash_width': 76
        },
        {
            'name': 'Rehau Geneva',
            'description': 'Трехкамерный профиль, ширина 70 мм',
            'axis_offset': 33.5,
            'sash_thickness': 60,
            'frame_width': 70,
            'sash_width': 70
        },
        {
            'name': 'KBE Evolution',
            'description': 'Пятикамерный профиль, ширина 80 мм',
            'axis_offset': 38.0,
            'sash_thickness': 72,
            'frame_width': 80,
            'sash_width': 80
        }
    ]
    
    for profile in profile_data:
        db.add_profile_system(profile)
        print(f"Added profile system: {profile['name']}")
    
    # Add sample hardware components
    hardware_data = [
        {
            'article_number': 'H-001',
            'name': 'Петля верхняя',
            'category': 'Петли',
            'description': 'Верхняя петля для поворотной створки',
            'width': 30,
            'height': 100,
            'depth': 10,
            'mounting_points': '{"top": [15, 5], "bottom": [15, 95]}',
            'mounting_schemes': '["scheme_1.png"]',
            'manufacturer': 'Roto',
            'supplier': 'Оконные системы',
            'price': 150.0
        },
        {
            'article_number': 'H-002',
            'name': 'Петля средняя',
            'category': 'Петли',
            'description': 'Средняя петля для поворотной створки',
            'width': 30,
            'height': 100,
            'depth': 10,
            'mounting_points': '{"top": [15, 5], "bottom": [15, 95]}',
            'mounting_schemes': '["scheme_1.png"]',
            'manufacturer': 'Roto',
            'supplier': 'Оконные системы',
            'price': 150.0
        },
        {
            'article_number': 'H-003',
            'name': 'Петля нижняя',
            'category': 'Петли',
            'description': 'Нижняя петля для поворотной створки',
            'width': 30,
            'height': 100,
            'depth': 10,
            'mounting_points': '{"top": [15, 5], "bottom": [15, 95]}',
            'mounting_schemes': '["scheme_1.png"]',
            'manufacturer': 'Roto',
            'supplier': 'Оконные системы',
            'price': 150.0
        },
        {
            'article_number': 'H-004',
            'name': 'Ручка поворотная',
            'category': 'Ручки',
            'description': 'Поворотная ручка для пластиковых окон',
            'width': 120,
            'height': 40,
            'depth': 25,
            'mounting_points': '{"screw_1": [20, 20], "screw_2": [100, 20]}',
            'mounting_schemes': '["scheme_2.png"]',
            'manufacturer': 'Maco',
            'supplier': 'Оконные системы',
            'price': 350.0
        },
        {
            'article_number': 'H-005',
            'name': 'Замок центральный',
            'category': 'Замки',
            'description': 'Центральный замок для поворотной створки',
            'width': 80,
            'height': 80,
            'depth': 15,
            'mounting_points': '{"main_bolt": [40, 40], "aux_bolt_1": [20, 20], "aux_bolt_2": [60, 60]}',
            'mounting_schemes': '["scheme_3.png"]',
            'manufacturer': 'Siegenia',
            'supplier': 'Оконные системы',
            'price': 420.0
        },
        {
            'article_number': 'H-006',
            'name': 'Микролифт',
            'category': 'Микролифты',
            'description': 'Механизм микролифта для проветривания',
            'width': 60,
            'height': 20,
            'depth': 10,
            'mounting_points': '{"mount_points": [[10, 10], [50, 10]]}',
            'mounting_schemes': '["scheme_4.png"]',
            'manufacturer': 'Roto',
            'supplier': 'Оконные системы',
            'price': 280.0
        },
        {
            'article_number': 'H-007',
            'name': 'Отлив',
            'category': 'Отливы',
            'description': 'Внутренний отлив ПВХ белый',
            'width': 200,  # This will be variable based on window width
            'height': 20,
            'depth': 10,
            'mounting_points': '{}',
            'mounting_schemes': '["scheme_5.png"]',
            'manufacturer': 'Космо',
            'supplier': 'Оконные системы',
            'price': 450.0
        }
    ]
    
    for hardware in hardware_data:
        db.add_hardware_component(hardware)
        print(f"Added hardware component: {hardware['name']} (Article: {hardware['article_number']})")
    
    print("Database setup completed successfully!")


if __name__ == "__main__":
    setup_database()