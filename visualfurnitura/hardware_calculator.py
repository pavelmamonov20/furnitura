"""
Hardware calculator module for VisualFurnitura
Calculates coordinates for hardware placement based on profile system parameters
"""
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ProfileSystem:
    """Data class for profile system parameters"""
    name: str
    axis_offset: float  # mm
    sash_thickness: float  # mm
    frame_width: float  # mm
    sash_width: float  # mm
    description: str = ""


@dataclass
class HardwarePlacement:
    """Data class for hardware placement result"""
    article: str
    name: str
    x: float  # mm from left edge
    y: float  # mm from top edge
    rotation: float  # degrees
    notes: str = ""


class HardwareCalculator:
    def __init__(self):
        self.profile_systems = {}
        self.hardware_templates = {}
        self._initialize_default_templates()

    def _initialize_default_templates(self):
        """Initialize default hardware placement templates"""
        # Template for hinges (assuming 3 hinges for a standard door/window)
        self.hardware_templates['hinge'] = [
            {'name': 'Петля верхняя', 'x_offset': 0.05, 'y_offset': 0.05, 'type': 'position'},  # 5% from top
            {'name': 'Петля средняя', 'x_offset': 0.05, 'y_offset': 0.5, 'type': 'position'},   # Middle height
            {'name': 'Петля нижняя', 'x_offset': 0.05, 'y_offset': 0.95, 'type': 'position'}   # 5% from bottom
        ]
        
        # Template for handle
        self.hardware_templates['handle'] = [
            {'name': 'Ручка', 'x_offset': 0.5, 'y_offset': 0.75, 'type': 'position'}  # Middle width, 75% height
        ]
        
        # Template for lock
        self.hardware_templates['lock'] = [
            {'name': 'Замок', 'x_offset': 0.95, 'y_offset': 0.5, 'type': 'position'}  # 95% width (right side), middle height
        ]
        
        # Template for sills
        self.hardware_templates['sill'] = [
            {'name': 'Отлив', 'x_offset': 0, 'y_offset': 0.99, 'width_ratio': 1.0, 'height_ratio': 0.01, 'type': 'dimension'}
        ]

    def add_profile_system(self, profile: ProfileSystem):
        """Add a profile system to the calculator"""
        self.profile_systems[profile.name] = profile

    def calculate_hardware_placement(self, 
                                   window_width: float, 
                                   window_height: float, 
                                   profile_name: str,
                                   hardware_type: str) -> List[HardwarePlacement]:
        """
        Calculate hardware placement based on window dimensions and profile system
        """
        if profile_name not in self.profile_systems:
            raise ValueError(f"Profile system '{profile_name}' not found")
        
        profile = self.profile_systems[profile_name]
        template = self.hardware_templates.get(hardware_type, [])
        
        placements = []
        
        for item in template:
            if item['type'] == 'position':
                x = window_width * item['x_offset']
                y = window_height * item['y_offset']
                
                placement = HardwarePlacement(
                    article=f"{hardware_type}-{len(placements)+1}",
                    name=item['name'],
                    x=x,
                    y=y,
                    rotation=0  # Default rotation
                )
                placements.append(placement)
            
            elif item['type'] == 'dimension':
                # For items with dimensions (like sills)
                x = window_width * item.get('x_offset', 0)
                y = window_height * item.get('y_offset', 0)
                width = window_width * item.get('width_ratio', 0.1)
                height = window_height * item.get('height_ratio', 0.05)
                
                # Calculate center position for the dimensional item
                center_x = x + width / 2
                center_y = y + height / 2
                
                placement = HardwarePlacement(
                    article=f"{hardware_type}-{len(placements)+1}",
                    name=item['name'],
                    x=center_x,
                    y=center_y,
                    rotation=0
                )
                placements.append(placement)
        
        return placements

    def calculate_custom_placement(self, 
                                 window_width: float, 
                                 window_height: float,
                                 profile_name: str,
                                 hardware_specs: List[Dict]) -> List[HardwarePlacement]:
        """
        Calculate custom hardware placement based on specific specifications
        """
        if profile_name not in self.profile_systems:
            raise ValueError(f"Profile system '{profile_name}' not found")
        
        profile = self.profile_systems[profile_name]
        placements = []
        
        for spec in hardware_specs:
            # Calculate position based on various possible specifications
            x = self._calculate_position(spec.get('x'), spec.get('x_offset'), window_width)
            y = self._calculate_position(spec.get('y'), spec.get('y_offset'), window_height)
            
            placement = HardwarePlacement(
                article=spec.get('article', f"HW-{len(placements)+1}"),
                name=spec.get('name', f"Компонент-{len(placements)+1}"),
                x=x,
                y=y,
                rotation=spec.get('rotation', 0),
                notes=spec.get('notes', '')
            )
            
            placements.append(placement)
        
        return placements

    def _calculate_position(self, absolute_pos: Optional[float], 
                          relative_offset: Optional[float], 
                          dimension: float) -> float:
        """
        Calculate position based on absolute value or relative offset
        """
        if absolute_pos is not None:
            return absolute_pos
        elif relative_offset is not None:
            return dimension * relative_offset
        else:
            return 0  # Default to 0 if neither is specified

    def calculate_symmetric_placement(self, 
                                    window_width: float, 
                                    window_height: float,
                                    profile_name: str,
                                    hardware_article: str,
                                    hardware_name: str,
                                    count: int,
                                    alignment: str = 'horizontal') -> List[HardwarePlacement]:
        """
        Calculate symmetric placement for multiple identical components
        """
        if profile_name not in self.profile_systems:
            raise ValueError(f"Profile system '{profile_name}' not found")
        
        placements = []
        
        if alignment == 'horizontal':
            # Distribute horizontally along the width
            if count == 1:
                x_positions = [window_width / 2]
            else:
                # Add margin to prevent placing items at the very edge
                margin = 0.05 * window_width  # 5% margin
                step = (window_width - 2 * margin) / (count - 1) if count > 1 else 0
                x_positions = [margin + i * step for i in range(count)]
            
            for i, x in enumerate(x_positions):
                placement = HardwarePlacement(
                    article=f"{hardware_article}-{i+1}",
                    name=f"{hardware_name} {i+1}",
                    x=x,
                    y=window_height / 2,  # Center vertically
                    rotation=0
                )
                placements.append(placement)
        
        elif alignment == 'vertical':
            # Distribute vertically along the height
            if count == 1:
                y_positions = [window_height / 2]
            else:
                # Add margin to prevent placing items at the very edge
                margin = 0.05 * window_height  # 5% margin
                step = (window_height - 2 * margin) / (count - 1) if count > 1 else 0
                y_positions = [margin + i * step for i in range(count)]
            
            for i, y in enumerate(y_positions):
                placement = HardwarePlacement(
                    article=f"{hardware_article}-{i+1}",
                    name=f"{hardware_name} {i+1}",
                    x=window_width / 2,  # Center horizontally
                    y=y,
                    rotation=0
                )
                placements.append(placement)
        
        return placements

    def calculate_from_pdf_data(self, 
                              window_width: float, 
                              window_height: float,
                              profile_name: str,
                              pdf_hardware_list: List[Dict]) -> List[HardwarePlacement]:
        """
        Calculate hardware placement based on data extracted from PDF
        """
        if profile_name not in self.profile_systems:
            raise ValueError(f"Profile system '{profile_name}' not found")
        
        profile = self.profile_systems[profile_name]
        placements = []
        
        for hw_item in pdf_hardware_list:
            # For now, if coordinates are provided in the PDF data, use them directly
            # Otherwise, calculate default positions based on component type
            x = hw_item.get('x_position')
            y = hw_item.get('y_position')
            
            if x is not None and y is not None:
                # Use coordinates from PDF if available
                placement = HardwarePlacement(
                    article=hw_item.get('article', 'N/A'),
                    name=hw_item.get('name', 'Unknown'),
                    x=x,
                    y=y,
                    rotation=hw_item.get('rotation', 0),
                    notes=hw_item.get('notes', '')
                )
            else:
                # Calculate default position based on hardware type
                hw_type = self._categorize_hardware_type(hw_item.get('name', ''))
                default_placements = self.calculate_hardware_placement(
                    window_width, window_height, profile_name, hw_type
                )
                
                # If we have default placements, use the first one
                if default_placements:
                    default_placement = default_placements[0]
                    placement = HardwarePlacement(
                        article=hw_item.get('article', 'N/A'),
                        name=hw_item.get('name', 'Unknown'),
                        x=default_placement.x,
                        y=default_placement.y,
                        rotation=default_placement.rotation,
                        notes=hw_item.get('notes', '')
                    )
                else:
                    # Default fallback: center of window
                    placement = HardwarePlacement(
                        article=hw_item.get('article', 'N/A'),
                        name=hw_item.get('name', 'Unknown'),
                        x=window_width / 2,
                        y=window_height / 2,
                        rotation=0,
                        notes=hw_item.get('notes', '')
                    )
            
            placements.append(placement)
        
        return placements

    def _categorize_hardware_type(self, hardware_name: str) -> str:
        """
        Categorize hardware type based on name
        """
        name_lower = hardware_name.lower()
        
        if any(word in name_lower for word in ['петля', 'hinge', 'шарнир']):
            return 'hinge'
        elif any(word in name_lower for word in ['ручка', 'handle', 'кноб']):
            return 'handle'
        elif any(word in name_lower for word in ['замок', 'lock', 'засов']):
            return 'lock'
        elif any(word in name_lower for word in ['отлив', 'sill', 'подоконник']):
            return 'sill'
        elif any(word in name_lower for word in ['угол', 'corner']):
            return 'corner'
        else:
            return 'other'  # Default category

    def get_mounting_recommendations(self, 
                                   window_width: float, 
                                   window_height: float,
                                   profile_name: str) -> Dict:
        """
        Get recommended mounting points for common hardware based on window size
        """
        if profile_name not in self.profile_systems:
            raise ValueError(f"Profile system '{profile_name}' not found")
        
        profile = self.profile_systems[profile_name]
        
        recommendations = {
            'hinges': self.calculate_hardware_placement(window_width, window_height, profile_name, 'hinge'),
            'handle': self.calculate_hardware_placement(window_width, window_height, profile_name, 'handle'),
            'lock': self.calculate_hardware_placement(window_width, window_height, profile_name, 'lock'),
            'sill': self.calculate_hardware_placement(window_width, window_height, profile_name, 'sill')
        }
        
        return recommendations