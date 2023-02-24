import pygame
from ..include import constants as ct
from ..base.numeric import Numeric

class Interval(Numeric):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._use_color_limits = False
        self._start = 0
        self._end = 100
        self._step = 1
        self._range = list(range(0, 100, 1))
        self._range.append(100)
        self._green_limit = 50
        self._yellow_limit = 80
        self._is_integer_only = False

    @property
    def upper_bound(self):
        return None

    @upper_bound.setter
    def upper_bound(self, _upper_bound):
        _type = str(type(self)).split('.')[-1].replace("'","").replace(">","")
        raise TypeError(f'Upper bound must not be used as attribute of a type {_type}. Instead, I might want to use the attribute \'limits\' to set up the limits of an interval.')       

    @property
    def lower_bound(self):
        return None

    @lower_bound.setter
    def lower_bound(self, _lower_bound):
        _type = str(type(self)).split('.')[-1].replace("'","").replace(">","")
        raise TypeError(f'Lower bound must not be used as attribute of a type {_type}. Instead, I might want to use the attribute \'limits\' to set up the limits of an interval.')       

    def _update_value(self, _value = None):
        if _value is None:
            _value = self._value
        if self._emitter and not self._value == _value:
            self._interface._emitting = self
        self._value = max(self._start, min(self._end, _value))

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def step(self):
        return self._step

    @property
    def range(self):
        return self._range
    
    @property
    def green_limit(self):
        return self._green_limit

    @property
    def yellow_limit(self):
        return self._yellow_limit

    @property
    def limits(self):
        return self._start, self._end

    @limits.setter
    def limits(self, _limits):
        limit_keys = ['start', 'end', 'step', 'green_limit', 'yellow_limit']
        if not isinstance(_limits, dict):
            raise TypeError(f'Argument of limits must be a dictionary with possible keys: {limit_keys}.')
        
        for key in _limits.keys():
            if key not in limit_keys:
                raise ValueError(f'Possible limit keys: {limit_keys}.')

        if 'start' in _limits.keys():
            start = _limits['start']
        else:
            start = self.start

        if 'end' in _limits.keys():
            end = _limits['end']
        else:
            end = self.end

        if 'step' in _limits.keys():
            step = _limits['step']
        else:
            step = self.step

        if self._is_integer_only:
            if not isinstance(start, int):
                raise TypeError(f'Start value must be integer. Instead, type {type(start)} was given.')

            if not isinstance(end, int):
                raise TypeError(f'End value must be integer. Instead, type {type(end)} was given.')

            if not isinstance(step, int):
                raise TypeError(f'Step value must be integer. Instead, type {type(step)} was given.')
        else:
            if not (isinstance(start, int) or isinstance(start, float)):
                raise TypeError(f'Start value must be integer or float. Instead, type {type(start)} was given.')

            if not (isinstance(end, int) or isinstance(end, float)):
                raise TypeError(f'End value must be integer or float. Instead, type {type(end)} was given.')

            if not (isinstance(step, int) or isinstance(step, float)):
                raise TypeError(f'Step value must be integer or float. Instead, type {type(step)} was given.')

        if self._use_color_limits:
            if 'green_limit' in _limits.keys():
                green_limit = _limits['green_limit']
            else:
                green_limit = self.green_limit

            if 'yellow_limit' in _limits.keys():
                yellow_limit = _limits['yellow_limit']
            else:
                yellow_limit = self.yellow_limit

            if self._is_integer_only:
                if not isinstance(green_limit, int):
                    raise TypeError(f'Green limit value must be integer. Instead, type {type(green_limit)} was given.')

                if not isinstance(yellow_limit, int):
                    raise TypeError(f'Yellow limit must be integer. Instead, type {type(yellow_limit)} was given.')
            else:
                if not (isinstance(green_limit, int) or isinstance(green_limit, float)):
                    raise TypeError(f'Green limit value must be integer or float. Instead, type {type(green_limit)} was given.')

                if not (isinstance(yellow_limit, int) or isinstance(yellow_limit, float)):
                    raise TypeError(f'Yellow limit must be integer or float. Instead, type {type(yellow_limit)} was given.')

            if start >= green_limit:
                raise ValueError(f'Start value ({start}) should be smaller than green limit ({green_limit}).')
            if green_limit >= yellow_limit:
                raise ValueError(f'Green limit ({green_limit}) should be smaller than yellow limit ({yellow_limit}).')
            if yellow_limit >= end:
                raise ValueError(f'Yellow limit ({yellow_limit}) should be smaller than end value ({end}).')
        else:
            if start >= end:
                raise ValueError(f'Yellow limit ({yellow_limit}) should be smaller than end value ({end}).')

        self._start = start
        self._end = end
        self._step = step
        if isinstance(start, float) or isinstance(end, float) or isinstance(step, float):
            _range = self._float_range(start, step, end)
        else:
            _range = list(range(start, end, step))
        _range.append(end)
        self._range = _range
        
        if self._use_color_limits:
            self._green_limit = green_limit
            self._yellow_limit = yellow_limit

        self._update_value()

    def _float_range(self, start, end, step):
        _range = []
        value = start
        while value < end:
            _range.append(value)
            value += step

        return _range