import pygame
from ..include import constants as ct
from ..include import draw
from ..base.chart import Chart

class SparkLine(Chart):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._min_size = ct.SPARKLINE_MIN_SIZE_FACTOR
        self._max_size = ct.SPARKLINE_MAX_SIZE_FACTOR
        self.size = ct.SPARKLINE_DEFAULT_SIZE_FACTOR
        self._dataset = []
        self._type = 'line'
        self._color = 'red'

    @property
    def value(self):
        '''Get the last value of the dataset (int or float) or None if dataset is empty.

        Overrides :attr:`pygameyagui.Numeric.value`.
        
        Default value is None. It is a read-only property.
        '''
        if self._data_set:
            return self._dataset[-1]
        else:
            return None

    @value.setter
    def value(self, _value):
        raise ValueError(f'value can not be set for sparkline chart. Use the method update_dataset().')

    @property
    def color(self):
        '''Get or set the graph color (str).

        Note: Accepted values are **red**, **green**, **yellow** or **blue**. Default value is **red**.'''
        return self._color

    @color.setter
    def color(self, _color):
        if _color in ['red', 'green', 'yellow', 'blue']:
            self._color = _color
        else:
            raise ValueError(f'color can only be set to red, green, yellow or blue. Instead, {_color} was given.')

    def update_dataset(self, value):
        '''Use this to add a value to the dataset.

        :param value: A value to be added
        :type value: int or float

        :rtype: NoneType
        '''
        if self._enabled:
            if not isinstance(value, int) and not isinstance(value, float):
                raise TypeError(f'update_dataset only accepts type int or float. Instead, argument of type {type(value)} was given.')

            value = self._update_value(value)
            self._dataset.append(value)
            if len(self._dataset) > self._chart_width:
                self._dataset.pop(0)

            self._data_min_y_value = min(self._dataset)
            self._data_max_y_value = max(self._dataset)
            self._data_min_x_value = 0
            self._data_max_x_value = len(self._dataset)

    def _graphing(self):
        if self._enabled:
            if self._color == 'green':
                self._line_color = ct.SPARKLINE_LINE_GREEN_COLOR
                self._fill_color = ct.SPARKLINE_FILL_GREEN_COLOR

            elif self._color == 'yellow':
                self._line_color = ct.SPARKLINE_LINE_YELLOW_COLOR
                self._fill_color = ct.SPARKLINE_FILL_YELLOW_COLOR

            elif self._color == 'red':
                self._line_color = ct.SPARKLINE_LINE_RED_COLOR
                self._fill_color = ct.SPARKLINE_FILL_RED_COLOR
            
            elif self._color == 'blue':
                self._line_color = ct.SPARKLINE_LINE_BLUE_COLOR
                self._fill_color = ct.SPARKLINE_FILL_BLUE_COLOR
        else:
            self._line_color = ct.WIDGET_DISABLED_BORDER_COLOR
            self._fill_color = ct.WIDGET_DISABLED_BG_COLOR

        bullet_border_color = self._line_color
        bullet_bg_color = ct.SPARKLINE_BULLET_BG_COLOR

        if len(self._dataset) >= 2:
            points = [(self._lerp_x(_x), self._lerp_y(_y)) for _x, _y in enumerate(self._dataset)]
            points_for_fill = points[:]
            points_for_fill.append((points[-1][0], self._chart_min_y_pos))
            points_for_fill.append((points[0][0], self._chart_min_y_pos))
            pygame.draw.polygon(self._surface, self._fill_color, points_for_fill) 
            pygame.draw.lines(self._surface, self._line_color, False, points, width=ct.SPARKLINE_LINE_WIDTH) 
            pygame.draw.circle(self._surface, bullet_bg_color, points[-1],3)
            pygame.draw.circle(self._surface, bullet_border_color, points[-1],3,width=1)

    def _show_max_label(self):
        if len(self._dataset):
            _max = max(self._dataset)
            _max_str = self._value_to_string(_max)
            pos = self._lerp_x(self._dataset.index(_max)), self._chart_max_y_pos - ct.CHART_LABEL_PADDING_VERTICAL
            label_rect = draw._label(self, _max_str, 'midbottom', pos, bg_color = self._fill_color, limits=self._chart_area_rect)

            start = self._lerp_x(self._dataset.index(_max)), self._lerp_y(_max) - 2
            end = self._lerp_x(self._dataset.index(_max)), self._lerp_y(_max) - ct.CHART_LABEL_PADDING_VERTICAL
            pygame.draw.line(self._surface, self._fill_color, start, end, width=ct.SPARKLINE_LINE_WIDTH)

    def _show_min_label(self):
        if len(self._dataset):
            _min = min(self._dataset)
            _min_str = self._value_to_string(_min)
            pos = self._lerp_x(self._dataset.index(_min)), self._chart_min_y_pos + ct.CHART_LABEL_PADDING_VERTICAL
            label_rect = draw._label(self, _min_str, 'midtop', pos, bg_color = self._fill_color, limits=self._chart_area_rect)
            
            start = self._lerp_x(self._dataset.index(_min)), self._lerp_y(_min) + 2
            end = self._lerp_x(self._dataset.index(_min)), self._lerp_y(_min) + ct.CHART_LABEL_PADDING_VERTICAL
            pygame.draw.line(self._surface, self._fill_color, start, end, width=ct.SPARKLINE_LINE_WIDTH)

    def _show(self):
        self._show_label()
        self._get_chart_area_rect()
        self._graphing()
        self._show_max_label()
        self._show_min_label()
        draw._widget_border(self)