import pygame
import pygameyagui
from . import constants as ct
from .error import raise_type_error, raise_value_error

def _rect(self, rect, bg_color = None, border_color = None, border_width = None, border_radius = 0):
    if not isinstance(self,pygameyagui.Interface) and not isinstance(self,pygameyagui.MenuItem):
        if not self._enabled:
            if bg_color is not None and bg_color != (255,255,255):
                bg_color = ct.WIDGET_DISABLED_BG_COLOR
            if border_color is not None:
                border_color = ct.WIDGET_DISABLED_BORDER_COLOR
        if not isinstance(self, pygameyagui.Toolbox) and not self._toolbox._enabled:
            if bg_color is not None and bg_color != (255,255,255):
                bg_color = ct.WIDGET_DISABLED_BG_COLOR
            if border_color is not None:
                border_color = ct.WIDGET_DISABLED_BORDER_COLOR

    if bg_color is not None:
        pygame.draw.rect(self._surface, bg_color, rect, border_radius = border_radius)
    if border_color is not None and border_width is not None:
        pygame.draw.rect(self._surface, border_color, rect, width = border_width, border_radius = border_radius)

def _rect2(self, pos_ref, pos, w, h,
           bg_color = None,
           border_color = None,
           border_width = None,
           border_radius = 0,
           just_get_rect=False):

    rect = pygame.Rect(0,0,w,h)

    if pos_ref == 'topleft':
        rect.topleft = pos
    elif pos_ref == 'bottomleft':
        rect.bottomleft = pos
    elif pos_ref == 'topright':
        rect.topright = pos
    elif pos_ref == 'bottomright':
        rect.bottomright = pos
    elif pos_ref == 'midtop':
        rect.midtop = pos
    elif pos_ref == 'midleft':
        rect.midleft = pos
    elif pos_ref == 'midbottom':
        rect.midbottom = pos
    elif pos_ref == 'midright':
        rect.midright = pos
    elif pos_ref == 'center':
        rect.center = pos

    if not just_get_rect:
        _rect(self, rect, bg_color = bg_color, border_color = border_color, border_width = border_width, border_radius = border_radius)
    
    return rect

def _circle(self, center, radius, bg_color = None, border_color = None, border_width = None):
    if not self._enabled:
        if bg_color is not None and bg_color != (255,255,255):
            bg_color = ct.WIDGET_DISABLED_BG_COLOR
        if border_color is not None:
            border_color = ct.WIDGET_DISABLED_BORDER_COLOR
    if not isinstance(self, pygameyagui.Toolbox) and not self._toolbox._enabled:
        if bg_color is not None and bg_color != (255,255,255):
            bg_color = ct.WIDGET_DISABLED_BG_COLOR
        if border_color is not None:
            border_color = ct.WIDGET_DISABLED_BORDER_COLOR

    if bg_color is not None:
        pygame.draw.circle(self._surface, bg_color, center, radius)
    if border_color is not None and border_width is not None:
        pygame.draw.circle(self._surface, border_color, center, radius, width = border_width)

def _line(self, start, end, color = None, width = 1):
    if not self._enabled:
        if color is not None and color != (255,255,255):
            color = ct.WIDGET_DISABLED_BORDER_COLOR
    if not isinstance(self, pygameyagui.Toolbox) and not self._toolbox._enabled:
        if color is not None and color != (255,255,255):
            color = ct.WIDGET_DISABLED_BORDER_COLOR

    if color is not None:
        pygame.draw.line(self._surface, color, start, end, width = width)

def _widget_border(self):
    '''This is the widget envelope border '''
    pygame.draw.rect(self._surface, ct.WIDGET_BORDER_COLOR, self._widget_rect, width = ct.WIDGET_BORDER_WIDTH, border_radius = ct.WIDGET_BORDER_RADIUS)
    _widget_emitter_icon(self)

def _widget_emitter_icon(self):
    if self._can_be_emitter:
        center = self._widget_rect.inflate(-5,-5).topright
        side = ct.WIDGET_RESETICON_SIDE
        self.emitter_rect = pygame.Rect(0,0,side,side)
        self.emitter_rect.center = center
        if self._emitter:
            bg_color = ct.WIDGET_RESETICON_CHECKED_BG_COLOR
        elif self.emitter_rect.collidepoint(self._interface._mouse_pos) and self._enabled:
            bg_color = ct.WIDGET_RESETICON_CHECKED_BG_MOUSEOVER_COLOR
        else:
            bg_color = ct.WIDGET_RESETICON_UNCHECKED_BG_COLOR
        
        border_color = ct.WIDGET_RESETICON_BORDER_COLOR
        border_width = ct.WIDGET_RESETICON_BORDER_WIDTH
        _rect(self, self.emitter_rect, bg_color = bg_color, border_color = border_color, border_width = border_width)



def _label(obj, text, pos_ref, pos,
               color = 'standard',
               area=None,
               limits=None,
               just_get_rect=False,
               bg_color = None,
               border_color = None,
               border_width = None,
               font_type = 'standard'):

    if color == 'standard':
        color = ct.TOOLBOX_STANDARD_TEXT_COLOR

    if isinstance(obj, pygameyagui.Interface):
        interface = obj
    elif isinstance(obj, pygameyagui.MenuItem):
        interface = obj._interface
    else:
        interface = obj._interface
        if not obj._enabled:
            color = ct.TOOLBOX_DISABLED_TEXT_COLOR
        if not isinstance(obj, pygameyagui.Toolbox) and not obj._toolbox._enabled:
            color = ct.TOOLBOX_DISABLED_TEXT_COLOR

    label = interface._font[font_type].render(text, True, color)
    label_rect = label.get_rect()
    
    x,y,w,h = 0,0,label_rect.width, label_rect.height
    if area is not None:
        new_x = label_rect.width - area.width
        new_y = label_rect.height - area.height
        if new_x > 0:
            w = area.width
            if 'right' in pos_ref:
                x = new_x
        if new_y > 0:
            h = area.height
            if 'bottom' in pos_ref:
                y = new_y
    
    clipping_area = pygame.Rect(x,y,w,h)
    label_rect.size = w, h

    if pos_ref == 'topleft':
        label_rect.topleft = pos
    elif pos_ref == 'bottomleft':
        label_rect.bottomleft = pos
    elif pos_ref == 'topright':
        label_rect.topright = pos
    elif pos_ref == 'bottomright':
        label_rect.bottomright = pos
    elif pos_ref == 'midtop':
        label_rect.midtop = pos
    elif pos_ref == 'midleft':
        label_rect.midleft = pos
    elif pos_ref == 'midbottom':
        label_rect.midbottom = pos
    elif pos_ref == 'midright':
        label_rect.midright = pos
    elif pos_ref == 'center':
        label_rect.center = pos

    if limits is not None:
        if label_rect.left < limits.left:
            label_rect.left = limits.left
        elif label_rect.right > limits.right:
            label_rect.right = limits.right

    if not just_get_rect:
        if bg_color is not None or border_color is not None:
            _rect(obj, label_rect, bg_color = bg_color, border_color = border_color, border_width = border_width)   
        interface._surface.blit(label, label_rect, clipping_area)
    return label_rect