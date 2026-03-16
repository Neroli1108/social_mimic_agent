"""RimWorld-style solid panel component."""
import pygame
from game.theme import (
    BG_PANEL, BG_HEADER, BORDER, TEXT_HEAD, AMBER,
    draw_panel_border, draw_divider,
)


class RimPanel:
    def __init__(self, rect, title=None, color=None):
        self.rect = pygame.Rect(rect)
        self.title = title
        self.color = color or AMBER  # used for title text and accent strip

    def draw(self, surface, fonts=None):
        f = fonts['small'] if fonts else pygame.font.SysFont('verdana', 13)

        # Fill
        pygame.draw.rect(surface, BG_PANEL, self.rect)

        # Border
        draw_panel_border(surface, self.rect, BORDER)

        # Title bar
        if self.title:
            bar_h = 22
            bar_r = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, bar_h)
            pygame.draw.rect(surface, BG_HEADER, bar_r)

            # Bottom divider of title bar
            draw_divider(surface, bar_r, color=BORDER)

            # Left accent strip
            pygame.draw.rect(surface, self.color or AMBER,
                             pygame.Rect(self.rect.x, self.rect.y, 3, bar_h))

            t = f.render(self.title.upper(), True, self.color or TEXT_HEAD)
            surface.blit(t, (self.rect.x + 10,
                             self.rect.y + (bar_h - t.get_height()) // 2))

    def content_rect(self):
        """Return rect for content area (below title bar if present)."""
        offset = 26 if self.title else 6
        return pygame.Rect(
            self.rect.x + 6,
            self.rect.y + offset,
            self.rect.w - 12,
            self.rect.h - offset - 6,
        )


# Alias for backward compatibility
CyberPanel = RimPanel
