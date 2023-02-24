import pygame
from ..include import constants as ct
from ..include import draw
from ..base.widget import Widget

class Label(Widget):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._alignment = 'center'
        self._min_size = ct.LABEL_MIN_SIZE_FACTOR
        self._max_size = ct.LABEL_MAX_SIZE_FACTOR
        self.size = ct.LABEL_DEFAULT_SIZE_FACTOR

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, _alignment):
        '''This sets the self._alignment which can only be left, center or right'''
        if _alignment in ['left', 'center', 'right']:
            self._alignment = _alignment
        else:
            raise ValueError('Argument can only be left, center or right')

    def _show_label(self):
        if self._alignment == 'center':
            pos_ref = 'center'
            pos = self._widget_rect.center
        elif  self._alignment == 'left':
            pos_ref = 'midleft'
            pos = self._widget_rect.inflate(-ct.WIDGET_PADDING_LEFT, 0).midleft
        elif  self._alignment == 'right':
            pos_ref = 'midright'
            pos = self._widget_rect.inflate(-ct.WIDGET_PADDING_RIGHT, 0).midright
        
        draw._label(self, self._label, pos_ref, pos)

    def _show(self):
        self._show_label()
        draw._widget_border(self)
        