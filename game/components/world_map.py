"""WorldMap component: RimWorld-style top-down view with pawn agents."""
import pygame
import math
import random

from game.theme import (
    BG_DARK, BG_PANEL, BORDER, BORDER_LT,
    TEXT_MAIN, TEXT_SEC, TEXT_HEAD,
    AMBER, SAGE, BRICK, TAN, STEEL,
    SUPPORT_COLOR, OPPOSE_COLOR, NEUTRAL_COLOR,
    get_agent_color, draw_panel_border,
)

# Node positions for each world type (relative to ~760x480 draw area)
WORLD_NODE_POSITIONS = {
    'workplace': [
        (150, 120), (380, 120), (610, 120),
        (150, 240), (380, 240), (610, 240),
        (150, 360), (380, 360), (610, 360),
        (700, 240),
    ],
    'town': [
        (380, 200), (180, 140), (580, 140),
        (130, 300), (630, 300), (280, 380),
        (480, 380), (380, 80),  (380, 440),
        (700, 200),
    ],
    'government': [
        (380, 150), (200, 240), (560, 240),
        (150, 360), (380, 360), (610, 360),
        (300, 100), (460, 100), (680, 300),
        (60,  240),
    ],
    'ancient_city': [
        (380, 200), (200, 150), (560, 150),
        (150, 320), (610, 320), (300, 400),
        (460, 400), (380, 80),  (680, 200),
        (60,  300),
    ],
    'default': [
        (380, 200), (200, 150), (560, 150),
        (150, 320), (610, 320), (300, 400),
        (460, 400), (380, 80),  (680, 200),
        (60,  300),
    ],
}


class AgentNode:
    def __init__(self, name, personality, node_pos, color):
        self.name = name
        self.personality = personality
        self.color = color
        self.x = float(node_pos[0])
        self.y = float(node_pos[1])
        self.target_x = self.x
        self.target_y = self.y
        self.home_x = self.x
        self.home_y = self.y
        self.thinking = False
        self.think_timer = 0.0
        self.bob = random.uniform(0, math.pi * 2)
        self.stance = None
        self.last_action = ''

    def set_target(self, tx, ty):
        self.target_x = tx
        self.target_y = ty

    def update(self, dt):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        self.x += dx * min(dt * 2.5, 1)
        self.y += dy * min(dt * 2.5, 1)
        self.bob += dt * 1.5
        if self.think_timer > 0:
            self.think_timer -= dt
            if self.think_timer <= 0:
                self.thinking = False

    def start_thinking(self):
        self.thinking = True
        self.think_timer = 3.0

    def get_stance_color(self):
        if self.stance:
            s = self.stance.lower()
            if any(w in s for w in ('support', 'positive', 'beneficial')):
                return SAGE
            if any(w in s for w in ('skeptic', 'concern', 'oppos', 'worried',
                                    'against', 'resist')):
                return BRICK
        return TAN

    def draw(self, surface, ox, oy, fonts):
        cx = int(self.x) + ox
        cy = int(self.y) + oy

        # Gentle bob when thinking
        if self.thinking:
            cy += int(math.sin(self.bob) * 1.5)

        col = self.color
        stance_col = self.get_stance_color()
        darker = tuple(max(0, c - 40) for c in col)

        # Shadow (ellipse on ground)
        shadow = pygame.Surface((28, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), (0, 0, 28, 8))
        surface.blit(shadow, (cx - 14, cy + 12))

        # Body (oval)
        body_rect = pygame.Rect(cx - 9, cy - 8, 18, 22)
        pygame.draw.ellipse(surface, darker, body_rect)
        inner_body = pygame.Rect(cx - 7, cy - 6, 14, 18)
        pygame.draw.ellipse(surface, col, inner_body)

        # Head (circle)
        pygame.draw.circle(surface, col, (cx, cy - 14), 9)
        pygame.draw.circle(surface, darker, (cx, cy - 14), 9, 1)

        # Stance indicator dot on chest
        pygame.draw.circle(surface, stance_col, (cx, cy - 2), 4)
        pygame.draw.circle(surface,
                           tuple(max(0, c - 30) for c in stance_col),
                           (cx, cy - 2), 4, 1)

        # Thinking ellipsis above head
        if self.thinking:
            for i in range(3):
                dot_x = cx - 6 + i * 6
                dot_y = cy - 30
                pygame.draw.circle(surface, TEXT_SEC, (dot_x, dot_y), 2)

        # Name label
        f = fonts['tiny']
        first_name = self.name.split()[0]
        nt = f.render(first_name, True, TEXT_MAIN)
        lw = nt.get_width() + 6
        lx = cx - lw // 2
        ly = cy + 18
        bg_r = pygame.Rect(lx - 1, ly - 1, lw + 2, nt.get_height() + 2)
        bg_surf = pygame.Surface((bg_r.w, bg_r.h), pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 140))
        surface.blit(bg_surf, bg_r.topleft)
        surface.blit(nt, (lx + 3, ly))


class MessageDot:
    """Simple dot traveling from sender to receiver."""

    def __init__(self, start, end, color):
        self.start = start
        self.end = end
        self.color = color
        self.progress = 0.0
        self.done = False

    def update(self, dt):
        self.progress += dt * 1.4
        if self.progress >= 1.0:
            self.done = True

    def draw(self, surface, ox, oy):
        t = min(self.progress, 1.0)
        x = int(self.start[0] + (self.end[0] - self.start[0]) * t) + ox
        y = int(self.start[1] + (self.end[1] - self.start[1]) * t) + oy
        pygame.draw.circle(surface, self.color, (x, y), 4)
        pygame.draw.circle(surface, TEXT_MAIN, (x, y), 4, 1)


# Keep DataStream as alias for backward compat
DataStream = MessageDot


class WorldMap:
    def __init__(self, rect, world_type='default'):
        self.rect = pygame.Rect(rect)
        self.world_type = world_type
        self.nodes: dict = {}
        self.messages: list = []
        # Keep both attribute names for compatibility
        self.active_connections: list = []  # (from_name, to_name, timer)
        self.connection_lines = self.active_connections  # alias
        self._grid_offset = 0

    def setup_agents(self, agent_configs):
        positions = WORLD_NODE_POSITIONS.get(self.world_type,
                                             WORLD_NODE_POSITIONS['default'])
        self.nodes.clear()
        for i, ac in enumerate(agent_configs):
            pos = positions[i % len(positions)]
            col = get_agent_color(ac['personality'])
            self.nodes[ac['name']] = AgentNode(
                ac['name'], ac['personality'], pos, col
            )

    def agent_thinking(self, name):
        if name in self.nodes:
            self.nodes[name].start_thinking()

    def agent_acted(self, name, action, stance):
        if name in self.nodes:
            n = self.nodes[name]
            n.last_action = action
            n.stance = stance
            n.thinking = False

    def broadcast(self, from_name, to_names):
        if from_name not in self.nodes:
            return
        fn = self.nodes[from_name]
        for tn_name in to_names:
            if tn_name in self.nodes:
                tn = self.nodes[tn_name]
                self.messages.append(
                    MessageDot((fn.x, fn.y), (tn.x, tn.y), fn.color)
                )
                self.active_connections.append([from_name, tn_name, 2.0])

    def update(self, dt):
        for n in self.nodes.values():
            n.update(dt)
        self.messages = [m for m in self.messages if not m.done]
        for m in self.messages:
            m.update(dt)
        self.active_connections = [
            [f, t, timer - dt]
            for f, t, timer in self.active_connections
            if timer - dt > 0
        ]
        self._grid_offset = (self._grid_offset + dt * 8) % 40

    # ------------------------------------------------------------------ #
    # Background drawing helpers                                           #
    # ------------------------------------------------------------------ #

    def _draw_bg(self, surface):
        r = self.rect
        pygame.draw.rect(surface, (24, 22, 18), r)

        # Subtle static grid (stone floor tiles)
        tile = 32
        for x in range(r.x, r.x + r.w, tile):
            pygame.draw.line(surface, (30, 27, 22), (x, r.y), (x, r.y + r.h))
        for y in range(r.y, r.y + r.h, tile):
            pygame.draw.line(surface, (30, 27, 22), (r.x, y), (r.x + r.w, y))

        wt = self.world_type
        if wt == 'workplace':
            self._draw_workplace(surface, r)
        elif wt == 'town':
            self._draw_town(surface, r)
        elif wt == 'government':
            self._draw_government(surface, r)
        elif wt == 'ancient_city':
            self._draw_ancient_city(surface, r)
        # default: plain tile grid only

    def _draw_workplace(self, surface, r):
        desk_col   = (72, 58, 40)
        desk_border = (58, 46, 30)
        wall_col   = (45, 40, 34)

        # Walls
        pygame.draw.rect(surface, wall_col, (r.x + 10, r.y + 10, r.w - 20, 12))
        pygame.draw.rect(surface, wall_col, (r.x + 10, r.y + r.h - 22, r.w - 20, 12))
        pygame.draw.rect(surface, wall_col, (r.x + 10, r.y + 10, 12, r.h - 20))
        pygame.draw.rect(surface, wall_col, (r.x + r.w - 22, r.y + 10, 12, r.h - 20))

        desk_locs = [
            (120, 100), (350, 100), (580, 100),
            (120, 220), (350, 220), (580, 220),
            (120, 340), (350, 340), (580, 340),
        ]
        for dx, dy in desk_locs:
            pygame.draw.rect(surface, desk_col,
                             (r.x + dx - 28, r.y + dy - 18, 56, 36))
            pygame.draw.rect(surface, desk_border,
                             (r.x + dx - 28, r.y + dy - 18, 56, 36), 1)
            # Monitor
            pygame.draw.rect(surface, (18, 16, 14),
                             (r.x + dx - 16, r.y + dy - 12, 22, 16))
            pygame.draw.rect(surface, (60, 80, 50),
                             (r.x + dx - 16, r.y + dy - 12, 22, 16), 1)

        # Server rack
        pygame.draw.rect(surface, (35, 32, 26), (r.x + r.w - 70, r.y + 90, 50, 180))
        pygame.draw.rect(surface, (50, 45, 36), (r.x + r.w - 70, r.y + 90, 50, 180), 1)
        for i in range(7):
            c = (60, 90, 60) if (pygame.time.get_ticks() // 600 + i) % 3 != 0 \
                else (80, 60, 40)
            pygame.draw.rect(surface, c,
                             (r.x + r.w - 64, r.y + 98 + i * 22, 38, 12))

    def _draw_town(self, surface, r):
        path_col   = (52, 44, 32)
        bldg_col   = (44, 38, 30)
        bldg_border = (60, 52, 40)
        park_col   = (38, 48, 28)

        # Cross-shaped paths
        pygame.draw.rect(surface, path_col,
                         (r.x, r.centery - 16, r.w, 32))
        pygame.draw.rect(surface, path_col,
                         (r.centerx - 16, r.y, 32, r.h))

        # Park ellipse
        pygame.draw.ellipse(surface, park_col,
                            (r.centerx - 55, r.centery - 38, 110, 76))
        pygame.draw.ellipse(surface, (48, 60, 36),
                            (r.centerx - 55, r.centery - 38, 110, 76), 1)

        buildings = [
            (60,  60,  90, 110), (200, 50, 70, 100),
            (500, 55,  90, 105), (610, 70, 70,  90),
            (55,  250, 70, 110), (670, 240, 60, 120),
            (100, 370, 80,  80), (560, 375, 80,  75),
        ]
        rng = random.Random(42)
        for bx, by, bw, bh in buildings:
            pygame.draw.rect(surface, bldg_col,
                             (r.x + bx, r.y + by, bw, bh))
            pygame.draw.rect(surface, bldg_border,
                             (r.x + bx, r.y + by, bw, bh), 1)
            for wy in range(by + 12, by + bh - 10, 22):
                for wx in range(bx + 10, bx + bw - 10, 18):
                    wc = (72, 80, 60) if rng.random() > 0.35 else (40, 36, 28)
                    pygame.draw.rect(surface, wc, (r.x + wx, r.y + wy, 9, 9))

    def _draw_government(self, surface, r):
        stone_col = (50, 46, 38)
        col_col   = (62, 58, 48)
        floor_col = (34, 32, 26)
        pygame.draw.rect(surface, floor_col, r)

        cx = r.x + r.w // 2
        cy = r.y + 120

        # Main building body
        pygame.draw.rect(surface, stone_col, (cx - 90, cy - 40, 180, 70))
        pygame.draw.rect(surface, col_col,   (cx - 90, cy - 40, 180, 70), 1)

        # Pediment triangle
        pts = [(cx - 100, cy - 40), (cx + 100, cy - 40), (cx, cy - 80)]
        pygame.draw.polygon(surface, (56, 50, 40), pts)
        pygame.draw.polygon(surface, col_col, pts, 1)

        # Columns
        for i in range(7):
            px = cx - 78 + i * 26
            pygame.draw.rect(surface, col_col, (px - 4, cy - 40, 8, 70))

        # Steps
        for s in range(3):
            sw = 190 + s * 16
            pygame.draw.rect(surface, (44, 40, 32),
                             (cx - sw // 2, cy + 28 + s * 8, sw, 10))

        # Side buildings
        for bx in (100, 530):
            pygame.draw.rect(surface, stone_col, (r.x + bx, r.y + 180, 110, 160))
            pygame.draw.rect(surface, col_col,   (r.x + bx, r.y + 180, 110, 160), 1)

    def _draw_ancient_city(self, surface, r):
        sand_col  = (44, 38, 24)
        stone_col = (56, 50, 34)
        wall_col  = (62, 54, 36)

        pygame.draw.rect(surface, sand_col, r)

        # Sandy variation tiles
        for i in range(0, r.w, 48):
            for j in range(0, r.h, 48):
                if (i + j) % 96 == 0:
                    pygame.draw.rect(surface, (48, 42, 28),
                                     (r.x + i, r.y + j, 48, 48))

        # City walls
        pygame.draw.rect(surface, wall_col,
                         (r.x + 15, r.y + 15, r.w - 30, r.h - 30), 5)

        cx = r.x + r.w // 2
        cy = r.y + r.h // 2

        # Colosseum
        pygame.draw.ellipse(surface, stone_col,
                            (cx - 100, cy - 68, 200, 136), 12)
        pygame.draw.ellipse(surface, wall_col,
                            (cx - 100, cy - 68, 200, 136), 2)
        pygame.draw.ellipse(surface, sand_col,
                            (cx - 68, cy - 46, 136, 92))

        # Forum
        pygame.draw.rect(surface, stone_col, (r.x + 90, r.y + 70, 130, 90))
        pygame.draw.rect(surface, wall_col,  (r.x + 90, r.y + 70, 130, 90), 1)
        for i in range(5):
            pygame.draw.rect(surface, wall_col,
                             (r.x + 100 + i * 24, r.y + 70, 6, 90))

        # Roads
        pygame.draw.line(surface, (38, 34, 22),
                         (r.x, cy), (r.x + r.w, cy), 6)
        pygame.draw.line(surface, (38, 34, 22),
                         (cx, r.y), (cx, r.y + r.h), 6)

    # ------------------------------------------------------------------ #
    # Main draw                                                            #
    # ------------------------------------------------------------------ #

    def draw(self, surface, fonts):
        clip = surface.get_clip()
        surface.set_clip(self.rect)

        self._draw_bg(surface)

        ox, oy = self.rect.x, self.rect.y

        # Connection lines (fading)
        for from_name, to_name, timer in self.active_connections:
            if from_name in self.nodes and to_name in self.nodes:
                fn = self.nodes[from_name]
                tn = self.nodes[to_name]
                alpha = int(min(timer / 2.0, 1.0) * 100)
                ls = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
                pygame.draw.line(ls, (*BORDER_LT, alpha),
                                 (int(fn.x), int(fn.y)),
                                 (int(tn.x), int(tn.y)), 1)
                surface.blit(ls, (ox, oy))

        # Message dots
        for m in self.messages:
            m.draw(surface, ox, oy)

        # Agent nodes
        for n in self.nodes.values():
            n.draw(surface, ox, oy, fonts)

        surface.set_clip(clip)

        # Panel border
        draw_panel_border(surface, self.rect, BORDER)
