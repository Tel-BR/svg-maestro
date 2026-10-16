# Contribuindo com o SVG Maestro 🎨🤝

Obrigado pelo interesse em contribuir com o **SVG Maestro**! Este projeto é de código aberto e tem como objetivo fornecer aos agentes de IA a melhor infraestrutura para gerar vetores geométricos, acessíveis e editáveis no Inkscape.

## Diretrizes de Contribuição

1. **Zero-Bias Policy**:
   - Não adicione templates visuais estáticos ou clipart pronto na documentação da skill (`SKILL.md`). Mantemos o repositório focado em regras matemáticas, semântica de camadas e lógica de animação para não enviesar a criatividade dos modelos de IA.
2. **Compatibilidade Inkscape e Wrapper Pattern**:
   - Qualquer nova técnica de animação ou filtro vetorial proposto deve respeitar o **Wrapper Pattern** (`<g class="anim-wrapper-...">` envolvendo o conteúdo estático `<g inkscape:label="...">`) para que o arquivo continue 100% manipulável no Inkscape sem quebrar as animações no navegador.
3. **Validador Sem Dependências Externas**:
   - O linter `validate_svg.py` deve permanecer estritamente baseado na biblioteca padrão do Python (`xml.etree.ElementTree`, `re`, `argparse`, `sys`, `json`). Não introduza dependências de `pip` que possam quebrar a execução em ambientes isolados de agentes de IA.
4. **Testes e Fixtures**:
   - Sempre que adicionar uma nova regra ou suporte a uma tag SVG, adicione a fixture correspondente na suíte de testes.

## Como Enviar Modificações

1. Faça um Fork do repositório.
2. Crie uma branch para sua modificação: `git checkout -b feature/minha-melhoria`.
3. Valide o SVG e rode o linter: `python scripts/validate_svg.py tests/test_card.svg`.
4. Envie suas alterações via Pull Request detalhando o impacto no Inkscape e nos navegadores.

## Código de Conduta

Seja respeitoso, construtivo e colaborativo em todas as interações.
