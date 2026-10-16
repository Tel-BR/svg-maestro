# SVG Maestro

[English](README.md) | **Português (Brasil)**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](.github/workflows/ci.yml)
[![Inkscape: Compatível com Camadas](https://img.shields.io/badge/Inkscape-Camadas%20Compat%C3%ADveis-brightgreen.svg)](docs/SPEC.md)
[![Status: Beta v0.1.0-beta.1](https://img.shields.io/badge/status-v0.1.0--beta.1-orange.svg)](https://github.com/Tel-BR/svg-maestro/releases)

**SVG Maestro** é um sistema de design e orquestração de movimento vetorial para agentes de IA de programação (Antigravity, Claude Code, Codex, Cursor). Ele une disciplina arquitetural (briefing estruturado, fatiamento vertical em tickets, validação autônoma) com direção de arte expressiva (modos de superfície, verbos de refinamento não-destrutivos, tipografia desacoplada) para produzir layouts matemáticos em SVG, cartões de telemetria para dashboards e overlays para streaming no OBS Studio estruturados para o Inkscape.

---

## Início Rápido

Gere, valide e refine um cartão de telemetria em três comandos:

```bash
# 1. Gerar um cartão de telemetria no modo Operate
python scripts/dashboard_pipeline.py card \
  --output card.svg \
  --theme dark_slate \
  --kpi-value "$1,284,500" \
  --kpi-label "FLUXO DO SISTEMA"

# 2. Validar integridade estrutural e conformidade com o Inkscape
python scripts/validate_svg.py card.svg

# 3. Aplicar refinamento criativo não-destrutivo (grava em card_bolder.svg)
python scripts/refinement_verbs.py bolder --input card.svg
```

---

## Instalação e Uso em Agentes

### Antigravity (Google)
```bash
git clone https://github.com/Tel-BR/svg-maestro.git ~/.gemini/config/skills/svg-maestro
```

### Claude Code (Anthropic)
```bash
git clone https://github.com/Tel-BR/svg-maestro.git ~/.claude/skills/svg-maestro
```

### Codex, Cursor ou Agentes Customizados
Referencie [`SKILL.md`](SKILL.md) diretamente no prompt de sistema do seu agente ou conjunto de skills do workspace.

---

## Status do Projeto e Limites Conhecidos

> [!NOTE]
> O SVG Maestro está atualmente em fase **Beta (`v0.1.0-beta.1`)**. Contratos centrais e regras de validação estão ativos, mas parâmetros de linha de comando e limiares heurísticos estão sujeitos a ajustes com base no feedback da comunidade.

- **Avaliação de Contraste**: A crítica de paleta verifica a separação tonal entre chassis escuros e acentos luminosos usando limiares perceptuais HLS. Ela não calcula a razão euclidiana de luminância relativa por caractere de texto ($L_1 / L_2 \ge 7:1$). Os temas de alto contraste fornecidos servem como base inicial.
- **Saída DAX para Power BI**: O gerador DAX formata o SVG como uma Data URI padrão (`data:image/svg+xml;utf8,...`), escapando códigos hexadecimais `#` para `%23` e aspas duplas para `""`. Não se trata de uma codificação de URI RFC 3986 completa. Recomenda-se validar no visual de imagem do Power BI Desktop em seu ambiente.
- **Namespaces do Inkscape**: A hierarquia de camadas (`inkscape:groupmode="layer"`) e IDs da tag `<defs>` são otimizados especificamente para o Inkscape. Outros aplicativos vetoriais (Illustrator, Figma) importam esses grupos como nós `<g>` convencionais sem metadados nativos de camada.
- **Portabilidade de Animação**: Animações CSS embutidas declaram estritamente `transform-box: fill-box` e `transform-origin: center` para renderização estável em navegadores e no OBS Studio. Visualizadores de imagem rasterizada ou renderizadores de markdown simplificados que desabilitam CSS exibirão o SVG de forma estática em seu estado base.

---

## Capacidades Centrais

### 1. Geometria Matemática e Modos de Superfície
Todos os vetores são construídos com princípios geométricos (sequências de Fibonacci, Proporção Áurea $\phi \approx 1.618$, projeções isométricas), sem uso de clipart externo:
- **`Operate`**: Alta densidade de dados e legibilidade técnica para telemetria web e cartões do Power BI.
- **`Experience`**: Alto contraste e animações fluidas em CSS keyframes para overlays no OBS Studio.
- **`Persuade`**: Proporções euclidianas imponentes para identidade de marca e artes hero.

### 2. Compatibilidade com Inkscape e o Wrapper Pattern
- **Camadas Semânticas**: Grupos de elementos organizados em camadas nativas (`Background`, `Geometric Structure`, `Accents & Lighting`, `Typography & Labels`).
- **Higiene de `<defs>`**: IDs expressivos e humanos (`id="grad-neon-cyan"`, `id="filter-cyber-glow"`), sem hashes aleatórios opacos.
- **Wrapper Pattern**: Regras de animação visam exclusivamente grupos `<g class="anim-wrapper-...">`, protegendo a geometria estática contra conflitos de transformação durante edições manuais no Inkscape.

### 3. Verbos de Refinamento Não-Destrutivos (`scripts/refinement_verbs.py`)
Direcione vetores existentes com comandos expressivos de design sem manipulação manual de coordenadas:
- **`bolder`**: Aumenta espessura de traços (1.4x-1.8x), saturação de gradientes e intensidade de brilho.
- **`quieter`**: Desatura cores, suaviza iluminação e reduz espessura de linhas (0.6x-0.75x).
- **`distill`**: Remove detalhes decorativos secundários preservando hierarquia geométrica e métricas.
- **`delight`**: Adiciona micro-movimentos sutis (varreduras de radar, anéis orbitais) encapsulados em Wrappers.
- **`animate`**: Converte SVGs estáticos em ativos animados envolvendo elementos centrais em grupos de animação e injetando regras CSS `@keyframes`.
- **`critique`**: Emite relatório estruturado em dois eixos avaliando Padrões Técnicos (linter, camadas, higiene de defs) e Excelência Estética (proporções, harmonia de cores, desacoplamento tipográfico).

```bash
# Não-destrutivo por padrão: cria card_bolder.svg
python scripts/refinement_verbs.py bolder --input card.svg

# Especificar arquivo de saída customizado
python scripts/refinement_verbs.py quieter --input card.svg --output card_minimal.svg

# Sobrescrita in-place explícita
python scripts/refinement_verbs.py distill --input card.svg --in-place

# Executar crítica de design em dois eixos
python scripts/refinement_verbs.py critique --input card.svg
python scripts/refinement_verbs.py critique --input card.svg --json
```

### 4. Motor de Briefing Interativo (`scripts/briefing.py`)
Conduz eliciação estruturada cobrindo as 4 dimensões canônicas (Superfície/Viewport, Modo, Movimento e Destino), gerando um `BRIEF.md` vinculativo:

```bash
# Gerar payload localizado para questionário
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

# Validar completude do briefing antes de gerar código
python scripts/briefing.py validate BRIEF.md --json
```

### 5. Tipografia Multilíngue e Suporte a `<switch>`
O SVG Maestro desacopla textos da geometria, mantendo rótulos como nós `<text>` semânticos em camada dedicada:
- **Sem Caminhos Contornados**: O texto permanece editável na ferramenta de texto do Inkscape. Traçados vetoriais em camadas de tipografia geram aviso `OUTLINED_TEXT_WARNING`.
- **Contrato de `<switch>`**: Idiomas específicos (`systemLanguage="pt"`, `systemLanguage="es"`) antecedem o elemento final de fallback em inglês.
- **Exemplo de Referência**: Veja `examples/i18n/multilingual_card.svg`.

### 6. Roteador Navegador: `/ask-maestro`
Inspirado diretamente na metodologia `/ask-matt` de Matt Pocock, o `/ask-maestro` atua como bússola operacional para usuários e agentes de IA:
- **Fluxo Principal (Main Flow)**: Rota determinística da entrevista estruturada (`/svg-maestro brief` $\to$ `BRIEF.md`) à construção em 3 pilares, validação em ciclo fechado com linter (`validate_svg.py`), verbos de direção de arte e entrega.
- **Vias de Acesso (On-Ramps)**: Portas de entrada dedicadas para reparos em SVGs existentes (como `transform-box` ausente), importações externas (Figma/Inkscape), pacotes multi-asset (fatiamento em tickets tracer-bullet) e visualizações DAX para Power BI.
- **Higiene de Contexto**: Protege a **Smart Zone** do modelo (~150k tokens), exigindo contextos limpos por componente ao gerar marcações XML ricas em coordenadas.
- **Interação Poliglota**: Conduz briefings, diagnósticos e triagens no idioma nativo do usuário (como o Português), mantendo todo código XML e atributos em inglês canônico.

---

## Pipelines

### Overlays de Streaming para OBS (`scripts/obs_pipeline.py`)
Gera overlays com viewport transparente no modo `Experience`:

```bash
# Gerar kit completo de streaming (webcam 16:9 + banner de alertas)
python scripts/obs_pipeline.py generate-all --output-dir examples/obs/ --theme cyan_magenta

# Gerar moldura de webcam customizada
python scripts/obs_pipeline.py webcam \
  --output examples/obs/webcam_frame_16_9.svg \
  --theme cyan_magenta \
  --cam-label "CAM 01 // AO VIVO" \
  --status-label "REC ● 1080P"

# Gerar banner de alertas customizado
python scripts/obs_pipeline.py alert \
  --output examples/obs/alert_banner.svg \
  --theme cyan_magenta \
  --type "NOVO INSCRITO" \
  --user "CYBER_PHANTOM"
```

Temas disponíveis: `cyan_magenta`, `amber_gold`, `matrix_green`, `crimson_hazard`.

### Widgets de Dashboard e DAX para Power BI (`scripts/dashboard_pipeline.py`)
Gera cartões de telemetria no modo `Operate` e converte em medidas DAX para visuais de imagem do Power BI:

```bash
# Gerar kit de dashboard completo (SVG + medida DAX)
python scripts/dashboard_pipeline.py generate-all --output-dir examples/dashboard/ --theme dark_slate

# Converter qualquer SVG em medida DAX para Power BI
python scripts/dashboard_pipeline.py dax \
  --input examples/dashboard/telemetry_card.svg \
  --output examples/dashboard/telemetry_card.dax \
  --measure-name TelemetriaCard
```

Temas disponíveis: `dark_slate`, `obsidian_amber`, `matrix_emerald`, `deep_violet`.

---

## Validação Autônoma em Ciclo Fechado

O SVG Maestro inclui um linter de validação com zero dependências externas (`validate_svg.py`):

```bash
python scripts/validate_svg.py caminho/do/vetor.svg
```

Para consumo programático por agentes de IA:

```bash
python scripts/validate_svg.py caminho/do/vetor.svg --json
```

---

## Estrutura do Repositório

```
svg-maestro/
├── .github/workflows/ci.yml    # Workflow de integração contínua (CI)
├── CONTEXT.md                  # Glossário formal de domínio
├── SKILL.md                    # Especificação da skill para agentes
├── README.md                   # Documentação canônica em inglês
├── README.pt-BR.md             # Documentação localizada em português
├── CONTRIBUTING.md             # Guia de contribuição da comunidade
├── LICENSE                     # Licença permissiva MIT
├── scripts/
│   ├── briefing.py             # Motor de briefing interativo e eliciação
│   ├── dashboard_pipeline.py   # Cartões de telemetria e pipeline DAX
│   ├── obs_pipeline.py         # Gerador de overlays para OBS Studio
│   ├── refinement_verbs.py     # Verbos de refinamento e motor de crítica
│   └── validate_svg.py         # Linter de validação vetorial em Python puro
├── examples/
│   ├── dashboard/              # Cartões de telemetria e trecho DAX
│   │   ├── telemetry_card.svg
│   │   └── telemetry_card.dax
│   ├── i18n/                   # Ativos multilíngues (<switch> + systemLanguage)
│   │   └── multilingual_card.svg
│   └── obs/                    # Overlays para streaming
│       ├── webcam_frame_16_9.svg
│       └── alert_banner.svg
├── templates/
│   └── BRIEF.template.md       # Modelo canônico de briefing
├── docs/
│   ├── SPEC.md                 # Especificação do sistema
│   ├── tickets/                # Tickets executáveis (01 - 06)
│   └── adr/                    # Registros de decisões de arquitetura (ADRs 0001 - 0008)
└── tests/
    ├── fixtures/               # Matriz de fixtures para validação
    ├── test_briefing.py        # Suite de testes do motor de briefing
    ├── test_dashboard_pipeline.py # Suite de testes do pipeline de dashboards e DAX
    ├── test_i18n.py            # Suite de testes de tipografia e i18n
    ├── test_linter.py          # Suite de testes do linter central
    ├── test_obs_overlays.py    # Suite de testes de overlays do OBS
    ├── test_refinement_verbs.py # Suite de testes de verbos e crítica
    └── test_card.svg           # Fixture canônica de cartão
```

---

## Créditos e Agradecimentos

- Inspirado no ecossistema de engenharia com agentes de **Matt Pocock** (`grilling`, `domain-modeling`, `to-spec`, `to-tickets`, `tdd`).
- Inspirado na skill **Impeccable** por sua filosofia de modos de superfície e verbos de refinamento criativo.

---

## Licença

Distribuído sob a **Licença MIT**. Veja [LICENSE](LICENSE) para mais detalhes.
