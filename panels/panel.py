from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QTextEdit
from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap
from PyQt5.QtCore import Qt


class Panel(QWidget):
    def __init__(self, title=None, width=40, height=10,
                 title_style="embedded", border_color="#CCCCCC", title_color=None,
                 font_family="Courier New", font_size=12, parent=None):
        super().__init__(parent)

        self.title = title
        self.width_chars = width
        self.height_chars = height
        self.title_style = title_style
        self.border_color = border_color
        self.title_color = title_color or border_color
        self.font_family = font_family
        self.font_size = font_size

        self.font = QFont(self.font_family, self.font_size)
        self.setFont(self.font)

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        scrollbar_style = """ QScrollBar:vertical {
                background: black;
                width: 14px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #888888;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background: #AAAAAA;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: #666666;
                height: 14px;
                subcontrol-origin: margin;
            }

            QScrollBar::add-line:vertical:hover,
            QScrollBar::sub-line:vertical:hover {
                background: #AAAAAA;
            }

            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {
                width: 10px;
                height: 10px;
                background: #CCCCCC;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: black;
            }


            /* Horizontal Scrollbar */
            QScrollBar:horizontal {
                background: black;
                height: 14px;
                margin: 0px;
            }

            QScrollBar::handle:horizontal {
                background: #888888;
                min-width: 20px;
            }

            QScrollBar::handle:horizontal:hover {
                background: #AAAAAA;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                background: #666666;
                width: 14px;
                subcontrol-origin: margin;
            }

            QScrollBar::add-line:horizontal:hover,
            QScrollBar::sub-line:horizontal:hover {
                background: #AAAAAA;
            }

            QScrollBar::left-arrow:horizontal,
            QScrollBar::right-arrow:horizontal {
                width: 10px;
                height: 10px;
                background: #CCCCCC;
            }

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: black;
            }
        """
        self.scroll_area.setStyleSheet(
            f"background-color: black; border: none; {scrollbar_style}"
        )
        self.layout.addWidget(self.scroll_area)

        # Start with empty content
        self.content_widget = QLabel("")
        self.content_widget.setStyleSheet(f"background-color: black; color: {self.border_color};")
        self.scroll_area.setWidget(self.content_widget)

        fm = self.fontMetrics()
        self.char_width = fm.averageCharWidth()
        self.char_height = fm.height()

        # Adjust height if title exists
        adjust = 1 if self.title else 0
        self.setFixedSize(self.char_width * self.width_chars,
                          self.char_height * (self.height_chars + adjust))

    def set_text(self, text: str):
        text_edit = QTextEdit()
        text_edit.setFont(self.font)
        text_edit.setPlainText(text)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet(f"background-color: black; color: {self.border_color}; border: none;")
        self.scroll_area.setWidget(text_edit)
        self.content_widget = text_edit
        self.update()

    def set_image(self, path: str):
        label = QLabel()
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
        else:
            label.setText("[Image not found]")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"color: {self.border_color};")
        label.setStyleSheet("background-color: black; border: none;")
        self.scroll_area.setWidget(label)
        self.content_widget = label
        self.update()

    def clear_content(self):
        label = QLabel("")
        label.setStyleSheet(f"background-color: black; color: {self.border_color}; border: none;")
        self.scroll_area.setWidget(label)
        self.content_widget = label
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)

        border_pen = QColor(self.border_color)
        painter.setPen(border_pen)

        width = self.width_chars
        height = self.height_chars
        char_w = self.char_width
        char_h = self.char_height

        # Draw top border
        if self.title:
            if self.title_style == "embedded":
                painter.drawText(0, char_h, "┌─┤ ")
                painter.setPen(QColor(self.title_color))
                painter.drawText(char_w * 3, char_h, self.title)
                painter.setPen(QColor(self.border_color))
                painter.drawText(char_w * (3 + len(self.title)), char_h,
                                 " ├" + "─" * (width - len(self.title) - 6) + "┐")
            elif self.title_style == "floating":
                painter.drawText(0, char_h, "┌" + "─" * (width - 2) + "┐")
                painter.setPen(QColor(self.title_color))
                painter.drawText(0, char_h * 2, "│ " + self.title.ljust(width - 3) + "│")
                painter.setPen(QColor(self.border_color))
                painter.drawText(0, char_h * 3, "├" + "─" * (width - 2) + "┤")
            else:
                painter.drawText(0, char_h, "┌" + "─" * (width - 2) + "┐")
        else:
            painter.drawText(0, char_h, "┌" + "─" * (width - 2) + "┐")

        # Bottom border
        painter.setPen(QColor(self.border_color))
        painter.drawText(0, char_h * height, "└" + "─" * (width - 2) + "┘")

        # Side borders
        for row in range(2, height):
            painter.drawText(0, char_h * row, "│")
            painter.drawText(char_w * (width - 1), char_h * row, "│")

        painter.end()
