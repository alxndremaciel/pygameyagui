import pygame
from ..include import constants as ct
from ..input.slider import Slider

class SliderInt(Slider):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)

    def _value_from_handle(self):
        _value = self.slider_handler_rect.centerx - self.slider_track_rect.left
        _value /= self.slider_track_rect.width
        _value *= (self._end - self._start)
        _value += self._start

        for index, each in enumerate(self._range):
            if each > _value:
                break

        previous = self._range[index-1]
        delta_1 = each - _value
        delta_2 = _value - previous

        if delta_1 < delta_2:
            return each
        else:
            return previous

    def _verify_position(self):
        self.value = self._value_from_handle()