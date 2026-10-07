# Revisão visual com críticos independentes

Quem construiu o site não consegue julgá-lo com isenção: conhece o código, lembra o que tentou fazer e tende a enxergar a intenção em vez do resultado. Nesta fase, o resultado renderizado é julgado por **três críticos com contexto novo**, cada um contra um único documento, com veredito binário. O ciclo só termina quando os três aprovam todas as partes ou quando o usuário o interrompe.

Entradas: `docs/website/briefing.md`, `docs/website/design-direction.md` (tokens), a barra de qualidade em `docs/website/research.md` ([FIRECRAWL-RESEARCH.md](FIRECRAWL-RESEARCH.md#54-barra-de-qualidade-mecanismos-observáveis)) e a referência principal escolhida no G2.

Antes da primeira rodada, informe ao usuário que o ciclo segue até a aprovação, que cada rodada abre três subagentes e novas capturas, e que ele pode interromper ou definir um teto de rodadas.

---

## 1. Pré-verificação

É uma checagem, não outra entrevista. Confirme e relate em um bloco:

- **Referência acessível agora:** abra a referência principal e capture as mesmas páginas e viewports que serão julgadas. Se estiver inacessível, avise e combine outra; nunca substitua a referência pela memória dela.
- **Renderização do resultado:** confirme que consegue capturar o site (build de produção ou `preview`) com a ferramenta de navegador disponível ([QA-CHECKLIST.md](QA-CHECKLIST.md#8-revisão-visual-fase-9)).
- **Subagentes com contexto novo:** confirme que o ambiente permite abrir agentes que não herdam a conversa (no Claude Code, a ferramenta de subagentes sem fork da sessão).
- **Documentos de cada crítico:** briefing, direção visual com tokens e barra de qualidade existem e estão aprovados.

Diga o que funciona, o que falta e **qual crítico fica sem condições de julgar**. Sem capturas da referência, o crítico visual está cego; sem tokens, o crítico de sistema; sem subagentes, nenhum dos três é independente. Nunca prossiga em silêncio com um crítico cego e nunca substitua os críticos por três autoavaliações: registre a limitação, informe o usuário e ofereça a alternativa possível (ele fornecer capturas, revisar manualmente ou aceitar a limitação, registrada como decisão dele).

## 2. Partes julgáveis

Divida o resultado nas menores partes que possam ser melhoradas e julgadas por conta própria, por exemplo: primeira tela da home (desktop e mobile), home completa, uma página interna representativa, formulário principal com seus estados. Prefira **três ou quatro partes**; cada parte a mais multiplica capturas e julgamentos.

## 3. Evidências

Os críticos julgam o que veem, então a evidência precisa mostrar o comportamento relevante.

- Capture resultado e referência **nas mesmas larguras e nos mesmos estados** (primeira tela com primeira tela, menu aberto com menu aberto). Use as larguras do briefing e, no mínimo, uma mobile e uma desktop.
- **Elementos fixos, sticky, canvas ou vídeo** costumam sair errados na captura de página inteira. Nesses casos, capture por viewport, rolando a página, e confira se cada captura corresponde ao que aparece no navegador. Falha de captura não é defeito do produto: corrija a captura antes do julgamento.
- **Movimento (nível 2 ou 3 de motion):** uma tela parada não mostra a transição. Percorra a rolagem com capturas sequenciais por viewport ou grave a sessão e gere uma tira de frames, se `ffmpeg` estiver disponível:

  ```bash
  ffmpeg -i tmp/review/scroll.webm -vf "fps=4,scale=480:-1,tile=6x4" -frames:v 1 tmp/review/rodada-1/parte-2/frames-A.png
  ```

- **Pasta de avaliação por rodada e parte**, por exemplo `tmp/review/rodada-1/parte-1/`. Para o crítico visual, nomeie as capturas com rótulos neutros (`A-1440.png`, `B-1440.png`) e sorteie qual lado é o nosso a cada rodada. O mapa A/B fica **fora** da pasta de avaliação (ex.: `tmp/review/mapa.md`) e nunca é passado ao crítico.

## 4. Os três críticos

| Crítico | Recebe | Julga somente | Ignora |
|---|---|---|---|
| **Briefing** | `briefing.md` + capturas do resultado | Faz o que foi pedido? Público, objetivo, CTA, páginas e conteúdo exigidos estão presentes e funcionam na tela | estética |
| **Sistema** | tokens e regras de `design-direction.md` + capturas do resultado | Aderência objetiva ao sistema: escala tipográfica, cores, espaçamentos, raios, estados, consistência entre páginas | se ficou bonito |
| **Visual** | barra de qualidade + pares A/B às cegas | Qual lado é melhor em cada mecanismo da barra e no conjunto; a maior lacuna do lado pior | se cumpre o briefing |

Escreva as instruções de cada crítico **para este projeto**, a partir do modelo em [references/templates.md](references/templates.md#instruções-dos-críticos). Não reutilize instruções genéricas entre projetos.

### Dois ajustes obrigatórios no crítico visual

- **Originalidade:** além de comparar a qualidade, o crítico responde se um lado parece cópia do outro (layout distintivo, composição característica, identidade). Resultado reconhecível como cópia da referência é **REPROVADO**, mesmo que vença a comparação ([FIRECRAWL-RESEARCH.md](FIRECRAWL-RESEARCH.md#6-regras-de-não-cópia)).
- **Placeholders:** a referência tem fotografia e textos reais; o nosso site pode ter placeholders identificados. O crítico julga composição, hierarquia, ritmo, tipografia e acabamento, sem penalizar a ausência de conteúdo que o cliente ainda vai fornecer. Placeholder mal resolvido visualmente (proporção errada, bloco vazio que quebra o ritmo) continua contando.

O crítico visual não sabe qual lado é o nosso: ele responde qual é melhor e se há cópia, e o coordenador converte a resposta com o mapa A/B. É **APROVADO** quando o lado escolhido é o nosso e não há indício de cópia; se escolher a referência, é reprovação.

## 5. O ciclo

Uma **rodada** é: corrigir as partes pendentes → rebuild → recapturar → abrir três críticos novos por parte pendente → consolidar vereditos.

Regras:

- **Contexto novo, sempre.** Cada crítico é um subagente aberto sem o histórico da conversa nem da construção. Não use fork da sessão e não reutilize críticos de rodadas anteriores: um crítico que já viu a versão anterior julga a mudança, não o resultado.
- **Só o resultado renderizado.** Passe ao crítico apenas o documento do seu papel e os caminhos das capturas. Ele não recebe código, diffs, explicações do que foi tentado, o mapa A/B nem os vereditos dos outros críticos, e é instruído a não abrir outros arquivos.
- **Paralelo.** Os três críticos de uma parte podem julgar ao mesmo tempo; espere todos para fechar a rodada.
- **Duros e binários.** Veredito **APROVADO** ou **REPROVADO**, nunca nota: notas sobem sozinhas a cada rodada sem que nada tenha melhorado. Elogios não ajudam; o crítico aponta o que falta.
- **Uma lacuna por reprovação.** Cada crítico que reprova devolve apenas **a maior lacuna**, com onde ela aparece (parte, viewport, estado). Dez reparos de uma vez viram dez remendos rasos.
- **Os três precisam aprovar.** A parte está pronta quando os três aprovam na mesma rodada. A correção de uma lacuna pode quebrar o que outro crítico tinha aprovado; por isso, a cada rodada os três julgam de novo.
- **Quem corrige é o agente principal**, que conhece o repositório. Corrija a maior lacuna de cada crítico que reprovou, com a mudança mínima que a resolve, respeitando briefing, tokens e as regras de acessibilidade e performance. Se a correção mexer em imagens, scripts ou `<head>`, rode as auditorias de novo ([WORKFLOW.md](WORKFLOW.md#ciclo-de-correção-até-zerar-fases-8-a-10)).
- **Conflito entre críticos** (ex.: o visual pede algo que o sistema proíbe): o briefing prevalece sobre o sistema, e o sistema sobre a referência. Se a solução exigir mudar o sistema ou o briefing, isso é decisão do usuário: pergunte com as opções.
- **A barra não muda para caber no resultado.** Não reescreva a barra, o briefing ou os tokens depois de uma reprovação para conseguir aprovar. Mudança real de escopo ou de referência é decisão do usuário e fica registrada com data.

## 6. Rodadas, teto e custo

- **Não há número padrão de rodadas.** O ciclo termina quando os três críticos aprovam todas as partes ou quando o usuário interrompe.
- **Contagem global:** uma rodada global é uma passagem de correção e julgamento por todas as partes pendentes; o contador não reinicia ao trocar de parte. Ao fim de cada rodada, mostre ao usuário as rodadas executadas, as partes aprovadas e a maior lacuna de cada parte pendente.
- **Teto do usuário:** se o usuário definir um teto, ele é um ponto de parada, não uma meta. Ao atingi-lo, mostre o que ainda reprova, a maior lacuna de cada parte e o total executado, e peça autorização antes de seguir. Um teto global não é multiplicado pelo número de partes.
- **Teto atingido não vira aprovação.** Parte que saiu do ciclo sem os três aprovarem fica registrada como **interrompida pelo usuário**, com a lacuna em aberto, e aparece no relatório de entrega.
- **Não invente custo em tokens.** Informe rodadas e partes, que são o que se pode medir. O ciclo não amplia o escopo nem autoriza gastos ou ações externas além do combinado.

## 7. Registro

Mantenha a seção "Ciclo visual" de `docs/website/qa-report.md` atualizada a cada rodada ([modelo](references/templates.md#relatório-de-qa)): estado de cada parte, veredito de cada crítico, histórico das lacunas e contagem global de rodadas. As capturas ficam em `tmp/review/`.

## 8. O que faz o ciclo falhar

- Referência examinada superficialmente, ou barra feita de adjetivos.
- Quem construiu julgando o próprio trabalho, ou críticos com contexto contaminado (histórico da construção, código, mapa A/B, vereditos anteriores).
- Evidência inadequada: captura quebrada, estados diferentes entre A e B, tela parada para julgar movimento.
- Crítico permissivo ou com nota subindo a cada rodada.
- Tratar o teto como objetivo, ou afrouxar a barra para caber nele.
- Instruções de crítico longas demais: cada instrução desnecessária tira espaço do julgamento.

---

Método inspirado no [Gauntlet Loop](https://somethingbig.ai/gauntlet-loop), de Matt Shumer, e na skill [loop-de-design](https://github.com/Felpborges/loop-de-design), de Felipe Borges (ambos MIT), adaptado ao fluxo, aos princípios de originalidade e às auditorias desta Skill.
