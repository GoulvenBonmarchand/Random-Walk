"""Pygame button widget utilities."""


class Button:
    """
    Clickable button with optional image and text.

    Args:
        text (str | Any): Label string or pre-rendered surface.
        pos (tuple[int, int]): Center position in pixels.
        font (Any): Font used to render the label.
        screen (Any): Screen surface to draw on.
        base_color (str | tuple): Default text color.
        hovering_color (str | tuple): Hover text color.
        image (Any | None): Optional image surface.
    """

    def __init__(self, text, pos, font, screen, base_color="white", hovering_color="green", image=None):
        """
        Initialize a button with text, position, and colors.

        Args:
            text (str | Any): Label string or pre-rendered surface.
            pos (tuple[int, int]): Center position in pixels.
            font (Any): Font used to render the label.
            screen (Any): Screen surface to draw on.
            base_color (str | tuple): Default text color.
            hovering_color (str | tuple): Hover text color.
            image (Any | None): Optional image surface.

        Returns:
            None.
        """
        self._label = text if isinstance(text, str) else None
        if self._label is None:
            self._text = text
        else:
            self._text = font.render(self._label, True, base_color)
        self._text_rect = self._text.get_rect(center=pos)
        self._image = image
        if self._image is None:
            self._rect = self._text_rect
        else:
            self._rect = self._image.get_rect(center=pos)
        self._pos = pos
        self._font = font
        self._base_color = base_color
        self._hovering_color = hovering_color
        self._screen = screen

    def update(self):
        """
        Draw the button onto the screen.

        Args:
            None.

        Returns:
            None.
        """
        if self._image is not None:
            self._screen.blit(self._image, self._rect)
        self._screen.blit(self._text, self._text_rect)

    def check_for_input(self, position):
        """
        Return True if the given position is inside the button.

        Args:
            position (tuple[int, int]): Mouse position in pixels.

        Returns:
            bool: True if inside the button, otherwise False.
        """
        if position[0] in range(self._rect.left, self._rect.right) and position[1] in range(self._rect.top, self._rect.bottom):
            return True
        return False

    def change_color(self, position):
        """
        Update text color depending on hover state.

        Args:
            position (tuple[int, int]): Mouse position in pixels.

        Returns:
            None.
        """
        if self._label is None:
            return
        if position[0] in range(self._rect.left, self._rect.right) and position[1] in range(self._rect.top, self._rect.bottom):
            color = self._hovering_color
        else:
            color = self._base_color
        self._text = self._font.render(self._label, True, color)
