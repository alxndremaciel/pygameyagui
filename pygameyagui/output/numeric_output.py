import pygame
from ..include import constants as ct
from ..include import draw
from ..base.numeric import Numeric

class NumericOutput(Numeric):
    """This class creates a Numeric Output widget.

    :param toolbox: The toolbox that will host the widget.
    :type toolbox: :class:`pygameyagui.Toolbox`
    
    :param label: The text to be shown in the Numeric Output widget.
    :type label: str
    """
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._min_size = ct.NUMERIC_OUTPUT_MIN_SIZE_FACTOR
        self._max_size = ct.NUMERIC_OUTPUT_MAX_SIZE_FACTOR
        self.size = ct.NUMERIC_OUTPUT_DEFAULT_SIZE_FACTOR
        self._value = 0

    def _show_input_field(self):
        field_bg_color = ct.NUMERIC_OUTPUT_FIELD_BG_COLOR
        field_border_color = ct.NUMERIC_OUTPUT_FIELD_BORDER_COLOR
        field_border_width = ct.NUMERIC_OUTPUT_FIELD_BORDER_WIDTH
        self.field_rect = pygame.Rect(0, 0, ct.NUMERIC_OUTPUT_FIELD_WIDTH, ct.NUMERIC_OUTPUT_FIELD_HEIGHT)
        self.field_rect.midright = self._widget_rect.inflate(-2*ct.WIDGET_PADDING_RIGHT,0).midright
        draw._rect(self, self.field_rect, bg_color = field_bg_color, border_color = field_border_color, border_width = field_border_width)

    def _show_value(self):
        pos = self.field_rect.inflate(-2*ct.NUMERIC_OUTPUT_FIELD_PADDING,0).midright
        clipping_area_width = self.field_rect.width - 2*ct.NUMERIC_OUTPUT_FIELD_PADDING
        label_clipping_area = pygame.Rect(0, 0, clipping_area_width, ct.NUMERIC_OUTPUT_FIELD_HEIGHT)        
        draw._label(self, self._value_to_string(), 'midright', pos, area=label_clipping_area)

    def _show_label(self):
        pos = self._widget_rect.inflate(-2*ct.WIDGET_PADDING_RIGHT,0).midleft
        clipping_area_width = self._widget_rect.width - 3*ct.WIDGET_PADDING_RIGHT - self.field_rect.width
        label_clipping_area = pygame.Rect(0, 0, clipping_area_width, ct.NUMERIC_OUTPUT_FIELD_HEIGHT)
        label_rect = draw._label(self, self._label_with_unit(), 'midleft', pos, area=label_clipping_area)

    def _show(self):
        self._show_input_field()
        self._show_value()
        self._show_label()
        draw._widget_border(self)