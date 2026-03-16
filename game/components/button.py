"""RimWorld-style flat button and toggle components."""
import pygame
from game.theme import (
    BG_PANEL2, BG_HOVER, BG_SELECT, BORDER, BORDER_LT,
    TEXT_MAIN, TEXT_HEAD, TEXT_DIM, TEXT_SEC, AMBER,
    draw_panel_border,
)


class RimButton:
    """Flat RimWorld-style button."""

    def __init__(self, rect, text, accent=False, color=None, font=None,
                 action=None, enabled=True):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.accent = accent      # True = amber highlight (CTA button)
        self.color = color        # override text/border color if set
        self.font = font
        self.action = action
        self.enabled = enabled
        self.hovered = False
        self.pressed = False
        self._press_t = 0

    def set_enabled(self, v):
        self.enabled = v

    def handle_event(self, event):
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                self._press_t = 6
                if self.action:
                    self.action()
                return True
        return False

    def update(self):
        if self._press_t > 0:
            self._press_t -= 1
            if self._press_t == 0:
                self.pressed = False

    def draw(self, surface, fonts=None):
        f = self.font or (fonts['body'] if fonts else pygame.font.SysFont('verdana', 16))

        if not self.enabled:
            pygame.draw.rect(surface, BG_PANEL2, self.rect)
            draw_panel_border(surface, self.rect, BORDER)
            t = f.render(self.text, True, TEXT_DIM)
            surface.blit(t, t.get_rect(center=self.rect.center))
            return

        # Background
        if self.pressed:
            bg = BG_SELECT
        elif self.hovered:
            bg = BG_HOVER
        else:
            bg = BG_PANEL2
        pygame.draw.rect(surface, bg, self.rect)

        # Border
        border_col = self.color or (AMBER if self.accent else (BORDER_LT if self.hovered else BORDER))
        draw_panel_border(surface, self.rect, border_col)

        # Left accent strip for CTA buttons
        if self.accent:
            strip = pygame.Rect(self.rect.x, self.rect.y, 3, self.rect.h)
            pygame.draw.rect(surface, self.color or AMBER, strip)

        # Text
        text_col = self.color or (TEXT_HEAD if (self.accent or self.hovered) else TEXT_MAIN)
        t = f.render(self.text, True, text_col)
        surface.blit(t, t.get_rect(center=self.rect.center))


# Alias for backward compatibility
CyberButton = RimButton


class RimToggle:
    """Segmented toggle (tab bar style)."""

    def __init__(self, rect, options, selected=0, color=None, font=None, on_change=None):
        self.rect = pygame.Rect(rect)
        self.options = options
        self.selected = selected
        self.color = color  # unused but accepted for compat
        self.font = font
        self.on_change = on_change

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                w = self.rect.w // len(self.options)
                idx = min((event.pos[0] - self.rect.x) // w, len(self.options) - 1)
                if idx != self.selected:
                    self.selected = idx
                    if self.on_change:
                        self.on_change(self.selected)
                return True
        return False

    def draw(self, surface, fonts=None):
        f = self.font or (fonts['small'] if fonts else pygame.font.SysFont('verdana', 13))
        w = self.rect.w // len(self.options)

        pygame.draw.rect(surface, BG_PANEL2, self.rect)
        draw_panel_border(surface, self.rect, BORDER)

        for i, opt in enumerate(self.options):
            r = pygame.Rect(self.rect.x + i * w, self.rect.y, w, self.rect.h)
            if i == self.selected:
                pygame.draw.rect(surface, BG_SELECT, r)
                pygame.draw.rect(surface, AMBER,
                                 pygame.Rect(r.x, r.bottom - 2, r.w, 2))
            if i > 0:
                pygame.draw.line(surface, BORDER, r.topleft, r.bottomleft)
            col = TEXT_HEAD if i == self.selected else TEXT_SEC
            t = f.render(opt, True, col)
            surface.blit(t, t.get_rect(center=r.center))


# Alias for backward compatibility
CyberToggle = RimToggle
