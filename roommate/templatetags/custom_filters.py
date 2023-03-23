from colour import Color
from django import template

register = template.Library()


@register.filter
def percentage(value, total):
    if total == 0:
        return 0
    percentage_value = int((value / total) * 100)
    return max(min(percentage_value, 100), 0)


def interpolate_color(color1, color2, color3, value):
    if 0 <= value <= 50:
        ratio = value / 50
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        return f'#{r:02x}{g:02x}{b:02x}'
    else:
        value -= 50
        ratio = value / 50
        r = int(color2[0] * (1 - ratio) + color3[0] * ratio)
        g = int(color2[1] * (1 - ratio) + color3[1] * ratio)
        b = int(color2[2] * (1 - ratio) + color3[2] * ratio)
        return f'#{r:02x}{g:02x}{b:02x}'


@register.simple_tag
def progress_bar_color(value):
    if not value:
        value = 0
    else:
        value = int(value)
    red = Color("#dc3545")
    yellow = Color("#ffc107")
    green = Color("#28a745")
    red_tuple = (int(red.red * 255), int(red.green * 255), int(red.blue * 255))
    yellow_tuple = (int(yellow.red * 255), int(yellow.green * 255), int(yellow.blue * 255))
    green_tuple = (int(green.red * 255), int(green.green * 255), int(green.blue * 255))
    return interpolate_color(red_tuple, yellow_tuple, green_tuple, value)
