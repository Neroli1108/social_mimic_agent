"""RimWorld-style dropdown component."""
import pygame
from game.theme import (
    BG_PANEL, BG_PANEL2, BG_HOVER, BORDER, BORDER_LT,
    TEXT_MAIN, TEXT_SEC, AMBER,
    draw_panel_border,
)


class CyberDropdown:
    """Flat dropdown with RimWorld styling.

    The class name is kept as CyberDropdown for backward compatibility.
    """

    def __init__(self, rect, options, selected=0, color=None, font=None,
                 on_change=None):
        self.rect = pygame.Rect(rect)
        self.options = list(options)
        self.selected = selected
        self.color = color  # kept for compat but unused visually
        self.font = font
        self.on_change = on_change
        self.open = False
        self.item_h = 26

    @property
    def value(self):
        return self.options[self.selected] if self.options else None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
                return True
            if self.open:
                for i in range(len(self.options)):
                    item_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y + self.rect.h + i * self.item_h,
                        self.rect.w,
                        self.item_h,
                    )
                    if item_rect.collidepoint(event.pos):
                        if i != self.selected:
                            self.selected = i
                            if self.on_change:
                                self.on_change(i, self.options[i])
                        self.open = False
                        return True
                self.open = False
        return False

    def draw(self, surface, fonts=None):
        f = self.font or (fonts['body'] if fonts else pygame.font.SysFont('verdana', 16))

        # Main box background
        pygame.draw.rect(surface, BG_PANEL2, self.rect)

        # Border — amber when open, standard when closed
        border_col = AMBER if self.open else BORDER
        draw_panel_border(surface, self.rect, border_col)

        # Selected text
        sel_label = self.options[self.selected] if self.options else ''
        txt = f.render(sel_label, True, TEXT_MAIN)
        surface.blit(txt, (self.rect.x + 8,
                           self.rect.y + (self.rect.h - txt.get_height()) // 2))

        # Arrow
        ax = self.rect.right - 16
        ay = self.rect.centery
        arrow_col = AMBER if self.open else TEXT_SEC
        if self.open:
            pts = [(ax - 5, ay + 3), (ax + 5, ay + 3), (ax, ay - 3)]
        else:
            pts = [(ax - 5, ay - 3), (ax + 5, ay - 3), (ax, ay + 3)]
        pygame.draw.polygon(surface, arrow_col, pts)

        # Dropdown list (rendered on top)
        if self.open:
            list_h = len(self.options) * self.item_h
            list_rect = pygame.Rect(
                self.rect.x,
                self.rect.y + self.rect.h,
                self.rect.w,
                list_h,
            )
            pygame.draw.rect(surface, BG_PANEL, list_rect)
            draw_panel_border(surface, list_rect, AMBER)

            mouse_pos = pygame.mouse.get_pos()
            for i, opt in enumerate(self.options):
                ir = pygame.Rect(
                    self.rect.x,
                    self.rect.y + self.rect.h + i * self.item_h,
                    self.rect.w,
                    self.item_h,
                )
                if ir.collidepoint(mouse_pos):
                    pygame.draw.rect(surface, BG_HOVER, ir)

                tc = AMBER if i == self.selected else TEXT_MAIN
                t = f.render(opt, True, tc)
                surface.blit(t, (ir.x + 8, ir.y + (ir.h - t.get_height()) // 2))
