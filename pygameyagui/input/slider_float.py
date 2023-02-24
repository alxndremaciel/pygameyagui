import pygame
from ..include import constants as ct
from ..input.slider import Slider

class SliderFloat(Slider):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self.decimal_places = 1

    def _value_from_handle(self):
        _value = self.slider_handler_rect.centerx - self.slider_track_rect.left
        _value /= self.slider_track_rect.width
        _value *= (self._end - self._start)
        _value += self._start
        
        return round(_value, self._decimal_places) 

    def _verify_position(self):
        self.value = self._value_from_handle()