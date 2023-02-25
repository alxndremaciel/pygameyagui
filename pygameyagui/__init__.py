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
    :type fps: int (optional)
    
    :param window_width: The window width in pixels.
    :type window_width: int (optional)
    
    :param window_height: The window height in pixels.
    :type window_height: int (optional)

    :param show_status_bar: Flag to show or hide the status bar.
    :type show_status_bar: bool (optional)

    :param show_controls: Flag to show or hide the controls at the top right corner of the screen. Buttons for pause/resume, reload simulations and toolboxes (:class:`base.toolbox.Toolbox`) list is located at the controls.
    :type show_controls: bool (optional)

    :param screen_bg_color: Screen background color in the format (R,G,B).
    :type screen_bg_color: tuple (optional)
    """
    def __init__(self,
                 fps = ct.INTERFACE_CONFIG_FPS,
                 window_width = ct.INTERFACE_CONFIG_WINDOW_WIDTH,
                 window_heigth = ct.INTERFACE_CONFIG_WINDOW_HEIGHT,
                 show_status_bar = ct.INTERFACE_CONFIG_SHOW_STATUS_BAR,
                 show_controls = ct.INTERFACE_CONFIG_SHOW_CONTROLS,
                 screen_bg_color = ct.INTERFACE_CONFIG_SCREEN_BG_COLOR):
        self.config(fps = fps,
                    window_width = window_width,
                    window_heigth = window_heigth,
                    show_status_bar = show_status_bar,
                    show_controls = show_controls,
                    screen_bg_color = screen_bg_color)

        self._surface = pygame.display.set_mode((self._window_width, self._window_heigth))
        self._clock = pygame.time.Clock()
        
        pygame.font.get_init()
        self._font = {'standard': pygame.font.SysFont(ct.INTERFACE_FONT_FACE, ct.INTERFACE_FONT_SIZE, bold=False),
                      'bold': pygame.font.SysFont(ct.INTERFACE_FONT_FACE, ct.INTERFACE_FONT_SIZE, bold=True),
                      'big': pygame.font.SysFont(ct.INTERFACE_FONT_FACE, ct.INTERFACE_FONT_BIG_SIZE, bold=False)}

        self._toolboxes = []
        self._icons = []
        self._frame_count = 0
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

    def config(self, fps, window_width, window_heigth, show_status_bar, show_controls, screen_bg_color):
        if not isinstance(fps, int):
            raise_type_error(fps, 'fps', 'integer')
        if fps <= 0:
            raise_value_error(f'fps expect an integer greater than zero. Instead, {fps} was given.')
        self._fps = fps
        self._frame_dt = 1.0 / fps

        if not isinstance(window_width, int):
            raise_type_error(window_width, 'window_width', 'integer')
        if window_width <= 0:
            raise_value_error(f'window_width expect an integer greater than zero. Instead, {window_width} was given.')
        self._window_width = window_width 

        if not isinstance(window_heigth, int):
            raise_type_error(window_heigth, 'window_heigth', 'integer')
        if window_heigth <= 0:
            raise_value_error(f'window_heigth expect an integer greater than zero. Instead, {window_heigth} was given.')
        self._window_heigth = window_heigth

        if not isinstance(show_status_bar, bool):
            raise_type_error(show_status_bar, 'show_status_bar', 'bool')
        self._show_status_bar = show_status_bar

        if not isinstance(show_controls, bool):
            raise_type_error(show_controls, 'show_controls', 'bool')
        self._show_controls = show_controls
        self._run = not show_controls

        if not isinstance(screen_bg_color, tuple):
            raise_type_error(screen_bg_color, 'screen_bg_color', 'tuple')
        if len(screen_bg_color) != 3:
            raise_value_error(f'screen_bg_color must be a tuple of three integers. Instead, a tuple of size {len(screen_bg_color)}')
        for n, c in enumerate(screen_bg_color):
            if c < 0 or c > 255:
                raise_value_error(f'The value at index {n} of screen_bg_color is {c}. It must be between 0 and 255.')
        self._screen_bg_color = screen_bg_color

    @property
    def screen_width(self):
        return self._window_width

    @property
    def screen_height(self):
        return self._window_heigth

    @property
    def screen_center(self):
        return int(0.5*self._window_width), int(0.5*self._window_heigth)

    @property
    def screen_toplef(self):
        return 0, 0

    @property
    def screen_topright(self):
        return self._window_width, 0

    @property
    def screen_bottomleft(self):
        return 0, self._window_heigth

    @property
    def screen_bottomright(self):
        return self._window_width, self._window_heigth

    @property
    def screen_midtop(self):
        return int(0.5*self._window_width), 0

    @property
    def screen_midbottom(self):
        return int(0.5*self._window_width), self._window_heigth

    @property
    def screen_midleft(self):
        return 0, int(0.5*self._window_heigth)

    @property
    def screen_midright(self):
        return self._window_width, int(0.5*self._window_heigth)

    @property
    def screen_rect(self):
        return pygame.Rect(0,0,self._window_width,self._window_heigth)

    @property
    def mouse(self):
        return self._mouse_pos

    @property
    def mouse_x(self):
        return self._mouse_pos[0]

    @property
    def mouse_y(self):
        return self._mouse_pos[1]

    @property
    def surface(self):
        return self._surface

    @property
    def screen_bg_color(self):
        return self._screen_bg_color

    @property
    def time(self):
        return self._run_time_s

    @property
    def dt(self):
        return self._dt

    @property
    def fps(self):
        return self._fps

    @property
    def frame_count(self):
        return self._frame_count

    def contains_point(self, point):
        x, y = point
        return x >= 0 and x <= self.screen_width and y >= 0 and y <= self.screen_height

    def pause_and_reset(self):
        self._run = False
        self._restart._trigged = True

    def pause(self):
        self._run = False

    def reset(self):
        self._restart._trigged = True

    def running(self):
        return self._run

    def setting(self):
        return self._restart._trigged or self._frame_count == 1

    def active(self):
        return self._active

    def events(self):
        self._frame_count += 1
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

        return self._events

    def show(self):
        self._mouse_over = None
        open_toolboxes = [toolbox for toolbox in self._toolboxes if toolbox._open]       
        
        self._run_dt = self._current_global_time - self._show_global_time
        if self._run_dt >= self._frame_dt or self._frame_count == 1:
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

        if self._pause_resume._trigged:
            self._run = not self._run

        if self._restart._trigged:
            self._initial_perf_counter = None
            self._run_time_s = 0.0

        if self._hamburger._trigged:
            self._hamburger_menu = not self._hamburger_menu

        if self._hamburger_menu:
            for menu_item in self._hamburger_menu_itens:
                if menu_item._trigged:
                    self._execute_menu_item_signal(menu_item._signal)
                menu_item._handle_events()

        return True

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
        self._stats_bar_rect = pygame.Rect(0,0, self._window_width, ct.INTERFACE_STATUSBAR_HEIGTH)
        self._stats_bar_rect.bottom = self._window_heigth
        pygame.draw.rect(self._surface, ct.INTERFACE_STATUSBAR_COLOR, self._stats_bar_rect)
        
        if len(self._ipss) == ct.INTERFACE_IPS_AVERAGE:
            # Display the stats
            label = f'IPS: {int(self._average_ips)} / FPS: {int(self._average_fps)}' # ({percent_ips} %)'
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
    
    def variables(self):
        return Variable()

