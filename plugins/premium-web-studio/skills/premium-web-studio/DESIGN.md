# Direção visual

Objetivo: um resultado **premium, moderno, profissional, original e coerente com o nicho**. Premium não é "mais efeitos" — é intenção, precisão, consistência e conteúdo bem hierarquizado. Toda decisão visual precisa de uma justificativa ligada ao contexto (público, objetivo, marca, pesquisa).

Consulte [references/niche-profiles.md](references/niche-profiles.md) para o perfil do segmento.

---

## 1. Processo

1. **Revise as entradas:** briefing, referência principal escolhida pelo usuário (gate G2), síntese da pesquisa, identidade existente, perfil do nicho. A referência principal define o nível de qualidade e a direção (sofisticação, densidade, tom, tipo de composição); a solução continua original. Explique na proposta o que foi inspirado nela e o que é próprio do projeto.
2. **Defina o conceito:** uma ideia central em uma frase que guie todas as decisões. Ex.: "Precisão silenciosa — a autoridade vem do rigor, não do volume." Evite conceitos vagos como "moderno e clean".
3. **Defina 3–5 atributos de marca** e os traduza em decisões visuais (ex.: "confiável" → paleta contida, tipografia serifada de texto, alinhamentos rígidos, ausência de motion chamativo).
4. **Escolha a linguagem visual:** tipografia, cor, grid, espaçamento, forma, imagem, iconografia, motion.
5. **Formalize em tokens** (seção 8).
6. **Desenhe a estrutura das páginas principais** em texto (ordem das seções e propósito de cada uma) antes de codificar.
7. **Apresente ao usuário** (gate G3). Quando a direção não for óbvia, ofereça 2 direções contrastantes, cada uma com conceito, paleta, pares tipográficos e nível de motion, e uma recomendação.

## 2. Hierarquia

- Cada tela tem **um** foco principal. Defina o que é visto em 1º, 2º e 3º lugar.
- Contraste de escala real entre níveis (ex.: H1 2,5–4× o corpo em desktop). Hierarquia fraca é a causa nº 1 de sites "genéricos".
- Use peso, tamanho, cor, espaço e posição — não tudo ao mesmo tempo.
- Um CTA primário por contexto; secundários visualmente subordinados.

## 3. Tipografia

- Escolha **1–2 famílias** (no máximo 3, se uma for mono funcional). Combine por contraste (serifada + sans, grotesca + humanista), não por semelhança.
- Prefira fontes com boa renderização em telas, suporte completo aos caracteres dos idiomas do site e licença adequada para web (Google Fonts, Fontshare, fontes da marca licenciadas, fontes do sistema).
- Evite os pares padrão mais repetidos em sites gerados por IA (Inter em tudo, com gradiente roxo) quando não houver motivo — Inter é ótima, mas escolha conscientemente.
- Escala tipográfica modular (razão 1,2–1,333) com `clamp()` para fluidez entre mobile e desktop.
- Corpo: 16–20 px, altura de linha 1,5–1,7, comprimento de linha 60–75 caracteres.
- Títulos: altura de linha 1,05–1,25, `letter-spacing` levemente negativo em tamanhos grandes, `text-wrap: balance` para títulos e `text-wrap: pretty` para parágrafos quando suportado.
- Use números tabulares (`font-variant-numeric: tabular-nums`) em tabelas, preços e dados.
- Detalhes de carregamento em [SEO-PERFORMANCE.md](SEO-PERFORMANCE.md#fontes).

## 4. Cor

- Parta da identidade existente quando houver; caso contrário, derive a paleta do conceito e do nicho.
- Estrutura recomendada: neutros (5–9 tons, levemente tingidos pela cor da marca), 1 cor primária, no máximo 1 cor de destaque, cores semânticas (sucesso, alerta, erro, informação).
- Proporção aproximada 60/30/10 (neutros/superfícies secundárias/destaque). A cor de destaque perde força se usada em tudo.
- Defina cores em espaço perceptual (`oklch()`) quando a stack permitir, com fallback se necessário.
- Contraste mínimo WCAG AA: 4,5:1 texto normal, 3:1 texto grande e componentes de interface. Valide cada combinação usada.
- Modo escuro só se fizer sentido para o público ou se pedido; se existir, é projetado, não apenas invertido.

## 5. Grid, espaçamento e layout

- Escala de espaçamento consistente (base 4 ou 8 px). Nada de valores arbitrários soltos.
- Largura máxima de conteúdo definida (ex.: 1200–1440 px para layout, ~70ch para texto).
- Grid de 12 colunas (desktop), 8 (tablet), 4 (mobile) como ponto de partida; quebras intencionais do grid criam interesse.
- Ritmo vertical: espaçamento entre seções generoso e variável conforme importância — seções iguais com o mesmo padding criam monotonia.
- Varie a composição entre seções (texto + mídia, lista editorial, destaque em largura total, tabela, citação) de acordo com o conteúdo, não por enfeite.
- Alinhamento rigoroso: elementos compartilham eixos. Desalinhamentos de poucos pixels são o que separa o amador do premium.

## 6. Forma, superfícies e iconografia

- Defina 2–3 raios de borda com propósito (ex.: 4 px controles, 12 px cards, 999 px apenas para pills). Consistência > quantidade.
- Sombras sutis e com fonte de luz coerente; prefira bordas e contraste de superfície a sombras pesadas.
- Ícones de uma única família, com peso consistente, apenas quando ajudam a compreensão ou a escaneabilidade.
- Imagens: prefira fotografia real e autêntica do cliente; na falta, placeholders neutros com proporções finais e indicação de que serão substituídos. Defina direção de arte (enquadramento, luz, tratamento de cor). Use bancos de imagens livres apenas com licença verificada e de forma pontual.

## 7. Motion

Animações **não são obrigatórias**. Defina o nível pelo contexto:

Os contextos abaixo são exemplos; decida pelo perfil do projeto (público, objetivo, seriedade, dispositivos), não pelo rótulo do segmento.

| Nível | Contextos típicos | O que usar |
|---|---|---|
| **0 — Estático** | Governo, saúde, serviços públicos, sistemas críticos, público idoso ou com baixa conectividade | Apenas mudanças de estado instantâneas ou transições ≤150 ms em hover/foco |
| **1 — Sutil** | Advocacia, finanças, institucional, B2B tradicional, e-commerce | Transições de estado 150–250 ms, reveal discreto (opacidade + 8–16 px), feedback de formulários |
| **2 — Expressivo** | SaaS, startups, agências, produtos de consumo, marcas lifestyle | Reveals coordenados, scroll-linked moderado, microinterações elaboradas, transições de página |
| **3 — Imersivo** | Portfólios criativos, lançamentos, campanhas, experiências de marca | Storytelling por scroll, WebGL/3D, timelines complexas — somente com orçamento de performance e fallback |

Regras:
- Toda animação tem propósito: orientar, dar feedback, mostrar relação ou reforçar a narrativa.
- Anime apenas `transform` e `opacity` sempre que possível; evite animar propriedades de layout.
- Duração 150–400 ms para UI; easing de saída suave (`cubic-bezier(0.2, 0.8, 0.2, 1)` ou similar). Nada de bounce gratuito.
- Conteúdo nunca fica invisível se o JS falhar ou se a animação não disparar.
- **Sempre respeite `prefers-reduced-motion`**: remova movimentos de deslocamento, parallax, autoplay e scroll-jacking; mantenha só transições de opacidade curtas ou nenhuma.
- Nunca use scroll-jacking em sites de conteúdo ou conversão.
- Escolha de biblioteca: CSS primeiro; Motion (ex-Framer Motion) para React quando houver orquestração de estados; GSAP para timelines complexas e scroll-linked; View Transitions API para transições de página quando suportado. Ver política de dependências em [ENGINEERING.md](ENGINEERING.md#dependências).

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## 8. Tokens de design

Formalize a direção em tokens na forma idiomática da stack (variáveis CSS, `@theme` do Tailwind v4, `tailwind.config`, `theme.ts`). Conjunto mínimo:

- **Cores:** neutros, primária, destaque, semânticas, superfícies, bordas, texto (primário, secundário, desabilitado, sobre cor).
- **Tipografia:** famílias, escala (`--text-xs` … `--text-5xl` com `clamp()`), pesos, alturas de linha, tracking.
- **Espaçamento:** escala base.
- **Layout:** larguras máximas, breakpoints, gutters.
- **Forma:** raios, bordas, sombras.
- **Motion:** durações, easings.
- **Camadas:** z-index nomeados.

## Anti-padrões de site gerado por IA

Evite ativamente (e revise na fase 9):

- Gradientes gratuitos, especialmente roxo-azul em fundos, textos e botões sem relação com a marca.
- Glow e sombras coloridas em todos os elementos.
- Dezenas de cards idênticos em grade 3×N como solução para todo conteúdo.
- Bordas muito arredondadas em tudo sem motivo.
- Excesso de badges/pills ("✨ Novo", "🚀 Rápido") e emojis como ícones.
- Ícones decorativos em cada título e item de lista.
- Textos genéricos: "Transforme seu negócio", "Soluções inovadoras", "Leve sua empresa ao próximo nível", "Desbloqueie o potencial".
- Componentes e seções visualmente idênticos em sequência (hero → 3 features → 3 cards → depoimentos → CTA → FAQ, sempre com o mesmo padding e alinhamento centralizado).
- Tudo centralizado.
- Glassmorphism indiscriminado, blur em tudo, blobs abstratos de fundo.
- Animações de entrada em todos os elementos, contadores animados sem propósito, marquees de logos por padrão.
- Números e depoimentos inventados.
- Hierarquia artificial (tudo em negrito, tudo grande, tudo colorido).
- Efeitos que prejudicam leitura, contraste ou performance.

Antídotos: conteúdo específico do cliente, decisões tipográficas fortes, composição variada guiada pelo conteúdo, contenção cromática, detalhes precisos (alinhamento, ritmo, estados), fotografia autêntica, microcopy concreta.

## Saída da fase

`docs/website/design-direction.md` no modelo de [references/templates.md](references/templates.md#direção-visual), contendo conceito, atributos, justificativas, paleta com contrastes validados, tipografia, grid, espaçamento, forma, imagens, nível de motion, estrutura das páginas principais e tokens iniciais.
