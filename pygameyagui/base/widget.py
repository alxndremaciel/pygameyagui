import pygame
import pygameyagui
from ..include import constants as ct
from ..include.error import raise_type_error

class Widget:
    def __init__(self, toolbox, label):
        self._set_toolbox(toolbox)
        self._set_interface(toolbox._interface)
        self._surface = self._interface._surface
        self._toolbox._widgets.append(self)
        self._set_label(label)
        self._enabled = True
        self._mouse_over = False
        self._can_be_emitter = False
        self._emitter = True

    def _set_toolbox(self, _toolbox):
        if isinstance(_toolbox, pygameyagui.Toolbox):
            self._toolbox = _toolbox
        else:
            raise_type_error(_toolbox, 'toolbox', 'pygameyagui.Toolbox')

    def _set_interface(self, _interface):
        if isinstance(_interface, pygameyagui.Interface):
            self._interface = _interface
        else:
            raise_type_error(_interface, 'interface', 'pygameyagui.Interface')

    def _set_label(self, _label):
        '''This sets self._label which is a string'''
        if isinstance(_label, str):
            self._label = _label
        else:
            '''If label is not string it will raise an exception'''
            raise TypeError('Label is not string')

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, _enabled):
        if isinstance(_enabled, bool):
            self._enabled = _enabled
        else:
            raise TypeError(f'enabled argument must be of type boolean. Instead, type {type(_enabled)} was given.')

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    @property
    def size(self):
        '''This attribute is a size factor.'''
        return self._size

    @size.setter
    def size(self, _size):
        if isinstance(_size, int) or isinstance(_size, float):
            _size = max(self._min_size, _size)
            if self._max_size is not None:
                _size = min(self._max_size, _size)
            self._size = _size
            self._height_in_px = self._size * ct.WIDGET_STANDARD_SLOT_HEIGHT
        else:
            raise TypeError(f'Size multiplier must be of type int or float. Instead, type {type(_size)} was given.')
        
    def _handle_events(self):
        pass

    def _handle_emitter_button_events(self):
        if self.emitter_rect.collidepoint(self._interface._mouse_pos) and self._enabled:
            for event in self._interface._events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self._emitter = not self._emitter

    def _get_rects(self):
        index = self._toolbox._widgets.index(self)
        if index:
            previous = self._toolbox._widgets[index-1]._slot_rect
        else:
            previous = self._toolbox._body_rect

        self._slot_rect = pygame.Rect(0,0, self._toolbox._body_rect.width, self._height_in_px)
        self._slot_rect.topleft = previous.bottomleft

        pos = self._slot_rect.left + ct.WIDGET_MARGIN_LEFT, self._slot_rect.top + ct.WIDGET_MARGIN_TOP
        size = self._slot_rect.width - (ct.WIDGET_MARGIN_LEFT + ct.WIDGET_MARGIN_RIGHT), self._slot_rect.height - (ct.WIDGET_MARGIN_TOP + ct.WIDGET_MARGIN_BOTTOM), 
        self._widget_rect = pygame.Rect(pos, size)

        return self._slot_rect
        
    def _check_mouse_over(self):
        if self._widget_rect.collidepoint(self._interface._mouse_pos):
            self._mouse_over = True

    def set_as_emitter(self):
        self._emitter = True
