"""Pygame-YaGUI is Yet another GUI for Pygame."""

import importlib.metadata
__version__ = importlib.metadata.version(__package__ or __name__)

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys
import time
import pygame
from .include import constants as ct
from .include import draw
from .include.error import raise_type_error, raise_value_error
from .base.widget import Widget
from .base.variables import Variable
from .input.button import Button
from .input.button_icon import ButtonIcon
from .input.menu_item import MenuItem
from .input.checkbox import CheckBox
from .input.radio_button import RadioButton
from .input.slider_int import SliderInt
from .input.slider_float import SliderFloat
from .input.numeric_input import NumericInput
from .output.label import Label
from .output.numeric_output import NumericOutput
from .output.tank_meter import TankMeter
from .graph.sparkline import SparkLine
from .base.toolbox import Toolbox

class Interface:
    """This is the class that has to be instantiated once and only once to
    create the interface object.
    
    It will configure the FPS rate, window dimensions, status bar, controls and background color. It should be called after pygame.init() and uses pygame.display.set_mode() and pygame.time.Clock() to configure pygame environment.
    
    :param fps: Frames Per Second rate to update the screen. It does not influence the rate of simulation (IPS - Iteration per Seconds) which is only limited by the processing power of the CPU.
    :type fps: int [>0] (optional)
    
    :param window_width: The window width in pixelsels.
    :type window_width: int [>0] (optional)
    
    :param window_height: The window height in pixelsels.
    :type window_height: int [>0] (optional)

    :param show_status_bar: Flag to show or hide the status bar.
    :type show_status_bar: bool (optional)

    :param show_controls: Flag to show or hide the controls at the top right corner of the screen. Buttons for pause/resume, reload simulations and toolboxes (:class:`pygameyagui.Toolbox`) list is located at the controls.
    :type show_controls: bool (optional)

    :param screen_bg_color: Screen background color in the format (R,G,B).
    :type screen_bg_color: tuple (0<R,G,B<255) (optional)
    """
    def __init__(self,
                 fps = ct.INTERFACE_CONFIG_FPS,
                 window_width = ct.INTERFACE_CONFIG_WINDOW_WIDTH,
                 window_height = ct.INTERFACE_CONFIG_WINDOW_HEIGHT,
                 show_status_bar = ct.INTERFACE_CONFIG_SHOW_STATUS_BAR,
                 show_controls = ct.INTERFACE_CONFIG_SHOW_CONTROLS,
                 screen_bg_color = ct.INTERFACE_CONFIG_SCREEN_BG_COLOR):
        self.config(fps = fps,
                    window_width = window_width,
                    window_height = window_height,
                    show_status_bar = show_status_bar,
                    show_controls = show_controls,
                    screen_bg_color = screen_bg_color)

        self._clock = pygame.time.Clock()
        
        pygame.font.get_init()
        self._font = {'standard': pygame.font.SysFont(ct.INTERFACE_FONT_FACE, ct.INTERFACE_FONT_SIZE, bold=False),
                      'bold': pygame.font.SysFont(ct.INTERFACE_FONT_FACE, ct.INTERFACE_FONT_SIZE, bold=True),
                      'big': pygame.font.SysFont(ct.INTERFACE_FONT_FACE, ct.INTERFACE_FONT_BIG_SIZE, bold=False)}

        self._toolboxes = []
        self._icons = []
        self._iteration_count = 0
        self._hamburger_menu = False
        self._initial_perf_counter = None
        self._current_global_time = time.perf_counter()
        self._last_global_time = self._current_global_time
        self._show_global_time = self._current_global_time
        self._run_time_s = 0.0
        self._emitting = None
        self._ips = ct.INTERFACE_IPS_AVERAGE
        self._ipss = []
        self._fpss = []
        self._init_controls_menu()
        self._init_hamburger_menu()
        self._active = True

    def config(self, fps=None, window_width=None, window_height=None, show_status_bar=None, show_controls=None, screen_bg_color=None):
        '''Use this to change the interface settings during runtime.

        All the parameters of this methods can be set during the interface instantiation. However, one may need (programatically) to change this parameters during the execution of a simulation.

        Although all parameters in this method default to None, internally they will be left unchanged if not passed. Therefore, any combination of parameters can be passed as arguments. Also, this method can be called anytime and anywhere after the interface instantiation.

        Please, do refer to the parameters description of the :class:`pygameyagui.Interface`.

        :rtype: NoneType
        '''

        if fps is not None:
            if not isinstance(fps, int):
                raise_type_error(fps, 'fps', 'integer')
            if fps <= 0:
                raise_value_error(f'fps expect an integer greater than zero. Instead, {fps} was given.')
            self._fps = fps
            self._frame_dt = 1.0 / fps

        if window_width is not None:
            if not isinstance(window_width, int):
                raise_type_error(window_width, 'window_width', 'integer')
            if window_width <= 0:
                raise_value_error(f'window_width expect an integer greater than zero. Instead, {window_width} was given.')
            self._window_width = window_width 

        if window_height is not None:
            if not isinstance(window_height, int):
                raise_type_error(window_height, 'window_height', 'integer')
            if window_height <= 0:
                raise_value_error(f'window_height expect an integer greater than zero. Instead, {window_height} was given.')
            self._window_height = window_height

        if window_width is not None or window_height is not None:
            self._define_surface()

        if show_status_bar is not None:
            if not isinstance(show_status_bar, bool):
                raise_type_error(show_status_bar, 'show_status_bar', 'bool')
            self._show_status_bar = show_status_bar

        if show_controls is not None:
            if not isinstance(show_controls, bool):
                raise_type_error(show_controls, 'show_controls', 'bool')
            self._show_controls = show_controls
            self._run = not show_controls

        if screen_bg_color is not None:
            if not isinstance(screen_bg_color, tuple):
                raise_type_error(screen_bg_color, 'screen_bg_color', 'tuple')
            if len(screen_bg_color) != 3:
                raise_value_error(f'screen_bg_color must be a tuple of three integers. Instead, a tuple of size {len(screen_bg_color)} was given')
            for n, c in enumerate(screen_bg_color):
                if c < 0 or c > 255:
                    raise_value_error(f'The value at index {n} of screen_bg_color is {c}. It must be between 0 and 255.')
            self._screen_bg_color = screen_bg_color

    @property
    def window_width(self):
        '''This returns the window width in pixels.
                
        :rtype: int
        '''
        return self._window_width

    @property
    def screen_height(self):
        '''This returns the window height in pixels. 
                
        :rtype: int
        '''
        return self._window_height

    @property
    def screen_center(self):
        '''This return a pair of x, y for the center of the window in pixels.
                
        :rtype: tuple
        '''
        return int(0.5*self._window_width), int(0.5*self._window_height)

    @property
    def screen_toplef(self):
        '''This return a pair of x, y for the top left corner of the window in pixels.
                
        :rtype: tuple
        '''
        return 0, 0

    @property
    def screen_topright(self):
        '''This return a pair of x, y for the top right corner of the window in pixels.
                
        :rtype: tuple
        '''
        return self._window_width, 0

    @property
    def screen_bottomleft(self):
        '''This return a pair of x, y for the bottom left corner of the window in pixels.
                
        :rtype: tuple
        '''
        return 0, self._window_height

    @property
    def screen_bottomright(self):
        '''This return a pair of x, y for the bottom right corner of the window in pixels.
                
        :rtype: tuple
        '''
        return self._window_width, self._window_height

    @property
    def screen_midtop(self):
        '''This return a pair of x, y for the mid top position of the window in pixels.
                
        :rtype: tuple
        '''
        return int(0.5*self._window_width), 0

    @property
    def screen_midbottom(self):
        '''This return a pair of x, y for the mid bottom position of the window in pixels.
                
        :rtype: tuple
        '''
        return int(0.5*self._window_width), self._window_height

    @property
    def screen_midleft(self):
        '''This return a pair of x, y for the mid left position of the window in pixels.
                
        :rtype: tuple
        '''
        return 0, int(0.5*self._window_height)

    @property
    def screen_midright(self):
        '''This return a pair of x, y for the mid right position of the window in pixels.
                
        :rtype: tuple
        '''
        return self._window_width, int(0.5*self._window_height)

    @property
    def screen_rect(self):
        '''This returns a Pygame Rect for the window.
                
        :rtype: Pygame.Rect
        '''
        return pygame.Rect(0,0,self._window_width,self._window_height)

    @property
    def mouse(self):
        '''This return a pair of x, y for the mouse position inside the window in pixels.
                
        :rtype: tuple
        '''
        return self._mouse_pos

    @property
    def mouse_x(self):
        '''This return the x of the mouse position inside the window in pixels.
                
        :rtype: int
        '''
        return self._mouse_pos[0]

    @property
    def mouse_y(self):
        '''This return the y of the mouse position inside the window in pixels.
                
        :rtype: int
        '''
        return self._mouse_pos[1]

    @property
    def surface(self):
        '''This returns a Pygame Surface of the window.
                
        :rtype: Pygame.Surface
        '''
        return self._surface

    @property
    def screen_bg_color(self):
        '''This returns the current window background color in the format (R,G,B).
                
        :rtype: tuple
        '''
        return self._screen_bg_color

    @property
    def time(self):
        '''This returns the current time in seconds since the simulation was started or last resetted.
                
        :rtype: float
        '''
        return self._run_time_s

    @property
    def dt(self):
        '''This is the elapsed time between the current frame and previous frame in seconds
                
        :rtype: float
        '''
        return self._dt

    @property
    def fps(self):
        '''This returns the FPS value set at :class:`pygameyagui.Interface` or configured using :meth:`pygameyagui.Interface.config`.

        Note: this is not the actual FPS which is varies and its average is shown at the status bar.
                
        :rtype: int
        '''
        return self._fps

    @property
    def iteration_count(self):
        '''This is the number of iteration since the simulation was started.
        
        Note: this will not be resetted with time.
                
        :rtype: int
        '''
        return self._iteration_count

    def contains_point(self, point):
        '''This checks if a point is inside the window.

        :param point: A pair of two integers/floats that represents a point.
        :type point: tuple

        :rtype: bool
        '''
        if not isinstance(point, tuple):
            raise_type_error(point, 'point', 'tuple')
        if len(point) != 2:
            raise_value_error(f'point must be a tuple of two integers. Instead, a tuple of size {len(point)} was given.')
        x, y = point
        if not isinstance(x, int) and not isinstance(x, float) :
            raise_type_error(x, 'point[0]', 'int or float')
        if not isinstance(y, int) and not isinstance(y, float) :
            raise_type_error(y, 'point[1]', 'int or float')

        return x >= 0 and x <= self.window_width and \
               y >= 0 and y <= self.screen_height

    def pause(self):
        '''Use this to pause the simulation update process. 
        
        It is equivalent to freeze time.

        See also: :meth:`pygameyagui.Interface.running`, :meth:`pygameyagui.Interface.resume` and :meth:`pygameyagui.Interface.pause_and_reset`

        :rtype: NoneType
        '''
        self._run = False

    def resume(self):
        '''Use this to resume the simulation update process. 
        
        It is equivalent to unfreeze time.

        See also: :meth:`pygameyagui.Interface.running`, :meth:`pygameyagui.Interface.pause` and :meth:`pygameyagui.Interface.pause_and_reset`

        :rtype: NoneType
        '''
        self._run = True

    def reset(self):
        '''Use this to reset the simulation. 
        
        It is equivalent to zero time. It will make :meth:`pygameyagui.Interface.setting` return **True**.

        See also: :meth:`pygameyagui.Interface.setting` and :meth:`pygameyagui.Interface.pause_and_reset`

        :rtype: NoneType
        '''
        self._restart._trigged = True

    def pause_and_reset(self):
        '''Use this to pause and reset the simulation. 
        
        It is equivalent to zero and stop time. It will make :meth:`pygameyagui.Interface.setting` return **True** and :meth:`pygameyagui.Interface.running` return **False**.

        See also: :meth:`pygameyagui.Interface.setting` and :meth:`pygameyagui.Interface.running`

        :rtype: NoneType
        '''
        self._run = False
        self._restart._trigged = True

    def running(self):
        '''Use this to know if the simulation will be updated. 
        
        It is equivalent to know if time is passing.
        
        It will return **False** by the default if **show_controls** at :class:`pygameyagui.Interface` is set to **True**. On the other hand, it will return **True** by the default if **show_controls** is set to **False**.

        See also: :meth:`pygameyagui.Interface.pause`, :meth:`pygameyagui.Interface.resume` and :meth:`pygameyagui.Interface.pause_and_reset`

        :rtype: bool
        '''
        return self._run

    def setting(self):
        '''Use this to know if a setup is needed.
        
        It will return **True** during the execution of the first simulation iteration or if a restart condition is met. Otherwise, returns **False**.
         
        The restart condition is met if:

            * The **Reload** button at the interface controls is clicked;
            * Any widget set to be a emitter is trigged
        
        See also: :meth:`pygameyagui.Interface.reset` and :meth:`pygameyagui.Interface.pause_and_reset`

        :rtype: bool
        '''
        return self._restart._trigged or self._iteration_count == 1

    def active(self):
        '''Use this for the condition on the simulation loop while.
        
        It will return **True** by default and keep the simulation loop running. Use :meth:`pygameyagui.Interface.deactivate` method to set it to **False**.

        :rtype: bool
        '''
        return self._active
    
    def deactivate(self):
        '''Use this anywhere if you want to end the simulation loop.
        
        It will make the :meth:`pygameyagui.Interface.active` method return **False**. Depending how you organize your program this might close the Pygame window

        :rtype: NoneType
        '''
        self._active = False

    def events(self):
        '''Use this method to get the Pygame events.

        This method is required to be called once and only once in the simulation loop. It should be called on each iteration at the very top of the simulation loop.

        :rtype: Pygame.Eventlist
        '''
        self._iteration_count += 1
        self._clock.tick(self._ips)
        self._calculate_average_ips()
        self._last_global_time = self._current_global_time
        self._current_global_time = time.perf_counter()
        self._dt = self._current_global_time - self._last_global_time
        self._mouse_pos = pygame.mouse.get_pos()
        self._events = pygame.event.get()
        for event in self._events:
            if event.type == pygame.QUIT:
                sys.exit()

        self._surface.fill(self._screen_bg_color)
        if self._run:
            if self._initial_perf_counter is None:
                self._initial_perf_counter = self._current_global_time
            else:
                self._run_time_s = self._current_global_time - self._initial_perf_counter
        else:
            self._initial_perf_counter = self._current_global_time - self._run_time_s

        if self._emitting is not None:
            self.reset()
        self._emitting = None

        if self._pause_resume._trigged:
            self._run = not self._run

        if self._restart._trigged:
            self._zeroing_clock()

        if self._hamburger._trigged:
            self._hamburger_menu = not self._hamburger_menu

        return self._events

    def show(self):
        '''Use this method show the toolboxes, controls and status bar.

        This method is required to be called once and only once in the simulation loop. It should be called on each iteration at the very bottom of the simulation loop. Also, it handles all the events that concerns the graphical interface.

        :rtype: NoneType
        '''
        self._mouse_over = None

        open_toolboxes = [toolbox for toolbox in self._toolboxes if toolbox._open]       
        
        self._run_dt = self._current_global_time - self._show_global_time
        if self._run_dt >= self._frame_dt or self._iteration_count == 1:
            self._calculate_average_fps()
            self._show_global_time = self._current_global_time
            for toolbox in open_toolboxes:
                toolbox._show()
                if not toolbox._minimized:
                    for widget in toolbox._widgets:
                        widget._show()
                        widget._mouse_over = False

            if self._show_controls:
                self._draw_controls()
                if self._hamburger_menu:
                    self._draw_hamburger_menu()
            if self._show_status_bar:
                self._draw_status_bar()

            pygame.display.flip()

        open_toolboxes_reversed = reversed(open_toolboxes)
        self._toolbox_interaction = False
        for toolbox in open_toolboxes_reversed:
            toolbox._handle_events()
            if self._mouse_over is None:
                toolbox._check_mouse_over()
            for widget in toolbox._widgets:
                if widget._enabled and self._mouse_over == toolbox:
                    if widget._can_be_emitter:
                        widget._handle_emitter_button_events()
                    widget._handle_events()
            if self._toolbox_interaction:
                break

        if self._show_controls:
            for icon in self._icons:
                icon._handle_events()

        if self._hamburger_menu:
            for menu_item in self._hamburger_menu_itens:
                if menu_item._trigged:
                    self._execute_menu_item_signal(menu_item._signal)
                menu_item._handle_events()

    def variables(self):
        '''This creates a dummy object from a dummy class to use as a `global variable`.
        
        As long as this is created in the global scope, you can use this to set attributes that act like global without having to deal with declaring global variables. This is a hack it should be avoided if possible.

        :rtype: Variable
        '''
        return Variable()

    def _zeroing_clock(self):
        self._initial_perf_counter = None
        self._run_time_s = 0.0

    def _init_controls_menu(self):
        topright = (self._window_width-ct.INTERFACE_CONTROLS_MARGIN, ct.INTERFACE_CONTROLS_MARGIN)
        self._controls_panel_rect = pygame.Rect(0,0, ct.INTERFACE_CONTROLS_PANEL_WIDTH, ct.INTERFACE_CONTROLS_PANEL_HEIGHT)
        self._controls_panel_rect.topright = topright

        self._controls_bg_color = ct.INTERFACE_CONTROLS_PANEL_BG_COLOR
        self._controls_border_color = ct.INTERFACE_CONTROLS_PANEL_BORDER_COLOR
        self._controls_border_width = ct.INTERFACE_CONTROLS_PANEL_BORDER_WIDTH
        self._controls_border_radius = ct.INTERFACE_CONTROLS_PANEL_RADIUS
        
        controls_buttons_rect = self._controls_panel_rect.inflate(-ct.INTERFACE_CONTROLS_BUTTONS_PADDING, -ct.INTERFACE_CONTROLS_BUTTONS_PADDING)
        button_width = controls_buttons_rect.width / 3
        button_height = controls_buttons_rect.height

        pause_resume_rect = pygame.Rect(0,0,button_width,button_height)
        pause_resume_rect.inflate_ip(-5,-5)
        pause_resume_rect.midleft = controls_buttons_rect.midleft
        square = pause_resume_rect.inflate(-int(0.75*button_width),0)
        square.topleft = pause_resume_rect.inflate(-int(0.4*button_width),0).topleft
        p1 = pause_resume_rect.inflate(-int(0.9*button_width),0).bottomright
        p2 = pause_resume_rect.inflate(-int(0.9*button_width),0).topright
        p3 = pause_resume_rect.midright
        triangule = [p1, p2, p3]
        pause_resume_geometries = [
            {'type': 'rect', 'color': 'button', 'rect': square},
            {'type': 'polygon', 'color': 'button', 'points': triangule}
        ]
        self._pause_resume = ButtonIcon(self, pause_resume_rect, pause_resume_geometries)

        restart_rect = pygame.Rect(0,0,button_width,button_height)
        restart_rect.inflate_ip(-5,-5)
        restart_rect.center = controls_buttons_rect.center
        center = restart_rect.center
        radius_ex = 0.4 * restart_rect.width
        radius_in = 0.28 * restart_rect.width
        square = restart_rect.copy()
        square.inflate_ip(-0.2*square.width, -0.2*square.height)
        square.topleft = restart_rect.center
        triangule = square.copy()
        triangule.inflate_ip(-0.5*triangule.width, -0.5*triangule.height)
        triangule.top = restart_rect.center[1]
        triangule.move_ip(-2,0)
        points = [triangule.topleft, triangule.topright, triangule.midbottom]
        restart_geometries = [
            {'type': 'circle', 'color': 'button', 'center': center, 'radius': radius_ex},
            {'type': 'circle', 'color': 'panel', 'center': center, 'radius': radius_in},
            {'type': 'rect', 'color': 'panel', 'rect': square},
            {'type': 'polygon', 'color': 'button', 'points': points}
        ]
        self._restart= ButtonIcon(self, restart_rect, restart_geometries)

        hamburger_rect = pygame.Rect(0,0,button_width,button_height)
        hamburger_rect.inflate_ip(-5,-5)
        hamburger_rect.midright = controls_buttons_rect.midright

        line_1 = hamburger_rect.copy()
        line_1.inflate_ip(-6,-0.82*line_1.height)
        line_1.midtop = hamburger_rect.midtop
        line_2 = hamburger_rect.copy()
        line_2.inflate_ip(-6,-0.82*line_2.height)
        line_2.center = hamburger_rect.center
        line_3 = hamburger_rect.copy()
        line_3.inflate_ip(-6,-0.82*line_3.height)
        line_3.midbottom = hamburger_rect.midbottom
        
        hamburger_geometries = [
            {'type': 'rect', 'color': 'button', 'rect': line_1},
            {'type': 'rect', 'color': 'button', 'rect': line_2},
            {'type': 'rect', 'color': 'button', 'rect': line_3},
            ]
        self._hamburger= ButtonIcon(self, hamburger_rect, hamburger_geometries)

    def _init_hamburger_menu(self):
        self._hamburger_meta_menu_itens = []
        self._update_hamburger_menu_item('Mostrar Todos')
        self._update_hamburger_menu_item('Fechar Todos')
        
    def _update_hamburger_menu_item(self, item):
        max_label_width = 0
        max_label_height = 0
        self._hamburger_meta_menu_itens.append(item)
        for meta_item in self._hamburger_meta_menu_itens:
            if isinstance(meta_item, str):
                label = meta_item
            if isinstance(meta_item, Toolbox):
                label = meta_item._title
            rect = draw._label(self, label, 'topleft', (0,0), just_get_rect = True)
            max_label_width = max(max_label_width, rect.width)
            max_label_height = max(max_label_height, rect.height)

        vertical_padding = ct.INTERFACE_CONTROLS_MENU_VERTICAL_PADDING
        horizontal_padding = ct.INTERFACE_CONTROLS_MENU_HORIZONTAL_PADDING
        
        self._hamburger_menu_itens = []
        for meta_item in self._hamburger_meta_menu_itens:
            if len(self._hamburger_menu_itens):
                topright = self._hamburger_menu_itens[-1]._rect.bottomright
            else:
                topright = self._controls_panel_rect.bottomright

            if isinstance(meta_item, str):
                label = meta_item
                if meta_item == 'Fechar Todos':
                    signal = 'close_all'
                if meta_item == 'Mostrar Todos':
                    signal = 'show_all'
            if isinstance(meta_item, Toolbox):
                label = meta_item._title
                signal = meta_item

            menu_item_rect = pygame.Rect(0,0, max_label_width+horizontal_padding, max_label_height+3*vertical_padding)
            menu_item_rect.topright = topright
            menu_item_rect.move_ip(0, vertical_padding)
            self._hamburger_menu_itens.append(MenuItem(self, menu_item_rect, label, signal))
            topright = menu_item_rect.bottomright

    def _draw_controls(self):
        draw._rect(self,
                  self._controls_panel_rect, 
                  bg_color = self._controls_bg_color,
                  border_color = self._controls_border_color,
                  border_width = self._controls_border_width,
                  border_radius = self._controls_border_radius)

        for icon in self._icons:
            icon._show()

    def _draw_hamburger_menu(self):
        for menu_item in self._hamburger_menu_itens:
            menu_item._show()

    def _draw_status_bar(self):
        # Draw the bar
        self._stats_bar_rect = pygame.Rect(0,0, self._window_width, ct.INTERFACE_STATUSBAR_HEIGHT)
        self._stats_bar_rect.bottom = self._window_height
        pygame.draw.rect(self._surface, ct.INTERFACE_STATUSBAR_COLOR, self._stats_bar_rect)
        
        if len(self._ipss) == ct.INTERFACE_IPS_AVERAGE and \
            len(self._fpss) == ct.INTERFACE_FPS_AVERAGE:
            # Display the stats
            label = f'IPS: {int(self._average_ips)} / FPS: {int(self._average_fps)}' # ({percent_ips} %)'
        else:
            label = 'Averaging IPS and FPS ...'
        draw._label(self, label, 'midleft', self._stats_bar_rect.midleft)

        decimal_places = 2
        time = str(round(self._run_time_s,decimal_places))
        time +=(decimal_places-len(time.split('.')[1]))*'0' # Completa os zeros a direita
        time +=' s'
        draw._label(self, time, 'midright', self._stats_bar_rect.inflate(-5,0).midright)

    def _execute_menu_item_signal(self, signal):
        if signal == 'close_all':
            for toolbox in self._toolboxes:
                toolbox._open = False
        elif signal == 'show_all':
            for toolbox in self._toolboxes:
                toolbox._open = True
                toolbox._minimized = False
        else:
            signal._open = not signal._open
            signal._minimized = False

    def _calculate_average_ips(self):
        self._ipss.append(int(self._clock.get_fps()))
        if len(self._ipss) > ct.INTERFACE_IPS_AVERAGE:
            removed = self._ipss.pop(0)
            added = self._ipss[-1]
            self._average_ips += (added - removed) / ct.INTERFACE_IPS_AVERAGE
        elif len(self._ipss) == ct.INTERFACE_IPS_AVERAGE:
            self._average_ips = sum(self._ipss)/ct.INTERFACE_IPS_AVERAGE

    def _calculate_average_fps(self):
        self._fpss.append(int(1.0 / self._run_dt))
        if len(self._fpss) > ct.INTERFACE_FPS_AVERAGE:
            removed = self._fpss.pop(0)
            added = self._fpss[-1]
            self._average_fps += (added - removed) / ct.INTERFACE_FPS_AVERAGE
        elif len(self._fpss) == ct.INTERFACE_FPS_AVERAGE:
            self._average_fps = sum(self._fpss)/ct.INTERFACE_FPS_AVERAGE

    def _define_surface(self):
        self._surface = pygame.display.set_mode((self._window_width, self._window_height))

__all__ = ["Toolbox"]