import pygame
from ..include import constants as ct
from ..include.error import raise_type_error, raise_value_error
from ..base.widget import Widget

class Numeric(Widget):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._value = 0
        self._upper_bound = None
        self._lower_bound = None
        self.decimal_places = 0
        self._unit = ''

    @property
    def upper_bound(self):        
        '''Get or set the upper bound limit (int or float).
        
        Default value is **None** and this bound will be ignored if not set to a valid value. It should not be smaller than (:attr:`pygameyagui.Numeric.lower_bound`). The current value of the widget will be automatically forced to comply.
        '''
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, _upper_bound):
        if not (isinstance(_upper_bound, int) or isinstance(_upper_bound, float)):
            raise_type_error(_upper_bound, 'upper_bound', 'integer or float')
        if self._lower_bound is not None and _upper_bound < self._lower_bound:
            raise_value_error(f'_upper_bound should not be smaller than _lower_bound. Current _lower_bound is {self._lower_bound}')
        self._upper_bound = _upper_bound
        self._update_value()   

    @property
    def lower_bound(self):        
        '''Get or set the lower bound limit (int or float).
        
        Default value is **None** and this bound will be ignored if not set to a valid value. It should not be bigger than (:attr:`pygameyagui.Numeric.upper_bound`). The current value of the widget will be automatically forced to comply.
        '''
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, _lower_bound):
        if not (isinstance(_lower_bound, int) or isinstance(_lower_bound, float)):
            raise_type_error(_lower_bound, 'lower_bound', 'integer or float')
        if self._upper_bound is not None and _lower_bound > self._upper_bound:
            raise_value_error(f'_lower_bound should not be bigger than _upper_bound. Current _upper_bound is {self._upper_bound}')

        self._lower_bound = _lower_bound
        self._update_value()
        
    @property
    def unit(self):        
        '''Get or set the quantity unit (str).

        Default value is a empty string.
        '''
        return self._unit

    @unit.setter
    def unit(self, _unit):
        if isinstance(_unit, str):
            self._unit = _unit
        else:
            self._unit = ''

    @property
    def value(self):
        '''Get (int or float) or set (int, float or str) the value.
        
        Default value is 0 (int). It will be forced to comply to upper and lower bounds if they are set.

        See also: :attr:`pygameyagui.Numeric.upper_bound` and :attr:`pygameyagui.Numeric.lower_bound`
        '''
        return self._value

    @value.setter
    def value(self, _value):
        if self._enabled:
            if isinstance(_value, int) or isinstance(_value, float):
                '''Enforces specific update method'''
                self._update_value(_value)
            elif isinstance(_value, str):
                '''It will try to cast string to int and if it fails it will try casting to float'''
                try:
                    self._update_value(int(_value))
                except:
                    try:
                        self._update_value(float(_value))   
                    except:
                        '''If value is string but can not be cast to int or float it will raise an exception'''
                        raise ValueError(f'Argument {_value} is string but can be neither cast to int nor to float')
            else:
                '''If value is not int, float or string it will raise an exception'''
                raise_type_error(_value, 'value', 'int, float or str')

    @property
    def decimal_places(self):
        '''Get or set the number of decimal places (int >= 0).
        
        Default value is 0 (int). This property influences the string representation of the numeric value. It does not influences or rounds the value for calculations.
        '''
        return self._decimal_places

    @decimal_places.setter
    def decimal_places(self, _decimal_places):
        if isinstance(_decimal_places, int):
            self._decimal_places = _decimal_places
        else:
            raise_type_error(_decimal_places, 'decimal_places', 'int')

    def _update_value(self, _value = None):
        if _value is None:
            _value = self._value
        if self._emitter and not self._value == _value:
            self._interface._emitting = self
        if self.upper_bound is not None:
            _value = min(self.upper_bound, _value)
        if self.lower_bound is not None:
            _value = max(self.lower_bound, _value)
        self._value = _value
        return _value

    def _label_with_unit(self, _label = None, _unit = None):
        if _label is None:
            _label = self._label
        if _unit is None:
            _unit = self._unit

        if _unit:
            return f'{_label} ({_unit})'
            
        return _label

    def _value_to_string(self, _value = None, _decimal_places = None):
        '''This function returns a formated string representation of a _value.
        The _value can be passed or assumed to be self._value.'''
        if _value is None:
            _value = self._value

        '''The number of decimal places can be passed or assumed to be self._decimal_places'''
        if _decimal_places is None:
            _decimal_places = self._decimal_places

        if _decimal_places < 0:
            _decimal_places = 0

        if isinstance(_decimal_places, float):
            _decimal_places = int(_decimal_places)

        '''Formating will depende on the _value type or/and decimal_places.'''
        if isinstance(_value, int):
            return str(_value)
        elif isinstance(_value, float):
            _format = '{:.'+str(_decimal_places)+'f}'
            return _format.format(_value)