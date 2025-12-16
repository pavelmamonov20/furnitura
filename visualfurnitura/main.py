"""
Main application entry point for VisualFurnitura
"""
import sys
from PyQt6.QtWidgets import QApplication
from visualization.window import MainWindow


def main():
    """Main entry point of the application"""
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()