import pygame
from ..include import constants as ct
from ..include.error import raise_type_error, raise_value_error
from ..base.numeric import Numeric

class Interval(Numeric):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._is_integer_only = False
        self._lower_bound = 0
        self._upper_bound = 100
        self._step = 1
        self._range = self._int_range(self._lower_bound, self._upper_bound, self._step)
        self._use_color_limits = False
        self._color_limits = None

    @property
    def step(self):
        return self._step

    @property
    def range(self):
        return self._range
    
    @property
    def color_limits(self):
        return self._color_limits

    def set_limits(self, _lower_bound, _upper_bound, _step, color_limits=None):       
        if self._is_integer_only:
            if not isinstance(_lower_bound, int):
                raise_type_error(_lower_bound, 'lower_bound', 'int')
            if not isinstance(_upper_bound, int):
                raise_type_error(_upper_bound, 'upper_bound', 'int')
            if not isinstance(_step, int):
                raise_type_error(_step, 'step', 'int')
        else:
            if not (isinstance(_lower_bound, int) or isinstance(_lower_bound, float)):
                raise_type_error(_lower_bound, 'lower_bound', 'int or float')
            if not (isinstance(_upper_bound, int) or isinstance(_upper_bound, float)):
                raise_type_error(_upper_bound, 'upper_bound', 'int or float')
            if not (isinstance(_step, int) or isinstance(_step, float)):
                raise_type_error(_step, 'step', 'int or float')

        if self._use_color_limits:
            if color_limits is not None:
                if not isinstance(color_limits, tuple):
                    raise_type_error(color_limits, 'color_limits', 'tuple')
                if len(color_limits) != 2:
                    raise_value_error(f'color_limits needs to be a tuple of length 2. Insted, a tuple of length {len(tuple)} was given.')
                
                _green_limit, _yellow_limit = color_limits
                
                if self._is_integer_only:
                    if not isinstance(_green_limit, int):
                        raise_type_error(_green_limit, 'color_limits[0]', 'int')
                    if not isinstance(_yellow_limit, int):
                        raise_type_error(_yellow_limit, 'color_limits[1]', 'int')
                else:
                    if not (isinstance(_green_limit, int) or isinstance(_green_limit, float)):
                        raise_type_error(_green_limit, 'color_limits[0]', 'int or float')
                    if not (isinstance(_yellow_limit, int) or isinstance(_yellow_limit, float)):
                        raise_type_error(_yellow_limit, 'color_limits[1]', 'int or float')

                if _lower_bound >= _green_limit:
                    raise_value_error(f'lower_bound value ({_lower_bound}) should be smaller than color_limits[0] ({_green_limit}).')
                if _green_limit >= _yellow_limit:
                    raise_value_error(f'color_limits[0] ({_green_limit}) should be smaller than color_limits[1] ({_yellow_limit}).')
                if _yellow_limit >= _upper_bound:
                    raise_value_error(f'color_limits[1] ({_yellow_limit}) should be smaller than upper_bound value ({_upper_bound}).')

                self._color_limits = color_limits
            else:
                if _lower_bound >= _upper_bound:
                    raise_value_error(f'lower_bound ({_lower_bound}) should be smaller than upper_bound value ({_upper_bound}).')

        self._lower_bound = _lower_bound
        self._upper_bound = _upper_bound
        self._step = _step
        if isinstance(_lower_bound, float) or isinstance(_lower_bound, float) or isinstance(_step, float):
            self._range = self._float_range(_lower_bound, _upper_bound, _step)
        else:
            self._range = self._int_range(_lower_bound, _upper_bound, _step)

        self._update_value()

    def _int_range(self, _lower_bound, _upper_bound, _step):
        _range = list(range(_lower_bound, _upper_bound, _step))
        _range.append(_upper_bound)
        return _range

    def _float_range(self, _lower_bound, _upper_bound, _step):
        _range = []
        _value = _lower_bound
        while _value < _upper_bound:
            _range.append(_value)
            _value += _step
        _range.append(_upper_bound)
        return _range