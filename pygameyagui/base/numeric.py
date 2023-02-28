import pygame
from ..include import constants as ct
from ..base.widget import Widget

class Numeric(Widget):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._value = 0
        self._upper_bound = None
        self._lower_bound = None
        self.decimal_places = 0
        self._unit = ''
        self._power = 0

    # TODO: IMPLEMENTAR POTENCIA DE 10
    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, _power):
        if isinstance(_power, int):
            self._power = _power
        else:
            raise_type_error(_power, 'power', 'int')

    @property
    def upper_bound(self):
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, _upper_bound):
        if isinstance(_upper_bound, int) or isinstance(_upper_bound, float):
            self._upper_bound = _upper_bound
            self._update_value()
        else:
            raise TypeError(f'Upper bound must be integer or float. Instead, type {type(_upper_bound)} was given.')       

    @property
    def lower_bound(self):
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, _lower_bound):
        if isinstance(_lower_bound, int) or isinstance(_lower_bound, float):
            self._lower_bound = _lower_bound
            self._update_value()
        else:
            raise TypeError(f'Lower bound must be integer or float. Instead, type {type(_lower_bound)} was given.')       

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, _unit):
        if isinstance(_unit, str):
            self._unit = _unit
        else:
            self._unit = ''

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, _value):
        if self._enabled:
            '''This sets self._value which is a numeric value either int or float.
            It receives value (default is 0) as argument that must be int, float or string'''
            if isinstance(_value, int) or isinstance(_value, float):
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
                raise TypeError(f'Argument {_value} is not string, int or float. Argument type is {type(_value)}.')

    @property
    def decimal_places(self):
        return self._decimal_places

    @decimal_places.setter
    def decimal_places(self, _decimal_places):
        if isinstance(_decimal_places, int):
            self._decimal_places = _decimal_places
        else:
            raise TypeError('Decimal places must be integer.')

    def _update_value(self, _value = None):
        if _value is None:
            _value = self._value
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