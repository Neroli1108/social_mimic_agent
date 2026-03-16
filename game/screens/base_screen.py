"""Base screen class for all game screens."""


class BaseScreen:
    def __init__(self, engine):
        self.engine = engine

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
