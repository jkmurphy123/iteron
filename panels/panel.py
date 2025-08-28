from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QTextEdit
from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap
from PyQt5.QtCore import Qt, QRect


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

        # Monospaced font for authentic retro look
        self.font = QFont(self.font_family, self.font_size)
        self.setFont(self.font)

        # Layout: scrollable content inside panel
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)  # leave space for border
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Current content widget inside scroll area
        self.content_widget = QLabel("")  # default empty
        self.scroll_area.setWidget(self.content_widget)

        # Calculate pixel size based on char width/height
        fm = self.fontMetrics()
        self.char_width = fm.averageCharWidth()
        self.char_height = fm.height()
        self.setFixedSize(self.char_width * self.width_chars,
                          self.char_height * self.height_chars)

    def set_text(self, text: str):
        text_edit = QTextEdit()
        text_edit.setFont(self.font)
        text_edit.setPlainText(text)
        text_edit.setReadOnly(True)
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
        self.scroll_area.setWidget(label)
        self.content_widget = label
        self.update()

    def clear_content(self):
        label = QLabel("")
        self.scroll_area.setWidget(label)
        self.content_widget = label
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)

        # Draw border with box-drawing characters
        border_pen = QColor(self.border_color)
        painter.setPen(border_pen)

        width = self.width_chars
        height = self.height_chars

        # Precompute positions
        char_w = self.char_width
        char_h = self.char_height

        # Top border (depending on style)
        if self.title:
            if self.title_style == "embedded":
                left = "┌─┤ "
                right = " ├" + "─" * (width - len(self.title) - 6) + "┐"
                line = left + self.title + right
                # Draw title in mixed colors
                painter.drawText(0, char_h, "┌─┤ ")
                painter.setPen(QColor(self.title_color))
                painter.drawText(char_w * 3, char_h, self.title)
                painter.setPen(QColor(self.border_color))
                painter.drawText(char_w * (3 + len(self.title)), char_h, " ├" + "─" * (width - len(self.title) - 6) + "┐")
            elif self.title_style == "floating":
                top_line = "┌" + "─" * (width - 2) + "┐"
                title_line = "│ " + self.title.ljust(width - 3) + "│"
                sep_line = "├" + "─" * (width - 2) + "┤"
                painter.drawText(0, char_h, top_line)
                painter.setPen(QColor(self.title_color))
                painter.drawText(0, char_h * 2, title_line)
                painter.setPen(QColor(self.border_color))
                painter.drawText(0, char_h * 3, sep_line)
            else:  # no title
                top_line = "┌" + "─" * (width - 2) + "┐"
                painter.drawText(0, char_h, top_line)
        else:
            top_line = "┌" + "─" * (width - 2) + "┐"
            painter.drawText(0, char_h, top_line)

        # Bottom border
        bottom_line = "└" + "─" * (width - 2) + "┘"
        painter.drawText(0, char_h * height, bottom_line)

        # Side borders
        for row in range(2, height):
            painter.drawText(0, char_h * row, "│")
            painter.drawText(char_w * (width - 1), char_h * row, "│")

        painter.end()
