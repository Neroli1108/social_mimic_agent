"""Theme, colors, fonts, and drawing utilities for the Social Simulation Engine — RimWorld style."""
import pygame

# Screen settings
SCREEN_W = 1280
SCREEN_H = 720
FPS = 60
TITLE = "Social Simulation Engine"

# ─────────────────────────────────────────────────────────────────────────────
# RimWorld-inspired color palette
# ─────────────────────────────────────────────────────────────────────────────

BG_DARK    = (18, 16, 14)      # main background
BG_PANEL   = (30, 26, 22)      # panel background
BG_PANEL2  = (40, 35, 29)      # secondary panels, inputs
BG_HEADER  = (22, 20, 17)      # title bar in panels
BG_HOVER   = (52, 46, 38)      # hover state
BG_SELECT  = (62, 52, 36)      # selected/active state

BORDER      = (58, 52, 44)     # standard 1px borders
BORDER_LT   = (80, 72, 60)     # lighter border (hover)
BORDER_DK   = (38, 34, 28)     # darker border

TEXT_HEAD   = (232, 220, 192)  # headers, titles
TEXT_MAIN   = (200, 188, 168)  # body text
TEXT_SEC    = (148, 136, 114)  # secondary text
TEXT_DIM    = (88, 80, 66)     # dim/disabled text

AMBER       = (196, 158, 68)   # primary accent (like RimWorld gold)
AMBER_DIM   = (128, 102, 44)   # dim amber

SAGE        = (88, 148, 88)    # positive/support (muted green)
BRICK       = (168, 68, 68)    # negative/oppose (muted red)
TAN         = (180, 148, 60)   # neutral/warning (amber-tan)
STEEL       = (110, 134, 158)  # info (steel blue)
RUST        = (180, 100, 50)   # caution (rust orange)

SUPPORT_COLOR = SAGE
OPPOSE_COLOR  = BRICK
NEUTRAL_COLOR = TAN

# Legacy aliases for compatibility
CYAN       = STEEL
CYAN_DIM   = (70, 88, 108)
MAGENTA    = (160, 80, 140)
YELLOW     = TAN
GREEN      = SAGE
RED        = BRICK
ORANGE     = RUST
BLUE       = STEEL
PURPLE     = (120, 80, 160)
WHITE      = TEXT_HEAD
GRAY       = TEXT_SEC
DARK_GRAY  = (44, 40, 34)


# ─────────────────────────────────────────────────────────────────────────────
# World ground colors by world type
# ─────────────────────────────────────────────────────────────────────────────

WORLD_GROUND_COLORS = {
    'workplace':   (28, 25, 20),
    'town':        (30, 26, 20),
    'government':  (34, 32, 26),
    'ancient_city':(28, 24, 16),
    'default':     (24, 22, 18),
}


# ─────────────────────────────────────────────────────────────────────────────
# Fonts
# ─────────────────────────────────────────────────────────────────────────────

def get_fonts():
    """Return a dict of pygame fonts using warm readable typefaces."""
    candidates = ['verdana', 'arial', 'consolas', None]
    chosen = None
    for name in candidates:
        if name is None:
            chosen = None
            break
        try:
            test = pygame.font.SysFont(name, 16)
            if test is not None:
                chosen = name
                break
        except Exception:
            continue

    def make(size, bold=False):
        if chosen:
            return pygame.font.SysFont(chosen, size, bold=bold)
        return pygame.font.Font(None, size)

    return {
        'title':  make(32, bold=True),
        'header': make(22, bold=True),
        'body':   make(16),
        'small':  make(13),
        'tiny':   make(11),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Agent color mapping
# ─────────────────────────────────────────────────────────────────────────────

def get_agent_color(personality_str):
    """Return a muted color based on keywords in personality string."""
    if not personality_str:
        return AMBER
    p = personality_str.lower()
    if 'optimistic' in p or 'progressive' in p:
        return STEEL
    if 'conservative' in p or 'traditional' in p:
        return RUST
    if 'analytical' in p or 'data' in p:
        return STEEL
    if 'cautious' in p or 'risk' in p:
        return TAN
    if 'creative' in p or 'innovative' in p:
        return (160, 110, 180)
    if 'social' in p or 'community' in p or 'diplomatic' in p:
        return SAGE
    if 'ambitious' in p or 'aggressive' in p or 'militaristic' in p:
        return BRICK
    if 'empathetic' in p or 'compassion' in p:
        return (140, 100, 160)
    return AMBER


# ─────────────────────────────────────────────────────────────────────────────
# Drawing utilities — RimWorld flat style
# ─────────────────────────────────────────────────────────────────────────────

def draw_panel_border(surface, rect, color=None, thickness=1):
    """Draw a simple flat 1px border. No L-brackets, no glow."""
    pygame.draw.rect(surface, color or BORDER, pygame.Rect(rect), thickness)


def draw_divider(surface, rect_or_x1, y_or_none=None, x2=None, color=None):
    """Draw a horizontal divider line.

    Can be called as:
      draw_divider(surface, rect)          — draws at rect.bottom - 1
      draw_divider(surface, rect, color=c) — same with color override
    """
    col = color or BORDER
    if isinstance(rect_or_x1, pygame.Rect):
        r = rect_or_x1
        pygame.draw.line(surface, col, (r.x, r.bottom - 1), (r.right, r.bottom - 1), 1)
    else:
        # legacy positional signature: x1, y, x2
        x1 = rect_or_x1
        y  = y_or_none
        pygame.draw.line(surface, col, (x1, y), (x2, y), 1)


def draw_tooltip_bg(surface, rect):
    """Draw tooltip background: BG_PANEL2 fill + BORDER_LT border."""
    pygame.draw.rect(surface, BG_PANEL2, rect)
    draw_panel_border(surface, rect, BORDER_LT)


# ─────────────────────────────────────────────────────────────────────────────
# Legacy stubs — kept so old imports don't crash during transition
# ─────────────────────────────────────────────────────────────────────────────

def draw_glow(surface, color, center, radius, layers=4):
    """No-op: glow effects removed in RimWorld style."""
    pass


def draw_cyber_border(surface, rect, color, thickness=1, corner_size=12):
    """Legacy alias — draws a plain flat border."""
    draw_panel_border(surface, rect, color, thickness)


def draw_scanlines(surface, rect, alpha=15):
    """No-op: scanlines removed in RimWorld style."""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Historical presets
# ─────────────────────────────────────────────────────────────────────────────

HISTORICAL_PRESETS = [
    {
        'id': 'rome_ottoman',
        'title': 'ROME NEVER FELL',
        'subtitle': 'What if Rome defeated the Ottoman Empire?',
        'year': '1453 AD',
        'color': (200, 160, 40),
        'world_type': 'ancient_city',
        'policy': (
            'The Roman Senate decrees a grand military campaign to reclaim Constantinople '
            'and push Ottoman forces back across Anatolia, calling all citizens to support the war effort.'
        ),
        'agents': [
            {'name': 'Senator Aurelius',   'personality': 'militaristic, traditional, and aristocratic'},
            {'name': 'General Marcus',     'personality': 'disciplined, strategic, and battle-hardened'},
            {'name': 'Merchant Demetrius', 'personality': 'pragmatic, cautious, and trade-focused'},
            {'name': 'Scholar Helena',     'personality': 'analytical, progressive, and philosophical'},
            {'name': 'Soldier Titus',      'personality': 'loyal, brave, and patriotic'},
        ],
    },
    {
        'id': 'cold_war',
        'title': 'COLD WAR CRISIS',
        'subtitle': 'Cuban Missile Crisis: Will reason prevail?',
        'year': '1962 AD',
        'color': (168, 68, 68),
        'world_type': 'government',
        'policy': (
            'The President orders a naval blockade of Cuba and demands the immediate removal of '
            'Soviet nuclear missiles, placing US forces on DEFCON 2.'
        ),
        'agents': [
            {'name': 'President Kennedy',    'personality': 'charismatic, strategic, and measured'},
            {'name': 'Gen. LeMay',           'personality': 'aggressive, militaristic, and hawkish'},
            {'name': 'Sec. McNamara',        'personality': 'analytical, pragmatic, and data-driven'},
            {'name': 'Ambassador Stevenson', 'personality': 'diplomatic, persuasive, and principled'},
            {'name': 'NSA Bundy',            'personality': 'cautious, intelligent, and risk-aware'},
        ],
    },
    {
        'id': 'french_revolution',
        'title': 'LA RÉVOLUTION',
        'subtitle': 'France 1789: The people rise',
        'year': '1789 AD',
        'color': (110, 134, 158),
        'world_type': 'town',
        'policy': (
            'The National Assembly declares the abolition of feudal privileges and demands '
            'King Louis XVI accept constitutional monarchy and the rights of man.'
        ),
        'agents': [
            {'name': 'Robespierre',      'personality': 'idealistic, passionate, and uncompromising'},
            {'name': 'Marie Antoinette', 'personality': 'aristocratic, isolated, and resistant'},
            {'name': 'Lafayette',        'personality': 'liberal, military, and reformist'},
            {'name': 'Marat',            'personality': 'radical, populist, and inflammatory'},
            {'name': 'Necker',           'personality': 'pragmatic, financial, and moderate'},
        ],
    },
    {
        'id': 'industrial_revolution',
        'title': 'AGE OF INDUSTRY',
        'subtitle': 'Britain 1850: Workers demand rights',
        'year': '1850 AD',
        'color': (140, 100, 60),
        'world_type': 'workplace',
        'policy': (
            'Parliament debates the Ten Hours Act limiting factory working hours, with factory '
            'owners and workers in fierce opposition over labor rights.'
        ),
        'agents': [
            {'name': 'Lord Shaftesbury',   'personality': 'reformist, compassionate, and persistent'},
            {'name': 'Factory Owner Mills', 'personality': 'capitalist, profit-driven, and change-resistant'},
            {'name': 'Worker Mary',         'personality': 'exhausted, determined, and community-minded'},
            {'name': 'MP Thompson',         'personality': 'politically cautious and persuadable'},
            {'name': 'Economist Ricardo',   'personality': 'theoretical, free-market, and analytical'},
        ],
    },
    {
        'id': 'mongol_storm',
        'title': 'MONGOL STORM',
        'subtitle': 'What if Mongols conquered all Europe?',
        'year': '1241 AD',
        'color': (180, 100, 50),
        'world_type': 'ancient_city',
        'policy': (
            'The Great Khan orders the Western Campaign to continue beyond the Battle of Legnica, '
            'pushing deep into the Holy Roman Empire with full Mongol force.'
        ),
        'agents': [
            {'name': 'Khan Batu',        'personality': 'conquering, strategic, and ruthless'},
            {'name': 'General Subutai',  'personality': 'genius tactician, disciplined, and calculating'},
            {'name': 'Pope Innocent IV', 'personality': 'spiritual, desperate, and politically savvy'},
            {'name': 'King Louis IX',    'personality': 'devout, brave, and rallying'},
            {'name': 'Merchant Marco',   'personality': 'opportunistic, adaptive, and survival-focused'},
        ],
    },
]

EXAMPLE_POLICIES = [
    "The government mandates a four-day work week for all employees to improve work-life balance and productivity.",
    "Universal basic income of $1,000 per month is introduced for all citizens above age 18.",
    "All fossil fuel vehicles must be replaced with electric vehicles within the next 10 years.",
    "Free higher education is guaranteed for every citizen regardless of income or background.",
    "A carbon tax of $50 per ton is imposed on all businesses emitting greenhouse gases.",
]

SCENARIO_WORLD_TYPES = {
    'workplace':    'workplace',
    'town':         'town',
    'school':       'town',
    'neighborhood': 'town',
    'government':   'government',
    'ancient_city': 'ancient_city',
    'custom':       'default',
    'default':      'default',
}
