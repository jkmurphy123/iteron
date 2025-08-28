import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from panels.panel import Panel


def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)


def main():
    app = QApplication(sys.argv)

    config = load_config()

    rows = config.get("rows", 1)
    cols = config.get("cols", 1)
    font_family = config.get("font_family", "Courier New")
    font_size = config.get("font_size", 12)

    window = QWidget()
    layout = QGridLayout(window)

    panels_config = config.get("panels", [])

    for i, panel_cfg in enumerate(panels_config):
        title = panel_cfg.get("title")
        width = panel_cfg.get("width", 40)
        height = panel_cfg.get("height", 10)
        title_style = panel_cfg.get("title_style", "embedded")
        border_color = panel_cfg.get("border_color", "#CCCCCC")
        title_color = panel_cfg.get("title_color")

        panel = Panel(
            title=title,
            width=width,
            height=height,
            title_style=title_style,
            border_color=border_color,
            title_color=title_color,
            font_family=font_family,
            font_size=font_size
        )

        # Demo content
        if i == 0:
            panel.set_text("Error: Missing semicolon\nInfo: Compiled successfully\nWarning: Deprecated API")
        elif i == 1:
            panel.set_image("example.png")  # put any image file here
        elif i == 2:
            panel.set_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n" * 3)
        else:
            panel.clear_content()

        row = i // cols
        col = i % cols
        layout.addWidget(panel, row, col)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
