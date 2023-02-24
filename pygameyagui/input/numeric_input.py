import pygame
from ..include import constants as ct
from ..include import draw
from ..base.numeric import Numeric

class NumericInput(Numeric):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._min_size = ct.NUMERIC_INPUT_MIN_SIZE_FACTOR
        self._max_size = ct.NUMERIC_INPUT_MAX_SIZE_FACTOR
        self.size = ct.NUMERIC_INPUT_DEFAULT_SIZE_FACTOR
        self._field_width = ct.NUMERIC_INPUT_FIELD_WIDTH
        self.value = 0
        self._resettable = True

    @property
    def temp_value(self):
        return self._temp_value

    @temp_value.setter
    def temp_value(self, _temp_value):
        accept_edit = False
        self._is_temp_value_valid = False
        try:
            int(_temp_value)
            accept_edit = True
            self._is_temp_value_valid = True
        except:
            try:
                float(_temp_value)
                accept_edit = True
                self._is_temp_value_valid = True
            except:
                pass

        if not _temp_value or _temp_value == '.' or _temp_value.endswith('e') or _temp_value.endswith('e-'):
            accept_edit = True
        
        if accept_edit:
            self._temp_value = _temp_value

    def _show_input_field(self):
        if self._toolbox._editing_focus is self:
            if self._is_temp_value_valid: 
                field_bg_color = ct.NUMERIC_INPUT_FIELD_BG_EDITING_VALID_COLOR
            else:
                field_bg_color = ct.NUMERIC_INPUT_FIELD_BG_EDITING_INVALID_COLOR
        else:
            field_bg_color = ct.NUMERIC_INPUT_FIELD_BG_COLOR

        label_color = ct.TOOLBOX_STANDARD_TEXT_COLOR
        field_border_color = ct.NUMERIC_INPUT_FIELD_BORDER_COLOR
        field_border_width = ct.NUMERIC_INPUT_FIELD_BORDER_WIDTH

        self._field_rect = pygame.Rect(0, 0, ct.NUMERIC_INPUT_FIELD_WIDTH, ct.NUMERIC_INPUT_FIELD_HEIGHT)
        self._field_rect.midright = self._widget_rect.inflate(-2*ct.WIDGET_PADDING_RIGHT,0).midright
        draw._rect(self, self._field_rect, bg_color = field_bg_color, border_color = field_border_color, border_width = field_border_width)
        
    def _show_value(self):
        if self._toolbox._editing_focus is self:
            _value  = self.temp_value
        else:
            _value = self._value_to_string()
        pos = self._field_rect.inflate(-2*ct.NUMERIC_INPUT_FIELD_PADDING,0).midright
        clipping_area_width = self._field_rect.width - 2*ct.NUMERIC_INPUT_FIELD_PADDING
        label_clipping_area = pygame.Rect(0, 0, clipping_area_width, ct.NUMERIC_INPUT_FIELD_HEIGHT)        
        draw._label(self, _value, 'midright', pos, area=label_clipping_area)

    def _show_label(self):
        pos = self._widget_rect.inflate(-2*ct.WIDGET_PADDING_RIGHT,0).midleft
        clipping_area_width = self._widget_rect.width - 3*ct.WIDGET_PADDING_RIGHT - self._field_rect.width
        label_clipping_area = pygame.Rect(0, 0, clipping_area_width, ct.NUMERIC_INPUT_FIELD_HEIGHT)
        label_rect = draw._label(self, self._label_with_unit(), 'midleft', pos, area=label_clipping_area)

    def _show(self):
        self._show_input_field()
        self._show_value()
        self._show_label()    
        draw._widget_border(self)
        
    def _get_focus(self):
        self.temp_value = self._value_to_string()
        self._is_temp_value_valid = True

    def _loose_focus(self):
        if self._is_temp_value_valid:
            self.value = self.temp_value
        else:
            self.temp_value = self._value_to_string()
            self._is_temp_value_valid = True

    def _handle_events(self):
        for event in self._interface._events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self._field_rect.collidepoint(self._interface._mouse_pos):
                        if self._toolbox._editing_focus is not None:
                            self._toolbox._editing_focus._loose_focus()
                        self._toolbox._editing_focus = self
                        self._get_focus()

            if self._toolbox._editing_focus is self:
                if event.type == pygame.KEYDOWN:
                    char_ = pygame.key.name(event.key).strip('[').strip(']')
                    # TODO: Implementar possibilidade de algebra (+,-,*,/)
                    if char_ in '0123456789.e-':
                        if not (char_ in '.e-' and char_ in self.temp_value):
                            self.temp_value = self._temp_value+char_
                    if char_ == 'delete':
                        self.temp_value = ''

                    if char_ == 'backspace':
                        self.temp_value = self._temp_value[:-1]

                    if char_ == 'escape':
                        self._toolbox._editing_focus = None
                        self.temp_value = self._value_to_string()

                    if char_ == 'return' or char_ == 'enter':
                        self._toolbox._editing_focus = None
                        self._loose_focus()