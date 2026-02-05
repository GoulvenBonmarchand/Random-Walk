class Button():
    def __init__(self, text, pos, font, screen, base_color="white", hovering_color="green", image=None):
        self._text = text
        self._text_rect = self._text.get_rect(center=pos)
        self._image = image
        self._rect = self._image.get_rect(center=pos)
        self._pos = pos
        self._font = font
        self._base_color = base_color
        self._hovering_color = hovering_color
        self._screen = screen

    def update(self):
        if self._image is not None:
            self._screen.blit(self._image, self._rect)
        self._screen.blit(self._text, self._text_rect)
    
    def check_for_input(self, position):
        if position[0] in range(self._rect.left, self._rect.right) and position[1] in range(self._rect.top, self._rect.bottom):
            return True
        return False
    
    def change_color(self, position):
        if position[0] in range(self._rect.left, self._rect.right) and position[1] in range(self._rect.top, self._rect.bottom):
            self._text = self._font.render(self._text.get_text(), True, self._hovering_color)
        else:
            self._text = self._font.render(self._text.get_text(), True, self._base_color)
        
        
    