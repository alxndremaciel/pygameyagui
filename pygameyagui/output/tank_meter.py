import pygame
from ..include import constants as ct
from ..include import draw, tools
from ..base.interval import Interval

class TankMeter(Interval):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._min_size = ct.TANK_MIN_SIZE_FACTOR
        self._max_size = ct.TANK_MAX_SIZE_FACTOR
        self.size = ct.TANK_DEFAULT_SIZE_FACTOR
        
        '''By default a Tank Meter uses color limits and show all marks'''
        self._use_color_limits = True
        self.show_all_marks()

    def hide_extreme_marks(self):
        self._show_extreme_marks = False

    def hide_color_marks(self):
        self._show_color_marks = False

    def hide_all_marks(self):
        self._show_extreme_marks = False
        self._show_color_marks = False

    def show_all_marks(self):
        self._show_extreme_marks = True
        self._show_color_marks = True

    def no_color_limits(self):
        self._use_color_limits = False

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
            '''Decide what is the color of the meter based on the _value compared to _green_limit and _yellow_limit'''
            if self._value < self._green_limit:
                self._meter_color = ct.TANK_BG_GREEN_COLOR
            elif self._value < self._yellow_limit:
                self._meter_color = ct.TANK_BG_YELLOW_COLOR
            else:
                self._meter_color = ct.TANK_BG_RED_COLOR
        else:
            self._meter_color = ct.TANK_BG_GREEN_COLOR

        self._tank_width = ct.TANK_WIDTH
        self._tank_height = self._widget_rect.bottom - self._label_rect.bottom - 2 * ct.TANK_MARGIN
        self._tank_rect = pygame.Rect(0,0,self._tank_width,self._tank_height)
        self._tank_rect.bottomright = self._widget_rect.inflate(-2 * ct.TANK_MARGIN, -2 * ct.TANK_MARGIN).bottomright
        meter_top = tools.lerp(self._tank_rect, y=self._value, y_limits=self.limits)
        self._meter_rect = pygame.Rect(0,0,self._tank_width,self._tank_rect.bottom-meter_top)
        self._meter_rect.bottomleft = self._tank_rect.bottomleft

    def _show_tank(self):
        border_color = ct.TANK_BORDER_COLOR
        border_width = ct.TANK_BORDER_WIDTH
        border_radius = ct.TANK_BORDER_RADIUS
        hack_color = ct.TOOLBOX_BODY_BG_COLOR
        hack_width = ct.TANK_BORDER_HACK_WIDTH
        hack_inflate = ct.TANK_BORDER_HACK_INFLATE
        draw._rect(self, self._tank_rect, bg_color = ct.COLOR_WHITE)
        draw._rect(self, self._meter_rect, bg_color = self._meter_color)
        pygame.draw.rect(self._surface, hack_color, self._tank_rect.inflate(hack_inflate, hack_inflate), width = hack_width, border_radius = border_radius)
        draw._rect(self, self._tank_rect.inflate(border_width, border_width), border_color = border_color, border_width = border_width, border_radius = border_radius)

    def _show_level_marks(self):
        self._marks_rect = pygame.Rect(0,self._tank_rect.top,0.5*self._tank_width,self._tank_height)
        self._marks_rect.right = self._tank_rect.inflate(ct.TANK_MARGIN,0).left

        # '''This function is responsible for drawing the marks on the left side of the tank'''
        if self._show_extreme_marks:
            start = self._marks_rect.bottomleft
            end = self._marks_rect.bottomright
            draw._line(self, start, end, ct.TANK_BORDER_COLOR, ct.TANK_MARK_WIDTH)
            pos = self._marks_rect.inflate(ct.TANK_MARGIN,0).bottomleft
            draw._label(self, self._value_to_string(self._start), 'midright', pos)

            start = self._marks_rect.topleft
            end = self._marks_rect.topright
            draw._line(self, start, end, ct.TANK_BORDER_COLOR, ct.TANK_MARK_WIDTH)
            pos = self._marks_rect.inflate(ct.TANK_MARGIN,0).topleft
            draw._label(self, self._value_to_string(self._end), 'midright', pos)

        if self._show_color_marks and self._use_color_limits:
            x_limits = self._marks_rect.left, self._marks_rect.right
            start = self._marks_rect.left, tools.lerp(self._marks_rect, y = self._green_limit, y_limits = self.limits)
            end = self._marks_rect.right, tools.lerp(self._marks_rect, y = self._green_limit, y_limits = self.limits)
            draw._line(self, start, end, ct.TANK_BORDER_COLOR, ct.TANK_MARK_WIDTH)
            pos = self._marks_rect.inflate(ct.TANK_MARGIN,0).left, start[1]
            draw._label(self, self._value_to_string(self._green_limit), 'midright', pos)
            x_limits = self._marks_rect.left, self._marks_rect.right
            start = self._marks_rect.left, tools.lerp(self._marks_rect, y = self._yellow_limit, y_limits = self.limits)
            end = self._marks_rect.right, tools.lerp(self._marks_rect, y = self._yellow_limit, y_limits = self.limits)
            draw._line(self, start, end, ct.TANK_BORDER_COLOR, ct.TANK_MARK_WIDTH)
            pos = self._marks_rect.inflate(ct.TANK_MARGIN,0).left, start[1]
            draw._label(self, self._value_to_string(self._yellow_limit), 'midright', pos)

    def _show_meter_value(self):
        pos = self._widget_rect.inflate(-2*ct.TANK_MARGIN,0).midleft
        draw._label(self, self._value_to_string(), 'midleft', pos, color= self._meter_color, font_type = 'big')
