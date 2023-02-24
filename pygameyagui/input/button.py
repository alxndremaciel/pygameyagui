import pygame
from ..include import constants as ct
from ..include import draw
from ..base.widget import Widget

class Button(Widget):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._min_size = ct.BUTTON_MIN_SIZE_FACTOR
        self._max_size = ct.BUTTON_MAX_SIZE_FACTOR
        self.size = ct.BUTTON_DEFAULT_SIZE_FACTOR
        self.being_pressed = False
        self.trigged = False
        
    @property
    def trigged(self):
        return self._trigged

    @trigged.setter
    def trigged(self, _trigged):
        if self._enabled:
            if isinstance(_trigged, bool):
                self._trigged = _trigged
            else:
                raise ValueError(f'trigged expect a boolean as argument. Instead, type {type(_trigged)} was given.')

    def activate(self):
        if self._enabled:
            self._trigged = True

    def deactivate(self):
        self._trigged = False

    def toggle(self):
        if self._enabled:
            self._trigged = not(self._trigged)

    def _show(self):
        bg_color = ct.BUTTON_BG_COLOR
        if self._mouse_over:
            bg_color = ct.BUTTON_BG_HOVER_COLOR
        if self.being_pressed:
            bg_color = ct.BUTTON_BG_CLICKED_COLOR
        
        border_color = ct.BUTTON_BORDER_COLOR
        border_width = ct.BUTTON_BORDER_WIDTH
        border_radius = ct.BUTTON_BORDER_RADIUS
        
        draw._rect(self, self._widget_rect, bg_color = bg_color, border_color = border_color, border_width = border_width, border_radius = border_radius)
        draw._label(self, self._label, 'center', self._widget_rect.center, area=self._widget_rect)
        
    def _handle_events(self):
        self._check_mouse_over()
        self.deactivate()
        for event in self._interface._events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self._widget_rect.collidepoint(self._interface._mouse_pos):
                        if self.being_pressed:
                            self.activate()
                        self.being_pressed = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self._widget_rect.collidepoint(self._interface._mouse_pos):
                        self.being_pressed = True