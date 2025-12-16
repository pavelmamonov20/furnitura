"""
Database manager module for VisualFurnitura
Handles SQLite database operations for hardware components
"""
import sqlite3
import os
from typing import List, Dict, Optional


class DBManager:
    def __init__(self, db_path: str = "visualfurnitura.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create table for hardware components
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hardware_components (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_number TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                category TEXT,
                description TEXT,
                image_path TEXT,
                width REAL,
                height REAL,
                depth REAL,
                mounting_points TEXT,  -- JSON string with mounting point coordinates
                mounting_schemes TEXT, -- JSON string with mounting schemes
                manufacturer TEXT,
                supplier TEXT,
                price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create table for profile systems
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile_systems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                axis_offset REAL,
                sash_thickness REAL,
                frame_width REAL,
                sash_width REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create table for orders/projects
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                window_width REAL,
                window_height REAL,
                profile_system_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profile_system_id) REFERENCES profile_systems(id)
            )
        ''')

        # Create table for order hardware assignments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_hardware (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                component_id INTEGER,
                quantity INTEGER DEFAULT 1,
                x_position REAL,
                y_position REAL,
                rotation REAL DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (component_id) REFERENCES hardware_components(id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_hardware_component(self, data: Dict) -> int:
        """Add a new hardware component to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO hardware_components 
            (article_number, name, category, description, image_path, 
             width, height, depth, mounting_points, mounting_schemes, 
             manufacturer, supplier, price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('article_number'),
            data.get('name'),
            data.get('category'),
            data.get('description'),
            data.get('image_path'),
            data.get('width'),
            data.get('height'),
            data.get('depth'),
            data.get('mounting_points'),
            data.get('mounting_schemes'),
            data.get('manufacturer'),
            data.get('supplier'),
            data.get('price')
        ))

        component_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return component_id

    def get_hardware_component(self, component_id: int) -> Optional[Dict]:
        """Get a hardware component by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM hardware_components WHERE id = ?', (component_id,))
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            result = dict(zip(columns, row))
            conn.close()
            return result
        
        conn.close()
        return None

    def get_hardware_by_article(self, article_number: str) -> Optional[Dict]:
        """Get a hardware component by article number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM hardware_components WHERE article_number = ?', (article_number,))
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            result = dict(zip(columns, row))
            conn.close()
            return result
        
        conn.close()
        return None

    def update_hardware_component(self, component_id: int, data: Dict):
        """Update a hardware component"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE hardware_components SET
                name = ?,
                category = ?,
                description = ?,
                image_path = ?,
                width = ?,
                height = ?,
                depth = ?,
                mounting_points = ?,
                mounting_schemes = ?,
                manufacturer = ?,
                supplier = ?,
                price = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data.get('name'),
            data.get('category'),
            data.get('description'),
            data.get('image_path'),
            data.get('width'),
            data.get('height'),
            data.get('depth'),
            data.get('mounting_points'),
            data.get('mounting_schemes'),
            data.get('manufacturer'),
            data.get('supplier'),
            data.get('price'),
            component_id
        ))

        conn.commit()
        conn.close()

    def delete_hardware_component(self, component_id: int):
        """Delete a hardware component"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM hardware_components WHERE id = ?', (component_id,))

        conn.commit()
        conn.close()

    def get_all_hardware(self, category: Optional[str] = None) -> List[Dict]:
        """Get all hardware components, optionally filtered by category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if category:
            cursor.execute('SELECT * FROM hardware_components WHERE category = ? ORDER BY name', (category,))
        else:
            cursor.execute('SELECT * FROM hardware_components ORDER BY name')

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        conn.close()
        return results

    def add_profile_system(self, data: Dict) -> int:
        """Add a new profile system to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO profile_systems 
            (name, description, axis_offset, sash_thickness, frame_width, sash_width)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name'),
            data.get('description'),
            data.get('axis_offset'),
            data.get('sash_thickness'),
            data.get('frame_width'),
            data.get('sash_width')
        ))

        system_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return system_id

    def get_all_profile_systems(self) -> List[Dict]:
        """Get all profile systems"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM profile_systems ORDER BY name')
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        conn.close()
        return results

    def add_order(self, data: Dict) -> int:
        """Add a new order to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO orders 
            (name, description, window_width, window_height, profile_system_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('name'),
            data.get('description'),
            data.get('window_width'),
            data.get('window_height'),
            data.get('profile_system_id')
        ))

        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return order_id

    def add_order_hardware(self, order_id: int, component_id: int, quantity: int = 1, 
                          x_position: float = 0, y_position: float = 0, rotation: float = 0, 
                          notes: str = "") -> int:
        """Add hardware to an order"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO order_hardware 
            (order_id, component_id, quantity, x_position, y_position, rotation, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, component_id, quantity, x_position, y_position, rotation, notes))

        assignment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return assignment_id

    def get_order_hardware(self, order_id: int) -> List[Dict]:
        """Get all hardware assigned to an order"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT oh.*, hc.name as component_name, hc.article_number, hc.image_path
            FROM order_hardware oh
            JOIN hardware_components hc ON oh.component_id = hc.id
            WHERE oh.order_id = ?
        ''', (order_id,))
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        conn.close()
        return results

    def search_hardware(self, query: str) -> List[Dict]:
        """Search for hardware components by name or article number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM hardware_components 
            WHERE name LIKE ? OR article_number LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        conn.close()
        return results