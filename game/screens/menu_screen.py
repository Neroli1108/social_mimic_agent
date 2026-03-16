"""Main menu screen — RimWorld-inspired layout with scenario cards."""
import pygame
import random

from game.screens.base_screen import BaseScreen
from game.theme import (
    SCREEN_W, SCREEN_H,
    BG_DARK, BG_PANEL, BG_PANEL2, BG_HEADER, BG_HOVER,
    BORDER, BORDER_LT,
    TEXT_HEAD, TEXT_MAIN, TEXT_SEC, TEXT_DIM,
    AMBER, AMBER_DIM,
    HISTORICAL_PRESETS,
    draw_panel_border, draw_divider,
)
from game.components.button import RimButton


class MenuScreen(BaseScreen):
    def __init__(self, engine):
        super().__init__(engine)
        self.fonts = engine.fonts
        self.hovered = -1
        self._bg = self._make_bg()

        # Layout: left sidebar 272px, cards fill the rest
        sidebar_w = 272
        card_area_x = sidebar_w + 20
        card_area_w = SCREEN_W - card_area_x - 20

        card_w = (card_area_w - 20) // 3
        card_h = 140
        gap = 10

        row1_y = 120
        row2_y = row1_y + card_h + gap

        self.preset_rects = []
        # Row 1: 3 cards
        for i in range(3):
            x = card_area_x + i * (card_w + gap)
            self.preset_rects.append(pygame.Rect(x, row1_y, card_w, card_h))
        # Row 2: 2 cards centered
        row2_total = 2 * card_w + gap
        row2_x = card_area_x + (card_area_w - row2_total) // 2
        for i in range(2):
            x = row2_x + i * (card_w + gap)
            self.preset_rects.append(pygame.Rect(x, row2_y, card_w, card_h))

        self.custom_btn = RimButton(
            (card_area_x, row2_y + card_h + 16, 280, 38),
            '+ CUSTOM SIMULATION',
            accent=True,
        )

    # ------------------------------------------------------------------ #

    def _make_bg(self):
        bg = pygame.Surface((SCREEN_W, SCREEN_H))
        bg.fill(BG_DARK)
        # Very subtle noise texture (parchment-like)
        for _ in range(4000):
            x = random.randint(0, SCREEN_W - 1)
            y = random.randint(0, SCREEN_H - 1)
            v = random.randint(0, 8)
            c = (18 + v, 16 + v, 14 + v)
            bg.set_at((x, y), c)
        return bg

    # ------------------------------------------------------------------ #
    # Events / Update / Draw                                               #
    # ------------------------------------------------------------------ #

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = -1
            for i, r in enumerate(self.preset_rects):
                if r.collidepoint(event.pos):
                    self.hovered = i

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(self.preset_rects):
                if r.collidepoint(event.pos) and i < len(HISTORICAL_PRESETS):
                    self.engine.start_config(HISTORICAL_PRESETS[i])
                    return
            if self.custom_btn.rect.collidepoint(event.pos):
                self.engine.start_config(None)
                return

        self.custom_btn.handle_event(event)

    def update(self, dt):
        self.custom_btn.update()

    def draw(self, surface):
        surface.blit(self._bg, (0, 0))
        self._draw_sidebar(surface)
        self._draw_cards(surface)
        self.custom_btn.draw(surface, self.fonts)
        # Bottom credits
        cr = self.fonts['tiny'].render(
            'ESC to return  |  Social Mimic Agent System  v1.0',
            True, TEXT_DIM,
        )
        surface.blit(cr, (SCREEN_W - cr.get_width() - 12, SCREEN_H - 18))

    # ------------------------------------------------------------------ #
    # Sidebar                                                              #
    # ------------------------------------------------------------------ #

    def _draw_sidebar(self, surface):
        sb = pygame.Rect(0, 0, 272, SCREEN_H)
        pygame.draw.rect(surface, BG_PANEL, sb)
        # Right border of sidebar
        pygame.draw.line(surface, BORDER,
                         (sb.right - 1, 0), (sb.right - 1, SCREEN_H))

        # Title block
        header_h = 90
        pygame.draw.rect(surface, BG_HEADER, (0, 0, 272, header_h))
        draw_divider(surface, pygame.Rect(0, header_h, 272, 1), color=AMBER_DIM)

        t1 = self.fonts['header'].render('SOCIAL', True, AMBER)
        t2 = self.fonts['header'].render('SIMULATION', True, TEXT_HEAD)
        t3 = self.fonts['body'].render('ENGINE', True, TEXT_SEC)
        surface.blit(t1, (16, 10))
        surface.blit(t2, (16, 36))
        surface.blit(t3, (16, 64))

        # Left accent strip
        pygame.draw.rect(surface, AMBER, (0, 0, 4, header_h))

        # Body items
        y = 108
        draw_divider(surface, pygame.Rect(16, y, 240, 1))
        y += 6
        sec_t = self.fonts['small'].render('SCENARIOS', True, TEXT_SEC)
        surface.blit(sec_t, (16, y))
        y += sec_t.get_height() + 6
        draw_divider(surface, pygame.Rect(16, y, 240, 1))
        y += 8

        features = [
            'Historical simulations',
            'Policy impact analysis',
            'Custom scenarios',
            'Multi-LLM support',
        ]
        for feat in features:
            t = self.fonts['tiny'].render(f'  ·  {feat}', True, TEXT_DIM)
            surface.blit(t, (16, y))
            y += t.get_height() + 4

        # Instructions block at bottom
        y = SCREEN_H - 80
        for line in [
            'Click a scenario card',
            'to begin simulation.',
            '',
            'Or create a custom',
            'simulation below.',
        ]:
            if line:
                t = self.fonts['tiny'].render(line, True, TEXT_DIM)
                surface.blit(t, (16, y))
            y += 14

    # ------------------------------------------------------------------ #
    # Scenario cards                                                       #
    # ------------------------------------------------------------------ #

    def _draw_cards(self, surface):
        # Section header above cards
        hdr = self.fonts['small'].render('SELECT HISTORICAL SCENARIO', True, TEXT_SEC)
        surface.blit(hdr, (292, 96))
        draw_divider(surface, pygame.Rect(292, 112, SCREEN_W - 312, 1))

        for i, (rect, preset) in enumerate(
                zip(self.preset_rects, HISTORICAL_PRESETS)):
            hov = (i == self.hovered)
            pcol = preset['color']

            # Card background
            bg_col = BG_HOVER if hov else BG_PANEL2
            pygame.draw.rect(surface, bg_col, rect)

            # Left color accent strip
            pygame.draw.rect(surface, pcol,
                             pygame.Rect(rect.x, rect.y, 4, rect.h))

            # Border
            border_col = pcol if hov else BORDER
            draw_panel_border(surface, rect, border_col)

            # Year badge (top right)
            yr = self.fonts['tiny'].render(preset['year'], True, TEXT_SEC)
            surface.blit(yr, (rect.right - yr.get_width() - 10, rect.y + 7))

            # Title
            t_col = TEXT_HEAD if hov else TEXT_MAIN
            title_surf = self.fonts['body'].render(preset['title'], True, t_col)
            if title_surf.get_width() > rect.w - 30:
                title_surf = self.fonts['small'].render(preset['title'], True, t_col)
            surface.blit(title_surf, (rect.x + 12, rect.y + 18))

            # Divider under title
            draw_divider(surface,
                         pygame.Rect(rect.x + 10, rect.y + 40, rect.w - 20, 1))

            # Subtitle
            sub_col = TEXT_MAIN if hov else TEXT_SEC
            st = self.fonts['tiny'].render(preset['subtitle'], True, sub_col)
            surface.blit(st, (rect.x + 12, rect.y + 50))

            # Agent count
            at = self.fonts['tiny'].render(
                f'{len(preset["agents"])} agents', True, pcol
            )
            surface.blit(at, (rect.x + 12, rect.y + rect.h - 20))

            # Hover arrow
            if hov:
                arr = self.fonts['small'].render('▶', True, pcol)
                surface.blit(arr,
                             (rect.right - 20,
                              rect.centery - arr.get_height() // 2))
