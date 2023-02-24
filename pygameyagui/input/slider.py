import pygame
from ..include import constants as ct
from ..include import draw
from ..base.interval import Interval

class Slider(Interval):
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._min_size = ct.SLIDER_MIN_SIZE_FACTOR
        self._max_size = ct.SLIDER_MAX_SIZE_FACTOR
        self.size = ct.SLIDER_DEFAULT_SIZE_FACTOR
        self.value = 0
        self._being_dragged = False
        self._can_be_emitter = True

    def _set_appeareance(self):
        self.handle_bg_color = ct.SLIDER_HANDLE_BG_COLOR
        self.handle_border_color = ct.SLIDER_HANDLE_BORDER_COLOR
        self.handle_border_width = ct.SLIDER_HANDLE_BORDER_WIDTH
        self.track_to_left_bg_color = ct.SLIDER_TRACK_TO_LEFT_BG_COLOR    
        self.track_to_right_bg_color = ct.SLIDER_TRACK_TO_RIGHT_BG_COLOR
        self.track_border_color = ct.SLIDER_TRACK_BORDER_COLOR
        self.track_border_width = ct.SLIDER_TRACK_BORDER_WIDTH
        if self._mouse_over:
            self.handle_bg_color = ct.SLIDER_HANDLE_BG_MOUSE_OVER_COLOR
            self.track_to_left_bg_color = ct.SLIDER_TRACK_TO_LEFT_BG_MOUSE_OVER_COLOR
        if self._being_dragged:
            self.handle_bg_color = ct.SLIDER_HANDLE_BG_DRAGGED_COLOR
            self.track_to_left_bg_color = ct.SLIDER_TRACK_TO_LEFT_BG_DRAGGED_COLOR

    def _show_label(self):
        pos = self._widget_rect.inflate(0, -2 * ct.WIDGET_PADDING_TOP).midtop
        self._label_rect = draw._label(self, self._label_with_unit(), 'midtop', pos)

    def _show_track(self):
        track_width = self._widget_rect.width - (ct.WIDGET_PADDING_LEFT + ct.WIDGET_PADDING_RIGHT)
        self.slider_track_rect = pygame.Rect(0, 0, track_width, ct.SLIDER_TRACK_THICKNESS)
        self.slider_track_rect.midleft = self._widget_rect.inflate(-2*ct.WIDGET_PADDING_LEFT,0).midleft
        draw._rect(self, self.slider_track_rect, bg_color = self.track_to_right_bg_color, border_color = self.track_border_color, border_width = self.track_border_width)

        slider_track_left_rect = pygame.Rect(0, 0, 0, ct.SLIDER_TRACK_THICKNESS)
        slider_track_left_rect.midleft = self.slider_track_rect.midleft
        if self._being_dragged:
            dx = self._current_mouse_x - self.slider_track_rect.left
            dx = min(self.slider_track_rect.width, dx)
        else:
            dx = (self._value - self._start) * self.slider_track_rect.width / (self._end - self._start)
        slider_track_left_rect.width = dx
        draw._rect(self, slider_track_left_rect, bg_color =  self.track_to_left_bg_color, border_color = self.track_border_color, border_width = self.track_border_width)

    def _show_handle(self):
        if self._being_dragged:
            dx = self._current_mouse_x - self._reference_mouse_x + self.handle_center_before_dragging
            dx = max(self.slider_track_rect.left, min(self.slider_track_rect.right, dx))
            self.slider_handler_rect = pygame.Rect(0, 0 , ct.SLIDER_HANDLE_SIZE, ct.SLIDER_HANDLE_SIZE)
            self.slider_handler_rect.center = dx, self.slider_track_rect.centery
        else:
            dx = (self._value - self._start) * self.slider_track_rect.width / (self._end - self._start)
            self.slider_handler_rect = pygame.Rect(0, 0 , ct.SLIDER_HANDLE_SIZE, ct.SLIDER_HANDLE_SIZE)
            self.slider_handler_rect.center = self.slider_track_rect.left + dx, self.slider_track_rect.centery
            self.handle_center_before_dragging = self.slider_handler_rect.centerx
        
        center = self.slider_handler_rect.center
        radius = ct.SLIDER_HANDLE_RADIUS
        draw._circle(self, center, radius, bg_color = self.handle_bg_color, border_color = self.handle_border_color, border_width = self.handle_border_width)

    def _show_handle_label(self):
        bg_color = ct.SLIDER_HANDLE_BG_COLOR        
        if self._being_dragged:
            _label_value = self._value_to_string(self._value_from_handle())
        else:
            _label_value = self._value_to_string()

        pos = self.slider_handler_rect.inflate(0,2).midbottom
        self.label_rect = draw._label(self, _label_value, 'midtop', pos, limits=self.slider_track_rect)

    def _show_limits_label(self):
        pos_label_start = self.slider_track_rect.left, self.label_rect.centery
        label_start_rect = draw._label(self, str(self._start), 'midleft', pos_label_start, just_get_rect=True)
        pos_label_end = self.slider_track_rect.right, self.label_rect.centery
        label_end_rect = draw._label(self, str(self._end), 'midright', pos_label_end, just_get_rect=True)

        if not label_start_rect.colliderect(self.label_rect):
            draw._label(self, str(self._start), 'midleft', pos_label_start)
        if not label_end_rect.colliderect(self.label_rect):
            draw._label(self, str(self._end), 'midright', pos_label_end)

    def _show(self):
        self._set_appeareance()
        self._show_label()
        self._show_track()   
        self._show_handle()
        self._show_handle_label()
        self._show_limits_label()
        draw._widget_border(self)

    def _handle_events(self):
        self._check_mouse_over()
        for event in self._interface._events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.slider_handler_rect.collidepoint(self._interface._mouse_pos):
                        self._being_dragged = True
                        self._current_mouse_x = pygame.mouse.get_pos()[0]
                        self._reference_mouse_x = pygame.mouse.get_pos()[0]

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self._being_dragged:
                    self._being_dragged = False
                    self._verify_position()

            if event.type == pygame.MOUSEMOTION:
                if self._being_dragged:
                    self._current_mouse_x = pygame.mouse.get_pos()[0]