"""RimWorld-style text input component (single-line and multiline)."""
import pygame
from game.theme import (
    BG_PANEL2, BORDER, TEXT_MAIN, TEXT_DIM, AMBER,
    draw_panel_border,
)


class CyberTextInput:
    """Text input with RimWorld flat styling.

    The class name is kept as CyberTextInput for backward compatibility.
    """

    def __init__(self, rect, placeholder='', color=None, font=None,
                 password=False, multiline=False):
        self.rect = pygame.Rect(rect)
        self.placeholder = placeholder
        self.color = color  # ignored visually — kept for compat
        self.font = font
        self.password = password
        self.multiline = multiline
        self.text = ''
        self.active = False
        self.cursor_pos = 0
        self.cursor_blink = 0
        self.scroll_offset = 0
        self.line_scroll = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
        if not self.active:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = (self.text[:self.cursor_pos - 1]
                                 + self.text[self.cursor_pos:])
                    self.cursor_pos -= 1
            elif event.key == pygame.K_DELETE:
                self.text = (self.text[:self.cursor_pos]
                             + self.text[self.cursor_pos + 1:])
            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos - 1)
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
            elif event.key == pygame.K_RETURN:
                if self.multiline:
                    self.text = (self.text[:self.cursor_pos]
                                 + '\n'
                                 + self.text[self.cursor_pos:])
                    self.cursor_pos += 1
                else:
                    self.active = False
            elif event.unicode and event.unicode.isprintable():
                self.text = (self.text[:self.cursor_pos]
                             + event.unicode
                             + self.text[self.cursor_pos:])
                self.cursor_pos += 1
            return True
        return False

    def update(self):
        self.cursor_blink = (self.cursor_blink + 1) % 60

    def draw(self, surface, fonts=None):
        f = self.font or (fonts['body'] if fonts else pygame.font.SysFont('verdana', 16))

        # Background
        pygame.draw.rect(surface, BG_PANEL2, self.rect)

        # Border — amber when active, standard border when inactive
        border_col = AMBER if self.active else BORDER
        draw_panel_border(surface, self.rect, border_col)

        inner = pygame.Rect(
            self.rect.x + 6,
            self.rect.y + 4,
            self.rect.w - 12,
            self.rect.h - 8,
        )

        display_text = self.text
        if self.password:
            display_text = '*' * len(self.text)

        if self.multiline:
            self._draw_multiline(surface, f, inner, display_text)
        else:
            self._draw_single(surface, f, inner, display_text)

    def _draw_single(self, surface, f, inner, display_text):
        clip = surface.get_clip()
        surface.set_clip(inner)

        if self.text:
            txt_color = TEXT_MAIN
            render_text = display_text
        else:
            txt_color = TEXT_DIM
            render_text = self.placeholder

        txt_surf = f.render(render_text, True, txt_color)

        # Scroll to keep cursor visible
        if self.text:
            pre_cursor = f.render(display_text[:self.cursor_pos], True, TEXT_MAIN)
            cx = pre_cursor.get_width()
            if cx - self.scroll_offset > inner.w - 10:
                self.scroll_offset = cx - inner.w + 10
            elif cx - self.scroll_offset < 0:
                self.scroll_offset = max(0, cx - 10)

        surface.blit(
            txt_surf,
            (inner.x - self.scroll_offset,
             inner.y + (inner.h - txt_surf.get_height()) // 2),
        )
        surface.set_clip(clip)

        # Cursor
        if self.active and self.cursor_blink < 30 and self.text is not None:
            pre = f.render(display_text[:self.cursor_pos], True, TEXT_MAIN)
            cxp = inner.x + pre.get_width() - self.scroll_offset
            cy = inner.y + 2
            ch = inner.h - 4
            if inner.x <= cxp <= inner.x + inner.w:
                pygame.draw.line(surface, AMBER, (cxp, cy), (cxp, cy + ch), 2)

    def _draw_multiline(self, surface, f, inner, display_text):
        clip = surface.get_clip()
        surface.set_clip(inner)

        lines = display_text.split('\n') if display_text else [self.placeholder]
        if not self.text:
            lines = [self.placeholder]
        line_h = f.get_height() + 2
        max_visible = max(1, inner.h // line_h)

        # Compute cursor line for scrolling
        pre = display_text[:self.cursor_pos]
        cursor_line = pre.count('\n')
        if cursor_line - self.line_scroll >= max_visible:
            self.line_scroll = cursor_line - max_visible + 1
        elif cursor_line < self.line_scroll:
            self.line_scroll = cursor_line

        txt_color = TEXT_MAIN if self.text else TEXT_DIM
        visible_lines = lines[self.line_scroll: self.line_scroll + max_visible]
        for i, line in enumerate(visible_lines):
            ls = f.render(line, True, txt_color)
            surface.blit(ls, (inner.x, inner.y + i * line_h))

        surface.set_clip(clip)

        # Cursor
        if self.active and self.cursor_blink < 30:
            pre_text = display_text[:self.cursor_pos]
            lines_before = pre_text.split('\n')
            cur_line = len(lines_before) - 1 - self.line_scroll
            cur_col_text = lines_before[-1]
            if 0 <= cur_line < max_visible:
                cx_text = f.render(cur_col_text, True, TEXT_MAIN)
                cxp = inner.x + cx_text.get_width()
                cyp = inner.y + cur_line * line_h
                pygame.draw.line(surface, AMBER,
                                 (cxp, cyp), (cxp, cyp + line_h - 2), 2)
