import pygame
from ..include import constants as ct
from ..include import draw, tools
from ..base.interval import Interval

class TankMeter(Interval):
    """This class creates a TankMeter widget.

    :param toolbox: The toolbox that will host the widget.
    :type toolbox: :class:`pygameyagui.Toolbox`
    
    :param label: The text to be shown in the TankMeter widget.
    :type label: str
    """
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._min_size = ct.TANKMETER_MIN_SIZE_FACTOR
        self._max_size = ct.TANKMETER_MAX_SIZE_FACTOR
        self.size = ct.TANKMETER_DEFAULT_SIZE_FACTOR
        
        '''By default a Tank Meter uses color limits and show all marks'''
        self._use_color_limits = True
        self.show_all_marks()

    def hide_extreme_marks(self):
        """Use this to hide the tick marks and labels for the lower_bound and upper_bound values.
        
        See also: :attr:`pygameyagui.Numeric.lower_bound` and :attr:`pygameyagui.Numeric.upper_bound`
        
        :rtype: NoneType"""
        self._show_extreme_marks = False

    def hide_color_marks(self):
        """Use this to hide the tick marks and labels for the color_limits values.
        
        See also: :attr:`pygameyagui.Inteval.color_limits`
        
        :rtype: NoneType"""
        self._show_color_marks = False

    def hide_all_marks(self):
        """Use this to hide all tick marks and labels.
        
        :rtype: NoneType"""
        self._show_extreme_marks = False
        self._show_color_marks = False

    def show_all_marks(self):
        """Use this to show all tick marks and labels.
        
        :rtype: NoneType"""
        self._show_extreme_marks = True
        self._show_color_marks = True

    def _show(self):
        self._show_label()
        self._setup_tank()
        self._show_tank()
        self._show_level_marks()
        self._show_meter_value()

        draw._widget_border(self)

    def _show_label(self):
        pos = self._widget_rect.inflate(0, -2 * ct.WIDGET_PADDING_TOP).midtop
        self._label_rect = draw._label(self, self._label_with_unit(), 'midtop', pos)

    def _setup_tank(self):
        '''Decide if whether color limits is to be used or not'''
        if self._use_color_limits:
            '''Decide what is the color of the meter based on the _value compared to _green_limit and _color_limits[1]'''
            if self._value < self._color_limits[0]:
                self._meter_color = ct.TANKMETER_BG_GREEN_COLOR
            elif self._value < self._color_limits[1]:
                self._meter_color = ct.TANKMETER_BG_YELLOW_COLOR
            else:
                self._meter_color = ct.TANKMETER_BG_RED_COLOR
        else:
            self._meter_color = ct.TANKMETER_BG_GREEN_COLOR

        self._tank_width = ct.TANKMETER_WIDTH
        self._tank_height = self._widget_rect.bottom - self._label_rect.bottom - 2 * ct.TANKMETER_MARGIN
        self._tank_rect = pygame.Rect(0,0,self._tank_width,self._tank_height)
        self._tank_rect.bottomright = self._widget_rect.inflate(-2 * ct.TANKMETER_MARGIN, -2 * ct.TANKMETER_MARGIN).bottomright
        meter_top = tools.lerp(self._tank_rect, y=self._value, y_limits=self.limits)
        self._meter_rect = pygame.Rect(0,0,self._tank_width,self._tank_rect.bottom-meter_top)
        self._meter_rect.bottomleft = self._tank_rect.bottomleft

    def _show_tank(self):
        border_color = ct.TANKMETER_BORDER_COLOR
        border_width = ct.TANKMETER_BORDER_WIDTH
        border_radius = ct.TANKMETER_BORDER_RADIUS
        hack_color = ct.TOOLBOX_BODY_BG_COLOR
        hack_width = ct.TANKMETER_BORDER_HACK_WIDTH
        hack_inflate = ct.TANKMETER_BORDER_HACK_INFLATE
        draw._rect(self, self._tank_rect, bg_color = ct.COLOR_WHITE)
        draw._rect(self, self._meter_rect, bg_color = self._meter_color)
        pygame.draw.rect(self._surface, hack_color, self._tank_rect.inflate(hack_inflate, hack_inflate), width = hack_width, border_radius = border_radius)
        draw._rect(self, self._tank_rect.inflate(border_width, border_width), border_color = border_color, border_width = border_width, border_radius = border_radius)

    def _show_level_marks(self):
        self._marks_rect = pygame.Rect(0,self._tank_rect.top,0.5*self._tank_width,self._tank_height)
        self._marks_rect.right = self._tank_rect.inflate(ct.TANKMETER_MARGIN,0).left

        # '''This function is responsible for drawing the marks on the left side of the tank'''
        if self._show_extreme_marks:
            start = self._marks_rect.bottomleft
            end = self._marks_rect.bottomright
            draw._line(self, start, end, ct.TANKMETER_BORDER_COLOR, ct.TANKMETER_MARK_WIDTH)
            pos = self._marks_rect.inflate(ct.TANKMETER_MARGIN,0).bottomleft
            draw._label(self, self._value_to_string(self._lower_bound), 'midright', pos)

            start = self._marks_rect.topleft
            end = self._marks_rect.topright
            draw._line(self, start, end, ct.TANKMETER_BORDER_COLOR, ct.TANKMETER_MARK_WIDTH)
            pos = self._marks_rect.inflate(ct.TANKMETER_MARGIN,0).topleft
            draw._label(self, self._value_to_string(self._upper_bound), 'midright', pos)

        if self._show_color_marks and self._use_color_limits:
            x_limits = self._marks_rect.left, self._marks_rect.right
            start = self._marks_rect.left, tools.lerp(self._marks_rect, y = self._color_limits[0], y_limits = self.limits)
            end = self._marks_rect.right, tools.lerp(self._marks_rect, y = self._color_limits[0], y_limits = self.limits)
            draw._line(self, start, end, ct.TANKMETER_BORDER_COLOR, ct.TANKMETER_MARK_WIDTH)
            pos = self._marks_rect.inflate(ct.TANKMETER_MARGIN,0).left, start[1]
            draw._label(self, self._value_to_string(self._color_limits[0]), 'midright', pos)
            x_limits = self._marks_rect.left, self._marks_rect.right
            start = self._marks_rect.left, tools.lerp(self._marks_rect, y = self._color_limits[1], y_limits = self.limits)
            end = self._marks_rect.right, tools.lerp(self._marks_rect, y = self._color_limits[1], y_limits = self.limits)
            draw._line(self, start, end, ct.TANKMETER_BORDER_COLOR, ct.TANKMETER_MARK_WIDTH)
            pos = self._marks_rect.inflate(ct.TANKMETER_MARGIN,0).left, start[1]
            draw._label(self, self._value_to_string(self._color_limits[1]), 'midright', pos)

    def _show_meter_value(self):
        pos = self._widget_rect.inflate(-2*ct.TANKMETER_MARGIN,0).midleft
        draw._label(self, self._value_to_string(), 'midleft', pos, color= self._meter_color, font_type = 'big')
