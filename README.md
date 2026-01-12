# Pure Python Vector-Based Barcode Generator

This project creates high-quality, centered barcodes in Excel files using a pure Python approach without external dependencies like Cairo.

## Features

- **High-Quality Barcodes**: Uses SVG generation with python-barcode library for vector-quality barcodes
- **Perfect Centering**: Barcodes are properly centered in Excel cells
- **No External Dependencies**: Pure Python solution that works without Cairo or other external libraries
- **Optimized Settings**: Enhanced barcode readability with increased module height and width

## How It Works

1. **SVG Generation**: Uses python-barcode to generate vector-based SVG barcodes
2. **SVG Parsing**: Manually parses the SVG XML structure to extract barcode elements
3. **High-Quality Rendering**: Renders the barcode to a large image (upscaled by factor of 3) then resizes down for anti-aliasing
4. **Excel Integration**: Inserts the rendered PNG images into Excel cells with proper centering

## Technical Details

- **Module Height**: 20.0 (increased for better readability)
- **Module Width**: 0.6 (wider bars for clarity)
- **Quiet Zone**: 15.0 (more space on both sides)
- **Font Size**: 12 (larger human-readable text)
- **Resolution**: 300 DPI for high-quality output
- **Upscaling Factor**: 3x for anti-aliasing effect

## Usage

Run the script and select either:
- Mode 1: Create test file with 20 barcodes
- Mode 2: Create full file with 200 barcodes

The resulting Excel file will have perfectly centered, high-quality barcodes in column C.

## Solution Approach

Instead of trying to use external SVG-to-PNG converters that require Cairo, this solution:
1. Generates SVG barcodes using python-barcode
2. Parses the SVG XML structure directly
3. Extracts the rectangle elements that represent the bars
4. Draws these rectangles using PIL/Pillow
5. Upscales and then downscales the image for anti-aliasing
6. Inserts the resulting PNG into Excel

This approach eliminates all external dependencies while maintaining excellent barcode quality and proper centering in Excel cells.