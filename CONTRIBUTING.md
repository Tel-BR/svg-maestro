# Contribuindo com o SVG Maestro

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

## Protocolo de Release e Bump de Versão (Release & Version Bumping Protocol)

O SVG Maestro utiliza **Versionamento Semântico (`MAJOR.MINOR.PATCH`)** (e.g., `0.1.0-beta.1`). Para garantir a integridade do ecossistema distribuído em múltiplos marketplaces e agentes de IA, todas as versões devem permanecer em estrita sincronia (**Zero-Drift Parity**).

### 1. Arquivos com Versionamento Centralizado
Ao incrementar uma versão (patch, minor ou major), o mantenedor deve atualizar os seguintes arquivos:

1. **`SKILL.md`**: Campo `metadata.version` no frontmatter YAML do cabeçalho.
2. **`skills/ask-maestro/SKILL.md`**: Campo `metadata.version` no frontmatter YAML.
3. **`.claude-plugin/plugin.json`**: Campo `"version"`.
4. **`plugin.json`**: Campo `"version"` (deve permanecer 100% idêntico a `.claude-plugin/plugin.json`).
5. **`skills.json`**:
   - Campo raiz `"version"`.
   - Campo `"version"` em cada entrada do array `"skills"` (`svg-maestro`, `ask-maestro`, etc.).
6. **`scripts/update_notifier.py`**: Constante `DEFAULT_VERSION`.
7. **`README.md` e `README.pt-BR.md`**: Badges de status no topo dos documentos (`[![Status: ...](...)]`).

### 2. Validação Obrigatória Pré-Release
Antes de submeter o commit de release, execute a suíte de testes de manifestos para comprovar que não há divergência de versão (*version drift*) nem quebra de schema:

```bash
# Validar conformidade de schemas e paridade de versão em todos os manifestos
pytest tests/test_distribution_manifests.py -v

# Executar a suíte de testes completa do repositório (170+ testes)
pytest
```

Nenhum release deve ser publicado se algum teste de paridade ou retrocompatibilidade falhar.

### 3. Publicação e Tagging no Git
Após a validação bem-sucedida de todos os testes:

```bash
# 1. Comitar as alterações sincronizadas
git add SKILL.md skills/ask-maestro/SKILL.md .claude-plugin/plugin.json plugin.json skills.json scripts/update_notifier.py README.md README.pt-BR.md
git commit -m "chore(release): bump version to v0.X.Y"

# 2. Criar a tag semântica anotada correspondente
git tag -a v0.X.Y -m "Release v0.X.Y"

# 3. Enviar branches e tags para o repositório remoto
git push origin main --tags
```

### 4. Publicação da Release no GitHub
1. Acesse [Releases no GitHub](https://github.com/Tel-BR/svg-maestro/releases) e clique em **Draft a new release**.
2. Selecione a tag recém-criada (`v0.X.Y`).
3. Documente o changelog com foco em:
   - Novos verbos de refinamento ou pipelines.
   - Melhorias de compatibilidade e camadas do Inkscape.
   - Novas regras do linter ou dicas de upgrade (`UPGRADE_*`).
   - Breaking changes (se houver, com guia de migração).

---

## Código de Conduta

Seja respeitoso, construtivo e colaborativo em todas as interações.
