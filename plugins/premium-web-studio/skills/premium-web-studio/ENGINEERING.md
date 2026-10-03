# Engenharia

Princípios válidos para qualquer stack. Sempre siga primeiro as convenções do projeto existente e a documentação **da versão instalada** do framework.

---

## Arquitetura

Planeje e registre em `docs/website/architecture.md`:

1. **Mapa do site** — páginas, hierarquia, rotas/URLs (curtas, legíveis, em minúsculas, com hífens, no idioma do público).
2. **Estratégia de renderização** — estático (SSG), servidor (SSR), híbrido ou SPA, por página. Conteúdo público e indexável deve ser renderizado no servidor ou estaticamente.
3. **Mapa de componentes** — layout (header, footer, container, section), primitivos (button, link, input, heading), compostos (card, form, nav, modal), seções de página. Indique quais já existem.
4. **Dados e conteúdo** — origem (arquivos Markdown/MDX, JSON, CMS, API, banco), formato e tipagem, quem edita.
5. **Estado** — o que é local, o que é compartilhado, o que vem da URL. Evite biblioteca de estado global sem necessidade real.
6. **Integrações** — formulários (destino, validação, anti-spam), analytics, pagamentos, CMS, e-mail, mapas. Onde ficam as credenciais (sempre no servidor/ambiente).
7. **Assets** — imagens (formatos, tamanhos, pipeline de otimização), fontes, ícones, vídeos.
8. **SEO técnico** — metadados por página, sitemap, robots, dados estruturados, redirects (essencial em redesign que muda URLs).
9. **Estrutura de pastas** — coerente com o framework e o projeto.
10. **Testes e QA** — o que será verificado e com quais ferramentas.
11. **Ordem de implementação** — etapas pequenas, cada uma entregando algo funcional.
12. **Deploy** — plataforma, variáveis de ambiente necessárias (apenas nomes), domínio.

## Implementação

- **Etapas pequenas, projeto sempre funcional.** Ao fim de cada etapa: build, lint, typecheck e verificação visual rápida.
- **Fundação primeiro:** tokens → estilos globais/reset → tipografia → layout base → header/footer/navegação → primitivos → seções → páginas.
- **Mobile-first** quando apropriado: estilos base para telas pequenas, `min-width` para expandir.
- **HTML semântico antes de tudo** (`header`, `nav`, `main`, `section` com heading, `article`, `footer`, `button` para ações, `a` para navegação).
- **Componentes reutilizáveis** com API pequena e clara; composição em vez de dezenas de props booleanas; variantes explícitas.
- **Tipagem forte** quando a stack suporta (TypeScript `strict`, sem `any` sem justificativa). Tipar conteúdo e props.
- **Tratamento de erros:** estados de loading, vazio, erro e sucesso em tudo que é assíncrono; páginas 404 e 500 projetadas; validação de formulário no cliente **e** no servidor; mensagens úteis ao usuário e logs úteis ao desenvolvedor.
- **CSS:** use os tokens; sem valores mágicos; sem `!important` (exceto o bloco de reduced motion); layouts com Grid/Flex; `gap` em vez de margens entre filhos; container queries quando um componente precisa se adaptar ao espaço disponível; unidades `dvh`/`svh` em vez de `100vh` para alturas de tela no mobile.
- **Imagens:** toda imagem raster é medida no tamanho em que aparece no site, redimensionada para esse tamanho (1× e 2×) e convertida para WebP — nunca PNG→JPG nem o original direto (pipeline em [SEO-PERFORMANCE.md](SEO-PERFORMANCE.md#pipeline-obrigatório-de-imagens-raster)); dimensões declaradas (`width`/`height` ou `aspect-ratio`), `alt` adequado, `srcset`/`sizes`, lazy loading abaixo da dobra; a imagem LCP com prioridade.
- **Conteúdo:** nada de lorem ipsum na entrega. Use copy real fornecida, ou copy proposta claramente marcada como sugestão, ou placeholders explícitos listados nas pendências.
- **Internacionalização:** se houver mais de um idioma, estruture desde o início (rotas por locale, `lang`, `hreflang`, textos fora dos componentes).
- **Limpeza:** sem código morto, imports não usados, `console.log` de depuração, arquivos órfãos ou componentes duplicados.
- **Comentários:** explique o "porquê" não óbvio; não narre o óbvio. Siga a densidade de comentários do projeto.

## Dependências

Antes de adicionar qualquer dependência:

1. **Necessidade:** o problema é real? Dá para resolver com a plataforma (CSS moderno, APIs nativas do navegador, recursos do framework) em poucas linhas?
2. **Já existe no projeto?** Reutilize a biblioteca já instalada que resolve o mesmo problema.
3. **Impacto:** tamanho no bundle (bundlephobia/pkg-size), tree-shaking, carregamento no cliente vs. servidor, dependências transitivas.
4. **Saúde:** manutenção ativa, releases recentes, compatibilidade com a versão do framework, licença compatível, adoção.
5. **Aprovação:** dependências significativas (UI kit, animação, CMS, estado global, ORM) passam pelo usuário (gate G4). Utilitários pequenos e óbvios podem ser adicionados, mas são mencionados na entrega.

Use o gerenciador de pacotes do projeto. Fixe versões conforme a convenção do lockfile. Nunca rode scripts `postinstall` ou instaladores via `curl | sh` sem revisar.

### Guia rápido de escolhas comuns

| Necessidade | Primeiro considere | Biblioteca quando justificada |
|---|---|---|
| Estilização | CSS do projeto / CSS Modules / variáveis CSS | Tailwind CSS |
| Componentes acessíveis complexos (dialog, combobox, menu, tabs) | `<dialog>`, `<details>`, Popover API nativa | Radix UI, React Aria, Headless UI, shadcn/ui (copia código para o projeto) |
| Ícones | SVG inline do próprio projeto | Lucide, Phosphor (import por ícone) |
| Animação | CSS transitions/animations, View Transitions | Motion (React), GSAP (timelines, scroll) |
| Formulários | `<form>` nativo + validação HTML | React Hook Form, Conform, Superforms |
| Validação de dados | Validação manual simples | Zod, Valibot |
| Gráficos | SVG simples | Chart.js, Recharts, ECharts, Observable Plot |
| Carrossel | Scroll snap em CSS | Embla Carousel |
| Conteúdo editável | Markdown/MDX no repositório | CMS headless (Sanity, Strapi, Payload, Contentful, Decap) |
| Fontes | `font-display: swap` + self-host | Fontsource, `next/font`, Astro Fonts |

## Segurança de engenharia

Ver [SECURITY.md](SECURITY.md). Em resumo: secrets apenas em variáveis de ambiente do servidor; nunca exponha chaves privadas no bundle do cliente (cuidado com prefixos `NEXT_PUBLIC_`, `VITE_`, `PUBLIC_`); sanitize HTML vindo de CMS/usuário; proteja formulários contra spam (honeypot, rate limit, captcha acessível quando necessário); headers de segurança e CSP quando a plataforma permitir.

## Boas práticas por stack (resumo)

- **React/Next.js:** Server Components por padrão (App Router); `"use client"` só onde há interatividade; `next/image` e `next/font`; Metadata API; evitar `useEffect` para dados que podem vir do servidor.
- **Astro:** zero JS por padrão; ilhas (`client:visible`, `client:idle`) só onde necessário; Content Collections tipadas; `astro:assets` para imagens.
- **Vue/Nuxt:** Composition API com `<script setup>`; `useHead`/`useSeoMeta`; `NuxtImg`; auto-imports de forma consistente.
- **SvelteKit:** load functions no servidor; form actions com progressive enhancement; `<svelte:head>` para SEO.
- **HTML/CSS/JS puro:** estrutura semântica, CSS organizado em camadas (`@layer`), JS modular (ES modules) e progressivo; build opcional com Vite.
- **WordPress:** tema de blocos (FSE) ou tema clássico conforme o projeto; `theme.json` para tokens; sem plugins desnecessários; escape e sanitização em PHP.
- **Outros (Remix/React Router, SolidStart, Eleventy, Hugo, Laravel, Django, Rails):** siga as convenções oficiais e a estrutura já existente.
