"""Visual language shared by every explainer: dark background, a small fixed palette,
LaTeX typography, and a few layout helpers."""

from manim import (
  DOWN, LEFT, RIGHT, UP, UL, UR, BLUE_C, BLUE_D, BLUE_E, GOLD_C, GREEN_C, GREY_B, GREY_BROWN,
  RED_C, TEAL_C, WHITE, YELLOW_C, MAROON_C, config, Tex, MathTex, VGroup, SurroundingRectangle,
  RoundedRectangle, FadeIn, Write,
)

BACKGROUND = '#0d0f12'
INK = WHITE
MUTED = GREY_B
PRIMARY = BLUE_C      # main object
SECONDARY = YELLOW_C  # the thing being changed / highlighted
ACCENT = TEAL_C       # a second object or "good" outcome
WARN = RED_C          # contradiction, failure, counterexample
WARM = GOLD_C
EARTH = GREY_BROWN
SOFT = BLUE_E
EXTRA = MAROON_C
OK = GREEN_C

PALETTE = [PRIMARY, SECONDARY, ACCENT, WARN, WARM, OK, EXTRA, SOFT]

config.background_color = BACKGROUND


def title(text, scale=1.0):
  """Large heading at the top edge."""
  t = Tex(text).scale(1.1 * scale)
  return t.to_edge(UP, buff=0.5)


def caption(text, scale=0.8, color=INK):
  """One line of on-screen text near the bottom; keep it shorter than the narration."""
  t = Tex(text, color=color).scale(scale)
  return t.to_edge(DOWN, buff=0.45)


def boxed(mob, color=SECONDARY, buff=0.18):
  return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08)


def card(mob, color=MUTED, buff=0.35, opacity=0.08):
  """A quiet rounded panel behind a group, for statements of theorems."""
  r = RoundedRectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff, corner_radius=0.15,
                       stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=opacity)
  r.move_to(mob)
  return VGroup(r, mob)


def statement(label, body_tex, width=11.5, color=PRIMARY):
  """A theorem-style panel: a coloured label and a LaTeX body wrapped to a width."""
  head = Tex(r'\textbf{' + label + '}', color=color).scale(0.8)
  body = Tex(r'\parbox{' + f'{width}cm' + r'}{\raggedright ' + body_tex + '}').scale(0.7)
  grp = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
  return card(grp, color=color)


__all__ = [n for n in dir() if not n.startswith('_')]
