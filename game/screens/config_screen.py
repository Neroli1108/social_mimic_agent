"""Multi-page configuration wizard — RimWorld flat styling."""
import pygame

from game.screens.base_screen import BaseScreen
from game.theme import (
    SCREEN_W, SCREEN_H,
    BG_DARK, BG_PANEL, BG_PANEL2, BG_HEADER, BG_HOVER, BG_SELECT,
    BORDER, BORDER_LT, BORDER_DK,
    TEXT_HEAD, TEXT_MAIN, TEXT_SEC, TEXT_DIM,
    AMBER, AMBER_DIM, SAGE, BRICK, TAN, STEEL,
    HISTORICAL_PRESETS, EXAMPLE_POLICIES,
    draw_panel_border, draw_divider,
)
from game.components.button import RimButton, RimToggle
from game.components.panel import RimPanel
from game.components.text_input import CyberTextInput
from game.components.dropdown import CyberDropdown

PROVIDERS = ['gemini', 'openai', 'huggingface']
SCENARIOS = ['workplace', 'town', 'school', 'neighborhood', 'government',
             'ancient_city', 'custom']

_PAGE_TITLES = [
    'LLM SETUP',
    'POLICY & SCENARIO',
    'AGENTS',
    'RUN SETTINGS',
]

# Content area dimensions
CONTENT_X = 20
CONTENT_Y = 56
CONTENT_W = SCREEN_W - 40
CONTENT_H = SCREEN_H - 56 - 58   # below header, above nav bar


# ─────────────────────────────────────────────────────────────────────────────
# RimSlider
# ─────────────────────────────────────────────────────────────────────────────

class RimSlider:
    """Flat RimWorld-style slider."""

    def __init__(self, rect, min_val, max_val, value):
        self.rect = pygame.Rect(rect)
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_from_mouse(event.pos[0])
        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        if event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_from_mouse(event.pos[0])

    def _update_from_mouse(self, mx):
        r = (mx - self.rect.x) / max(self.rect.w, 1)
        self.value = int(self.min_val + r * (self.max_val - self.min_val))
        self.value = max(self.min_val, min(self.max_val, self.value))

    def draw(self, surface, fonts=None):
        f = fonts['small'] if fonts else pygame.font.SysFont('verdana', 13)
        cy = self.rect.centery

        # Track
        pygame.draw.rect(surface, BG_PANEL2,
                         pygame.Rect(self.rect.x, cy - 4, self.rect.w, 8))
        draw_panel_border(surface,
                          pygame.Rect(self.rect.x, cy - 4, self.rect.w, 8),
                          BORDER)

        # Fill
        ratio = (self.value - self.min_val) / max(1, self.max_val - self.min_val)
        fw = int(ratio * self.rect.w)
        if fw > 0:
            pygame.draw.rect(surface, AMBER,
                             pygame.Rect(self.rect.x, cy - 4, fw, 8))

        # Thumb
        tx = self.rect.x + fw
        pygame.draw.rect(surface, TEXT_HEAD,
                         pygame.Rect(tx - 6, cy - 10, 12, 20))
        draw_panel_border(surface,
                          pygame.Rect(tx - 6, cy - 10, 12, 20), AMBER)

        # Value label above thumb
        vt = f.render(str(self.value), True, AMBER)
        surface.blit(vt, (tx - vt.get_width() // 2, self.rect.y - 20))


# Alias for backward compatibility
CyberSlider = RimSlider


# ─────────────────────────────────────────────────────────────────────────────
# ConfigScreen
# ─────────────────────────────────────────────────────────────────────────────

class ConfigScreen(BaseScreen):

    def __init__(self, engine, preset=None):
        super().__init__(engine)
        self.fonts = engine.fonts
        self.preset = preset
        self.page = 0
        self.total_pages = 4
        self._error_msg = ''
        self._error_timer = 0.0

        self._build_page0()
        self._build_page1()
        self._build_page2()
        self._build_page3()

        # Navigation buttons
        nav_y = SCREEN_H - 48
        self.back_btn = RimButton(
            (CONTENT_X, nav_y, 130, 34), '← BACK'
        )
        self.next_btn = RimButton(
            (SCREEN_W - 170, nav_y, 150, 34), 'NEXT →', accent=True
        )
        self.launch_btn = RimButton(
            (SCREEN_W - 220, nav_y, 200, 34),
            'LAUNCH SIMULATION ▶', accent=True, color=AMBER,
        )

    # ------------------------------------------------------------------ #
    # Page builders                                                        #
    # ------------------------------------------------------------------ #

    def _build_page0(self):
        """Page 0: LLM Provider, Model, API Key."""
        lx = CONTENT_X + 20
        base_y = CONTENT_Y + 44  # panel top (66) + title bar (24) + padding (10) = 100

        provider_idx = 0
        self.provider_dd = CyberDropdown(
            (lx, base_y + 17, 420, 32),
            PROVIDERS, selected=provider_idx,
        )

        self.model_input = CyberTextInput(
            (lx, base_y + 87, 420, 32),
            placeholder='Leave blank for provider default  (e.g. gemini-1.5-flash)',
        )

        self.api_key_input = CyberTextInput(
            (lx, base_y + 144, 420, 32),
            placeholder='API Key  (leave blank to use .env)',
            password=True,
        )

        self._provider_hints = {
            'gemini':      'Google Gemini  —  env: GEMINI_API_KEY  —  default: gemini-1.5-flash',
            'openai':      'OpenAI  —  env: OPENAI_API_KEY  —  default: gpt-4o',
            'huggingface': 'HuggingFace  —  env: HUGGINGFACE_API_KEY  —  set model explicitly',
        }

    def _build_page1(self):
        """Page 1: Policy text, example buttons, scenario dropdown."""
        lx = CONTENT_X + 20
        base_y = CONTENT_Y + 42  # panel top (64) + title bar (24) + padding (10) = 98

        policy_text = ''
        if self.preset:
            policy_text = self.preset.get('policy', '')

        self.policy_input = CyberTextInput(
            (lx, base_y + 17, 700, 160),
            placeholder='Enter policy text...',
            multiline=True,
        )
        self.policy_input.text = policy_text
        self.policy_input.cursor_pos = len(policy_text)

        # Example policy buttons
        self._example_btns = []
        for i, ep in enumerate(EXAMPLE_POLICIES[:3]):
            short = ep[:48] + '...' if len(ep) > 48 else ep
            btn = RimButton(
                (lx + i * 238, base_y + 197, 228, 26),
                short,
            )
            btn._full_policy = ep
            self._example_btns.append(btn)

        scenario_idx = 0
        if self.preset:
            wt = self.preset.get('world_type', 'default')
            for idx, s in enumerate(SCENARIOS):
                if s == wt:
                    scenario_idx = idx
                    break
        self.scenario_dd = CyberDropdown(
            (lx, base_y + 248, 340, 32),
            SCENARIOS, selected=scenario_idx,
        )

        self.custom_scenario_input = CyberTextInput(
            (lx, base_y + 305, 340, 80),
            placeholder='Describe your custom scenario...',
            multiline=True,
        )

    def _build_page2(self):
        """Page 2: Agent rows (name + personality)."""
        preset_agents = []
        if self.preset and 'agents' in self.preset:
            preset_agents = self.preset['agents']

        default_count = max(2, len(preset_agents)) if preset_agents else 3
        self._agent_count = default_count
        self._max_agents = 8
        self._agent_inputs = []
        self._rebuild_agent_inputs(preset_agents)

        cx = SCREEN_W // 2
        self.add_agent_btn = RimButton(
            (cx - 115, SCREEN_H - 110, 105, 30),
            '+ AGENT', color=SAGE,
        )
        self.remove_agent_btn = RimButton(
            (cx + 10, SCREEN_H - 110, 105, 30),
            '- AGENT', color=BRICK,
        )

    def _rebuild_agent_inputs(self, preset_agents=None):
        lx = CONTENT_X + 20
        base_y = CONTENT_Y + 60  # panel top (64) + title bar (24) + header row (18) + padding (10) = 116
        row_h = 56

        existing = []
        for ni, pi in self._agent_inputs:
            existing.append((ni.text, pi.text))

        self._agent_inputs = []
        for i in range(self._agent_count):
            name_input = CyberTextInput(
                (lx, base_y + i * row_h, 210, 32),
                placeholder=f'Agent {i + 1} name',
            )
            personality_input = CyberTextInput(
                (lx + 220, base_y + i * row_h, 500, 32),
                placeholder='personality traits (e.g. analytical, cautious)',
            )
            if i < len(existing):
                name_input.text = existing[i][0]
                personality_input.text = existing[i][1]
                name_input.cursor_pos = len(name_input.text)
                personality_input.cursor_pos = len(personality_input.text)
            elif preset_agents and i < len(preset_agents):
                name_input.text = preset_agents[i]['name']
                personality_input.text = preset_agents[i]['personality']
                name_input.cursor_pos = len(name_input.text)
                personality_input.cursor_pos = len(personality_input.text)
            self._agent_inputs.append((name_input, personality_input))

    @property
    def agent_inputs(self):
        return self._agent_inputs

    def _build_page3(self):
        """Page 3: Steps slider, mode toggle."""
        cx = SCREEN_W // 2
        base_y = CONTENT_Y + 42  # panel top (64) + title bar (24) + padding (10) = 98

        self.steps_slider = RimSlider(
            (cx - 220, base_y + 20, 440, 20),
            min_val=1, max_val=20, value=5,
        )

        self.mode_toggle = RimToggle(
            (cx - 160, base_y + 82, 320, 34),
            options=['STEP-BY-STEP', 'CONTINUOUS'],
            selected=0,
        )

    # ------------------------------------------------------------------ #
    # Event handling                                                       #
    # ------------------------------------------------------------------ #

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.page > 0 and self.back_btn.rect.collidepoint(event.pos):
                self.page -= 1
                return
            if (self.page < self.total_pages - 1
                    and self.next_btn.rect.collidepoint(event.pos)):
                if self._validate_page():
                    self.page += 1
                return
            if (self.page == self.total_pages - 1
                    and self.launch_btn.rect.collidepoint(event.pos)):
                if self._validate_all():
                    self.engine.start_simulation(self._get_config())
                return

        self.back_btn.handle_event(event)
        self.next_btn.handle_event(event)
        self.launch_btn.handle_event(event)

        if self.page == 0:
            self._handle_page0(event)
        elif self.page == 1:
            self._handle_page1(event)
        elif self.page == 2:
            self._handle_page2(event)
        elif self.page == 3:
            self._handle_page3(event)

    def _handle_page0(self, event):
        self.provider_dd.handle_event(event)
        self.model_input.handle_event(event)
        self.api_key_input.handle_event(event)

    def _handle_page1(self, event):
        self.policy_input.handle_event(event)
        self.scenario_dd.handle_event(event)
        self.custom_scenario_input.handle_event(event)
        for btn in self._example_btns:
            if btn.handle_event(event):
                self.policy_input.text = btn._full_policy
                self.policy_input.cursor_pos = len(btn._full_policy)

    def _handle_page2(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.add_agent_btn.rect.collidepoint(event.pos):
                if self._agent_count < self._max_agents:
                    self._agent_count += 1
                    self._rebuild_agent_inputs()
                return
            if self.remove_agent_btn.rect.collidepoint(event.pos):
                if self._agent_count > 2:
                    self._agent_count -= 1
                    self._rebuild_agent_inputs()
                return
        for ni, pi in self._agent_inputs:
            ni.handle_event(event)
            pi.handle_event(event)

    def _handle_page3(self, event):
        self.steps_slider.handle_event(event)
        self.mode_toggle.handle_event(event)

    # ------------------------------------------------------------------ #
    # Validation                                                           #
    # ------------------------------------------------------------------ #

    def _validate_page(self):
        if self.page == 1:
            if not self.policy_input.text.strip():
                self._set_error('Please enter a policy text.')
                return False
        if self.page == 2:
            for i, (ni, pi) in enumerate(self._agent_inputs):
                if not ni.text.strip():
                    self._set_error(f'Agent {i + 1} needs a name.')
                    return False
                if not pi.text.strip():
                    self._set_error(f'Agent {i + 1} needs personality traits.')
                    return False
        return True

    def _validate_all(self):
        if not self.policy_input.text.strip():
            self._set_error('Policy text is required.')
            return False
        for i, (ni, pi) in enumerate(self._agent_inputs):
            if not ni.text.strip():
                self._set_error(f'Agent {i + 1} needs a name.')
                return False
        return True

    def _set_error(self, msg):
        self._error_msg = msg
        self._error_timer = 3.0

    # ------------------------------------------------------------------ #
    # Update                                                               #
    # ------------------------------------------------------------------ #

    def update(self, dt):
        if self._error_timer > 0:
            self._error_timer -= dt

        self.back_btn.update()
        self.next_btn.update()
        self.launch_btn.update()

        if self.page == 0:
            self.model_input.update()
            self.api_key_input.update()
        elif self.page == 1:
            self.policy_input.update()
            self.custom_scenario_input.update()
            for btn in self._example_btns:
                btn.update()
        elif self.page == 2:
            for ni, pi in self._agent_inputs:
                ni.update()
                pi.update()

    # ------------------------------------------------------------------ #
    # Drawing                                                              #
    # ------------------------------------------------------------------ #

    def draw(self, surface):
        surface.fill(BG_DARK)
        self._draw_header(surface)
        self._draw_page(surface)
        self._draw_nav(surface)
        if self._error_timer > 0:
            self._draw_error(surface)

    def _draw_header(self, surface):
        bar = pygame.Rect(0, 0, SCREEN_W, 52)
        pygame.draw.rect(surface, BG_PANEL, bar)
        # Left accent strip
        pygame.draw.rect(surface, AMBER, (0, 0, 4, 52))
        draw_divider(surface, pygame.Rect(0, 52, SCREEN_W, 1), color=BORDER)

        title = self.fonts['header'].render(
            f'SIMULATION CONFIGURATION  —  {_PAGE_TITLES[self.page]}',
            True, TEXT_HEAD,
        )
        surface.blit(title, (20, 14))

        if self.preset:
            p = self.fonts['tiny'].render(
                f'Preset: {self.preset.get("title", "")}', True, TEXT_SEC
            )
            surface.blit(p, (SCREEN_W - p.get_width() - 16, 18))

        # Page step indicators (dots + labels)
        dot_y = 38
        spacing = 120
        start_x = SCREEN_W // 2 - (self.total_pages - 1) * spacing // 2
        for i in range(self.total_pages):
            if i < self.page:
                col = AMBER_DIM
            elif i == self.page:
                col = AMBER
            else:
                col = TEXT_DIM
            pygame.draw.circle(surface, col, (start_x + i * spacing, dot_y), 4)
            lbl = self.fonts['tiny'].render(_PAGE_TITLES[i], True, col)
            surface.blit(lbl, lbl.get_rect(
                centerx=start_x + i * spacing, top=dot_y + 8))

    def _draw_nav(self, surface):
        nav_y = SCREEN_H - 58
        bar = pygame.Rect(0, nav_y, SCREEN_W, 58)
        pygame.draw.rect(surface, BG_PANEL, bar)
        draw_divider(surface, pygame.Rect(0, nav_y, SCREEN_W, 1), color=BORDER)
        # Left accent strip
        pygame.draw.rect(surface, AMBER, (0, nav_y, 4, 58))

        if self.page > 0:
            self.back_btn.draw(surface, self.fonts)

        if self.page < self.total_pages - 1:
            self.next_btn.draw(surface, self.fonts)
        else:
            self.launch_btn.draw(surface, self.fonts)

    def _draw_error(self, surface):
        err = self.fonts['body'].render(f'  {self._error_msg}  ', True, BRICK)
        er = err.get_rect(centerx=SCREEN_W // 2, bottom=SCREEN_H - 62)
        bg = pygame.Surface((er.w + 8, er.h + 4), pygame.SRCALPHA)
        bg.fill((*BRICK, 40))
        surface.blit(bg, (er.x - 4, er.y - 2))
        surface.blit(err, er)

    def _draw_page(self, surface):
        if self.page == 0:
            self._draw_page0(surface)
        elif self.page == 1:
            self._draw_page1(surface)
        elif self.page == 2:
            self._draw_page2(surface)
        elif self.page == 3:
            self._draw_page3(surface)

    # ------------------------------------------------------------------ #
    # Page renderers                                                       #
    # ------------------------------------------------------------------ #

    def _draw_label(self, surface, text, x, y, color=None):
        lbl = self.fonts['small'].render(text, True, color or TEXT_SEC)
        surface.blit(lbl, (x, y))

    def _draw_page0(self, surface):
        lx = CONTENT_X + 20
        base_y = CONTENT_Y + 44  # matches _build_page0

        # Panel background for the form
        form_rect = pygame.Rect(CONTENT_X, CONTENT_Y + 10,
                                500, CONTENT_H - 20)
        pygame.draw.rect(surface, BG_PANEL, form_rect)
        draw_panel_border(surface, form_rect, BORDER)
        # Title bar
        pygame.draw.rect(surface, BG_HEADER,
                         pygame.Rect(form_rect.x, form_rect.y, form_rect.w, 24))
        draw_divider(surface,
                     pygame.Rect(form_rect.x, form_rect.y + 24, form_rect.w, 1),
                     color=AMBER_DIM)
        pygame.draw.rect(surface, AMBER,
                         pygame.Rect(form_rect.x, form_rect.y, 3, 24))
        hdr = self.fonts['small'].render('LLM PROVIDER', True, AMBER)
        surface.blit(hdr, (form_rect.x + 10,
                           form_rect.y + (24 - hdr.get_height()) // 2))

        self._draw_label(surface, 'PROVIDER', lx, base_y)
        self.provider_dd.draw(surface, self.fonts)

        hint = self._provider_hints.get(PROVIDERS[self.provider_dd.selected], '')
        ht = self.fonts['tiny'].render(hint, True, TEXT_DIM)
        surface.blit(ht, (lx, base_y + 53))

        self._draw_label(surface, 'MODEL  (optional)', lx, base_y + 70)
        self.model_input.draw(surface, self.fonts)

        self._draw_label(surface, 'API KEY  (optional — overrides .env)',
                         lx, base_y + 127)
        self.api_key_input.draw(surface, self.fonts)

        # Info box on right side
        info_rect = pygame.Rect(CONTENT_X + 520, CONTENT_Y + 10,
                                SCREEN_W - CONTENT_X - 540, CONTENT_H - 20)
        pygame.draw.rect(surface, BG_PANEL, info_rect)
        draw_panel_border(surface, info_rect, BORDER)
        pygame.draw.rect(surface, BG_HEADER,
                         pygame.Rect(info_rect.x, info_rect.y, info_rect.w, 24))
        draw_divider(surface,
                     pygame.Rect(info_rect.x, info_rect.y + 24, info_rect.w, 1),
                     color=BORDER)
        pygame.draw.rect(surface, STEEL,
                         pygame.Rect(info_rect.x, info_rect.y, 3, 24))
        ih = self.fonts['small'].render('INFORMATION', True, STEEL)
        surface.blit(ih, (info_rect.x + 10,
                          info_rect.y + (24 - ih.get_height()) // 2))

        info_lines = [
            'API keys are loaded from your .env file by default.',
            'You can override them here for this session only.',
            '',
            'Supported providers:',
            '  gemini  |  openai  |  huggingface',
            '',
            'Leave model blank to use the provider default.',
        ]
        iy = info_rect.y + 32
        for ln in info_lines:
            if ln:
                lt = self.fonts['tiny'].render(ln, True, TEXT_DIM)
                surface.blit(lt, (info_rect.x + 12, iy))
            iy += 18

    def _draw_page1(self, surface):
        lx = CONTENT_X + 20
        base_y = CONTENT_Y + 42  # matches _build_page1

        # Left panel: policy
        left_r = pygame.Rect(CONTENT_X, CONTENT_Y + 8,
                             740, CONTENT_H - 16)
        pygame.draw.rect(surface, BG_PANEL, left_r)
        draw_panel_border(surface, left_r, BORDER)
        pygame.draw.rect(surface, BG_HEADER,
                         pygame.Rect(left_r.x, left_r.y, left_r.w, 24))
        draw_divider(surface,
                     pygame.Rect(left_r.x, left_r.y + 24, left_r.w, 1),
                     color=AMBER_DIM)
        pygame.draw.rect(surface, AMBER,
                         pygame.Rect(left_r.x, left_r.y, 3, 24))
        ph = self.fonts['small'].render('POLICY & SCENARIO', True, AMBER)
        surface.blit(ph, (left_r.x + 10,
                          left_r.y + (24 - ph.get_height()) // 2))

        self._draw_label(surface, 'POLICY TEXT', lx, base_y)
        self.policy_input.draw(surface, self.fonts)

        # Example buttons
        ep_l = self.fonts['tiny'].render('Quick examples:', True, TEXT_DIM)
        surface.blit(ep_l, (lx, base_y + 181))
        for btn in self._example_btns:
            btn.draw(surface, self.fonts)

        self._draw_label(surface, 'SCENARIO / WORLD TYPE', lx, base_y + 233)
        self.scenario_dd.draw(surface, self.fonts)

        if self.scenario_dd.value == 'custom':
            self._draw_label(surface, 'CUSTOM SCENARIO DESCRIPTION',
                             lx, base_y + 290)
            self.custom_scenario_input.draw(surface, self.fonts)

        # Right info panel
        right_r = pygame.Rect(760 + CONTENT_X, CONTENT_Y + 8,
                              SCREEN_W - 780 - CONTENT_X, CONTENT_H - 16)
        pygame.draw.rect(surface, BG_PANEL, right_r)
        draw_panel_border(surface, right_r, BORDER)
        pygame.draw.rect(surface, BG_HEADER,
                         pygame.Rect(right_r.x, right_r.y, right_r.w, 24))
        draw_divider(surface,
                     pygame.Rect(right_r.x, right_r.y + 24, right_r.w, 1),
                     color=BORDER)
        pygame.draw.rect(surface, TEXT_SEC,
                         pygame.Rect(right_r.x, right_r.y, 3, 24))
        rh = self.fonts['small'].render('TIPS', True, TEXT_SEC)
        surface.blit(rh, (right_r.x + 10,
                          right_r.y + (24 - rh.get_height()) // 2))

        tips = [
            'Write a clear, specific',
            'policy statement.',
            '',
            'The agents will debate',
            'and respond to this.',
            '',
            'Examples range from',
            'economic to social',
            'to military policies.',
        ]
        ty = right_r.y + 32
        for tip in tips:
            if tip:
                tt = self.fonts['tiny'].render(tip, True, TEXT_DIM)
                surface.blit(tt, (right_r.x + 10, ty))
            ty += 16

    def _draw_page2(self, surface):
        lx = CONTENT_X + 20
        base_y = CONTENT_Y + 60  # matches _rebuild_agent_inputs
        row_h = 56

        # Container panel
        cont_r = pygame.Rect(CONTENT_X, CONTENT_Y + 8,
                             SCREEN_W - CONTENT_X * 2, CONTENT_H - 16)
        pygame.draw.rect(surface, BG_PANEL, cont_r)
        draw_panel_border(surface, cont_r, BORDER)
        pygame.draw.rect(surface, BG_HEADER,
                         pygame.Rect(cont_r.x, cont_r.y, cont_r.w, 24))
        draw_divider(surface,
                     pygame.Rect(cont_r.x, cont_r.y + 24, cont_r.w, 1),
                     color=AMBER_DIM)
        pygame.draw.rect(surface, AMBER,
                         pygame.Rect(cont_r.x, cont_r.y, 3, 24))
        ah = self.fonts['small'].render('AGENTS', True, AMBER)
        surface.blit(ah, (cont_r.x + 10,
                          cont_r.y + (24 - ah.get_height()) // 2))

        # Column headers
        nh = self.fonts['small'].render('AGENT NAME', True, TEXT_SEC)
        ph = self.fonts['small'].render('PERSONALITY TRAITS', True, TEXT_SEC)
        surface.blit(nh, (lx, base_y - 18))
        surface.blit(ph, (lx + 220, base_y - 18))

        for i, (ni, pi) in enumerate(self._agent_inputs):
            y = base_y + i * row_h
            if y + 36 > cont_r.bottom - 50:
                break
            # Row number + divider
            num = self.fonts['tiny'].render(f'{i + 1}', True, TEXT_DIM)
            surface.blit(num, (lx - 14, y + 10))
            if i > 0:
                draw_divider(surface,
                             pygame.Rect(lx, y - 2, cont_r.w - 40, 1),
                             color=BORDER_DK)
            ni.draw(surface, self.fonts)
            pi.draw(surface, self.fonts)

        # Add/Remove buttons + count
        self.add_agent_btn.draw(surface, self.fonts)
        self.remove_agent_btn.draw(surface, self.fonts)

        ct = self.fonts['small'].render(
            f'{self._agent_count} agents configured  (max {self._max_agents})',
            True, TEXT_SEC,
        )
        surface.blit(ct, ct.get_rect(centerx=SCREEN_W // 2,
                                     top=SCREEN_H - 130))

    def _draw_page3(self, surface):
        cx = SCREEN_W // 2
        base_y = CONTENT_Y + 42  # matches _build_page3

        # Left panel: run settings
        left_r = pygame.Rect(CONTENT_X, CONTENT_Y + 8, 600, CONTENT_H - 16)
        pygame.draw.rect(surface, BG_PANEL, left_r)
        draw_panel_border(surface, left_r, BORDER)
        pygame.draw.rect(surface, BG_HEADER,
                         pygame.Rect(left_r.x, left_r.y, left_r.w, 24))
        draw_divider(surface,
                     pygame.Rect(left_r.x, left_r.y + 24, left_r.w, 1),
                     color=AMBER_DIM)
        pygame.draw.rect(surface, AMBER,
                         pygame.Rect(left_r.x, left_r.y, 3, 24))
        rs = self.fonts['small'].render('RUN SETTINGS', True, AMBER)
        surface.blit(rs, (left_r.x + 10,
                          left_r.y + (24 - rs.get_height()) // 2))

        # Steps slider section
        lx = CONTENT_X + 20
        self._draw_label(surface, 'SIMULATION STEPS', lx, base_y)
        self.steps_slider.draw(surface, self.fonts)

        st = self.fonts['tiny'].render(
            'Each step: every agent acts once and broadcasts to all others.',
            True, TEXT_DIM,
        )
        surface.blit(st, (lx, base_y + 44))

        # Mode toggle section
        self._draw_label(surface, 'SIMULATION MODE',
                         cx - 160, base_y + 64)
        self.mode_toggle.draw(surface, self.fonts)

        hint_step = 'Step-by-step: pause after each step, advance manually.'
        hint_cont = 'Continuous: run all steps automatically without pausing.'
        hint = hint_step if self.mode_toggle.selected == 0 else hint_cont
        ht = self.fonts['tiny'].render(hint, True, TEXT_DIM)
        surface.blit(ht, (cx - 160, base_y + 124))

        # Right panel: config summary
        right_r = pygame.Rect(620 + CONTENT_X, CONTENT_Y + 8,
                              SCREEN_W - 640 - CONTENT_X, CONTENT_H - 16)
        self._draw_summary(surface, right_r)

    def _draw_summary(self, surface, rect):
        pygame.draw.rect(surface, BG_PANEL, rect)
        draw_panel_border(surface, rect, BORDER)
        pygame.draw.rect(surface, BG_HEADER,
                         pygame.Rect(rect.x, rect.y, rect.w, 24))
        draw_divider(surface,
                     pygame.Rect(rect.x, rect.y + 24, rect.w, 1), color=BORDER)
        pygame.draw.rect(surface, TEXT_SEC,
                         pygame.Rect(rect.x, rect.y, 3, 24))
        sh = self.fonts['small'].render('CONFIGURATION SUMMARY', True, TEXT_SEC)
        surface.blit(sh, (rect.x + 10, rect.y + (24 - sh.get_height()) // 2))

        lines = []
        lines.append(('Provider', PROVIDERS[self.provider_dd.selected]))
        model_val = self.model_input.text or '(default)'
        lines.append(('Model', model_val))
        policy_short = self.policy_input.text[:60].replace('\n', ' ')
        if len(self.policy_input.text) > 60:
            policy_short += '...'
        lines.append(('Policy', policy_short))
        lines.append(('Scenario', self.scenario_dd.value or ''))
        agent_names = ', '.join(
            ni.text for ni, _ in self._agent_inputs if ni.text
        )
        if len(agent_names) > 60:
            agent_names = agent_names[:57] + '...'
        lines.append(('Agents', agent_names))
        lines.append(('Steps', str(self.steps_slider.value)))
        mode_str = 'Step-by-step' if self.mode_toggle.selected == 0 else 'Continuous'
        lines.append(('Mode', mode_str))

        y = rect.y + 32
        for key, val in lines:
            kt = self.fonts['tiny'].render(f'{key}:', True, TEXT_SEC)
            vt = self.fonts['tiny'].render(val, True, TEXT_MAIN)
            surface.blit(kt, (rect.x + 10, y))
            surface.blit(vt, (rect.x + 80, y))
            y += 20

    # ------------------------------------------------------------------ #
    # Config builder                                                       #
    # ------------------------------------------------------------------ #

    def _get_config(self):
        return {
            'provider': PROVIDERS[self.provider_dd.selected],
            'model': self.model_input.text.strip() or None,
            'api_key': self.api_key_input.text.strip() or None,
            'policy': self.policy_input.text.strip(),
            'scenario': SCENARIOS[self.scenario_dd.selected],
            'agents': [
                {'name': ni.text.strip(), 'personality': pi.text.strip()}
                for ni, pi in self._agent_inputs
                if ni.text.strip()
            ],
            'steps': self.steps_slider.value,
            'step_mode': self.mode_toggle.selected == 0,
        }
