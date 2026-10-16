# SVG Maestro 🎨✨

[English](README.md) | 🌐 **Português (Brasil)**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](scripts/validate_svg.py)
[![Inkscape: Fully Compatible](https://img.shields.io/badge/Inkscape-Compatible-brightgreen.svg)](docs/SPEC.md)

**SVG Maestro** é um sistema de design e orquestração de movimento vetorial de código aberto para agentes de inteligência artificial (Antigravity, Claude, Codex). Ele funde a **disciplina arquitetural de Matt Pocock** (eliciação de briefing, fatias verticais e validação mecânica) com a **alta direção de arte do Impeccable** (modos de superfície, verbos criativos de refinamento e regras inegociáveis de qualidade visual), gerando layouts matemáticos em SVG, cartões de telemetria para dashboards e overlays para streaming no OBS Studio que são 100% editáveis no Inkscape.

---

## 🏛️ Os Três Pilares Fundamentais

### 1. Direção de Arte & Geometria Matemática (Dual-Engine)
- **Zero-Bias Policy**: Sem templates ou clipart genérico. Toda arte é criada do zero a partir de sequências de Fibonacci, Proporção Áurea ($\phi \approx 1.618$), malhas isométricas de $30^\circ$ e tangências euclidianas.
- **Modos de Superfície**:
  - `Operate`: Alta densidade e escaneabilidade para dashboards web e cartões do Power BI.
  - `Experience`: Iluminação néon vibrante, alto contraste e animações em loop a 60fps para overlays de streaming no OBS Studio.
  - `Persuade`: Proporções monumentais e narrativa visual para ilustrações hero e branding.
- **Craft Floor**: Piso inegociável de qualidade que proíbe expressamente "clipart genérico de IA", gradientes lodosos e curvas mal conectadas.
- **Autonomia Total**: Opera 100% independente do zero. Opcionalmente conecta-se aos tokens de `DESIGN.md` ou `PRODUCT.md` caso o projeto já utilize a skill `impeccable`.

### 2. Compatibilidade Total com Inkscape
- Conformidade estrita com namespaces (`xmlns:inkscape`, `xmlns:sodipodi`).
- Camadas semânticas nativas do Inkscape (`inkscape:groupmode="layer"` e `inkscape:label`).
- Higiene rigorosa em `<defs>` com identificadores semânticos descritivos.

### 3. Animação Vetorial Nativa à Prova de Mutação (Wrapper Pattern)
- **Wrapper Pattern**: Encapsula elementos animados em invólucros dedicados (`<g class="anim-wrapper-...">`), protegendo os nós estáticos (`<g inkscape:label="...">`) contra colisões de transformação durante edições manuais no Inkscape.
- **Tier 1 (CSS Universal)**: `@keyframes` com `transform-box: fill-box` e `transform-origin: center` obrigatórios para estabilidade entre navegadores e OBS.
- **Tier 2 (SMIL Vector Motion)**: Morphing de caminhos vetoriais e animação sobre guias de movimento.
- **Filtros Vetoriais FX**: Filtros nativos acelerados por hardware (`feTurbulence`, `feDisplacementMap`, `feDropShadow`) para distorções orgânicas e néon.

---

## 🌐 Internacionalização (i18n)

- **Agente Poliglota**: O agente conduz o briefing interativo e as críticas no idioma nativo do usuário, mantendo os atributos XML e classes em inglês canônico para interoperabilidade global.
- **Tipografia Desacoplada**: Textos nunca são convertidos em curvas vetoriais (`path`). Permanecem como tags semânticas `<text>` na camada `layer-typography`, com suporte nativo a tags multilíngues `<switch>` e `systemLanguage`.

---

## ⚡ Verbos de Refinamento Criativo

Itere sobre os vetores gerados usando comandos expressivos de direção de arte:
- `/svg-maestro brief`: Dispara a entrevista interativa via `ask_question` cobrindo as 4 dimensões canônicas (Superfície/Viewport, Modo, Movimento e Destino), gerando um `BRIEF.md` vinculativo.
- `/svg-maestro bolder`: Intensifica traços, saturação de gradientes e contraste de néon.
- `/svg-maestro quieter`: Suaviza luzes, reduz saturação e refina linhas para um estilo mais discreto.
- `/svg-maestro distill`: Remove elementos decorativos secundários, deixando apenas as linhas geométricas essenciais.
- `/svg-maestro delight`: Adiciona micro-detalhes de movimento (varreduras de radar, anéis orbitais, brilhos de borda).
- `/svg-maestro animate`: Transforma vetores estáticos do Inkscape em ativos animados aplicando o Wrapper Pattern.
- `/svg-maestro critique`: Avaliação em dois eixos cobrindo Padrões Técnicos (Inkscape/linter) e Excelência Estética.

### 📋 Motor de Briefing Interativo (`scripts/briefing.py`)

Gere os prompts de eliciação para o `ask_question` e valide contratos de design vinculativos:

```bash
# Gerar payload localizado para ask_question
python scripts/briefing.py questions --lang pt --json

# Sintetizar documento vinculativo de briefing
python scripts/briefing.py create \
  --name "Moldura Stream" \
  --viewport "webcam_16_9" \
  --mode "experience" \
  --motion "radar_pulse" \
  --handoff "obs_browser_source" \
  --output BRIEF.md \
  --lang pt

# Validar completude do briefing antes de gerar o código SVG
python scripts/briefing.py validate BRIEF.md --json
```

### 🎥 Pipeline de Overlays de Streaming para OBS (`scripts/obs_pipeline.py`)

Gere overlays de streaming modulares com viewport transparente no modo `Experience`:

```bash
# Gerar kit completo de overlays (moldura de webcam 16:9 + banner de alerta)
python scripts/obs_pipeline.py generate-all --output-dir examples/obs/ --theme cyan_magenta

# Gerar moldura de webcam customizada
python scripts/obs_pipeline.py webcam \
  --output examples/obs/webcam_frame_16_9.svg \
  --theme cyan_magenta \
  --cam-label "CAM 01 // AO VIVO" \
  --status-label "REC ● 1080P 60FPS"

# Gerar banner de notificação de alerta customizado
python scripts/obs_pipeline.py alert \
  --output examples/obs/alert_banner.svg \
  --theme cyan_magenta \
  --type "NOVO INSCRITO" \
  --user "CYBER_PHANTOM" \
  --detail "TIER 3 // 12 MESES SEGUIDOS"
```

Temas visuais disponíveis: `cyan_magenta`, `amber_gold`, `matrix_green` e `crimson_hazard`.

### 📊 Pipeline de Widgets de Dashboard e Power BI DAX (`scripts/dashboard_pipeline.py`)

Gere cartões de métricas modulares e densos em dados no modo `Operate`, respeitando proporções áureas ($\phi \approx 1.618$), com indicadores de varredura radar brilhantes, sparklines de tendência, tipografia desacoplada e snippets de medidas DAX codificados em URL para visuais de imagem do Power BI:

```bash
# Gerar kit completo de dashboard (cartão SVG + medida DAX para Power BI)
python scripts/dashboard_pipeline.py generate-all --output-dir examples/dashboard/ --theme dark_slate

# Gerar cartão de telemetria SVG standalone customizado
python scripts/dashboard_pipeline.py card \
  --output examples/dashboard/telemetry_card.svg \
  --theme dark_slate \
  --kpi-value "$1,284,500" \
  --kpi-change "+14.2% ↑" \
  --kpi-label "TOTAL SYSTEM THROUGHPUT"

# Converter qualquer SVG em medida DAX para visual Image URL do Power BI
python scripts/dashboard_pipeline.py dax \
  --input examples/dashboard/telemetry_card.svg \
  --output examples/dashboard/telemetry_card.dax \
  --measure-name TelemetryCard
```

Temas visuais disponíveis: `dark_slate`, `obsidian_amber`, `matrix_emerald` e `deep_violet`.

---

## 🚀 Validação Autônoma em Loop Fechado

O sistema inclui o linter autônomo sem dependências externas (`validate_svg.py`):

```bash
python scripts/validate_svg.py caminho/para/vetor.svg
```

Para consumo automatizado por agentes de IA:

```bash
python scripts/validate_svg.py caminho/para/vetor.svg --json
```

---

## ❓ Preciso ter a skill Impeccable instalada?

**Não! O SVG Maestro é 100% autossuficiente.**

- **Modo Autônomo (Padrão):** Gera todas as proporções matemáticas, geometrias euclidianas e paletas harmônicas (com contraste WCAG AAA) a partir de primeiros princípios.
- **Modo Integrado (Opcional):** Se o seu repositório já contiver `DESIGN.md` ou `PRODUCT.md`, o SVG Maestro herda automaticamente esses tokens para casar com a identidade visual da sua aplicação.

---

## 📦 Instalação e Uso em Agentes de IA

### No Antigravity (Google)
```bash
git clone https://github.com/Tel-BR/svg-maestro.git ~/.gemini/config/skills/svg-maestro
```

### No Claude Code (Anthropic)
```bash
git clone https://github.com/Tel-BR/svg-maestro.git ~/.claude/skills/svg-maestro
```

### No Codex, Cursor ou Outros Ambientes
Aponte o arquivo [`SKILL.md`](SKILL.md) como especificação no prompt de sistema ou habilidades do workspace.

---

## 📂 Estrutura do Repositório

```
svg-maestro/
├── CONTEXT.md                  # Glossário de termos e conceitos de domínio
├── SKILL.md                    # Especificação da Skill para agentes
├── README.md                   # Documentação canônica em inglês
├── README.pt-BR.md             # Documentação localizada em português
├── CONTRIBUTING.md             # Guia de contribuição da comunidade
├── LICENSE                     # Licença MIT permissiva
├── scripts/
│   ├── briefing.py             # Motor de briefing interativo e elicitação
│   ├── dashboard_pipeline.py   # Pipeline de cartões de telemetria e Power BI DAX
│   ├── obs_pipeline.py         # Gerador e pipeline de overlays para OBS
│   └── validate_svg.py         # Linter autônomo zero-dependency em Python
├── examples/
│   ├── dashboard/              # Cartões de métricas prontos e snippet DAX
│   │   ├── telemetry_card.svg
│   │   └── telemetry_card.dax
│   └── obs/                    # Overlays de streaming prontos para produção
│       ├── webcam_frame_16_9.svg
│       └── alert_banner.svg
├── docs/
│   ├── SPEC.md                 # Especificação técnica do sistema
│   ├── tickets/                # Tickets verticais executáveis (ready-for-agent)
│   │   ├── 01-core-linter-test-suite.md
│   │   ├── 02-interactive-briefing-module.md
│   │   ├── 03-obs-streaming-overlays-pipeline.md
│   │   ├── 04-dashboard-widgets-and-powerbi-dax-pipeline.md
│   │   ├── 05-art-direction-refinement-verbs.md
│   │   └── 06-multilingual-typography-and-i18n.md
│   └── adr/                    # Registros de Decisões de Arquitetura (ADRs 0001 - 0008)
└── tests/
    ├── fixtures/               # Fixtures abrangentes para validação de linter
    ├── test_briefing.py        # Suíte de testes do motor de briefing
    ├── test_dashboard_pipeline.py # Suíte de testes do dashboard e pipeline DAX
    ├── test_linter.py          # Suíte de testes do linter
    ├── test_obs_overlays.py    # Suíte de testes dos overlays de OBS
    └── test_card.svg           # Fixture de teste canônica
```

---

## 🙏 Créditos e Reconhecimento

**SVG Maestro** apoia-se no trabalho de pioneiros:
- Inspirado no ecossistema de fluxos de trabalho de **Matt Pocock** (`grilling`, `domain-modeling`, `to-spec`, `to-tickets`, `tdd`).
- Inspirado na skill de design **Impeccable** por sua filosofia radical de direção de arte, modos de superfície e verbos de refinamento criativo.

---

## 📜 Licença

Distribuído sob a **Licença MIT**. Consulte o arquivo [LICENSE](LICENSE) para detalhes. Uso totalmente livre para fins pessoais, acadêmicos e comerciais.
