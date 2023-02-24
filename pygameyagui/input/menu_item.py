import pygame
from ..include import constants as ct
from ..include import draw
from ..base.widget import Widget

class MenuItem:
    def __init__(self, interface, rect, label, signal):
        self._interface = interface
        self._interface._hamburger_menu_itens.append(self)
        self._surface = interface._surface
        self._rect = rect
        self._label = label
        self._signal = signal
        self._being_pressed = False
        self._trigged = False
        self._mouse_over = False
        self._enabled = True
        
    def _show(self):
        _menu_item_bg_color = ct.INTERFACE_CONTROLS_BUTTONS_BG_COLOR
        if self._mouse_over:        
            _menu_item_bg_color = ct.INTERFACE_CONTROLS_BUTTONS_BG_MOUSEOVER_COLOR
        if self._being_pressed:
            _menu_item_bg_color = ct.INTERFACE_CONTROLS_BUTTONS_BG_CLICKED_COLOR

        draw._rect(self, self._rect, bg_color = _menu_item_bg_color)
        draw._label(self, self._label, 'center', self._rect.center)

    def _activate(self):
        self._trigged = True

    def _deactivate(self):
        self._trigged = False

    def _toggle(self):
        self._trigged = not self._trigged

    def _show(self):
        bg_color = ct.INTERFACE_CONTROLS_MENUITEM_BG_COLOR
        if self._mouse_over:
            bg_color = ct.INTERFACE_CONTROLS_MENUITEM_BG_MOUSEOVER_COLOR
        if self._being_pressed:
            bg_color = ct.INTERFACE_CONTROLS_MENUITEM_BG_CLICKED_COLOR

        draw._rect(self, self._rect, bg_color = bg_color,)

        draw._label(self, self._label, 'center', self._rect.center)

    def _handle_events(self):
        self._check_mouse_over()
        self._deactivate()
        for event in self._interface._events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self._rect.collidepoint(self._interface._mouse_pos):
                        if self._being_pressed:
                            self._activate()
                        self._being_pressed = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self._rect.collidepoint(self._interface._mouse_pos):
                        self._being_pressed = True

    def _check_mouse_over(self):
        self._mouse_over = False
        if self._rect.collidepoint(self._interface._mouse_pos):
            self._mouse_over = True