"""
PDF processor module for VisualFurnitura
Handles parsing of PDF files to extract hardware information
"""
import fitz  # PyMuPDF
import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class HardwareItem:
    """Data class for hardware items extracted from PDF"""
    article: str
    name: str
    quantity: int
    part: str  # e.g., 'C-1', 'C-2'
    position: Optional[str] = None  # Position information if available


@dataclass
class WindowDimensions:
    """Data class for window dimensions"""
    width: int
    height: int


class PDFProcessor:
    def __init__(self):
        pass

    def parse_hardware_pdf(self, pdf_path: str) -> Dict:
        """
        Parse PDF file to extract hardware information
        Returns a dictionary with parsed data
        """
        doc = fitz.open(pdf_path)
        text = ""
        
        # Extract text from all pages
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        
        doc.close()
        
        # Parse the extracted text
        result = {
            'hardware_items': [],
            'window_dimensions': None,
            'parts': [],
            'raw_text': text
        }
        
        # Find window dimensions (look for patterns like 1540x1790)
        dimension_pattern = r'(\d{3,4})[x\u00D7](\d{3,4})'
        dimension_matches = re.findall(dimension_pattern, text)
        
        if dimension_matches:
            # Take the first match as the window size (or the largest if multiple found)
            dims = [(int(w), int(h)) for w, h in dimension_matches]
            # Sort by area to find the most likely window size
            dims.sort(key=lambda x: x[0] * x[1], reverse=True)
            width, height = dims[0]
            result['window_dimensions'] = WindowDimensions(width, height)
        
        # Find hardware items by looking for article numbers and quantities
        # Common patterns for articles: alphanumeric codes like A1234, 123456, etc.
        article_patterns = [
            r'(?:арт\.?|article|артикул)[\s:]*([A-Za-z0-9\-]+)',  # artpatterns
            r'([A-Z]{1,2}\d{3,6}(?:-\d+)?)',  # Standard article format like A1234
            r'(\d{5,8})'  # Numeric articles
        ]
        
        # Look for quantity patterns (numbers followed by pieces, шт, etc.)
        quantity_patterns = [
            r'(\d+)\s*(?:шт\.?|pcs?\.?|pieces?|qty)',
            r'qty[.:]?\s*(\d+)',
            r'(\d+)\s+(?:шт|pcs|pieces)'
        ]
        
        # Look for part identifiers (C-1, C-2, etc.)
        part_patterns = [
            r'[Cc]-(\d+)',
            r'(?:часть|part)\s*[Cc]-(\d+)',
            r'([Cc]-\d+)'
        ]
        
        # Extract all potential articles
        all_articles = []
        for pattern in article_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            all_articles.extend(matches)
        
        # Extract quantities
        all_quantities = []
        for pattern in quantity_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            all_quantities.extend([int(q) for q in matches])
        
        # Extract parts
        all_parts = []
        for pattern in part_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            all_parts.extend([f"C-{part}" if not part.startswith('C-') else part for part in matches])
        
        # Combine the information (this is a simplified approach)
        # In a real implementation, we would need more sophisticated matching
        for i, article in enumerate(all_articles[:min(len(all_articles), len(all_quantities), len(all_parts))]):
            if i < len(all_quantities) and i < len(all_parts):
                hardware_item = HardwareItem(
                    article=article.strip(),
                    name=self._guess_name_from_context(article, text),
                    quantity=all_quantities[i],
                    part=all_parts[i]
                )
                result['hardware_items'].append(hardware_item)
        
        # If we couldn't match by index, try to create items based on available info
        if not result['hardware_items']:
            # Just create basic items with articles found
            for article in all_articles[:10]:  # Limit to first 10 to avoid noise
                hardware_item = HardwareItem(
                    article=article.strip(),
                    name=self._guess_name_from_context(article, text),
                    quantity=1,  # Default quantity
                    part="C-1"   # Default part
                )
                result['hardware_items'].append(hardware_item)
        
        return result

    def _guess_name_from_context(self, article: str, text: str) -> str:
        """
        Try to guess the name of the hardware item based on context around the article number
        """
        # Find the article in the text and look for descriptive words nearby
        pattern = rf'.{{0,50}}{re.escape(article)}.*?.{{0,50}}'
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if matches:
            # Extract likely name candidates (words that appear near the article)
            # This is a simplified approach - in reality, this would need more sophisticated NLP
            context = matches[0]
            
            # Look for words that might describe the hardware type
            name_patterns = [
                r'([а-яёa-z]+\s*[а-яёa-z]*)\s+' + re.escape(article),
                re.escape(article) + r'\s+([а-яёa-z]+(?:\s+[а-яёa-z]+)*)',
                r'(' + re.escape(article) + r'\s+[а-яёa-z]+)'
            ]
            
            for pattern in name_patterns:
                found = re.search(pattern, context, re.IGNORECASE)
                if found:
                    name = found.group(1).strip()
                    # Remove the article from the name if it was included
                    name = re.sub(re.escape(article), '', name, flags=re.IGNORECASE).strip()
                    if len(name) > 1:  # Make sure we have a meaningful name
                        return name.title()
        
        # If we can't find a specific name, return the article itself
        return article

    def parse_technical_pdf(self, pdf_path: str) -> Dict:
        """
        Parse technical PDF files to extract component specifications
        """
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        
        doc.close()
        
        # Extract technical specifications
        result = {
            'specifications': {},
            'mounting_schemes': [],
            'dimensions': {},
            'raw_text': text
        }
        
        # Look for dimension specifications (width, height, thickness, etc.)
        dimension_keywords = ['ширина', 'высота', 'толщина', 'размер', 'width', 'height', 'thickness', 'size']
        for keyword in dimension_keywords:
            pattern = rf'{keyword}[:\s]+(\d+\.?\d*)\s*мм?|mm?|cm?'
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                result['dimensions'][keyword] = [float(m) for m in matches]
        
        # Look for mounting schemes (common terms in Russian and English)
        mounting_terms = ['монтаж', 'крепление', 'установка', 'mounting', 'installation', 'fixing']
        for term in mounting_terms:
            if re.search(term, text, re.IGNORECASE):
                result['mounting_schemes'].append({
                    'term_found': term,
                    'context': self._extract_context(text, term, 100)
                })
        
        # Extract other technical specs
        spec_patterns = {
            'material': [r'материал|material', r'сталь|steel|алюминий|aluminum|пластик|plastic'],
            'color': [r'цвет|color', r'белый|white|коричневый|brown|черный|black'],
            'weight': [r'вес|weight', r'(\d+\.?\d*)\s*(?:кг|kg|g)'],
            'load_capacity': [r'грузоподъемность|load\s+capacity', r'(\d+\.?\d*)\s*(?:кг|kg)']
        }
        
        for spec_type, patterns in spec_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    result['specifications'][spec_type] = matches
                    break
        
        return result

    def _extract_context(self, text: str, target: str, char_count: int = 100) -> str:
        """Extract context around a target word"""
        pattern = rf'.{{0,{char_count}}}{target}.{{0,{char_count}}}'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(0) if match else ""

    def extract_images_from_pdf(self, pdf_path: str, output_dir: str) -> List[str]:
        """
        Extract images from PDF file
        """
        doc = fitz.open(pdf_path)
        image_paths = []
        
        for page_index in range(len(doc)):
            page = doc.load_page(page_index)
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                if pix.n < 5:  # Check if not CMYK
                    img_path = f"{output_dir}/page_{page_index}_img_{img_index}.png"
                    pix.save(img_path)
                    image_paths.append(img_path)
                else:  # CMYK: convert via the original base image
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                    img_path = f"{output_dir}/page_{page_index}_img_{img_index}.png"
                    pix.save(img_path)
                    image_paths.append(img_path)
                
                pix = None  # Free memory
        
        doc.close()
        return image_paths