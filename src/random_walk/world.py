class World:
    def __init__(self, hwidth = 30, hheight = 30) -> None:
        self._walkers = Walker()
        self._hwidth = hwidth
        self._hheight = hheight

    @setter
    def set_width(self, hwidth : int) -> None:
        self._hwidth = hwidth

    @setter
    def set_height(self, hheight : int) -> None:   
        self._hheight = hheight

    @property
    def hwidth(self) -> int:
        return self._hwidth
    
    @property
    def hheight(self) -> int:
        return self._hheight

    

