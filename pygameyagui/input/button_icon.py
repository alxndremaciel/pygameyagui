import pygame
from ..include import constants as ct
from ..include import draw
from ..base.widget import Widget

class ButtonIcon:
    def __init__(self, interface, rect, geometries):
        self._interface = interface
        self._interface._icons.append(self)
        self._rect = rect
        self._geometries = geometries
        self._being_pressed = False
        self._trigged = False
        self._mouse_over = False
        
    def _show(self):
        panel_bg_color = ct.INTERFACE_CONTROLS_PANEL_BG_COLOR
        button_bg_color = ct.INTERFACE_CONTROLS_BUTTONS_BG_COLOR
        if self._mouse_over:        
            button_bg_color = ct.INTERFACE_CONTROLS_BUTTONS_BG_MOUSEOVER_COLOR
        if self._being_pressed:
            button_bg_color = ct.INTERFACE_CONTROLS_BUTTONS_BG_CLICKED_COLOR

        for geometry in self._geometries:
            if geometry['color'] == 'button':
                bg_color = button_bg_color
            elif geometry['color'] == 'test':
                bg_color = (0,0,255)
            else:
                bg_color = panel_bg_color
            if geometry['type'] == 'rect':
                rect = geometry['rect']
                pygame.draw.rect(self._interface._surface, bg_color, rect)
            if geometry['type'] == 'polygon':
                points = geometry['points']
                pygame.draw.polygon(self._interface._surface, bg_color, points)
            if geometry['type'] == 'circle':
                center, radius = geometry['center'], geometry['radius']
                pygame.draw.circle(self._interface._surface, bg_color, center, radius)

    def _activate(self):
        self._trigged = True

    def _deactivate(self):
        self._trigged = False

    def _toggle(self):
        self._trigged = not self._trigged

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