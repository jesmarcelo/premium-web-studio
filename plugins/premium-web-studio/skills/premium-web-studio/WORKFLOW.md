# Workflow detalhado

Cada fase tem **objetivo**, **ações**, **saída** e **critério de saída**. Não avance enquanto o critério de saída não for atendido. Fases podem ser encurtadas conforme o modo de trabalho (ver SKILL.md), mas nunca puladas silenciosamente — diga ao usuário quais fases serão abreviadas e por quê.

Use uma lista de tarefas (todo list) para acompanhar as fases em projetos completos.

---

## Fase 1 — Discovery

**Objetivo:** entender projeto, nicho, objetivos, público, conteúdo, funcionalidades, stack e restrições.

**Ações:**
1. Leia o pedido e o que já existe (mensagem, arquivos, repositório) para não perguntar o que já foi respondido.
2. Classifique o modo de trabalho (projeto completo, evolução, melhoria focada).
3. Faça as perguntas em **no máximo 2 rodadas**, em blocos agrupados (ver [DISCOVERY.md](DISCOVERY.md)). Prefira a ferramenta de perguntas estruturadas (AskUserQuestion) quando disponível, com opções concretas e recomendação marcada.
4. Se o usuário não souber a stack, apresente opções com trade-offs ([references/stack-options.md](references/stack-options.md)).
5. Consolide o briefing e apresente-o de forma resumida.

**Saída:** `docs/website/briefing.md` (modelo em [references/templates.md](references/templates.md)).

**Critério de saída (G1):** usuário confirmou briefing, stack e escopo. Suposições restantes estão listadas.

---

## Fase 2 — Repository Audit

**Objetivo:** compreender o código existente antes de qualquer edição. Pule apenas se o projeto for realmente do zero (diretório vazio ou sem código de site).

**Ações:** siga [REPOSITORY-AUDIT.md](REPOSITORY-AUDIT.md). O script `scripts/audit-repo.sh` gera um panorama inicial.

**Saída:** resumo da auditoria (stack, versões, convenções, design system, problemas encontrados, o que preservar) apresentado ao usuário e anexado ao briefing.

**Critério de saída:** você sabe como o projeto roda, builda e é organizado; conhece os componentes e tokens existentes; conseguiu rodar o build ou registrou por que não conseguiu.

---

## Fase 3 — Research

**Objetivo:** estudar referências reais e concorrentes do nicho.

**Se o usuário já forneceu site(s) de referência:** não use nem configure o Firecrawl e não busque outras referências; colete e analise apenas os sites fornecidos conforme [FIRECRAWL-RESEARCH.md](FIRECRAWL-RESEARCH.md#0-referências-fornecidas-pelo-usuário) e siga para a fase 4.

**Ações (sem referências fornecidas):**
1. Verifique a disponibilidade do Firecrawl ([FIRECRAWL-RESEARCH.md](FIRECRAWL-RESEARCH.md#1-verificar-disponibilidade)).
2. Se não estiver disponível, siga o fluxo de configuração e **aguarde**. Só ofereça seguir sem pesquisa se o usuário recusar explicitamente configurar — e registre isso como limitação.
3. Inclua as referências fornecidas pelo usuário.
4. Selecione 5–10 referências variadas (líderes, concorrentes, boa reputação visual, premiadas quando relevante).
5. Colete estrutura, conteúdo e, quando possível, screenshots.

**Quando pular:** melhorias focadas sem decisão visual (ex.: corrigir meta tags, otimizar imagens). Diga explicitamente que a pesquisa foi dispensada e por quê.

**Saída:** lista de referências com URL, motivo da escolha e dados coletados.

**Critério de saída:** referências suficientes e variadas para identificar padrões do nicho.

---

## Fase 4 — Reference Analysis

**Objetivo:** transformar referências em princípios reutilizáveis, sem copiar.

**Ações:**
1. Analise cada referência com a matriz de [FIRECRAWL-RESEARCH.md](FIRECRAWL-RESEARCH.md#5-análise-das-referências).
2. Dê nota a todas as referências em todos os critérios e monte o ranking ([seção 5.1](FIRECRAWL-RESEARCH.md#51-avaliação-e-ranking)).
3. Apresente as **3 melhores com nota, URL, pontos fortes e fracos** (ou, com uma única referência fornecida pelo usuário, sua análise para confirmação) e peça que o usuário escolha a referência principal ([seção 5.2](FIRECRAWL-RESEARCH.md#52-apresentar-as-3-melhores-e-pedir-a-escolha-gate-g2)). Aguarde a escolha.
4. Com a escolha feita, produza a síntese: padrões **do nicho** (convenções que o público espera), **diferenciais** (o que as melhores fazem melhor) e **armadilhas** (o que evitar).

**Saída:** `docs/website/research.md` com tabela de notas, top 3, referência principal escolhida, síntese de padrões e oportunidades de diferenciação.

**Critério de saída (G2):** usuário escolheu a referência principal (ou pediu nova pesquisa, que reinicia esta fase), e a síntese foi apresentada antes da direção visual.

---

## Fase 5 — Design Direction

**Objetivo:** definir uma direção visual original, premium e coerente com o nicho.

**Ações:** siga [DESIGN.md](DESIGN.md). Defina conceito, estilo, hierarquia, tipografia, cores, grid, espaçamento, linguagem visual, imagens e nível de motion. Justifique cada decisão pelo contexto (público, objetivo, marca, pesquisa). Use a referência principal escolhida no G2 como padrão de qualidade e direção, sem copiá-la. Quando útil, ofereça 2 direções contrastantes para o usuário escolher.

**Saída:** `docs/website/design-direction.md` com tokens iniciais (cores, tipografia, espaçamento, raios, sombras, motion).

**Critério de saída (G3):** usuário aprovou a direção. Em melhorias focadas sem impacto visual, esta fase se reduz a "seguir o design system existente".

---

## Fase 6 — Architecture

**Objetivo:** planejar a estrutura técnica.

**Ações:** siga [ENGINEERING.md](ENGINEERING.md#arquitetura). Defina páginas, rotas, mapa de componentes, fonte e formato dos dados/conteúdo, estados, integrações, assets, estrutura de pastas, estratégia de SEO e de testes, e a ordem de implementação em etapas.

**Saída:** `docs/website/architecture.md`.

**Critério de saída (G4, quando aplicável):** aprovação do usuário para mudanças estruturais, novas dependências relevantes ou reescritas.

---

## Fase 7 — Implementation

**Objetivo:** construir em pequenas etapas, mantendo o projeto funcional.

**Ações:**
1. Comece pela fundação: tokens, estilos globais, tipografia, layout base, navegação e rodapé.
2. Depois componentes reutilizáveis, depois páginas/seções na ordem de prioridade do negócio.
3. Ao fim de cada etapa: rode build/lint/tipos e confira visualmente quando possível.
4. Corrija erros encontrados no caminho, inclusive os que você mesmo introduziu.
5. Não deixe código morto, `console.log` de depuração, TODOs sem registro ou componentes duplicados.
6. Configure minificação no build e gere a configuração de compressão e cache da hospedagem (ex.: `.htaccess` em Apache/LiteSpeed) conforme [references/server-config.md](references/server-config.md), dentro da pasta que o build copia (ex.: `public/.htaccess`), e confirme que ele aparece na saída do build. Imagens com `srcset`/`sizes` desde o primeiro componente, e JS sem reflow forçado ([SEO-PERFORMANCE.md](SEO-PERFORMANCE.md#reflow-forçado-layout-thrashing)).
7. Se o usuário usa git, sugira commits por etapa; só faça commit se ele pedir.

**Critério de saída:** escopo implementado, build passando.

---

## Fase 8 — QA

**Objetivo:** validar tecnicamente.

**Ações:** execute [QA-CHECKLIST.md](QA-CHECKLIST.md) seções técnicas, com apoio de [ACCESSIBILITY.md](ACCESSIBILITY.md) e [SEO-PERFORMANCE.md](SEO-PERFORMANCE.md). Rode as ferramentas disponíveis (build, lint, typecheck, testes, Lighthouse, axe). Registre o resultado real de cada verificação.

**Saída:** `docs/website/qa-report.md`.

---

## Fase 9 — Visual Review

**Objetivo:** olhar o resultado como um diretor de arte exigente.

**Ações:** capture e inspecione as páginas em 375, 768, 1024, 1440 e 1920 px (seção "Revisão visual" de [QA-CHECKLIST.md](QA-CHECKLIST.md)). Use a ferramenta de navegador disponível (Playwright MCP, Claude in Chrome, `npx playwright screenshot`). Se nenhuma estiver disponível, diga isso e peça ao usuário screenshots ou uma revisão manual guiada.

**Saída:** lista priorizada de problemas visuais.

---

## Fase 10 — Refinement

**Objetivo:** corrigir os problemas das fases 8 e 9.

**Ações:** corrija por prioridade (bloqueadores → acessibilidade → quebras de layout → hierarquia/estética → polimento). Revalide o que foi alterado. Repita 8–10 até não restarem problemas bloqueadores ou até o limite combinado com o usuário.

---

## Fase 11 — Delivery

**Objetivo:** entregar um resumo objetivo e honesto.

**Saída:** relatório no formato de [references/templates.md](references/templates.md#relatório-de-entrega): o que foi feito, decisões importantes, arquivos principais, testes realizados (e não realizados), pendências, placeholders de conteúdo e sugestões futuras.
