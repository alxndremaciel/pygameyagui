import pygame
from ..include import constants as ct
from ..include import draw
from ..base.numeric import Numeric

class Chart(Numeric):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self.decimal_places = 0
        self._unit = ''

    def _show_label(self):
        pos = self._widget_rect.inflate(0,-2*ct.WIDGET_PADDING_TOP).midtop
        self.label_rect = draw._label(self, self._label_with_unit(), 'midtop', pos)
        
    def _get_chart_area_rect(self):
        self._chart_area_rect = pygame.Rect(
            self._widget_rect.left,
            self.label_rect.bottom,
            self._widget_rect.width,
            self._widget_rect.bottom - self.label_rect.bottom)
        self._chart_area_rect.inflate_ip(-ct.CHART_AREA_PADDING_HORIZONTAL,-ct.CHART_AREA_PADDING_VERTICAL)

        self._chart_min_y_pos = self._chart_area_rect.bottom
        self._chart_max_y_pos = self._chart_area_rect.top
        self._chart_height = self._chart_min_y_pos - self._chart_max_y_pos

        self._chart_min_x_pos = self._chart_area_rect.left
        self._chart_max_x_pos = self._chart_area_rect.right
        self._chart_width = self._chart_max_x_pos - self._chart_min_x_pos

    def _lerp_y(self, _value):
        y1 = self._chart_max_y_pos
        y0 = self._chart_min_y_pos
        x0 = self._data_min_y_value
        x1 = self._data_max_y_value
        if (x1 - x0):
            return int((y0*(x1-_value)+y1*(_value-x0)) / (x1 - x0))
        else:
            return int(y0 - 0.5 * self._chart_height)

    def _lerp_x(self, _value):
        y1 = self._chart_max_x_pos
        y0 = self._chart_min_x_pos
        x0 = self._data_min_x_value
        x1 = self._data_max_x_value
        if (x1 - x0):
            return int((y0*(x1-_value)+y1*(_value-x0)) / (x1 - x0))
        else:
            return int(y0 - 0.5 * self._chart_width)