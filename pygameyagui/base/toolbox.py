import pygame
import pygameyagui
from ..include import constants as ct
from ..include import draw
from ..include.error import raise_type_error

class Toolbox:
    """This class creates a toolbox objetc.

    :param interface: The interface created.
    :type interface: :class:`pygameyagui.Interface`
    
    :param title: Toolbox title.
    :type title: str
    """
    def __init__(self, interface, title):
        self._set_interface(interface)
        self._surface = interface._surface
        self._interface._toolboxes.append(self)
        self._title(title)
        self._x = len(interface._toolboxes) * ct.TOOLBOX_INITIAL_X
        self._y = len(interface._toolboxes) * ct.TOOLBOX_INITIAL_Y
        self._enabled = True
        self._minimized = False
        self._open = True
        self._being_dragged = False
        self._mouse_over = False
        self._editing_focus = None
        self._toolbox_width = ct.TOOLBOX_MIN_WIDTH
        self._widgets = []
        self._interface._update_hamburger_menu_item(self)

    def _set_interface(self, _interface):
        if isinstance(_interface, pygameyagui.Interface):
            self._interface = _interface
        else:
            raise_type_error(_interface, 'interface', 'pygameyagui.Interface')

    def _title(self, _title):
        if isinstance(_title, str):
            self._title = _title
        else:
            raise_type_error(_title, 'title', 'str')

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, _enabled):
        if isinstance(_enabled, bool):
            self._enabled = _enabled
        else:
            raise TypeError(f'enabled argument must be of type boolean. Instead, type {type(_enabled)} was given.')

    def minimize(self):
        '''Use this to programatically minimize a toolbox.

        The toolbox will collapse such that only its title bar is visible. It is called internally when the user clicks in the minimize icon of an expanded toolbox at the left end of the title bar.

        :rtype: NoneType
        '''
        self._minimized = True

    def restore(self):
        '''Use this to programatically restore/expand a toolbox.

        The toolbox will restore such that its body is visible. It is called internally when the user clicks in the minimize icon of a minimized/collapsed toolbox at the right end of the title bar. 

        :rtype: NoneType
        '''
        self._minimized = False

    def enable(self):
        '''Use this to 

        :rtype: NoneType
        '''
        self._enabled = True

    def disable(self):
        '''Use this to 

        :rtype: NoneType
        '''
        self._enabled = False

    def open(self):
        '''Use this to 

        :rtype: NoneType
        '''
        self._open = True

    def close(self):
        '''Use this to 

        :rtype: NoneType
        '''
        self._open = False

    def _show(self):
        self._draw_title_bar()
        if not self._minimized:
            self._draw_toolbox_body()

    def _draw_title_bar(self):
        # Create rect for title bar
        pos = self._x, self._y
        size = self._toolbox_width, ct.TOOLBOX_TITLE_BAR_HEIGHT
        self._title_bar_rect = pygame.Rect(pos, size)

        # Draw the title bar
        bg_color = ct.TOOLBOX_TITLE_BAR_BG_COLOR
        border_color = ct.TOOLBOX_TITLE_BAR_BORDER_COLOR
        border_width = ct.TOOLBOX_BORDER_WIDTH
        draw._rect(self, self._title_bar_rect, bg_color = bg_color, border_color = border_color, border_width = border_width)
        
        # Draw the window title
        if self._interface._toolboxes[-1] == self:
            font_type = 'bold'
        else:
            font_type = 'standard'
            
        draw._label(self, self._title, 'center', self._title_bar_rect.center, font_type=font_type)

        padding = ct.TOOLBOX_BUTTON_PADDING
        w, h = ct.TOOLBOX_TITLE_BAR_HEIGHT - 2 * padding, ct.TOOLBOX_TITLE_BAR_HEIGHT - 2 * padding
        bg_color = ct.TOOLBOX_TITLE_BAR_CE_BUTTOM_BG_COLOR
        border_color = ct.TOOLBOX_TITLE_BAR_CE_BUTTOM_BORDER_COLOR
        border_width = ct.TOOLBOX_BORDER_WIDTH

        if self._interface._show_controls:
            # Draw the title bar close buttom
            pos = self._title_bar_rect.inflate(-2 * padding,0).midright
            self._close_button_rect = draw._rect2(self, 'midright', pos, w, h, bg_color = bg_color, border_color = border_color, border_width = border_width)
            start = self._close_button_rect.inflate(-12,-12).topleft
            end = self._close_button_rect.inflate(-12,-12).bottomright
            draw._line(self, start, end, color = border_color, width = border_width)
            start = self._close_button_rect.inflate(-12,-12).bottomleft
            end = self._close_button_rect.inflate(-12,-12).topright
            draw._line(self, start, end, color = border_color, width = border_width)


        # Draw the title bar minimize buttom
        pos = self._title_bar_rect.inflate(-2 * padding,0).midleft
        self._minimize_button_rect = draw._rect2(self, 'midleft', pos, w, h, bg_color = bg_color, border_color = border_color, border_width = border_width)
        start = self._minimize_button_rect.inflate(-12,-12).midleft
        end = self._minimize_button_rect.inflate(-12,-12).midright
        draw._line(self, start, end, color = border_color, width = border_width)

    def _draw_toolbox_body(self):
        # Create rect for minimal toolbox below the title bar
        self._body_rect = pygame.Rect(0,0,self._toolbox_width,0)
        self._body_rect.topleft = self._title_bar_rect.bottomleft
        self._body_rect.width = self._toolbox_width
        self._body_rect.height = ct.TOOLBOX_MIN_HEIGHT
        
        # Collect slot rects for all widgets in the toolbox 
        widgets_slot_rect = [widget._get_rects() for widget in self._widgets]
        self._body_rect = self._body_rect.unionall(widgets_slot_rect)
        
        # Create rect for footer
        self._body_rect_footer = pygame.Rect(0,0,self._toolbox_width,0)
        self._body_rect_footer.topleft = self._body_rect.bottomleft
        self._body_rect_footer.width = self._toolbox_width
        self._body_rect_footer.height = ct.TOOLBOX_FOOTER_HEIGHT
        self._body_rect = self._body_rect.union(self._body_rect_footer)


        # Draw the title bar
        bg_color = ct.TOOLBOX_BODY_BG_COLOR
        border_color = ct.TOOLBOX_BODY_BORDER_COLOR
        border_width = ct.TOOLBOX_BORDER_WIDTH
        draw._rect(self, self._body_rect, bg_color = bg_color, border_color = border_color, border_width = border_width)
        
    def _check_mouse_over(self):
        if self._title_bar_rect.collidepoint(self._interface._mouse_pos):
            self._interface._mouse_over = self
        if self._body_rect.collidepoint(self._interface._mouse_pos) and not self._minimized:
            self._interface._mouse_over = self

    def _handle_events(self):
        self._interface._toolbox_interaction = False
        for event in self._interface._events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self._title_bar_rect.collidepoint(self._interface._mouse_pos):
                        self._handle_toolbox_selection()
                        self._being_dragged = True
                        pygame.mouse.get_rel()
                    if self._body_rect.collidepoint(self._interface._mouse_pos) and not self._minimized:
                        self._handle_toolbox_selection()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:                    
                    if self._minimize_button_rect.collidepoint(self._interface._mouse_pos):
                        self._interface.toolbox_interaction = True
                        self._minimized = not self._minimized
                    if self._interface._show_controls:                   
                        if self._close_button_rect.collidepoint(self._interface._mouse_pos):
                            self._interface.toolbox_interaction = True
                            self._open = not self._open
                    if self._body_rect.collidepoint(self._interface._mouse_pos):
                        self._interface.toolbox_interaction = True
                self._being_dragged = False

            if event.type == pygame.MOUSEMOTION:
                if self._being_dragged:
                    delta = pygame.mouse.get_rel()
                    self._x += delta[0]
                    self._y += delta[1]

    def _handle_toolbox_selection(self):
        if self._interface._toolboxes[-1]._editing_focus is not None:
            self._interface._toolboxes[-1]._editing_focus._loose_focus()
            self._interface._toolboxes[-1]._editing_focus = None
        self._interface._toolbox_interaction = True
        self._interface._toolboxes.remove(self)
        self._interface._toolboxes.append(self)
        