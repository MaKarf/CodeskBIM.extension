import clr

clr.AddReference("PresentationCore")
clr.AddReference("System.Windows")
from System.Windows.Media import Color, SolidColorBrush


def hex_color_wpf_brush(hex_color):
    """Remove the '#' if it is present"""
    hex_color = hex_color.lstrip('#')

    """Convert hex to RGB"""
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    """Create a Color object"""
    color = Color.FromArgb(255, *rgb)

    """Create a SolidColorBrush"""
    brush = SolidColorBrush(color)

    return brush


def set_wpf_component_foreground_color(hex_color, wpf_component):
    color_brush = hex_color_wpf_brush(hex_color=hex_color)
    wpf_component.Foreground = color_brush


def set_wpf_component_background_color(hex_color, wpf_component):
    color_brush = hex_color_wpf_brush(hex_color=hex_color)
    wpf_component.Background = color_brush
