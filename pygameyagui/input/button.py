import pygame
from ..include import constants as ct
from ..include import draw
from ..base.widget import Widget

class Button(Widget):
    """This class creates a Button widget.

    :param toolbox: The toolbox that will host the widget.
    :type toolbox: :class:`pygameyagui.Toolbox`
    
    :param label: The text to be shown in the Button widget.
    :type label: str
    """
    def __init__(self, toolbox, label):
        super().__init__(toolbox = toolbox, label = label)
        self._min_size = ct.BUTTON_MIN_SIZE_FACTOR
        self._max_size = ct.BUTTON_MAX_SIZE_FACTOR
        self.size = ct.BUTTON_DEFAULT_SIZE_FACTOR
        self.being_pressed = False
        self.clicked = False
        
    @property
    def clicked(self):
        '''Get or set the the state of a Button (bool).

        Default value is **False** and it is toggled to **True** if there is a pygame.MOUSEBUTTONUP event during the button being clicked.

        Note: This property is always set back to **False** every iteration of the event loop.'''
        return self._clicked

    @clicked.setter
    def clicked(self, _clicked):
        if self._enabled:
            if isinstance(_clicked, bool):
                self._clicked = _clicked
            else:
                raise ValueError(f'clicked expect a boolean as argument. Instead, type {type(_clicked)} was given.')

    def _activate(self):
        if self._enabled:
            self._clicked = True

    def _deactivate(self):
        self._clicked = False

    def _toggle(self):
        if self._enabled:
            self._clicked = not(self._clicked)

    def _show(self):
        bg_color = ct.BUTTON_BG_COLOR
        if self._mouse_over:
            bg_color = ct.BUTTON_BG_HOVER_COLOR
        if self.being_pressed:
            bg_color = ct.BUTTON_BG_CLICKED_COLOR
        
        border_color = ct.BUTTON_BORDER_COLOR
        border_width = ct.BUTTON_BORDER_WIDTH
        border_radius = ct.BUTTON_BORDER_RADIUS
        
        draw._rect(self, self._widget_rect, bg_color = bg_color, border_color = border_color, border_width = border_width, border_radius = border_radius)
        draw._label(self, self._label, 'center', self._widget_rect.center, area=self._widget_rect)
        
    def _handle_events(self):
        self._check_mouse_over()
        self._deactivate()
        for event in self._interface._events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self._widget_rect.collidepoint(self._interface._mouse_pos):
                        if self.being_pressed:
                            self._activate()
                        self.being_pressed = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self._widget_rect.collidepoint(self._interface._mouse_pos):
                        self.being_pressed = True