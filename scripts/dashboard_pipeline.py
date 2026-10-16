#!/usr/bin/env python3
"""
SVG Maestro - Dashboard Widgets & Power BI DAX Pipeline (Operate Mode)
Programmatic vector engine and generator for modular telemetry cards and metric cards
in Operate mode, featuring golden ratio proportions, radar sweep indicators, sparklines,
Inkscape semantic layers, and automatic URL-encoded DAX measure generation for Power BI.
"""

import os
import sys
import re
import argparse
from typing import Dict, Any, Optional

# Add scripts directory to sys.path to access validate_svg
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from validate_svg import validate_svg_file


THEMES: Dict[str, Dict[str, str]] = {
    "dark_slate": {
        "bg_chassis": "#0a0e17",
        "bg_card_start": "#0e1726",
        "bg_card_end": "#0a0e17",
        "border_card": "#1b2940",
        "border_inner": "#152238",
        "grid_line": "#142138",
        "grid_subtle": "#0e1726",
        "primary": "#00f0ff",        # Cyber Neon Cyan
        "primary_dark": "#0077aa",
        "secondary": "#00ff88",      # Cyber Emerald
        "secondary_dark": "#009955",
        "accent": "#ffb703",         # Electric Amber
        "text_primary": "#ffffff",
        "text_secondary": "#8ca0be",
        "text_muted": "#526582",
        "glow_primary": "#00f0ff",
        "glow_secondary": "#00ff88",
        "badge_bg": "#08221b",
        "badge_border": "#00ff88",
    },
    "obsidian_amber": {
        "bg_chassis": "#120e0a",
        "bg_card_start": "#1c150e",
        "bg_card_end": "#0e0a06",
        "border_card": "#3d2b15",
        "border_inner": "#291d0e",
        "grid_line": "#2b1f12",
        "grid_subtle": "#1f160d",
        "primary": "#ffb703",        # Electric Amber
        "primary_dark": "#cc8800",
        "secondary": "#00f0ff",      # Cyan Accent
        "secondary_dark": "#0099aa",
        "accent": "#ff5500",         # Blaze Orange
        "text_primary": "#ffffff",
        "text_secondary": "#d4b896",
        "text_muted": "#8a755e",
        "glow_primary": "#ffb703",
        "glow_secondary": "#00f0ff",
        "badge_bg": "#2b1e0a",
        "badge_border": "#ffb703",
    },
    "matrix_emerald": {
        "bg_chassis": "#06120b",
        "bg_card_start": "#0b1e13",
        "bg_card_end": "#040d07",
        "border_card": "#143d24",
        "border_inner": "#0d2918",
        "grid_line": "#123620",
        "grid_subtle": "#0a2113",
        "primary": "#00ff88",        # Phosphor Neon Green
        "primary_dark": "#009955",
        "secondary": "#00e5ff",      # Cyan Accent
        "secondary_dark": "#008899",
        "accent": "#76ff03",         # Toxic Lime
        "text_primary": "#ffffff",
        "text_secondary": "#88d4aa",
        "text_muted": "#528568",
        "glow_primary": "#00ff88",
        "glow_secondary": "#00e5ff",
        "badge_bg": "#0a2916",
        "badge_border": "#00ff88",
    },
    "deep_violet": {
        "bg_chassis": "#0e0a17",
        "bg_card_start": "#181226",
        "bg_card_end": "#090610",
        "border_card": "#321f4d",
        "border_inner": "#221536",
        "grid_line": "#25183d",
        "grid_subtle": "#191029",
        "primary": "#a855f7",        # Electric Violet
        "primary_dark": "#7928ca",
        "secondary": "#00f0ff",      # Cyan Accent
        "secondary_dark": "#0077aa",
        "accent": "#ff007f",         # Neon Magenta
        "text_primary": "#ffffff",
        "text_secondary": "#c4b5fd",
        "text_muted": "#7c6f9e",
        "glow_primary": "#a855f7",
        "glow_secondary": "#00f0ff",
        "badge_bg": "#231138",
        "badge_border": "#a855f7",
    }
}


def get_theme(theme_name: str) -> Dict[str, str]:
    """Retrieve theme tokens or fallback to dark_slate."""
    return THEMES.get(theme_name, THEMES["dark_slate"])


def generate_telemetry_card(
    theme_name: str = "dark_slate",
    kpi_value: str = "$1,284,500",
    kpi_change: str = "+14.2% ↑",
    kpi_label: str = "TOTAL SYSTEM THROUGHPUT",
    kpi_sublabel: str = "OPERATE // METRIC TELEMETRY",
    kpi_comparison: str = "vs 30-day baseline",
    scan_label: str = "ACTIVE SCAN: 4.2 GHz",
    status_label: str = "ONLINE 99.9%",
    timeline_label: str = "TELEMETRY TIMELINE // 24-HOUR TREND",
    timeline_peak: str = "PEAK: $1.42M ● VOL: NOMINAL",
    width: int = 800,
    height: int = 494
) -> str:
    """
    Generate a production-ready Golden Ratio Telemetry Card SVG in Operate mode.
    - ViewBox: 0 0 {width} {height} (Default: 800x494, golden ratio approx 1.618)
    - Dark slate background (#0a0e17) with subtle gradients and corner brackets.
    - Crisp data grids, coordinate axes, and technical crosshairs.
    - Glowing radar sweep indicator with rotating beam and target blip.
    - Sparkline/trendline with area gradient, glowing stroke, inflection points, and pulsing endpoint.
    - Decoupled typography in 'layer-typography' (semantic <text> elements, not paths).
    - Wrapper Pattern on all animated groups (<g class="anim-..."> wrapping static geometry <g inkscape:label="...">).
    - Universal CSS Transform Contract (transform-box: fill-box; transform-origin: center;).
    - Strict Inkscape Semantic Layers: layer-background, layer-grid, layer-telemetry, layer-typography.
    """
    t = get_theme(theme_name)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {width} {height}"
     width="100%" height="100%">
  <defs>
    <!-- Card Chassis Gradients -->
    <linearGradient id="grad-card-chassis" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['bg_card_start']}" />
      <stop offset="100%" stop-color="{t['bg_card_end']}" />
    </linearGradient>
    <linearGradient id="grad-telemetry-primary" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['primary']}" />
      <stop offset="100%" stop-color="{t['primary_dark']}" />
    </linearGradient>
    <linearGradient id="grad-telemetry-secondary" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['secondary']}" />
      <stop offset="100%" stop-color="{t['secondary_dark']}" />
    </linearGradient>
    <linearGradient id="grad-sparkline-area" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['primary']}" stop-opacity="0.32" />
      <stop offset="50%" stop-color="{t['primary_dark']}" stop-opacity="0.10" />
      <stop offset="100%" stop-color="{t['bg_chassis']}" stop-opacity="0.0" />
    </linearGradient>
    <linearGradient id="grad-radar-sweep" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['primary']}" stop-opacity="0.80" />
      <stop offset="100%" stop-color="{t['primary']}" stop-opacity="0.0" />
    </linearGradient>

    <!-- Technical Glow Filters -->
    <filter id="filter-telemetry-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur-glow" />
      <feMerge>
        <feMergeNode in="blur-glow" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="filter-radar-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur-radar" />
      <feMerge>
        <feMergeNode in="blur-radar" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="filter-subtle-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur-subtle" />
      <feMerge>
        <feMergeNode in="blur-subtle" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    /* SVG Maestro Universal CSS Transform Contract */
    .anim-radar-sweep {{
      transform-box: fill-box;
      transform-origin: center;
      animation: radar-sweep 5s linear infinite;
    }}
    @keyframes radar-sweep {{
      0% {{
        transform: rotate(0deg);
      }}
      100% {{
        transform: rotate(360deg);
      }}
    }}

    .anim-radar-blip {{
      transform-box: fill-box;
      transform-origin: center;
      animation: radar-blip 2.2s ease-in-out infinite;
    }}
    @keyframes radar-blip {{
      0%, 100% {{
        opacity: 0.25;
        transform: scale(0.8);
      }}
      50% {{
        opacity: 1;
        transform: scale(1.25);
      }}
    }}

    .anim-spark-pulse {{
      transform-box: fill-box;
      transform-origin: center;
      animation: spark-pulse 2s ease-in-out infinite;
    }}
    @keyframes spark-pulse {{
      0% {{
        transform: scale(0.7);
        opacity: 0.9;
      }}
      50% {{
        transform: scale(1.6);
        opacity: 0.15;
      }}
      100% {{
        transform: scale(0.7);
        opacity: 0.9;
      }}
    }}

    .anim-beacon {{
      transform-box: fill-box;
      transform-origin: center;
      animation: beacon-pulse 1.8s ease-in-out infinite;
    }}
    @keyframes beacon-pulse {{
      0%, 100% {{
        opacity: 0.4;
        transform: scale(0.9);
      }}
      50% {{
        opacity: 1;
        transform: scale(1.1);
      }}
    }}
  </style>

  <!-- ========================================== -->
  <!-- LAYER 1: Card Background & Chassis        -->
  <!-- ========================================== -->
  <g inkscape:groupmode="layer" id="layer-background" inkscape:label="Card Background &amp; Chassis">
    <!-- Main Card Body -->
    <rect x="0" y="0" width="{width}" height="{height}" rx="16" fill="url(#grad-card-chassis)" stroke="{t['border_card']}" stroke-width="2" />

    <!-- Inner Geometric Hairline Border -->
    <rect x="12" y="12" width="{width - 24}" height="{height - 24}" rx="12" fill="none" stroke="{t['border_inner']}" stroke-width="1" stroke-dasharray="6 6" />

    <!-- Corner Technical Brackets -->
    <path d="M 16 36 L 16 16 L 36 16" fill="none" stroke="{t['primary']}" stroke-width="1.5" opacity="0.65" />
    <path d="M {width - 16} 36 L {width - 16} 16 L {width - 36} 16" fill="none" stroke="{t['primary']}" stroke-width="1.5" opacity="0.65" />
    <path d="M 16 {height - 36} L 16 {height - 16} L 36 {height - 16}" fill="none" stroke="{t['primary']}" stroke-width="1.5" opacity="0.65" />
    <path d="M {width - 16} {height - 36} L {width - 16} {height - 16} L {width - 36} {height - 16}" fill="none" stroke="{t['primary']}" stroke-width="1.5" opacity="0.65" />

    <!-- Header Divider Rule -->
    <line x1="30" y1="75" x2="{width - 30}" y2="75" stroke="{t['border_inner']}" stroke-width="1.5" />

    <!-- Status Badge Container Base -->
    <rect x="{width - 154}" y="28" width="118" height="28" rx="14" fill="{t['bg_card_start']}" stroke="{t['primary']}" stroke-width="1" opacity="0.85" />

    <!-- KPI Change Pill Base -->
    <rect x="40" y="196" width="94" height="26" rx="6" fill="{t['badge_bg']}" stroke="{t['badge_border']}" stroke-width="1" />
  </g>

  <!-- ========================================== -->
  <!-- LAYER 2: Data Grid & Technical Markings    -->
  <!-- ========================================== -->
  <g inkscape:groupmode="layer" id="layer-grid" inkscape:label="Data Grid &amp; Markings">
    <!-- Header Crosshair Marker -->
    <line x1="395" y1="38" x2="405" y2="38" stroke="{t['grid_line']}" stroke-width="1" />
    <line x1="400" y1="33" x2="400" y2="43" stroke="{t['grid_line']}" stroke-width="1" />

    <!-- Radar Range Rings (Center: x=670, y=155) -->
    <circle cx="670" cy="155" r="18" fill="none" stroke="{t['border_inner']}" stroke-width="1" />
    <circle cx="670" cy="155" r="36" fill="none" stroke="{t['border_inner']}" stroke-width="1" />
    <circle cx="670" cy="155" r="54" fill="none" stroke="{t['border_card']}" stroke-width="1.2" stroke-dasharray="4 4" />

    <!-- Radar Reticle Crosshairs -->
    <line x1="610" y1="155" x2="730" y2="155" stroke="{t['border_inner']}" stroke-width="1" stroke-dasharray="2 4" />
    <line x1="670" y1="95" x2="670" y2="215" stroke="{t['border_inner']}" stroke-width="1" stroke-dasharray="2 4" />
    <line x1="632" y1="117" x2="708" y2="193" stroke="{t['grid_subtle']}" stroke-width="0.8" stroke-dasharray="2 4" />
    <line x1="632" y1="193" x2="708" y2="117" stroke="{t['grid_subtle']}" stroke-width="0.8" stroke-dasharray="2 4" />

    <!-- Outer Radar Ring Cardinal Tick Marks -->
    <line x1="670" y1="98" x2="670" y2="103" stroke="{t['primary']}" stroke-width="1.5" />
    <line x1="670" y1="207" x2="670" y2="212" stroke="{t['primary']}" stroke-width="1.5" />
    <line x1="613" y1="155" x2="618" y2="155" stroke="{t['primary']}" stroke-width="1.5" />
    <line x1="722" y1="155" x2="727" y2="155" stroke="{t['primary']}" stroke-width="1.5" />

    <!-- Sparkline Grid Lines (Horizontal Levels: y=285, 330, 375, 420) -->
    <line x1="75" y1="285" x2="760" y2="285" stroke="{t['grid_line']}" stroke-width="1" stroke-dasharray="4 4" />
    <line x1="75" y1="330" x2="760" y2="330" stroke="{t['grid_line']}" stroke-width="1" stroke-dasharray="4 4" />
    <line x1="75" y1="375" x2="760" y2="375" stroke="{t['grid_line']}" stroke-width="1" stroke-dasharray="4 4" />
    <line x1="75" y1="420" x2="760" y2="420" stroke="{t['grid_line']}" stroke-width="1" stroke-dasharray="4 4" />

    <!-- Sparkline Vertical Time Grid Columns -->
    <line x1="160" y1="280" x2="160" y2="425" stroke="{t['grid_subtle']}" stroke-width="1" stroke-dasharray="2 4" />
    <line x1="280" y1="280" x2="280" y2="425" stroke="{t['grid_subtle']}" stroke-width="1" stroke-dasharray="2 4" />
    <line x1="400" y1="280" x2="400" y2="425" stroke="{t['grid_subtle']}" stroke-width="1" stroke-dasharray="2 4" />
    <line x1="520" y1="280" x2="520" y2="425" stroke="{t['grid_subtle']}" stroke-width="1" stroke-dasharray="2 4" />
    <line x1="640" y1="280" x2="640" y2="425" stroke="{t['grid_subtle']}" stroke-width="1" stroke-dasharray="2 4" />
    <line x1="760" y1="280" x2="760" y2="425" stroke="{t['grid_subtle']}" stroke-width="1" stroke-dasharray="2 4" />

    <!-- Baseline Axis Rule -->
    <line x1="75" y1="425" x2="760" y2="425" stroke="{t['border_card']}" stroke-width="1.5" />
  </g>

  <!-- ========================================== -->
  <!-- LAYER 3: Telemetry Visuals & Data Curves   -->
  <!-- ========================================== -->
  <g inkscape:groupmode="layer" id="layer-telemetry" inkscape:label="Telemetry &amp; Visuals">
    <!-- Live Status Beacon Pulse Dot -->
    <g class="anim-beacon">
      <g id="geom-status-beacon" inkscape:label="Live Status Beacon">
        <circle cx="{width - 138}" cy="42" r="4" fill="{t['secondary']}" filter="url(#filter-subtle-glow)" />
      </g>
    </g>

    <!-- Radar Sweep Assembly (Wrapper Pattern) -->
    <g class="anim-radar-sweep">
      <g id="geom-radar-sweep" inkscape:label="Radar Sweep Beam">
        <!-- Symmetric invisible anchor bounding box for perfect center-point rotation -->
        <circle cx="670" cy="155" r="54" fill="none" stroke="none" opacity="0" pointer-events="none" />
        <!-- Radar beam wedge arc -->
        <path d="M 670 155 L 724 155 A 54 54 0 0 1 711 193 Z" fill="url(#grad-radar-sweep)" opacity="0.8" />
        <line x1="670" y1="155" x2="724" y2="155" stroke="{t['primary']}" stroke-width="1.8" filter="url(#filter-radar-glow)" />
      </g>
    </g>

    <!-- Radar Detected Target Blip (Wrapper Pattern) -->
    <g class="anim-radar-blip">
      <g id="geom-radar-blip" inkscape:label="Radar Target Blip">
        <circle cx="695" cy="132" r="3.5" fill="{t['secondary']}" filter="url(#filter-subtle-glow)" />
      </g>
    </g>

    <!-- Sparkline Area Gradient Fill -->
    <path d="M 80 395 C 105 385, 130 380, 155 398 C 180 416, 205 375, 230 365 C 255 355, 280 345, 305 355 C 330 365, 355 335, 380 325 C 405 315, 430 340, 455 330 C 480 320, 505 305, 530 315 C 555 325, 580 295, 605 285 C 630 275, 655 300, 680 280 C 705 260, 730 255, 760 245 L 760 425 L 80 425 Z" fill="url(#grad-sparkline-area)" />

    <!-- Sparkline Continuous Vector Trendline -->
    <path d="M 80 395 C 105 385, 130 380, 155 398 C 180 416, 205 375, 230 365 C 255 355, 280 345, 305 355 C 330 365, 355 335, 380 325 C 405 315, 430 340, 455 330 C 480 320, 505 305, 530 315 C 555 325, 580 295, 605 285 C 630 275, 655 300, 680 280 C 705 260, 730 255, 760 245" fill="none" stroke="url(#grad-telemetry-primary)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" filter="url(#filter-telemetry-glow)" />

    <!-- Sparkline Data Inflection Nodes -->
    <circle cx="80" cy="395" r="2.5" fill="{t['primary']}" opacity="0.8" />
    <circle cx="230" cy="365" r="2.5" fill="{t['primary']}" opacity="0.8" />
    <circle cx="380" cy="325" r="2.5" fill="{t['primary']}" opacity="0.8" />
    <circle cx="530" cy="315" r="2.5" fill="{t['primary']}" opacity="0.8" />
    <circle cx="605" cy="285" r="2.5" fill="{t['primary']}" opacity="0.8" />
    <circle cx="680" cy="280" r="2.5" fill="{t['primary']}" opacity="0.8" />

    <!-- Sparkline Endpoint Pulse Ring Assembly (Wrapper Pattern) -->
    <g class="anim-spark-pulse">
      <g id="geom-spark-pulse" inkscape:label="Sparkline Endpoint Pulse">
        <!-- Symmetric invisible anchor bounding box -->
        <circle cx="760" cy="245" r="16" fill="none" stroke="none" opacity="0" pointer-events="none" />
        <circle cx="760" cy="245" r="7" stroke="{t['primary']}" stroke-width="1.5" fill="none" filter="url(#filter-subtle-glow)" />
      </g>
    </g>
    <circle cx="760" cy="245" r="4" fill="{t['primary']}" />
  </g>

  <!-- ========================================== -->
  <!-- LAYER 4: Typography & Metric Readouts      -->
  <!-- ========================================== -->
  <g inkscape:groupmode="layer" id="layer-typography" inkscape:label="Typography &amp; Metrics">
    <!-- Header Category & Sublabel -->
    <text x="40" y="48" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="12" font-weight="700" letter-spacing="2" fill="{t['text_secondary']}">{kpi_sublabel}</text>

    <!-- Header Status Indicator Text -->
    <text x="{width - 124}" y="46" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="11" font-weight="700" fill="{t['secondary']}" letter-spacing="0.8">{status_label}</text>

    <!-- Primary Metric Title / Label -->
    <text x="40" y="116" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="12" font-weight="600" letter-spacing="1.5" fill="{t['text_secondary']}">{kpi_label}</text>

    <!-- Primary KPI Value Readout -->
    <text x="40" y="176" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="56" font-weight="800" letter-spacing="-1.5" fill="{t['text_primary']}">{kpi_value}</text>

    <!-- KPI Change % Readout -->
    <text x="87" y="213" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="12" font-weight="700" fill="{t['secondary']}" text-anchor="middle">{kpi_change}</text>

    <!-- Baseline Comparison Subtitle -->
    <text x="144" y="213" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="12" font-weight="500" fill="{t['text_muted']}">{kpi_comparison}</text>

    <!-- Radar Telemetry Readout -->
    <text x="670" y="230" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="10" font-weight="700" letter-spacing="1.2" fill="{t['primary']}" text-anchor="middle">{scan_label}</text>

    <!-- Timeline Title & Sublabel -->
    <text x="40" y="260" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="11" font-weight="700" letter-spacing="1.5" fill="{t['text_secondary']}">{timeline_label}</text>
    <text x="760" y="260" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="11" font-weight="600" fill="{t['text_muted']}" text-anchor="end">{timeline_peak}</text>

    <!-- Sparkline Y-Axis Scale Labels -->
    <text x="68" y="289" font-family="'JetBrains Mono', 'Segoe UI Mono', Consolas, monospace" font-size="10" fill="{t['text_muted']}" text-anchor="end">100k</text>
    <text x="68" y="334" font-family="'JetBrains Mono', 'Segoe UI Mono', Consolas, monospace" font-size="10" fill="{t['text_muted']}" text-anchor="end">75k</text>
    <text x="68" y="379" font-family="'JetBrains Mono', 'Segoe UI Mono', Consolas, monospace" font-size="10" fill="{t['text_muted']}" text-anchor="end">50k</text>
    <text x="68" y="424" font-family="'JetBrains Mono', 'Segoe UI Mono', Consolas, monospace" font-size="10" fill="{t['text_muted']}" text-anchor="end">25k</text>

    <!-- Sparkline X-Axis Timeline Markers -->
    <text x="80" y="445" font-family="'JetBrains Mono', 'Segoe UI Mono', Consolas, monospace" font-size="10" fill="{t['text_muted']}">00:00</text>
    <text x="216" y="445" font-family="'JetBrains Mono', 'Segoe UI Mono', Consolas, monospace" font-size="10" fill="{t['text_muted']}" text-anchor="middle">06:00</text>
    <text x="352" y="445" font-family="'JetBrains Mono', 'Segoe UI Mono', Consolas, monospace" font-size="10" fill="{t['text_muted']}" text-anchor="middle">12:00</text>
    <text x="488" y="445" font-family="'JetBrains Mono', 'Segoe UI Mono', Consolas, monospace" font-size="10" fill="{t['text_muted']}" text-anchor="middle">18:00</text>
    <text x="624" y="445" font-family="'JetBrains Mono', 'Segoe UI Mono', Consolas, monospace" font-size="10" fill="{t['text_muted']}" text-anchor="middle">22:00</text>
    <text x="760" y="445" font-family="'JetBrains Mono', 'Segoe UI Mono', Consolas, monospace" font-size="10" fill="{t['text_muted']}" text-anchor="end">NOW</text>
  </g>
</svg>'''

    return svg_content


def convert_svg_to_dax_measure(
    svg_content: str,
    measure_name: str = "TelemetryCard",
    dynamic_vars: Optional[Dict[str, str]] = None,
    var_definitions: Optional[Dict[str, str]] = None
) -> str:
    """
    Convert an SVG document into a production-ready Power BI DAX measure string.
    
    Escaping rules implemented:
    1. Replaces all '#' in color codes and URL fragment IDs with '%23' (mandatory for Power BI data URIs).
    2. Escapes double quotes '\"' as '\"\"' for valid DAX string literals.
    3. Prefixes with 'data:image/svg+xml;utf8,'.
    4. Wraps in standard Power BI DAX pattern:
       {measure_name} = 
       [Optional VAR declarations for dynamic interpolation]
       VAR SvgData = "data:image/svg+xml;utf8," & "..."
       RETURN
           SvgData
    
    Dynamic Variables Interpolation:
    If dynamic_vars is supplied, maps target string literals in the SVG (e.g. '$1,284,500')
    to DAX measure expressions or variable references (e.g. '_KpiValue' or '[KPI_Value]').
    """
    # 1. URL encode '#' to '%23'
    dax_svg = svg_content.replace("#", "%23")

    # 2. Escape double quotes for DAX string literal
    dax_svg = dax_svg.replace('"', '""')

    # 3. Process dynamic variables if provided
    var_lines = []
    if var_definitions:
        for vname, vval in var_definitions.items():
            var_lines.append(f"VAR {vname} = {vval}")
    elif dynamic_vars:
        # Default self-contained variable definitions with fallback
        for target, var_name in dynamic_vars.items():
            clean_name = var_name.strip()
            if clean_name.startswith("[") and clean_name.endswith("]"):
                def_name = "_" + clean_name[1:-1].replace(" ", "_")
                var_lines.append(f"VAR {def_name} = COALESCE({clean_name}, \"{target}\")")
            elif clean_name.startswith("_"):
                var_lines.append(f"VAR {clean_name} = \"{target}\" -- Replace with dynamic measure, e.g. [KPI_Value]")

    if dynamic_vars:
        for target, var_expr in dynamic_vars.items():
            escaped_target = target.replace("#", "%23").replace('"', '""')
            if escaped_target in dax_svg:
                dax_svg = dax_svg.replace(escaped_target, f'" & {var_expr} & "')

    lines = [f"{measure_name} = "]
    if var_lines:
        lines.extend(var_lines)
    lines.append('VAR SvgData = "data:image/svg+xml;utf8," &')
    lines.append(f'"{dax_svg}"')
    lines.append("RETURN")
    lines.append("    SvgData")

    return "\n".join(lines)


def export_dashboard_assets(
    output_dir: str = "examples/dashboard",
    theme_name: str = "dark_slate",
    measure_name: str = "TelemetryCard",
    validate: bool = True,
    dynamic: bool = True
) -> Dict[str, Any]:
    """
    Generate and save both the standalone SVG telemetry card and its corresponding
    Power BI DAX measure file, executing automated linter validation.
    """
    os.makedirs(output_dir, exist_ok=True)
    svg_filename = "telemetry_card.svg"
    dax_filename = "telemetry_card.dax"
    svg_path = os.path.join(output_dir, svg_filename)
    dax_path = os.path.join(output_dir, dax_filename)

    # 1. Generate standalone SVG card
    svg_code = generate_telemetry_card(theme_name=theme_name)
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_code)

    # 2. Generate DAX measure snippet
    dynamic_mapping = None
    if dynamic:
        dynamic_mapping = {
            "$1,284,500": "_KpiValue",
            "+14.2% ↑": "_KpiChange",
            "TOTAL SYSTEM THROUGHPUT": "_KpiLabel"
        }

    dax_code = convert_svg_to_dax_measure(
        svg_content=svg_code,
        measure_name=measure_name,
        dynamic_vars=dynamic_mapping
    )
    with open(dax_path, "w", encoding="utf-8") as f:
        f.write(dax_code)

    # 3. Autonomous validation
    results = {
        "theme": theme_name,
        "output_dir": output_dir,
        "files": {
            "svg": {
                "path": svg_path,
                "filename": svg_filename,
                "valid": True,
                "errors": [],
                "warnings": []
            },
            "dax": {
                "path": dax_path,
                "filename": dax_filename
            }
        }
    }

    if validate:
        val_res = validate_svg_file(svg_path)
        results["files"]["svg"]["valid"] = val_res.is_valid and len(val_res.warnings) == 0
        results["files"]["svg"]["errors"] = val_res.errors
        results["files"]["svg"]["warnings"] = val_res.warnings

    return results


def main():
    parser = argparse.ArgumentParser(description="SVG Maestro - Dashboard Widgets & Power BI DAX Pipeline")
    subparsers = parser.add_subparsers(dest="command", help="Pipeline command to execute")

    # generate-all command
    p_all = subparsers.add_parser("generate-all", help="Generate all dashboard telemetry assets and DAX snippet")
    p_all.add_argument("--output-dir", default="examples/dashboard", help="Target directory for generated assets")
    p_all.add_argument("--theme", default="dark_slate", choices=list(THEMES.keys()), help="Visual theme palette")
    p_all.add_argument("--measure-name", default="TelemetryCard", help="Power BI DAX measure name")
    p_all.add_argument("--no-validate", action="store_true", help="Skip automated linter validation")

    # card command
    p_card = subparsers.add_parser("card", help="Generate standalone telemetry card SVG")
    p_card.add_argument("--output", default="examples/dashboard/telemetry_card.svg", help="Output file path")
    p_card.add_argument("--theme", default="dark_slate", choices=list(THEMES.keys()), help="Visual theme palette")
    p_card.add_argument("--kpi-value", default="$1,284,500", help="Primary KPI readout value")
    p_card.add_argument("--kpi-change", default="+14.2% ↑", help="KPI change percentage string")
    p_card.add_argument("--kpi-label", default="TOTAL SYSTEM THROUGHPUT", help="Primary metric label")
    p_card.add_argument("--kpi-sublabel", default="OPERATE // METRIC TELEMETRY", help="Card sublabel")
    p_card.add_argument("--scan-label", default="ACTIVE SCAN: 4.2 GHz", help="Radar telemetry label")
    p_card.add_argument("--status-label", default="ONLINE 99.9%", help="Status pill text")
    p_card.add_argument("--no-validate", action="store_true", help="Skip automated linter validation")

    # dax command
    p_dax = subparsers.add_parser("dax", help="Convert an SVG card to a Power BI DAX measure snippet")
    p_dax.add_argument("--input", default="examples/dashboard/telemetry_card.svg", help="Input SVG file path")
    p_dax.add_argument("--output", default="examples/dashboard/telemetry_card.dax", help="Output DAX file path")
    p_dax.add_argument("--measure-name", default="TelemetryCard", help="Power BI DAX measure name")
    p_dax.add_argument("--static", action="store_true", help="Generate purely static measure without variable interpolation")

    args = parser.parse_args()

    if args.command == "generate-all" or not args.command:
        out_dir = getattr(args, "output_dir", "examples/dashboard")
        theme = getattr(args, "theme", "dark_slate")
        m_name = getattr(args, "measure_name", "TelemetryCard")
        skip_val = getattr(args, "no_validate", False)

        print(f"\n==========================================")
        print(f" SVG Maestro Dashboard & DAX Pipeline")
        print(f" Theme: {theme} | Output: {out_dir}")
        print(f"==========================================\n")

        res = export_dashboard_assets(
            output_dir=out_dir,
            theme_name=theme,
            measure_name=m_name,
            validate=not skip_val,
            dynamic=True
        )

        svg_info = res["files"]["svg"]
        dax_info = res["files"]["dax"]

        status_str = "[PASS] VALID" if svg_info["valid"] else "[FAIL] INVALID"
        warn_str = f"({len(svg_info['warnings'])} warnings)" if svg_info['warnings'] else "(0 warnings)"
        print(f"  * {svg_info['filename']}: {status_str} {warn_str}")
        print(f"  * {dax_info['filename']}: Generated Power BI DAX measure")

        if svg_info["errors"]:
            for err in svg_info["errors"]:
                print(f"      ERROR: {err}")
        if svg_info["warnings"]:
            for warn in svg_info["warnings"]:
                print(f"      WARN:  {warn}")

        print(f"\nPipeline execution completed successfully.")
        sys.exit(0)

    elif args.command == "card":
        out_path = args.output
        parent_dir = os.path.dirname(os.path.abspath(out_path))
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        svg_code = generate_telemetry_card(
            theme_name=args.theme,
            kpi_value=args.kpi_value,
            kpi_change=args.kpi_change,
            kpi_label=args.kpi_label,
            kpi_sublabel=args.kpi_sublabel,
            scan_label=args.scan_label,
            status_label=args.status_label
        )
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg_code)
        print(f"Telemetry card generated at: {out_path}")

        if not args.no_validate:
            val_res = validate_svg_file(out_path)
            if not val_res.is_valid or val_res.warnings:
                print(f"[!] Validation issues detected:")
                for e in val_res.errors:
                    print(f"    ERROR: {e}")
                for w in val_res.warnings:
                    print(f"    WARN:  {w}")
                sys.exit(1)
            else:
                print("[PASS] Linter check passed with 0 errors and 0 warnings.")

    elif args.command == "dax":
        in_path = args.input
        out_path = args.output
        if not os.path.exists(in_path):
            print(f"[ERROR] Input SVG file not found: {in_path}")
            sys.exit(1)

        with open(in_path, "r", encoding="utf-8") as f:
            svg_code = f.read()

        parent_dir = os.path.dirname(os.path.abspath(out_path))
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        dynamic_mapping = None
        if not args.static:
            dynamic_mapping = {
                "$1,284,500": "_KpiValue",
                "+14.2% ↑": "_KpiChange",
                "TOTAL SYSTEM THROUGHPUT": "_KpiLabel"
            }

        dax_code = convert_svg_to_dax_measure(
            svg_content=svg_code,
            measure_name=args.measure_name,
            dynamic_vars=dynamic_mapping
        )
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(dax_code)
        print(f"Power BI DAX measure generated at: {out_path}")


if __name__ == "__main__":
    main()
