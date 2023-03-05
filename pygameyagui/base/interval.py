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
        '''Get the step (int or float).
        
        Default value is **1**.
        '''
        return self._step

    @property
    def range(self):        
        '''Get the list with all values in the range (list).
        
        Default value is a integer range from 0 to 100 with step 1.
        '''
        return self._range
    
    @property
    def color_limits(self):  
        '''Get a pair of values for the color limits (tuple).
        
        Default value is **None**.

        If {py:attr}`pygameyagui.Interval.use_color_limits` is set to True, then the interval will be divided in three zones:
        
        Green Zone is for values between lower_bound and color_limits[0].

        Yellow Zone is for values between color_limits[0] and color_limits[1].

        Red Zone is for values between color_limits[1] and upper_bound.
        '''
        return self._color_limits

    @property
    def use_color_limits(self):
        '''Get or set if the interval will use color limits (bool).
        
        Default value is **False**.

        See also: :attr:`pygameyagui.Interval.color_limits`
        '''
        return self._use_color_limits
    
    @use_color_limits.setter
    def use_color_limits(self, _use):
        if not isinstance(_use, bool):
            raise_type_error(_use, 'use_color_limts', 'bool')
        self._use_color_limits = _use

    def set_limits(self, lower_bound, upper_bound, step, color_limits=None):
        '''Use this to set the interval properties.

        :param lower_bound: The value to start the interval
        :type lower_bound: int or float

        :param upper_bound: The value to end the interval
        :type upper_bound: int or float

        :param step: The separation between two values on the interval
        :type step: int or float

        :param color_limits: A pair of values to create color zones in the interval
        :type color_limits: tuple

        :rtype: NoneType
        '''
        if self._is_integer_only:
            if not isinstance(lower_bound, int):
                raise_type_error(lower_bound, 'lower_bound', 'int')
            if not isinstance(upper_bound, int):
                raise_type_error(upper_bound, 'upper_bound', 'int')
            if not isinstance(step, int):
                raise_type_error(step, 'step', 'int')
        else:
            if not (isinstance(lower_bound, int) or isinstance(lower_bound, float)):
                raise_type_error(lower_bound, 'lower_bound', 'int or float')
            if not (isinstance(upper_bound, int) or isinstance(upper_bound, float)):
                raise_type_error(upper_bound, 'upper_bound', 'int or float')
            if not (isinstance(step, int) or isinstance(step, float)):
                raise_type_error(step, 'step', 'int or float')

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

                if lower_bound >= _green_limit:
                    raise_value_error(f'lower_bound value ({lower_bound}) should be smaller than color_limits[0] ({_green_limit}).')
                if _green_limit >= _yellow_limit:
                    raise_value_error(f'color_limits[0] ({_green_limit}) should be smaller than color_limits[1] ({_yellow_limit}).')
                if _yellow_limit >= upper_bound:
                    raise_value_error(f'color_limits[1] ({_yellow_limit}) should be smaller than upper_bound value ({upper_bound}).')

                self._color_limits = color_limits
            else:
                if lower_bound >= upper_bound:
                    raise_value_error(f'lower_bound ({lower_bound}) should be smaller than upper_bound value ({upper_bound}).')

        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._step = step
        if isinstance(lower_bound, float) or isinstance(lower_bound, float) or isinstance(step, float):
            self._range = self._float_range(lower_bound, upper_bound, step)
        else:
            self._range = self._int_range(lower_bound, upper_bound, step)

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