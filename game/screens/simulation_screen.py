"""Live simulation screen — RimWorld-style layout."""
import pygame

from game.screens.base_screen import BaseScreen
from game.theme import (
    SCREEN_W, SCREEN_H,
    BG_DARK, BG_PANEL, BG_PANEL2, BG_HEADER,
    BORDER, BORDER_LT,
    TEXT_HEAD, TEXT_MAIN, TEXT_SEC, TEXT_DIM,
    AMBER, AMBER_DIM, SAGE, BRICK, TAN, STEEL,
    SUPPORT_COLOR, OPPOSE_COLOR, NEUTRAL_COLOR,
    SCENARIO_WORLD_TYPES,
    get_agent_color,
    draw_panel_border, draw_divider,
)
from game.components.button import RimButton
from game.components.panel import RimPanel
from game.components.world_map import WorldMap


def _stance_color(stance):
    if not stance:
        return TAN
    s = stance.lower()
    if any(w in s for w in ('support', 'positive', 'beneficial')):
        return SAGE
    if any(w in s for w in ('skeptic', 'concern', 'oppos', 'resist', 'worried')):
        return BRICK
    return TAN


class SimulationScreen(BaseScreen):

    def __init__(self, engine, config, bridge):
        super().__init__(engine)
        self.fonts = engine.fonts
        self.config = config
        self.bridge = bridge
        self.step = 0
        self.total_steps = config.get('steps', 5)
        self.status = 'INITIALIZING...'
        self.event_log = []       # list of (text, color)
        self.agent_data = {}      # name -> {stance, last_action, personality}
        self.step_mode = config.get('step_mode', True)
        self.waiting_for_step = False
        self.paused = False
        self.scroll_y = 0

        # World map: 750 wide, 440 tall, top-left area
        scenario = config.get('scenario', 'workplace')
        world_type = SCENARIO_WORLD_TYPES.get(scenario, 'default')
        self.world = WorldMap(pygame.Rect(8, 52, 750, 440), world_type)

        # Panels
        # Right column: agent list
        self.right_panel = RimPanel(
            pygame.Rect(766, 52, 506, 440), 'AGENTS', AMBER
        )
        # Bottom left: event log
        self.log_panel = RimPanel(
            pygame.Rect(8, 500, 750, 174), 'EVENT LOG', STEEL
        )
        # Bottom right: policy
        self.info_panel = RimPanel(
            pygame.Rect(766, 500, 506, 174), 'POLICY', TAN
        )

        # Control buttons — centered in 48px bar (SCREEN_H-48 to SCREEN_H)
        ctrl_y = SCREEN_H - 39  # = bar_top(672) + (48-30)/2 = 681, centers 30px btn
        self.step_btn  = RimButton((8,   ctrl_y, 90, 30), 'STEP',  color=STEEL)
        self.play_btn  = RimButton((106, ctrl_y, 90, 30), 'RUN',   color=SAGE)
        self.pause_btn = RimButton((204, ctrl_y, 90, 30), 'PAUSE', color=TAN)
        self.end_btn   = RimButton(
            (SCREEN_W - 120, ctrl_y, 112, 30), 'END', accent=True, color=AMBER
        )

    # ------------------------------------------------------------------ #

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.step_btn.rect.collidepoint(event.pos) and self.waiting_for_step:
                self.waiting_for_step = False
            elif self.play_btn.rect.collidepoint(event.pos):
                self.step_mode = False
                self.waiting_for_step = False
            elif self.pause_btn.rect.collidepoint(event.pos):
                self.paused = not self.paused
            elif self.end_btn.rect.collidepoint(event.pos):
                if self.bridge.is_complete and self.bridge.evaluation:
                    self.engine.show_evaluation(
                        self.bridge.evaluation, self.config
                    )
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y = max(0, self.scroll_y - event.y * 20)

        self.step_btn.handle_event(event)
        self.play_btn.handle_event(event)
        self.pause_btn.handle_event(event)
        self.end_btn.handle_event(event)

    def _add_log(self, text, color=None):
        self.event_log.append((text, color or TEXT_MAIN))
        if len(self.event_log) > 200:
            self.event_log = self.event_log[-200:]

    def update(self, dt):
        if not self.paused:
            self.world.update(dt)

        events = self.bridge.poll()
        for ev in events:
            etype = ev[0]

            if etype == 'log':
                col_name = ev[2] if len(ev) > 2 else 'main'
                col = STEEL if col_name == 'cyan' else TEXT_MAIN
                self._add_log(f'[SYS] {ev[1]}', col)

            elif etype == 'agents_ready':
                _, agent_list = ev
                self.world.setup_agents(agent_list)
                for a in agent_list:
                    self.agent_data[a['name']] = {
                        'stance': None,
                        'last_action': '',
                        'personality': a['personality'],
                    }
                self.status = 'RUNNING'
                self._add_log('Agents deployed into simulation.', STEEL)

            elif etype == 'step_start':
                _, data = ev
                self.step = data['step']
                self.status = f"STEP {data['step'] + 1} / {data['total']}"
                self._add_log(f"Step {data['step'] + 1} starting...", TAN)

            elif etype == 'agent_thinking':
                _, name = ev
                self.world.agent_thinking(name)
                self._add_log(f'  {name} is thinking...', TEXT_DIM)

            elif etype == 'agent_action':
                _, data = ev
                name   = data['name']
                action = data['action']
                stance = data['stance']
                if name in self.agent_data:
                    self.agent_data[name]['stance']      = stance
                    self.agent_data[name]['last_action'] = action
                self.world.agent_acted(name, action, stance)
                short = action[:90] + '...' if len(action) > 90 else action
                col = get_agent_color(
                    self.agent_data.get(name, {}).get('personality', '')
                )
                self._add_log(f'  {name}: {short}', col)

            elif etype == 'broadcast':
                _, data = ev
                self.world.broadcast(data['from'], data['to'])
                self._add_log(
                    f'  {data["from"]} broadcasts to {len(data["to"])} agents',
                    AMBER_DIM,
                )

            elif etype == 'step_complete':
                _, data = ev
                self._add_log(f'  Step {data["step"] + 1} complete.', SAGE)
                if self.step_mode:
                    self.waiting_for_step = True
                    self.status = 'PAUSED — press STEP to continue'

            elif etype == 'evaluation_ready':
                self.status = 'SIMULATION COMPLETE'
                self._add_log(
                    'Simulation complete — click END to view results.', AMBER
                )

            elif etype == 'error':
                _, msg = ev
                self._add_log(f'[ERROR] {msg}', BRICK)
                self.status = f'ERROR: {msg[:50]}'

        self.step_btn.update()
        self.play_btn.update()
        self.pause_btn.update()
        self.end_btn.update()

    # ------------------------------------------------------------------ #
    # Drawing                                                              #
    # ------------------------------------------------------------------ #

    def draw(self, surface):
        surface.fill(BG_DARK)
        self._draw_topbar(surface)
        self.world.draw(surface, self.fonts)
        self._draw_right_panel(surface)
        self._draw_log(surface)
        self._draw_info_panel(surface)
        self._draw_controls(surface)

    def _draw_topbar(self, surface):
        bar = pygame.Rect(0, 0, SCREEN_W, 46)
        pygame.draw.rect(surface, BG_PANEL, bar)
        # Amber left accent strip
        pygame.draw.rect(surface, AMBER, (0, 0, 4, 46))
        draw_divider(surface, pygame.Rect(0, 46, SCREEN_W, 1), color=BORDER)

        scenario_name = self.config.get('scenario', 'simulation').upper()
        title = self.fonts['body'].render(
            f'  {scenario_name}  |  {self.status}', True, TEXT_HEAD
        )
        surface.blit(title, (16, 13))

        step_txt = self.fonts['body'].render(
            f'STEP {self.step + 1} / {self.total_steps}', True, AMBER
        )
        surface.blit(step_txt, (SCREEN_W - step_txt.get_width() - 16, 13))

    def _draw_right_panel(self, surface):
        self.right_panel.draw(surface, self.fonts)
        cr = self.right_panel.content_rect()

        card_h = 86
        clip = surface.get_clip()
        surface.set_clip(cr)

        y = cr.y - self.scroll_y
        for name, data in self.agent_data.items():
            if y + card_h > cr.y and y < cr.y + cr.h:
                card_rect = pygame.Rect(cr.x, y, cr.w, card_h - 4)
                col = get_agent_color(data.get('personality', ''))

                # Card background
                pygame.draw.rect(surface, BG_PANEL2, card_rect)
                # Left color strip (agent color)
                pygame.draw.rect(surface, col,
                                 pygame.Rect(card_rect.x, card_rect.y,
                                             4, card_rect.h))
                draw_panel_border(surface, card_rect, BORDER)

                # Name
                nt = self.fonts['small'].render(name, True, TEXT_HEAD)
                surface.blit(nt, (card_rect.x + 10, card_rect.y + 6))

                # Stance badge
                stance = data.get('stance') or 'unknown'
                sc = _stance_color(stance)
                st_t = self.fonts['tiny'].render(stance[:40], True, sc)
                surface.blit(st_t, (card_rect.x + 10, card_rect.y + 24))

                # Personality (dim)
                pers = data.get('personality', '')
                if pers:
                    pt = self.fonts['tiny'].render(pers[:60], True, TEXT_DIM)
                    surface.blit(pt, (card_rect.x + 10, card_rect.y + 40))

                # Last action
                action = data.get('last_action', '')
                if action:
                    a1 = self.fonts['tiny'].render(action[:60], True, TEXT_SEC)
                    surface.blit(a1, (card_rect.x + 10, card_rect.y + 58))

            y += card_h

        surface.set_clip(clip)

    def _draw_log(self, surface):
        self.log_panel.draw(surface, self.fonts)
        cr = self.log_panel.content_rect()
        line_h = 15
        max_lines = cr.h // line_h
        visible = self.event_log[-max_lines:]
        clip = surface.get_clip()
        surface.set_clip(cr)
        for i, (text, col) in enumerate(visible):
            # Alternating row background for readability
            if i % 2 == 0:
                row_bg = pygame.Rect(cr.x, cr.y + i * line_h, cr.w, line_h)
                pygame.draw.rect(surface, (BG_PANEL2[0], BG_PANEL2[1],
                                           BG_PANEL2[2]), row_bg)
            t = self.fonts['tiny'].render(text[:100], True, col)
            surface.blit(t, (cr.x + 2, cr.y + i * line_h))
        surface.set_clip(clip)

    def _draw_info_panel(self, surface):
        self.info_panel.draw(surface, self.fonts)
        cr = self.info_panel.content_rect()
        policy = self.config.get('policy', '')

        # Word-wrap policy text
        words = policy.split()
        lines = []
        line = ''
        for w in words:
            test = (line + ' ' + w).strip()
            if (self.fonts['tiny'].render(test, True, TEXT_MAIN).get_width()
                    > cr.w - 8):
                if line:
                    lines.append(line)
                line = w
            else:
                line = test
        if line:
            lines.append(line)

        clip = surface.get_clip()
        surface.set_clip(cr)
        for i, ln in enumerate(lines[:10]):
            t = self.fonts['tiny'].render(ln, True, TEXT_MAIN)
            surface.blit(t, (cr.x, cr.y + i * 16))
        surface.set_clip(clip)

    def _draw_controls(self, surface):
        ctrl_y = SCREEN_H - 48
        bar = pygame.Rect(0, ctrl_y, SCREEN_W, 48)
        pygame.draw.rect(surface, BG_PANEL, bar)
        draw_divider(surface, pygame.Rect(0, ctrl_y, SCREEN_W, 1),
                     color=BORDER)
        # Accent strip
        pygame.draw.rect(surface, AMBER, (0, ctrl_y, 4, 48))

        self.step_btn.draw(surface, self.fonts)
        self.play_btn.draw(surface, self.fonts)
        self.pause_btn.draw(surface, self.fonts)
        self.end_btn.draw(surface, self.fonts)

        # Status hint
        if self.waiting_for_step:
            hint_text = 'Click STEP to advance'
            hint_col  = TAN
        elif self.bridge.is_complete:
            hint_text = 'Simulation complete — click END for results'
            hint_col  = SAGE
        elif self.paused:
            hint_text = 'Paused'
            hint_col  = TAN
        else:
            hint_text = 'Simulation running...'
            hint_col  = TEXT_DIM

        hint = self.fonts['small'].render(hint_text, True, hint_col)
        surface.blit(hint, (360, ctrl_y + 10))
