import pygame
from ..include import constants as ct
from ..include import draw
from ..base.widget import Widget

class RadioButton(Widget):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._options = ['Opção A', 'Opção B']
        self._selected = 0
        self._min_size = ct.RADIOBUTTON_MIN_SIZE_FACTOR
        self._max_size = ct.RADIOBUTTON_MAX_SIZE_FACTOR
        self.size = ct.RADIOBUTTON_DEFAULT_SIZE_FACTOR
        self._resettable = True

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, _selected):
        if self._enabled:
            if _selected in range(len(self._options)):
                self._selected = _selected
            else:
                self._selected = 0

    @property
    def selected_text(self):
        return self._options[self._selected]

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, _options):
        if self._enabled:
            if isinstance(_options, list):
                _options_str = []
                for _index, _option in enumerate(_options):
                    try:
                        _option_str = str(_option)
                    except:
                        raise TypeError(f'The option {_option} was expected to be of type string. Instead, type {type(_option)} was given.')

                    if _option_str.startswith('*'):
                        self._selected = _index
                        _option_str = _option_str[1:]
                    _options_str.append(_option_str)

                self._options = _options_str[:]
                self._recalculate_size()

            else:
                raise TypeError(f'options expect a type list as argument. Instead, type {type(_options)} was given.')

    def add_option(self, _option):
        if self._enabled:
            try:
                _option_str = str(_option)
            except:
                raise TypeError(f'The option {_option} was expected to be of type string. Instead, type {type(_option)} was given.')

            self._options.append(_option_str)
            self._recalculate_size()

    def del_option(self, _option):
        if self._enabled:
            if not str(_option) in self._options:
                raise ValueError(f'The option {_option} is not in {self._label}.')

            self._options.remove(str(_option))
            self._recalculate_size()

    def _recalculate_size(self):
        self.size = len(self._options) + 1

    def _show(self):
        option_rect_height = int(self._widget_rect.height / self._size)
        label_rect = pygame.Rect(self._widget_rect.left, self._widget_rect.top, self._widget_rect.width, option_rect_height)
        pos = label_rect.inflate(-2*ct.WIDGET_PADDING_LEFT,0).midleft
        draw._label(self, self._label, 'midleft', pos)
        inner_rects = [label_rect]
        self.radiobutton_rects = []
        self.option_label_rects = []

        unselected_color = ct.RADIOBUTTON_UNSELECTED_BG_COLOR
        selected_color = ct.RADIOBUTTON_SELECTED_BG_COLOR
        if self._mouse_over:
            selected_color = ct.RADIOBUTTON_SELECTED_BG_MOUSEOVER_COLOR
        border_color = ct.RADIOBUTTON_BORDER_COLOR
        border_width = ct.RADIOBUTTON_BORDER_WIDTH
        radius = ct.RADIOBUTTON_RADIUS

        for index, option in enumerate(self._options):
            option_rect = pygame.Rect(self._widget_rect.left, inner_rects[-1].bottom, self._widget_rect.width, option_rect_height)
            inner_rects.append(option_rect)
            radiobutton_rect = pygame.Rect(0, 0, ct.RADIOBUTTON_SIDE, ct.RADIOBUTTON_SIDE)
            radiobutton_rect.midleft = option_rect.inflate(-2*ct.WIDGET_PADDING_LEFT, 0).midleft
            if self._selected == index:
                draw._circle(self, radiobutton_rect.center, radius, bg_color = selected_color, border_color = border_color, border_width = border_width)
            else:
                draw._circle(self, radiobutton_rect.center, radius, bg_color = unselected_color, border_color = border_color, border_width = border_width)
            
            pos = radiobutton_rect.inflate(2*ct.WIDGET_PADDING_LEFT, 0).midright
            option_label_rect = draw._label(self, option, 'midleft', pos)
            self.radiobutton_rects.append({'value': index, 'rect': radiobutton_rect})
            self.option_label_rects.append({'value': index, 'rect': option_label_rect})

        draw._widget_border(self)

    def _handle_events(self):
        self._check_mouse_over()
        for event in self._interface._events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # TODO: Mudar isso aqui
                    for button, label in zip(self.radiobutton_rects,self.option_label_rects):
                        if button['rect'].collidepoint(self._interface._mouse_pos):
                            self.selected = button['value']
                        if label['rect'].collidepoint(self._interface._mouse_pos):
                            self.selected = label['value']
