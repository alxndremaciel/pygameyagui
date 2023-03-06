import pygame
from ..include import constants as ct
from ..include.error import raise_type_error, raise_value_error
from ..include import draw
from ..base.widget import Widget

class CheckBox(Widget):
    """This class creates a CheckBox widget.

    :param toolbox: The toolbox that will host the widget.
    :type toolbox: :class:`pygameyagui.Toolbox`
    
    :param label: The text to be shown in the CheckBox widget.
    :type label: str
    """
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._min_size = ct.CHECKBOX_MIN_SIZE_FACTOR
        self._max_size = ct.CHECKBOX_MAX_SIZE_FACTOR
        self.size = ct.CHECKBOX_DEFAULT_SIZE_FACTOR
        self._checked = False
        self._can_be_emitter = True
        
    @property
    def checked(self):
        '''Get or set the the state of a CheckBox (bool).'''
        return self._checked

    @checked.setter
    def checked(self, _checked):
        if self._enabled:
            if isinstance(_checked, bool):
                if _checked:
                    self._activate()
                else:
                    self._deactivate()
            else:
                raise_type_error(_checked, 'checked', 'bool')

    def _activate(self):
        if self._enabled:
            self._checked = self._trigger_emitter(True)

    def _deactivate(self):
        if self._enabled:
            self._checked = self._trigger_emitter(False)

    def _toggle(self):
        if self._enabled:
            if self._checked:
                self._deactivate()
            else:
                self._activate()

    def _trigger_emitter(self, _checked):
        if self._emitter and not self._checked == _checked:
            self._interface._emitting = self
        return _checked

    def _show(self):
        unchecked_color = ct.CHECKBOX_UNCHECKED_BG_COLOR
        checked_color = ct.CHECKBOX_CHECKED_BG_COLOR
        if self._mouse_over:
            checked_color = ct.CHECKBOX_CHECKED_BG_MOUSEOVER_COLOR
        border_color = ct.CHECKBOX_BORDER_COLOR
        border_width = ct.CHECKBOX_BORDER_WIDTH

        self.ckbox_rect = pygame.Rect(0, 0, ct.CHECKBOX_SIDE, ct.CHECKBOX_SIDE)
        self.ckbox_rect.midleft = self._widget_rect.inflate(-2*ct.WIDGET_PADDING_LEFT,0).midleft
        if self._checked:
            draw._rect(self, self.ckbox_rect, bg_color = checked_color, border_color = border_color, border_width = border_width)
        else:
            draw._rect(self, self.ckbox_rect, bg_color = unchecked_color, border_color = border_color, border_width = border_width)
        
        pos = self.ckbox_rect.inflate(2*ct.WIDGET_PADDING_LEFT,0).midright
        clippingarea = self._widget_rect.inflate(-(2*ct.WIDGET_PADDING_LEFT+self.ckbox_rect.width),0)
        self.label_rect = draw._label(self, self._label, 'midleft', pos, area=clippingarea)
        draw._widget_border(self)

    def _handle_events(self):
        self._check_mouse_over()
        for event in self._interface._events:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    if self.ckbox_rect.collidepoint(mouse_pos):
                        self._toggle()
                    if self.label_rect.collidepoint(mouse_pos):
                        self._toggle()