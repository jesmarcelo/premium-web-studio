# Acessibilidade

Meta padrão: **WCAG 2.2 nível AA**. Some a isso as exigências legais do país e do setor do projeto, levantadas no discovery. Exemplos: European Accessibility Act / EN 301 549 (União Europeia), ADA e Section 508 (EUA), Public Sector Bodies Accessibility Regulations (Reino Unido), eMAG e Lei Brasileira de Inclusão (Brasil). Na dúvida sobre a norma aplicável, pergunte ao usuário. Acessibilidade é requisito de projeto desde a fase 5, não correção de última hora.

## Estrutura e semântica

- `lang` correto no `<html>` (ex.: `en`, `es-MX`, `pt-BR`) e em trechos de outro idioma.
- Landmarks: um `<header>`, `<nav>` (com `aria-label` se houver mais de um), um `<main>`, `<footer>`.
- Um único `h1` por página; headings em ordem lógica, sem pular níveis por razões visuais.
- Listas como `ul`/`ol`, tabelas de dados com `th`, `scope` e `caption`.
- `button` para ações, `a href` para navegação. Nunca `div` clicável.
- Link "Pular para o conteúdo" como primeiro elemento focável.
- `title` de página único e descritivo.

## Teclado e foco

- Tudo que é interativo é alcançável e operável por teclado (Tab, Shift+Tab, Enter, Espaço, Esc, setas onde o padrão exige).
- Ordem de foco segue a ordem visual e lógica; sem `tabindex` positivo.
- **Foco visível** com contraste ≥ 3:1 em relação ao fundo (`:focus-visible`), nunca `outline: none` sem substituto.
- Foco não fica escondido sob header fixo ou banners (WCAG 2.4.11) — use `scroll-padding-top`.
- Modais: foco movido para dentro ao abrir, preso enquanto aberto, Esc fecha, foco retorna ao gatilho. Prefira `<dialog>` nativo ou biblioteca acessível.
- Menus mobile: botão com `aria-expanded` e `aria-controls`; fecha com Esc.

## Texto, cor e contraste

- Contraste de texto ≥ 4,5:1 (normal) e ≥ 3:1 (≥ 24 px, ou ≥ 18,66 px em negrito).
- Componentes de interface e elementos gráficos informativos ≥ 3:1.
- Cor nunca é o único meio de transmitir informação (erros, estados, gráficos, links no meio do texto).
- Texto redimensionável até 200% sem perda de conteúdo; layout funciona com zoom de 400% em 320 px de largura (reflow) sem rolagem horizontal.
- Use `rem` para tipografia; não bloqueie zoom (`user-scalable=no` é proibido).
- Respeite espaçamento de texto ajustado pelo usuário (WCAG 1.4.12).

## Imagens e mídia

- `alt` descritivo para imagens informativas; `alt=""` para decorativas; SVGs informativos com `role="img"` e título acessível; decorativos com `aria-hidden="true"`.
- Ícones isolados em botões têm nome acessível (`aria-label` ou texto visualmente oculto).
- Vídeos com legendas; áudio com transcrição; nada toca automaticamente com som.
- Conteúdo em movimento por mais de 5 s (carrosséis, marquees, vídeos de fundo) tem controle de pausa.

## Formulários

- Todo campo tem `<label>` visível e associado; placeholder não substitui label.
- Agrupamentos com `fieldset`/`legend`.
- Campos obrigatórios indicados em texto, não só com cor ou asterisco sem explicação.
- `autocomplete` adequado (`name`, `email`, `tel`, `street-address`…) e `type`/`inputmode` corretos.
- Erros: mensagem textual próxima ao campo, associada via `aria-describedby`, campo com `aria-invalid="true"`, resumo de erros no topo em formulários longos e foco movido para o primeiro erro.
- Mensagens de sucesso/status anunciadas com `role="status"` ou região `aria-live="polite"`.
- Não exija testes cognitivos para autenticação (WCAG 3.3.8); permita colar senhas.
- Não peça a mesma informação duas vezes no mesmo fluxo (WCAG 3.3.7).

## Interação

- Áreas de toque ≥ 24×24 px (WCAG 2.5.8); recomendado 44×44 px em mobile.
- Nada depende apenas de hover; conteúdo em hover/foco é dispensável (Esc), persistente e acessível com o ponteiro.
- Gestos complexos (arrastar, pinça) têm alternativa simples (WCAG 2.5.7).
- Sem limites de tempo, ou com aviso e extensão.
- Sem conteúdo que pisque mais de 3 vezes por segundo.

## Motion

- `prefers-reduced-motion: reduce` desativa deslocamentos, parallax, autoplay e scroll-linked (ver [DESIGN.md](DESIGN.md#7-motion)).
- Animações nunca são necessárias para entender o conteúdo.

## ARIA

- **Primeira regra de ARIA: não use ARIA se o HTML nativo resolve.**
- Quando usar, siga os padrões do ARIA Authoring Practices Guide (APG) por completo — ARIA incompleto é pior que nenhum.
- Não sobrescreva semântica nativa (`<button role="link">`).
- `aria-hidden="true"` nunca em elementos focáveis.

## Como testar

1. **Automático:** axe (`npx @axe-core/cli <url>`, extensão axe DevTools, `@axe-core/playwright`), Lighthouse (categoria Accessibility), linters (`eslint-plugin-jsx-a11y`, `eslint-plugin-vuejs-accessibility`, `svelte-check`). Testes automáticos detectam apenas parte dos problemas.
2. **Teclado:** percorra cada página só com o teclado verificando ordem, foco visível e operação de menus, modais e formulários.
3. **Zoom e reflow:** 200% e 400% em 1280 px; largura de 320 px.
4. **Contraste:** verifique cada par de cores do sistema de tokens.
5. **Leitor de tela (quando possível):** VoiceOver (macOS/iOS), NVDA (Windows), TalkBack (Android) — títulos, landmarks, formulários, anúncios de status.
6. **Reduced motion:** ative a preferência no sistema ou emule no DevTools/Playwright (`reducedMotion: 'reduce'`).

Registre no relatório o que foi testado automaticamente, o que foi testado manualmente e o que **não** foi testado (ex.: leitor de tela real).
