import pygame
from ..include import constants as ct
from ..include import draw
from ..base.widget import Widget

class CheckBox(Widget):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._min_size = ct.CHECKBOX_MIN_SIZE_FACTOR
        self._max_size = ct.CHECKBOX_MAX_SIZE_FACTOR
        self.size = ct.CHECKBOX_DEFAULT_SIZE_FACTOR
        self.checked = False
        self._can_be_emitter = True
        
    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, _checked):
        if self._enabled:
            if isinstance(_checked, bool):
                self._checked = _checked
            else:
                raise TypeError(f'checked expect a boolean as argument. Instead, type {type(_checked)} was given.')

    def activate(self):
        if self._enabled:
            self._checked = True

    def deactivate(self):
        if self._enabled:
            self._checked = False

    def toggle(self):
        if self._enabled:
            self._checked = not(self._checked)

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
                        self.toggle()
                    if self.label_rect.collidepoint(mouse_pos):
                        self.toggle()