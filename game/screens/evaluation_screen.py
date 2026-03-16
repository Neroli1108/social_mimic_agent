"""Policy impact evaluation results dashboard — RimWorld styling."""
import pygame
import math

from game.screens.base_screen import BaseScreen
from game.theme import (
    SCREEN_W, SCREEN_H,
    BG_DARK, BG_PANEL, BG_PANEL2, BG_HEADER,
    BORDER, BORDER_LT, BORDER_DK,
    TEXT_HEAD, TEXT_MAIN, TEXT_SEC, TEXT_DIM,
    AMBER, AMBER_DIM, SAGE, BRICK, TAN, STEEL, RUST,
    SUPPORT_COLOR, OPPOSE_COLOR, NEUTRAL_COLOR,
    draw_panel_border, draw_divider,
)
from game.components.button import RimButton
from game.components.panel import RimPanel


def _score_color(score):
    if score >= 7:
        return SAGE
    if score >= 5:
        return TAN
    if score >= 3:
        return RUST
    return BRICK


def _letter_grade(score):
    if score >= 9:
        return 'A+'
    if score >= 8:
        return 'A'
    if score >= 7:
        return 'B+'
    if score >= 6:
        return 'B'
    if score >= 5:
        return 'C'
    if score >= 3:
        return 'D'
    return 'F'


def _rating_text(score):
    if score >= 7:
        return 'EXCELLENT'
    if score >= 5:
        return 'MODERATE'
    if score >= 3:
        return 'CHALLENGING'
    return 'DIFFICULT'


class EvaluationScreen(BaseScreen):

    def __init__(self, engine, evaluation, config):
        super().__init__(engine)
        self.fonts = engine.fonts
        self.evaluation = evaluation
        self.config = config
        self.t = 0.0
        self.bar_progress = 0.0
        self.scroll_y = 0

        # Buttons
        self.menu_btn   = RimButton(
            (20, SCREEN_H - 46, 200, 34), 'MAIN MENU'
        )
        self.replay_btn = RimButton(
            (230, SCREEN_H - 46, 200, 34), 'NEW CONFIG', accent=True
        )

        # Panels layout:
        # Row 1 (y=52, h=220): score panel (left 360) | criteria panel (right)
        # Row 2 (y=280, h=354): support panel (left 520) | recommendations (right)
        self.score_panel    = RimPanel(
            pygame.Rect(8,   52, 360, 220), 'OVERALL SCORE',      AMBER
        )
        self.criteria_panel = RimPanel(
            pygame.Rect(376, 52, SCREEN_W - 384, 220), 'CRITERIA BREAKDOWN', TAN
        )
        self.support_panel  = RimPanel(
            pygame.Rect(8,   280, 520, SCREEN_H - 340), 'SUPPORT ANALYSIS',  SAGE
        )
        self.rec_panel      = RimPanel(
            pygame.Rect(536, 280, SCREEN_W - 544, SCREEN_H - 340),
            'RECOMMENDATIONS', STEEL,
        )

    # ------------------------------------------------------------------ #

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_btn.rect.collidepoint(event.pos):
                self.engine.show_menu()
                return
            if self.replay_btn.rect.collidepoint(event.pos):
                self.engine.start_config(None)
                return
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y = max(0, self.scroll_y - event.y * 20)
        self.menu_btn.handle_event(event)
        self.replay_btn.handle_event(event)

    def update(self, dt):
        self.t += dt
        self.bar_progress = min(1.0, self.bar_progress + dt * 0.8)
        self.menu_btn.update()
        self.replay_btn.update()

    def draw(self, surface):
        surface.fill(BG_DARK)
        self._draw_header(surface)
        self._draw_score(surface)
        self._draw_criteria(surface)
        self._draw_support(surface)
        self._draw_recommendations(surface)
        self.menu_btn.draw(surface, self.fonts)
        self.replay_btn.draw(surface, self.fonts)

    # ------------------------------------------------------------------ #
    # Header                                                               #
    # ------------------------------------------------------------------ #

    def _draw_header(self, surface):
        bar = pygame.Rect(0, 0, SCREEN_W, 46)
        pygame.draw.rect(surface, BG_PANEL, bar)
        pygame.draw.rect(surface, AMBER, (0, 0, 4, 46))
        draw_divider(surface, pygame.Rect(0, 46, SCREEN_W, 1), color=BORDER)

        title = self.fonts['header'].render(
            '  POLICY IMPACT EVALUATION', True, TEXT_HEAD
        )
        surface.blit(title, (16, 12))

        policy_short = self.config.get('policy', '')[:80]
        ps = self.fonts['tiny'].render(policy_short, True, TEXT_SEC)
        surface.blit(ps, (SCREEN_W - ps.get_width() - 16, 16))

    # ------------------------------------------------------------------ #
    # Overall score                                                        #
    # ------------------------------------------------------------------ #

    def _draw_score(self, surface):
        self.score_panel.draw(surface, self.fonts)
        cr = self.score_panel.content_rect()

        raw_score = self.evaluation.get('overall_score', 0)
        animated_score = raw_score * self.bar_progress
        sc = _score_color(raw_score)

        # Big numeric score
        score_txt = self.fonts['title'].render(
            f'{animated_score:.1f}', True, sc
        )
        surface.blit(score_txt,
                     score_txt.get_rect(centerx=cr.centerx - 30, top=cr.y + 10))

        out_of = self.fonts['body'].render('/ 10', True, TEXT_SEC)
        surface.blit(out_of, (
            score_txt.get_rect(centerx=cr.centerx - 30).right + 6,
            cr.y + 30,
        ))

        # Letter grade
        grade = _letter_grade(raw_score)
        gt = self.fonts['header'].render(grade, True, sc)
        surface.blit(gt, gt.get_rect(centerx=cr.centerx + 60, top=cr.y + 12))

        # Rating text
        rating = _rating_text(raw_score)
        rt = self.fonts['body'].render(rating, True, sc)
        surface.blit(rt, rt.get_rect(centerx=cr.centerx, top=cr.y + 80))

        # Horizontal score bar
        bar_y = cr.y + 110
        bar_rect = pygame.Rect(cr.x + 8, bar_y, cr.w - 16, 18)
        pygame.draw.rect(surface, BG_PANEL2, bar_rect)
        draw_panel_border(surface, bar_rect, BORDER)
        fill_w = int((animated_score / 10) * bar_rect.w)
        if fill_w > 0:
            pygame.draw.rect(surface, sc,
                             pygame.Rect(bar_rect.x, bar_rect.y,
                                         fill_w, bar_rect.h))

        # Segment ticks on bar
        for tick in range(1, 10):
            tx = bar_rect.x + int(tick / 10 * bar_rect.w)
            pygame.draw.line(surface, BG_DARK,
                             (tx, bar_rect.y), (tx, bar_rect.bottom), 1)

        # Tick labels
        for v in (0, 5, 10):
            tx = bar_rect.x + int(v / 10 * bar_rect.w)
            vt = self.fonts['tiny'].render(str(v), True, TEXT_DIM)
            surface.blit(vt, vt.get_rect(centerx=tx, top=bar_rect.bottom + 2))

        # Description label
        desc_text = self.evaluation.get('description', '')
        if desc_text:
            words = desc_text.split()
            line = ''
            lines = []
            for w in words:
                test = (line + ' ' + w).strip()
                if (self.fonts['tiny'].render(test, True, TEXT_MAIN).get_width()
                        > cr.w - 16):
                    if line:
                        lines.append(line)
                    line = w
                else:
                    line = test
            if line:
                lines.append(line)
            dy = cr.y + 140
            for ln in lines[:4]:
                lt = self.fonts['tiny'].render(ln, True, TEXT_MAIN)
                surface.blit(lt, (cr.x + 8, dy))
                dy += 15

    # ------------------------------------------------------------------ #
    # Criteria breakdown                                                   #
    # ------------------------------------------------------------------ #

    def _draw_criteria(self, surface):
        self.criteria_panel.draw(surface, self.fonts)
        cr = self.criteria_panel.content_rect()
        criteria_scores = self.evaluation.get('criteria_scores', {})

        bar_h  = 20
        gap    = 7
        x      = cr.x + 8
        max_w  = cr.w - 20

        for i, (name, score) in enumerate(criteria_scores.items()):
            y = cr.y + i * (bar_h + gap)
            if y + bar_h > cr.y + cr.h:
                break

            short_name = name[:28]
            lt = self.fonts['tiny'].render(short_name, True, TEXT_MAIN)
            surface.blit(lt, (x, y + 3))

            label_w  = 220
            bx       = x + label_w
            bar_max  = max_w - label_w - 52
            bg_rect  = pygame.Rect(bx, y + 4, bar_max, bar_h - 6)
            pygame.draw.rect(surface, BG_PANEL2, bg_rect)
            draw_panel_border(surface, bg_rect, BORDER_DK)

            fill_w = int((score / 10) * bar_max * self.bar_progress)
            col = _score_color(score)
            if fill_w > 0:
                pygame.draw.rect(surface, col,
                                 pygame.Rect(bg_rect.x, bg_rect.y,
                                              fill_w, bg_rect.h))

            st = self.fonts['tiny'].render(f'{score:.1f}', True, col)
            surface.blit(st, (bx + bar_max + 6, y + 3))

    # ------------------------------------------------------------------ #
    # Support analysis                                                     #
    # ------------------------------------------------------------------ #

    def _draw_support(self, surface):
        self.support_panel.draw(surface, self.fonts)
        cr = self.support_panel.content_rect()
        sa = self.evaluation.get('support_analysis', {})

        # Pie chart
        pie_cx = cr.x + 90
        pie_cy = cr.y + 80
        radius = 60

        sup_pct = sa.get('support_percentage', 0) / 100
        opp_pct = sa.get('opposition_percentage', 0) / 100
        neu_pct = sa.get('neutral_percentage', 0) / 100

        segs = [
            (sup_pct, SAGE),
            (opp_pct, BRICK),
            (neu_pct, TAN),
        ]
        start_a = -math.pi / 2
        for pct, col in segs:
            if pct <= 0:
                continue
            end_a = start_a + pct * math.pi * 2 * self.bar_progress
            steps = max(2, int(pct * 60))
            pts = [(pie_cx, pie_cy)]
            for s in range(steps + 1):
                a = start_a + (s / steps) * (end_a - start_a)
                pts.append((
                    pie_cx + int(radius * math.cos(a)),
                    pie_cy + int(radius * math.sin(a)),
                ))
            if len(pts) > 2:
                pygame.draw.polygon(surface, col, pts)
            start_a = end_a

        # Pie outline
        pygame.draw.circle(surface, BORDER_LT, (pie_cx, pie_cy), radius, 2)

        # Legend
        lx = cr.x + 168
        legend_entries = [
            ('Support', sa.get('support_percentage', 0),     SAGE),
            ('Oppose',  sa.get('opposition_percentage', 0),  BRICK),
            ('Neutral', sa.get('neutral_percentage', 0),     TAN),
        ]
        for i, (label, pct, col) in enumerate(legend_entries):
            ly = cr.y + 20 + i * 26
            pygame.draw.rect(surface, col, (lx, ly, 12, 12))
            draw_panel_border(surface, pygame.Rect(lx, ly, 12, 12), BORDER)
            lt = self.fonts['small'].render(f'{label}: {pct:.0f}%', True, TEXT_MAIN)
            surface.blit(lt, (lx + 18, ly - 1))

        # Agent breakdown list
        y = cr.y + 102
        for group_name, group_col, key in [
            ('SUPPORTERS', SAGE,  'supporters'),
            ('OPPONENTS',  BRICK, 'opponents'),
            ('NEUTRAL',    TAN,   'neutral'),
        ]:
            agents_in_group = sa.get(key, [])
            if not agents_in_group:
                continue
            if y + 18 > cr.y + cr.h:
                break

            # Group header
            ht = self.fonts['small'].render(group_name, True, group_col)
            surface.blit(ht, (cr.x + 8, y))
            y += 18

            for a in agents_in_group:
                if y + 14 > cr.y + cr.h:
                    break
                name  = a.get('name', '') if isinstance(a, dict) else str(a)
                stance = a.get('stance', '') if isinstance(a, dict) else ''
                at = self.fonts['tiny'].render(
                    f'  · {name}: {stance[:40]}', True, TEXT_SEC
                )
                surface.blit(at, (cr.x + 8, y))
                y += 14
            y += 4

    # ------------------------------------------------------------------ #
    # Recommendations                                                      #
    # ------------------------------------------------------------------ #

    def _draw_recommendations(self, surface):
        self.rec_panel.draw(surface, self.fonts)
        cr = self.rec_panel.content_rect()
        recs = self.evaluation.get('recommendations', [])

        y = cr.y
        for j, rec in enumerate(recs):
            if y >= cr.y + cr.h:
                break

            # Classify recommendation by keywords for icon
            rl = rec.lower()
            if any(w in rl for w in ('improve', 'increase', 'consider', 'should')):
                bullet_char = '▶'
                bullet_col  = STEEL
            elif any(w in rl for w in ('avoid', 'prevent', 'not', 'risk')):
                bullet_char = '✕'
                bullet_col  = BRICK
            else:
                bullet_char = '⚠'
                bullet_col  = TAN

            bullet = self.fonts['small'].render(bullet_char, True, bullet_col)
            surface.blit(bullet, (cr.x + 4, y))

            # Word-wrap recommendation text
            words = rec.split()
            line = ''
            first_line = True
            for w in words:
                test = (line + ' ' + w).strip()
                max_line_w = cr.w - (30 if first_line else 18)
                if (self.fonts['small'].render(test, True, TEXT_MAIN).get_width()
                        > max_line_w):
                    if line and y + 15 <= cr.y + cr.h:
                        indent = 22 if first_line else 16
                        rt = self.fonts['small'].render(line, True, TEXT_MAIN)
                        surface.blit(rt, (cr.x + indent, y))
                        y += 15
                        first_line = False
                    line = w
                else:
                    line = test

            if line and y + 15 <= cr.y + cr.h:
                indent = 22 if first_line else 16
                rt = self.fonts['small'].render(line, True, TEXT_MAIN)
                surface.blit(rt, (cr.x + indent, y))
                y += 15

            y += 8

            # Divider between recommendations
            if j < len(recs) - 1 and y + 4 < cr.y + cr.h:
                pygame.draw.line(surface, BORDER,
                                 (cr.x + 4, y + 2), (cr.right - 4, y + 2))
                y += 6
