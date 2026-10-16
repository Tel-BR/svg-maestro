#!/usr/bin/env python3
"""
SVG Maestro - OBS Streaming Overlays Pipeline (Experience Mode)
Programmatic vector engine and generator for modular, transparent-viewport OBS streaming
overlays adhering to the Wrapper Pattern, Inkscape semantic layers, and CSS transform contracts.
"""

import os
import sys
import argparse
from typing import Dict, Any, Optional

# Add parent directory to sys.path to access validate_svg
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from validate_svg import validate_svg_file


THEMES: Dict[str, Dict[str, str]] = {
    "cyan_magenta": {
        "primary": "#00f0ff",        # Cyber Neon Cyan
        "primary_dark": "#0077cc",
        "secondary": "#ff007f",      # Cyber Neon Magenta
        "secondary_dark": "#99004d",
        "accent": "#ffb703",         # Cyber Amber/Gold
        "chassis_dark": "#060a14",
        "chassis_mid": "#0d1627",
        "grid_hairline": "#142542",
        "text_primary": "#ffffff",
        "text_secondary": "#00f0ff",
        "text_muted": "#8ca0be",
        "glow_color": "#00f0ff",
    },
    "amber_gold": {
        "primary": "#ffb703",        # Electric Amber
        "primary_dark": "#cc8800",
        "secondary": "#ff5500",      # Deep Blaze Orange
        "secondary_dark": "#992200",
        "accent": "#00f0ff",         # Cyber Cyan Accent
        "chassis_dark": "#120d06",
        "chassis_mid": "#24190c",
        "grid_hairline": "#3d2b15",
        "text_primary": "#ffffff",
        "text_secondary": "#ffb703",
        "text_muted": "#b8a082",
        "glow_color": "#ffb703",
    },
    "matrix_green": {
        "primary": "#00ff66",        # Phosphor Neon Green
        "primary_dark": "#00aa44",
        "secondary": "#00e5ff",      # Cyan Accent
        "secondary_dark": "#008899",
        "accent": "#76ff03",         # Toxic Lime
        "chassis_dark": "#051208",
        "chassis_mid": "#0c2414",
        "grid_hairline": "#163d23",
        "text_primary": "#ffffff",
        "text_secondary": "#00ff66",
        "text_muted": "#82b892",
        "glow_color": "#00ff66",
    },
    "crimson_hazard": {
        "primary": "#ff2a4b",        # High-voltage Crimson
        "primary_dark": "#b3122c",
        "secondary": "#ffaa00",      # Hazard Amber
        "secondary_dark": "#aa6600",
        "accent": "#ff007f",         # Neon Magenta Accent
        "chassis_dark": "#140609",
        "chassis_mid": "#280d13",
        "grid_hairline": "#421620",
        "text_primary": "#ffffff",
        "text_secondary": "#ff2a4b",
        "text_muted": "#c08892",
        "glow_color": "#ff2a4b",
    }
}


def get_theme(theme_name: str) -> Dict[str, str]:
    """Retrieve theme tokens or fallback to cyan_magenta."""
    return THEMES.get(theme_name, THEMES["cyan_magenta"])


def generate_webcam_frame(
    theme_name: str = "cyan_magenta",
    cam_label: str = "CAM 01 // LIVE FEED",
    status_label: str = "REC ● 1080P 60FPS",
    audio_label: str = "AUDIO: CH 1/2 NOMINAL [48kHz 24-bit]",
    telemetry_label: str = "LATENCY: 14ms // BITRATE: 8500kbps"
) -> str:
    """
    Generate a production-ready 16:9 webcam frame SVG for OBS Studio.
    - ViewBox: 0 0 1920 1080 (16:9 aspect ratio)
    - Camera Aperture: 1600x900 (centered, x=160..1760, y=90..990)
    - Transparent Center: Zero opaque fills inside the camera aperture.
    - Animations: Breathing pulse corner brackets, REC beacon, audio visualizer bars, radar reticle.
    - Strict Inkscape Semantic Layers: layer-background, layer-frame, layer-accents, layer-typography.
    - Strict Wrapper Pattern: CSS keyframe transforms scoped to <g> wrapper nodes with transform-box and transform-origin.
    """
    t = get_theme(theme_name)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 1920 1080"
     width="100%" height="100%">
  <defs>
    <!-- Gradients -->
    <linearGradient id="grad-cyber-primary" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['primary']}" />
      <stop offset="100%" stop-color="{t['primary_dark']}" />
    </linearGradient>
    <linearGradient id="grad-cyber-secondary" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['secondary']}" />
      <stop offset="100%" stop-color="{t['secondary_dark']}" />
    </linearGradient>
    <linearGradient id="grad-cyber-accent" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['accent']}" />
      <stop offset="100%" stop-color="{t['primary']}" />
    </linearGradient>
    <linearGradient id="grad-chassis-top" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['chassis_dark']}" stop-opacity="0.95" />
      <stop offset="100%" stop-color="{t['chassis_mid']}" stop-opacity="0.85" />
    </linearGradient>
    <linearGradient id="grad-chassis-bottom" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['chassis_mid']}" stop-opacity="0.85" />
      <stop offset="100%" stop-color="{t['chassis_dark']}" stop-opacity="0.95" />
    </linearGradient>
    <linearGradient id="grad-chassis-wing" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['chassis_dark']}" stop-opacity="0.92" />
      <stop offset="100%" stop-color="{t['chassis_mid']}" stop-opacity="0.80" />
    </linearGradient>

    <!-- Glow Filters -->
    <filter id="filter-primary-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur-p" />
      <feMerge>
        <feMergeNode in="blur-p" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="filter-secondary-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur-s" />
      <feMerge>
        <feMergeNode in="blur-s" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="filter-hud-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur-h" />
      <feMerge>
        <feMergeNode in="blur-h" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    /* SVG Maestro Universal CSS Transform Contract */
    .anim-corner-pulse {{
      animation: pulse-corner-kf 3s ease-in-out infinite alternate;
      transform-box: fill-box;
      transform-origin: center;
    }}

    .anim-rec-beacon {{
      animation: blink-rec-kf 1.2s ease-in-out infinite alternate;
      transform-box: fill-box;
      transform-origin: center;
    }}

    .anim-radar-spin {{
      animation: spin-radar-kf 10s linear infinite;
      transform-box: fill-box;
      transform-origin: center;
    }}

    .anim-audio-bar-1 {{
      animation: audio-bounce-kf1 0.9s ease-in-out infinite alternate;
      transform-box: fill-box;
      transform-origin: center;
    }}

    .anim-audio-bar-2 {{
      animation: audio-bounce-kf2 1.3s ease-in-out infinite alternate;
      transform-box: fill-box;
      transform-origin: center;
    }}

    .anim-audio-bar-3 {{
      animation: audio-bounce-kf3 1.1s ease-in-out infinite alternate;
      transform-box: fill-box;
      transform-origin: center;
    }}

    @keyframes pulse-corner-kf {{
      0% {{
        opacity: 0.70;
        transform: scale(0.97);
      }}
      100% {{
        opacity: 1.0;
        transform: scale(1.03);
      }}
    }}

    @keyframes blink-rec-kf {{
      0% {{
        opacity: 0.25;
        transform: scale(0.85);
      }}
      100% {{
        opacity: 1.0;
        transform: scale(1.15);
      }}
    }}

    @keyframes spin-radar-kf {{
      0% {{
        transform: rotate(0deg);
      }}
      100% {{
        transform: rotate(360deg);
      }}
    }}

    @keyframes audio-bounce-kf1 {{
      0% {{ transform: scaleY(0.35); }}
      100% {{ transform: scaleY(1.0); }}
    }}

    @keyframes audio-bounce-kf2 {{
      0% {{ transform: scaleY(0.75); }}
      100% {{ transform: scaleY(0.30); }}
    }}

    @keyframes audio-bounce-kf3 {{
      0% {{ transform: scaleY(0.25); }}
      100% {{ transform: scaleY(0.90); }}
    }}
  </style>

  <!-- Layer 1: Background Framing (Outside Camera Viewport Only) -->
  <g inkscape:groupmode="layer" id="layer-background" inkscape:label="Background Framing">
    <!-- Top Header Chassis Plate -->
    <path d="M 140,16 L 1780,16 L 1756,86 L 164,86 Z"
          fill="url(#grad-chassis-top)" stroke="{t['grid_hairline']}" stroke-width="1.5" />

    <!-- Bottom Docking Chassis Plate -->
    <path d="M 164,994 L 1756,994 L 1780,1064 L 140,1064 Z"
          fill="url(#grad-chassis-bottom)" stroke="{t['grid_hairline']}" stroke-width="1.5" />

    <!-- Left Lateral Tech Wing -->
    <path d="M 32,106 L 156,106 L 156,974 L 32,974 L 18,944 L 18,136 Z"
          fill="url(#grad-chassis-wing)" stroke="{t['grid_hairline']}" stroke-width="1.5" />

    <!-- Right Lateral Tech Wing -->
    <path d="M 1764,106 L 1888,106 L 1902,136 L 1902,944 L 1888,974 L 1764,974 Z"
          fill="url(#grad-chassis-wing)" stroke="{t['grid_hairline']}" stroke-width="1.5" />

    <!-- Lateral Technical Grid Ticks (Left Wing) -->
    <path d="M 40,200 L 70,200 M 40,240 L 60,240 M 40,280 L 60,280 M 40,320 L 75,320
             M 40,360 L 60,360 M 40,400 L 60,400 M 40,440 L 70,440
             M 40,640 L 70,640 M 40,680 L 60,680 M 40,720 L 60,720 M 40,760 L 75,760
             M 40,800 L 60,800 M 40,840 L 60,840 M 40,880 L 70,880"
          stroke="{t['grid_hairline']}" stroke-width="1" />

    <!-- Lateral Technical Grid Ticks (Right Wing) -->
    <path d="M 1880,200 L 1850,200 M 1880,240 L 1860,240 M 1880,280 L 1860,280 M 1880,320 L 1845,320
             M 1880,360 L 1860,360 M 1880,400 L 1860,400 M 1880,440 L 1850,440
             M 1880,640 L 1850,640 M 1880,680 L 1860,680 M 1880,720 L 1860,720 M 1880,760 L 1845,760
             M 1880,800 L 1860,800 M 1880,840 L 1860,840 M 1880,880 L 1850,880"
          stroke="{t['grid_hairline']}" stroke-width="1" />
  </g>

  <!-- Layer 2: Frame Chassis & Bevel Rails -->
  <g inkscape:groupmode="layer" id="layer-frame" inkscape:label="Frame Chassis">
    <!-- Main Outer Aperture Neon Rail (Chamfered 16:9 Border) -->
    <path d="M 188,86 L 1732,86 L 1764,118 L 1764,962 L 1732,994 L 188,994 L 156,962 L 156,118 Z"
          fill="none" stroke="url(#grad-cyber-primary)" stroke-width="3.5" filter="url(#filter-primary-glow)" />

    <!-- Inner Aperture Precision Hairline -->
    <path d="M 188,90 L 1732,90 L 1760,118 L 1760,962 L 1732,990 L 188,990 L 160,962 L 160,118 Z"
          fill="none" stroke="{t['primary']}" stroke-width="1" stroke-opacity="0.45" />

    <!-- Top Structural Bridge Rail -->
    <path d="M 140,22 L 1780,22" fill="none" stroke="{t['secondary']}" stroke-width="2" filter="url(#filter-secondary-glow)" />

    <!-- Bottom Structural Docking Rail -->
    <path d="M 140,1058 L 1780,1058" fill="none" stroke="{t['primary']}" stroke-width="2" filter="url(#filter-primary-glow)" />

    <!-- Left & Right Accent Chevrons -->
    <path d="M 70,480 L 90,500 L 70,520 M 70,560 L 90,580 L 70,600"
          fill="none" stroke="{t['primary']}" stroke-width="2" />
    <path d="M 1850,480 L 1830,500 L 1850,520 M 1850,560 L 1830,580 L 1850,600"
          fill="none" stroke="{t['primary']}" stroke-width="2" />
  </g>

  <!-- Layer 3: Accents & Lighting (Animated via Wrapper Pattern) -->
  <g inkscape:groupmode="layer" id="layer-accents" inkscape:label="Accents and Lighting">
    <!-- Top-Left Animated Corner Bracket -->
    <g class="anim-corner-pulse" id="wrapper-corner-tl">
      <g id="geom-corner-tl" inkscape:label="Corner TL Bracket">
        <path d="M 120,136 L 120,54 L 224,54" fill="none" stroke="{t['primary']}" stroke-width="5" filter="url(#filter-primary-glow)" />
        <polygon points="120,54 148,54 120,82" fill="{t['primary']}" />
        <circle cx="120" cy="54" r="4.5" fill="{t['secondary']}" />
        <circle cx="224" cy="54" r="3.5" fill="{t['accent']}" />
        <circle cx="120" cy="136" r="3.5" fill="{t['accent']}" />
      </g>
    </g>

    <!-- Top-Right Animated Corner Bracket -->
    <g class="anim-corner-pulse" id="wrapper-corner-tr">
      <g id="geom-corner-tr" inkscape:label="Corner TR Bracket">
        <path d="M 1800,136 L 1800,54 L 1696,54" fill="none" stroke="{t['primary']}" stroke-width="5" filter="url(#filter-primary-glow)" />
        <polygon points="1800,54 1772,54 1800,82" fill="{t['primary']}" />
        <circle cx="1800" cy="54" r="4.5" fill="{t['secondary']}" />
        <circle cx="1696" cy="54" r="3.5" fill="{t['accent']}" />
        <circle cx="1800" cy="136" r="3.5" fill="{t['accent']}" />
      </g>
    </g>

    <!-- Bottom-Left Animated Corner Bracket -->
    <g class="anim-corner-pulse" id="wrapper-corner-bl">
      <g id="geom-corner-bl" inkscape:label="Corner BL Bracket">
        <path d="M 120,944 L 120,1026 L 224,1026" fill="none" stroke="{t['secondary']}" stroke-width="5" filter="url(#filter-secondary-glow)" />
        <polygon points="120,1026 148,1026 120,998" fill="{t['secondary']}" />
        <circle cx="120" cy="1026" r="4.5" fill="{t['primary']}" />
        <circle cx="224" cy="1026" r="3.5" fill="{t['accent']}" />
        <circle cx="120" cy="944" r="3.5" fill="{t['accent']}" />
      </g>
    </g>

    <!-- Bottom-Right Animated Corner Bracket -->
    <g class="anim-corner-pulse" id="wrapper-corner-br">
      <g id="geom-corner-br" inkscape:label="Corner BR Bracket">
        <path d="M 1800,944 L 1800,1026 L 1696,1026" fill="none" stroke="{t['secondary']}" stroke-width="5" filter="url(#filter-secondary-glow)" />
        <polygon points="1800,1026 1772,1026 1800,998" fill="{t['secondary']}" />
        <circle cx="1800" cy="1026" r="4.5" fill="{t['primary']}" />
        <circle cx="1696" cy="1026" r="3.5" fill="{t['accent']}" />
        <circle cx="1800" cy="944" r="3.5" fill="{t['accent']}" />
      </g>
    </g>

    <!-- Animated REC Indicator Beacon -->
    <g class="anim-rec-beacon" id="wrapper-rec-beacon">
      <g id="geom-rec-beacon" inkscape:label="REC Indicator">
        <circle cx="1636" cy="52" r="8.5" fill="{t['secondary']}" filter="url(#filter-secondary-glow)" />
        <circle cx="1636" cy="52" r="4" fill="#ffffff" />
      </g>
    </g>

    <!-- Animated Left Wing Radar Reticle -->
    <g class="anim-radar-spin" id="wrapper-radar-widget">
      <g id="geom-radar-widget" inkscape:label="Radar Scanner">
        <circle cx="86" cy="540" r="28" fill="none" stroke="{t['primary']}" stroke-width="1.5" stroke-dasharray="10 6" />
        <line x1="86" y1="510" x2="86" y2="570" stroke="{t['primary']}" stroke-width="1" />
        <line x1="56" y1="540" x2="116" y2="540" stroke="{t['primary']}" stroke-width="1" />
        <circle cx="86" cy="540" r="10" fill="none" stroke="{t['accent']}" stroke-width="1.5" />
      </g>
    </g>

    <!-- Animated Audio Visualizer Meter Bars (Bottom Docking Bar) -->
    <g id="cluster-audio-meter">
      <g class="anim-audio-bar-1" id="wrapper-audio-1">
        <g id="geom-audio-1" inkscape:label="Audio Bar 1">
          <rect x="910" y="1020" width="5" height="24" rx="2" fill="{t['primary']}" filter="url(#filter-hud-glow)" />
        </g>
      </g>
      <g class="anim-audio-bar-2" id="wrapper-audio-2">
        <g id="geom-audio-2" inkscape:label="Audio Bar 2">
          <rect x="922" y="1020" width="5" height="24" rx="2" fill="{t['primary']}" filter="url(#filter-hud-glow)" />
        </g>
      </g>
      <g class="anim-audio-bar-3" id="wrapper-audio-3">
        <g id="geom-audio-3" inkscape:label="Audio Bar 3">
          <rect x="934" y="1020" width="5" height="24" rx="2" fill="{t['accent']}" filter="url(#filter-hud-glow)" />
        </g>
      </g>
      <g class="anim-audio-bar-1" id="wrapper-audio-4">
        <g id="geom-audio-4" inkscape:label="Audio Bar 4">
          <rect x="946" y="1020" width="5" height="24" rx="2" fill="{t['accent']}" filter="url(#filter-hud-glow)" />
        </g>
      </g>
      <g class="anim-audio-bar-2" id="wrapper-audio-5">
        <g id="geom-audio-5" inkscape:label="Audio Bar 5">
          <rect x="958" y="1020" width="5" height="24" rx="2" fill="{t['secondary']}" filter="url(#filter-hud-glow)" />
        </g>
      </g>
      <g class="anim-audio-bar-3" id="wrapper-audio-6">
        <g id="geom-audio-6" inkscape:label="Audio Bar 6">
          <rect x="970" y="1020" width="5" height="24" rx="2" fill="{t['secondary']}" filter="url(#filter-hud-glow)" />
        </g>
      </g>
      <g class="anim-audio-bar-1" id="wrapper-audio-7">
        <g id="geom-audio-7" inkscape:label="Audio Bar 7">
          <rect x="982" y="1020" width="5" height="24" rx="2" fill="{t['primary']}" filter="url(#filter-hud-glow)" />
        </g>
      </g>
      <g class="anim-audio-bar-2" id="wrapper-audio-8">
        <g id="geom-audio-8" inkscape:label="Audio Bar 8">
          <rect x="994" y="1020" width="5" height="24" rx="2" fill="{t['primary']}" filter="url(#filter-hud-glow)" />
        </g>
      </g>
      <g class="anim-audio-bar-3" id="wrapper-audio-9">
        <g id="geom-audio-9" inkscape:label="Audio Bar 9">
          <rect x="1006" y="1020" width="5" height="24" rx="2" fill="{t['accent']}" filter="url(#filter-hud-glow)" />
        </g>
      </g>
    </g>

    <!-- Viewport Edge Alignment Crosshairs -->
    <path d="M 960,82 L 960,98 M 952,90 L 968,90" stroke="{t['primary']}" stroke-width="1.5" />
    <path d="M 960,982 L 960,998 M 952,990 L 968,990" stroke="{t['primary']}" stroke-width="1.5" />
    <path d="M 152,540 L 168,540 M 160,532 L 160,548" stroke="{t['primary']}" stroke-width="1.5" />
    <path d="M 1752,540 L 1768,540 M 1760,532 L 1760,548" stroke="{t['primary']}" stroke-width="1.5" />
  </g>

  <!-- Layer 4: Typography & HUD Labels (Decoupled Semantic Text) -->
  <g inkscape:groupmode="layer" id="layer-typography" inkscape:label="Typography and Labels">
    <!-- Camera Channel / Feed Label -->
    <text x="250" y="58" fill="{t['primary']}" font-family="'JetBrains Mono', 'Segoe UI', monospace" font-size="18" font-weight="700" letter-spacing="3">{cam_label}</text>

    <!-- REC Indicator & Format Readout -->
    <text x="1656" y="58" fill="{t['text_primary']}" font-family="'JetBrains Mono', 'Segoe UI', monospace" font-size="16" font-weight="600" letter-spacing="2">{status_label}</text>

    <!-- Audio Telemetry Readout (Bottom Left) -->
    <text x="250" y="1038" fill="{t['text_muted']}" font-family="'JetBrains Mono', 'Segoe UI', monospace" font-size="14" font-weight="500" letter-spacing="2">{audio_label}</text>

    <!-- Network / Bitrate Readout (Bottom Right) -->
    <text x="1410" y="1038" fill="{t['primary']}" font-family="'JetBrains Mono', 'Segoe UI', monospace" font-size="14" font-weight="600" letter-spacing="2">{telemetry_label}</text>

    <!-- Left Wing Calibration Readout -->
    <text x="86" y="240" fill="{t['grid_hairline']}" font-family="'JetBrains Mono', monospace" font-size="11" text-anchor="middle" letter-spacing="1">HUD.V-01</text>
    <text x="86" y="850" fill="{t['grid_hairline']}" font-family="'JetBrains Mono', monospace" font-size="11" text-anchor="middle" letter-spacing="1">OPT.SYNC</text>

    <!-- Right Wing Calibration Readout -->
    <text x="1834" y="240" fill="{t['grid_hairline']}" font-family="'JetBrains Mono', monospace" font-size="11" text-anchor="middle" letter-spacing="1">CH.DATA</text>
    <text x="1834" y="850" fill="{t['grid_hairline']}" font-family="'JetBrains Mono', monospace" font-size="11" text-anchor="middle" letter-spacing="1">STABLE</text>
  </g>
</svg>'''
    return svg_content


def generate_alert_banner(
    theme_name: str = "cyan_magenta",
    alert_type: str = "NEW SUBSCRIBER",
    username: str = "CYBER_PHANTOM",
    detail_text: str = "TIER 3 // 12 MONTH STREAK",
    channel_id: str = "SYS.ALERT // CH-09"
) -> str:
    """
    Generate a production-ready modular alert notification banner SVG for OBS Studio.
    - ViewBox: 0 0 1200 300 (Modular 4:1 aspect ratio)
    - Continuous Line Tracing: stroke-dasharray and stroke-dashoffset animation along perimeter.
    - Cyber Neon Illumination: High-contrast glows, gradients, and illuminated emblem.
    - Transparent Surrounding: Designed specifically as a floating browser source in streaming software.
    - Strict Inkscape Semantic Layers: layer-background, layer-frame, layer-accents, layer-typography.
    - Strict Wrapper Pattern: CSS keyframe transforms scoped to <g> wrapper nodes with transform-box and transform-origin.
    """
    t = get_theme(theme_name)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 1200 300"
     width="100%" height="100%">
  <defs>
    <!-- Chassis Gradients -->
    <linearGradient id="grad-alert-chassis" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['chassis_dark']}" stop-opacity="0.95" />
      <stop offset="100%" stop-color="{t['chassis_mid']}" stop-opacity="0.90" />
    </linearGradient>
    <linearGradient id="grad-alert-border" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['primary']}" />
      <stop offset="50%" stop-color="{t['secondary']}" />
      <stop offset="100%" stop-color="{t['accent']}" />
    </linearGradient>
    <linearGradient id="grad-badge-glow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['secondary']}" />
      <stop offset="100%" stop-color="{t['primary_dark']}" />
    </linearGradient>

    <!-- Glow Filters -->
    <filter id="filter-trace-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4.5" result="blur-t" />
      <feMerge>
        <feMergeNode in="blur-t" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="filter-badge-glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6" result="blur-b" />
      <feMerge>
        <feMergeNode in="blur-b" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="filter-neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3.5" result="blur-n" />
      <feMerge>
        <feMergeNode in="blur-n" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    /* Continuous Line Tracing Motion */
    .anim-line-trace {{
      stroke-dasharray: 240 760;
      animation: trace-perimeter-kf 4s linear infinite;
    }}

    .anim-line-trace-reverse {{
      stroke-dasharray: 180 520;
      animation: trace-reverse-kf 3s linear infinite;
    }}

    /* Wrapper Pattern Animated Elements */
    .anim-badge-pulse {{
      animation: badge-pulse-kf 2.4s ease-in-out infinite alternate;
      transform-box: fill-box;
      transform-origin: center;
    }}

    .anim-badge-ring {{
      animation: badge-spin-kf 9s linear infinite;
      transform-box: fill-box;
      transform-origin: center;
    }}

    .anim-status-pip {{
      animation: pip-blink-kf 1.2s ease-in-out infinite alternate;
      transform-box: fill-box;
      transform-origin: center;
    }}

    .anim-meter-wave {{
      animation: meter-wave-kf 1.5s ease-in-out infinite alternate;
      transform-box: fill-box;
      transform-origin: center;
    }}

    @keyframes trace-perimeter-kf {{
      0% {{
        stroke-dashoffset: 0;
      }}
      100% {{
        stroke-dashoffset: -2000;
      }}
    }}

    @keyframes trace-reverse-kf {{
      0% {{
        stroke-dashoffset: 0;
      }}
      100% {{
        stroke-dashoffset: 1400;
      }}
    }}

    @keyframes badge-pulse-kf {{
      0% {{
        transform: scale(0.96);
        opacity: 0.85;
      }}
      100% {{
        transform: scale(1.04);
        opacity: 1.0;
      }}
    }}

    @keyframes badge-spin-kf {{
      0% {{
        transform: rotate(0deg);
      }}
      100% {{
        transform: rotate(360deg);
      }}
    }}

    @keyframes pip-blink-kf {{
      0% {{
        opacity: 0.30;
        transform: scale(0.85);
      }}
      100% {{
        opacity: 1.0;
        transform: scale(1.15);
      }}
    }}

    @keyframes meter-wave-kf {{
      0% {{
        transform: scaleY(0.40);
      }}
      100% {{
        transform: scaleY(1.0);
      }}
    }}
  </style>

  <!-- Layer 1: Background Chassis Backplate (Floating with Transparent Canvas) -->
  <g inkscape:groupmode="layer" id="layer-background" inkscape:label="Chassis Backplate">
    <!-- Main Chamfered Banner Chassis Plate -->
    <path d="M 136,32 L 1064,32 L 1100,68 L 1100,232 L 1064,268 L 136,268 L 100,232 L 100,68 Z"
          fill="url(#grad-alert-chassis)" stroke="{t['grid_hairline']}" stroke-width="1.5" />

    <!-- Left Badge Recessed Backplate -->
    <polygon points="112,68 144,36 264,36 264,264 144,264 112,232"
             fill="{t['chassis_dark']}" fill-opacity="0.9" stroke="{t['grid_hairline']}" stroke-width="1" />

    <!-- Background Tech Grid Texture -->
    <path d="M 300,50 L 1050,50 M 300,250 L 1050,250
             M 400,32 L 400,268 M 600,32 L 600,268 M 800,32 L 800,268 M 1000,32 L 1000,268"
          stroke="{t['grid_hairline']}" stroke-width="0.75" stroke-opacity="0.6" stroke-dasharray="4 8" />
  </g>

  <!-- Layer 2: Frame Chassis & Continuous Tracing Rails -->
  <g inkscape:groupmode="layer" id="layer-frame" inkscape:label="Chassis Frame">
    <!-- Static Structural Frame Border -->
    <path d="M 136,32 L 1064,32 L 1100,68 L 1100,232 L 1064,268 L 136,268 L 100,232 L 100,68 Z"
          fill="none" stroke="{t['grid_hairline']}" stroke-width="2.5" />

    <!-- CONTINUOUS LINE TRACING PATH 1: Outer Chamfered Perimeter -->
    <path class="anim-line-trace"
          d="M 140,36 L 1060,36 L 1094,70 L 1094,230 L 1060,264 L 140,264 L 106,230 L 106,70 Z"
          fill="none" stroke="url(#grad-alert-border)" stroke-width="3.5"
          stroke-linecap="round" stroke-linejoin="round"
          filter="url(#filter-trace-glow)" />

    <!-- CONTINUOUS LINE TRACING PATH 2: Lower Energy Rail -->
    <path class="anim-line-trace-reverse"
          d="M 284,248 L 1030,248 L 1060,218"
          fill="none" stroke="{t['primary']}" stroke-width="2"
          stroke-linecap="round" filter="url(#filter-neon-glow)" />

    <!-- Chassis Mounting Brackets & Notches -->
    <polygon points="100,68 116,68 100,84" fill="{t['accent']}" />
    <polygon points="1100,68 1084,68 1100,84" fill="{t['secondary']}" />
    <polygon points="100,232 116,232 100,216" fill="{t['secondary']}" />
    <polygon points="1100,232 1084,232 1100,216" fill="{t['primary']}" />
  </g>

  <!-- Layer 3: Accents & Lighting (Emblem & Status Pips via Wrapper Pattern) -->
  <g inkscape:groupmode="layer" id="layer-accents" inkscape:label="Accents and Lighting">
    <!-- Animated Rotating Outer Telemetry Ring -->
    <g class="anim-badge-ring" id="wrapper-badge-ring">
      <g id="geom-badge-ring" inkscape:label="Rotating Ring">
        <circle cx="188" cy="150" r="62" fill="none" stroke="{t['primary']}" stroke-width="1.5" stroke-dasharray="16 12 4 12" />
        <circle cx="188" cy="88" r="3" fill="{t['accent']}" />
        <circle cx="188" cy="212" r="3" fill="{t['accent']}" />
      </g>
    </g>

    <!-- Animated Breathing Cyber Badge Emblem -->
    <g class="anim-badge-pulse" id="wrapper-alert-badge">
      <g id="geom-alert-badge" inkscape:label="Cyber Emblem">
        <!-- Outer Glowing Hexagon Shield -->
        <polygon points="188,96 234,123 234,177 188,204 142,177 142,123"
                 fill="url(#grad-badge-glow)" fill-opacity="0.30"
                 stroke="{t['secondary']}" stroke-width="3" filter="url(#filter-badge-glow)" />

        <!-- Inner Precision Diamond -->
        <polygon points="188,110 218,150 188,190 158,150"
                 fill="none" stroke="{t['primary']}" stroke-width="2" />

        <!-- Central Radiant Star Glyph -->
        <path d="M 188,134 L 192,145 L 204,150 L 192,155 L 188,166 L 184,155 L 172,150 L 184,145 Z"
              fill="#ffffff" filter="url(#filter-neon-glow)" />
      </g>
    </g>

    <!-- Animated Status Beacon Pip -->
    <g class="anim-status-pip" id="wrapper-status-pip">
      <g id="geom-status-pip" inkscape:label="Status Beacon">
        <circle cx="288" cy="86" r="6.5" fill="{t['accent']}" filter="url(#filter-neon-glow)" />
        <circle cx="288" cy="86" r="3" fill="#ffffff" />
      </g>
    </g>

    <!-- Animated Right Waveform Meter -->
    <g id="cluster-alert-meter">
      <g class="anim-meter-wave" id="wrapper-meter-1">
        <g id="geom-meter-1" inkscape:label="Wave Bar 1">
          <rect x="1020" y="130" width="4" height="40" rx="2" fill="{t['primary']}" filter="url(#filter-neon-glow)" />
        </g>
      </g>
      <g class="anim-meter-wave" id="wrapper-meter-2">
        <g id="geom-meter-2" inkscape:label="Wave Bar 2">
          <rect x="1030" y="120" width="4" height="60" rx="2" fill="{t['secondary']}" filter="url(#filter-neon-glow)" />
        </g>
      </g>
      <g class="anim-meter-wave" id="wrapper-meter-3">
        <g id="geom-meter-3" inkscape:label="Wave Bar 3">
          <rect x="1040" y="135" width="4" height="30" rx="2" fill="{t['accent']}" filter="url(#filter-neon-glow)" />
        </g>
      </g>
    </g>
  </g>

  <!-- Layer 4: Typography & Alert Copy (Decoupled Semantic Text) -->
  <g inkscape:groupmode="layer" id="layer-typography" inkscape:label="Typography and Labels">
    <!-- Alert Subheader / Event Type -->
    <text x="310" y="92" fill="{t['accent']}" font-family="'JetBrains Mono', 'Segoe UI', monospace" font-size="16" font-weight="800" letter-spacing="4">{alert_type}</text>

    <!-- Primary Username Readout -->
    <text x="310" y="168" fill="{t['text_primary']}" font-family="'JetBrains Mono', 'Segoe UI', sans-serif" font-size="44" font-weight="900" letter-spacing="2">{username}</text>

    <!-- Detail Message / Tier Readout -->
    <text x="310" y="214" fill="{t['primary']}" font-family="'JetBrains Mono', 'Segoe UI', monospace" font-size="18" font-weight="600" letter-spacing="2">{detail_text}</text>

    <!-- Channel / Watermark ID -->
    <text x="1050" y="92" text-anchor="end" fill="{t['text_muted']}" font-family="'JetBrains Mono', monospace" font-size="12" letter-spacing="2">{channel_id}</text>
  </g>
</svg>'''
    return svg_content


def export_obs_overlays(
    output_dir: str = "examples/obs",
    theme_name: str = "cyan_magenta",
    validate: bool = True
) -> Dict[str, Any]:
    """
    Generate and save both the 16:9 webcam frame and alert banner to output_dir.
    Optionally validate generated SVGs with validate_svg.py.
    """
    os.makedirs(output_dir, exist_ok=True)

    webcam_filename = "webcam_frame_16_9.svg"
    webcam_path = os.path.join(output_dir, webcam_filename)
    webcam_svg = generate_webcam_frame(theme_name=theme_name)

    with open(webcam_path, "w", encoding="utf-8") as f:
        f.write(webcam_svg)

    alert_filename = "alert_banner.svg"
    alert_path = os.path.join(output_dir, alert_filename)
    alert_svg = generate_alert_banner(theme_name=theme_name)

    with open(alert_path, "w", encoding="utf-8") as f:
        f.write(alert_svg)

    results = {
        "output_dir": output_dir,
        "theme": theme_name,
        "files": {
            "webcam": {
                "filename": webcam_filename,
                "path": webcam_path,
                "valid": None,
                "errors": [],
                "warnings": []
            },
            "alert": {
                "filename": alert_filename,
                "path": alert_path,
                "valid": None,
                "errors": [],
                "warnings": []
            }
        }
    }

    if validate:
        webcam_res = validate_svg_file(webcam_path)
        results["files"]["webcam"]["valid"] = webcam_res.is_valid
        results["files"]["webcam"]["errors"] = webcam_res.errors
        results["files"]["webcam"]["warnings"] = webcam_res.warnings

        alert_res = validate_svg_file(alert_path)
        results["files"]["alert"]["valid"] = alert_res.is_valid
        results["files"]["alert"]["errors"] = alert_res.errors
        results["files"]["alert"]["warnings"] = alert_res.warnings

    return results


def main():
    parser = argparse.ArgumentParser(description="SVG Maestro - OBS Streaming Overlays Pipeline")
    subparsers = parser.add_subparsers(dest="command", help="Pipeline command to execute")

    # generate-all command
    p_all = subparsers.add_parser("generate-all", help="Generate all OBS streaming overlay assets")
    p_all.add_argument("--output-dir", default="examples/obs", help="Target directory for generated SVGs")
    p_all.add_argument("--theme", default="cyan_magenta", choices=list(THEMES.keys()), help="Visual theme palette")
    p_all.add_argument("--no-validate", action="store_true", help="Skip automated linter validation")

    # webcam command
    p_cam = subparsers.add_parser("webcam", help="Generate 16:9 webcam frame overlay")
    p_cam.add_argument("--output", default="examples/obs/webcam_frame_16_9.svg", help="Output file path")
    p_cam.add_argument("--theme", default="cyan_magenta", choices=list(THEMES.keys()), help="Visual theme palette")
    p_cam.add_argument("--cam-label", default="CAM 01 // LIVE FEED", help="Camera channel label")
    p_cam.add_argument("--status-label", default="REC ● 1080P 60FPS", help="Status and resolution label")

    # alert command
    p_alert = subparsers.add_parser("alert", help="Generate modular alert notification banner")
    p_alert.add_argument("--output", default="examples/obs/alert_banner.svg", help="Output file path")
    p_alert.add_argument("--theme", default="cyan_magenta", choices=list(THEMES.keys()), help="Visual theme palette")
    p_alert.add_argument("--type", default="NEW SUBSCRIBER", help="Alert notification type")
    p_alert.add_argument("--user", default="CYBER_PHANTOM", help="Username displayed on banner")
    p_alert.add_argument("--detail", default="TIER 3 // 12 MONTH STREAK", help="Detail streak or message")

    args = parser.parse_args()

    if args.command == "generate-all" or not args.command:
        out_dir = getattr(args, "output_dir", "examples/obs")
        theme = getattr(args, "theme", "cyan_magenta")
        skip_val = getattr(args, "no_validate", False)

        print(f"\n==========================================")
        print(f" SVG Maestro OBS Overlays Pipeline")
        print(f" Theme: {theme} | Output: {out_dir}")
        print(f"==========================================\n")

        res = export_obs_overlays(output_dir=out_dir, theme_name=theme, validate=not skip_val)

        for name, info in res["files"].items():
            status_str = "[PASS] VALID" if info["valid"] else "[FAIL] INVALID"
            warn_str = f"({len(info['warnings'])} warnings)" if info['warnings'] else "(0 warnings)"
            print(f"  * {info['filename']}: {status_str} {warn_str}")
            if info["errors"]:
                for err in info["errors"]:
                    print(f"      ERROR: {err}")
            if info["warnings"]:
                for warn in info["warnings"]:
                    print(f"      WARN:  {warn}")

        print(f"\nPipeline execution completed successfully.")
        sys.exit(0)

    elif args.command == "webcam":
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        svg_code = generate_webcam_frame(
            theme_name=args.theme,
            cam_label=args.cam_label,
            status_label=args.status_label
        )
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(svg_code)
        print(f"Webcam frame generated at: {args.output}")

    elif args.command == "alert":
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        svg_code = generate_alert_banner(
            theme_name=args.theme,
            alert_type=args.type,
            username=args.user,
            detail_text=args.detail
        )
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(svg_code)
        print(f"Alert banner generated at: {args.output}")


if __name__ == "__main__":
    main()
