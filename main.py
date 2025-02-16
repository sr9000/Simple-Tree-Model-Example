import sys
from pathlib import Path

import yaml
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from tree_model import TreeModel


class AppDemo(QMainWindow):
    def __init__(self, yaml_filename: str):
        super(AppDemo, self).__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Load data from YAML file
        with open(yaml_filename) as file:
            data = yaml.safe_load(file)

        # Create TreeModel with the loaded data
        model = TreeModel(data)

        # Create QTreeView and set the model
        tree_view = QTreeView(self)
        tree_view.setModel(model)
        layout.addWidget(tree_view)


def main():
    filename = "data.yaml"

    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif not filename:
        print("Usage: python main.py <file-name.yaml>")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = AppDemo(filename)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
