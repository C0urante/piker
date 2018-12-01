"""Hoverable Behaviour (changing when the mouse is on the widget by O. Poyen.
License: LGPL
"""
__author__ = 'Olivier Poyen'


from kivy.properties import BooleanProperty, ObjectProperty
from kivy.core.window import Window


class HoverBehavior(object):
    """Hover behavior.

    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget.
    """
    hovered = BooleanProperty(False)
    # Contains the last relevant point received by the Hoverable. This can
    # be used in `on_enter` or `on_leave` in order to know where was dispatched
    # the event.
    border_point = ObjectProperty(None)
    _widgets = []
    _last_hovered = None

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        HoverBehavior._widgets.append(self)
        super(HoverBehavior, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    @classmethod
    def on_mouse_pos(cls, *args):
        # XXX: how to still do this at the class level?
        # don't proceed if I'm not displayed <=> If have no parent
        # if not self.get_root_window():
        #     return

        pos = args[1]
        # Next line to_widget allow to compensate for relative layout
        for widget in cls._widgets:
            w_coords = widget.to_widget(*pos)
            inside = widget.collide_point(*w_coords)
            if inside and widget.hovered:
                return
            elif inside:
                # un-highlight the last highlighted
                last_hovered = cls._last_hovered
                if last_hovered:
                    last_hovered.dispatch('on_leave')
                    last_hovered.hovered = False

                # highlight new widget
                widget.border_point = pos
                widget.hovered = True
                widget.dispatch('on_enter')
                cls._last_hovered = widget
                return

    # implement these in the widget impl

    @classmethod
    def on_enter(cls):
        pass

    @classmethod
    def on_leave(cls):
        pass
