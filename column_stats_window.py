from typing import Dict, List
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon
from styles import Styles
from widgets.utility_widgets.seperator import HorizontalSeperator
from widgets.utility_widgets.horizontal_group import HorizontalGroup
from widgets.utility_widgets.labeled_widget import LabeledWidget
from widgets.themed_widgets.colored_text import ColoredText
from widgets.utility_widgets.vertical_group import VerticalGroup
from PyQt6.QtGui import QFontMetrics, QFont

class ColumnStatsWindow(QWidget):
    def __init__(self, descriptions_dict: Dict[str, List], window_title: str, show_standard_description_labels: bool = False):
        super().__init__()

        self.setWindowTitle(window_title)
        self.setWindowIcon(QIcon("assets/logo.png"))

        description_names = ["Point count", "Mean", "SD", "Min", "25%", "Median", "75%", "max"]

        font_size = 12
        margin = 20

        font_metrics = QFontMetrics(QFont(Styles.theme.font_family, font_size))

        #region Calculate Column Widths
        description_widths = [0] * (len(description_names) + 1)
        # find widest description in pixels for each category
        for key, description in descriptions_dict.items():
            
            for i in range(0, len(description)):
                value = description[i]
                value_string = str(value)
                value_string = "{:.2f}".format(value)
                if show_standard_description_labels:
                    value_string = description_names[i] + ":  " + value_string
                description_widths[i+1] = max(description_widths[i+1], font_metrics.boundingRect(value_string.strip()).width())

            # also find key
            description_widths[0] = max(description_widths[0], font_metrics.boundingRect(key.strip()).width())


        #endregion
            

        self.setStyleSheet(f"background-color: {Styles.theme.mid_background_color_hex};")

        vertical_layout = VerticalGroup(margins=(margin, margin, margin, margin), spacing = 0)

        description_index:int = 0
        for key, description in descriptions_dict.items():
            row = HorizontalGroup()

            if show_standard_description_labels and len(description) != len(description_names):
                continue

            row_name = row.addWidget(ColoredText(key, color=Styles.theme.header_text_color, fontSize=font_size))
            row_name.setFixedWidth(int(description_widths[0] * 1.5))
            for i in range(0, len(description)):
                value = description[i]
                value_string = str(value)

                value_string = "{:.2f}".format(value)
                
                value_text = ColoredText(value_string, color=Styles.theme.label_color, fontSize=font_size)

                widget = None
                if show_standard_description_labels:
                    widget = LabeledWidget(description_names[i].strip() + ":", value_text, font_color=Styles.theme.header_text_color, font_size=font_size, spacing=0)
                else:
                    widget = value_text

                labeled_value = row.addWidget(widget)
                labeled_value.setFixedWidth(description_widths[i+1])

            vertical_layout.addWidget(row)
            if description_index != len(descriptions_dict) - 1:
                vertical_layout.addWidget(HorizontalSeperator(spacing=int(margin/2.0), thickness=1))

            description_index += 1

        self.setLayout(vertical_layout.layout())