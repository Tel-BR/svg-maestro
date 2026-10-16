# SVG Maestro 🎨✨

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](scripts/validate_svg.py)
[![Inkscape: Fully Compatible](https://img.shields.io/badge/Inkscape-Compatible-brightgreen.svg)](docs/SPEC.md)

**SVG Maestro** é uma solução e skill reutilizável de código aberto projetada para agentes de inteligência artificial (Antigravity, Claude, Codex) para concepção e engenharia de layouts, widgets de dashboards, overlays para streaming (OBS Studio) e ilustrações vetoriais geométricas avançadas em formato `.svg`, unindo direção de arte matemática, animação nativa e compatibilidade total com o Inkscape.

---

## 🏛️ Os Três Pilares Fundamentais

1. **Direção de Arte & Geometria Matemática (Dual-Engine)**:
   - **Zero-Bias Policy**: Sem blueprints ou clipart fixos que enviesem a criatividade do modelo. A arte é gerada do zero a partir de princípios matemáticos puros (Proporção Áurea $\phi \approx 1.618$, sequências de Fibonacci, malhas isométricas de $30^\circ$ e tangências euclidianas).
   - **Impeccable Bridge**: Herda automaticamente tokens de cores, tipografia e diretrizes de design do `DESIGN.md` ou `PRODUCT.md` gerados pela skill `impeccable` quando presentes no projeto.
2. **Compatibilidade Total com Inkscape**:
   - Declaração estrita de namespaces (`xmlns:inkscape`, `xmlns:sodipodi`).
   - Camadas semânticas nativas do Inkscape (`inkscape:groupmode="layer"` e `inkscape:label`).
   - Higiene estrita de `<defs>` com gradientes e filtros bem nomeados.
3. **Animação Vetorial Nativa e à Prova de Mutação (Wrapper Pattern)**:
   - **Wrapper Pattern**: Isola elementos animados em grupos dedicados (`<g class="anim-wrapper-...">`) separados dos grupos de geometria estática editados no Inkscape (`<g inkscape:label="...">`). Isso garante que edições humanas no Inkscape nunca quebrem ou sobrescrevam as animações.
   - **Tier 1 (Universal CSS)**: `@keyframes` puramente declarativos embutidos na tag `<style>` do próprio SVG, com uso obrigatório de `transform-box: fill-box` e `transform-origin: center`. Roda em navegadores, OBS Studio, Power BI e tags `<img>`.
   - **Tier 2 (SMIL Vector Motion)**: Animações de morphing de caminhos vetoriais (`attributeName="d"`) e trajetórias com `<animateMotion>`.
   - **Vector Filter FX**: Filtros nativos (`feTurbulence`, `feDisplacementMap`, `feDropShadow`) para efeitos de néon, líquidos ou aberração cibernética.

---

## 🚀 Loop Autônomo de Validação (Linter Python)

O sistema inclui um validador autônomo sem dependências externas (`validate_svg.py`, baseado apenas na biblioteca padrão do Python):

```bash
python scripts/validate_svg.py caminho/para/arquivo.svg
```

Para inspeção automatizada por agentes em formato JSON:

```bash
python scripts/validate_svg.py caminho/para/arquivo.svg --json
```

---

## 📦 Como Instalar e Usar em Qualquer Agente de IA

### No Antigravity (Google)
Clone ou copie a pasta da skill para o seu diretório global de skills:
```bash
git clone https://github.com/Tel-BR/svg-maestro.git ~/.gemini/config/skills/svg-maestro
```

### No Claude Code (Anthropic)
Clone para o diretório de skills do Claude:
```bash
git clone https://github.com/Tel-BR/svg-maestro.git ~/.claude/skills/svg-maestro
```

### No Codex, Cursor ou Outros Ambientes
Basta apontar o arquivo [`SKILL.md`](SKILL.md) como especificação para o agente ou adicionar suas instruções de arquitetura vetorial ao contexto da IA.

---

## 📂 Estrutura do Repositório

```
svg-maestro/
├── CONTEXT.md                  # Glossário formal de termos e conceitos de domínio
├── SKILL.md                    # Especificação da Skill interoperável para IAs
├── README.md                   # Documentação geral e guia rápido
├── CONTRIBUTING.md             # Guia de contribuição da comunidade
├── LICENSE                     # Licença MIT permissiva e livre
├── scripts/
│   └── validate_svg.py         # Linter autônomo zero-dependency (Inkscape + CSS + Wrapper)
├── docs/
│   ├── SPEC.md                 # Especificação técnica completa do sistema
│   ├── tickets/                # Tickets verticais executáveis (ready-for-agent)
│   │   ├── 01-core-linter-test-suite.md
│   │   ├── 02-obs-streaming-overlays-pipeline.md
│   │   ├── 03-dashboard-widgets-and-powerbi-dax-pipeline.md
│   │   └── 04-impeccable-bridge-design-tokens.md
│   └── adr/                    # Registros de Decisões de Arquitetura (ADRs)
│       ├── 0001-skill-packaging-and-validation-linter.md
│       ├── 0002-wrapper-pattern-for-animation-isolation.md
│       ├── 0003-modular-viewports-over-monolithic-scenes.md
│       ├── 0004-dual-engine-aesthetics-and-impeccable-bridge.md
│       ├── 0005-autonomous-closed-loop-linter-validation.md
│       ├── 0006-zero-visual-blueprints-anti-bias-policy.md
│       └── 0007-zero-dependency-python-linter.md
└── tests/
    └── test_card.svg           # Arquivo SVG de teste canônico validado com sucesso
```

---

## 🙏 Inspiração e Reconhecimento (Credits & Acknowledgments)

O **SVG Maestro** foi concebido e enriquecido a partir dos princípios estéticos de excelência em design estabelecidos pelo ecossistema da skill **Impeccable** (`impeccable`). Estendemos essa filosofia de alta direção de arte (*"out-of-distribution craft"* sem clichês genéricos de IA) para a engenharia vetorial matemática do SVG e do Inkscape.

---

## 📜 Licença

Distribuído sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. O uso é totalmente livre para fins pessoais, acadêmicos ou comerciais.
