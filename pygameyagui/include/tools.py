import pygame
from ..include import constants as ct
from ..include.error import raise_type_error, raise_value_error

def lerp(rect,
         x = None, x_limits = None,
         y = None, y_limits = None):

    pixel_x, pixel_y = None, None
    x0, x1, y0, y1 = None, None, None, None

    if x is not None:
        if isinstance(x_limits, tuple) and len(x_limits) == 2:
            x0, x1 = x_limits
            if not (isinstance(x0, int) or isinstance(x0, float)):
                raise_value_error('Bad definition of x_limits')
            if not x1 - x0:
                raise_value_error('x0 - x1 is zero.')
        else:
            raise_value_error('Bad definition of x_limits')

        pixel_x0 = rect.left
        pixel_x1 = rect.right
        pixel_x = int((pixel_x0*(x1-x)+pixel_x1*(x-x0))/(x1-x0))

    if y is not None:
        if isinstance(y_limits, tuple) and len(y_limits) == 2:
            y0, y1 = y_limits
            if not (isinstance(y0, int) or isinstance(y0, float)):
                raise_value_error('Bad definition of y_limits')
            if not y1 - y0:
                raise_value_error('y0 - y1 is zero.')
        else:
            raise_value_error('Bad definition of y_limits')

        pixel_y0 = rect.bottom
        pixel_y1 = rect.top
        pixel_y = int((pixel_y0*(y1-y)+pixel_y1*(y-y0))/(y1-y0))

    if pixel_x is not None and pixel_y is not None:
        return pixel_x, pixel_y
    elif pixel_x is not None:
        return pixel_x
    elif pixel_y is not None:
        return pixel_y
    else:
        return None