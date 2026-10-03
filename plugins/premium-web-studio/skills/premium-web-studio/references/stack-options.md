# Opções de stack e trade-offs

Use para apresentar 2–3 opções quando o usuário não souber qual stack escolher. A decisão é sempre do usuário. Recomende com base nos requisitos levantados no discovery (quem edita, dinamismo, escala, hospedagem, quem mantém).

## Perguntas que definem a stack

1. **Quem edita o conteúdo?** Desenvolvedor → conteúdo em arquivos. Equipe não técnica → CMS.
2. **Quão dinâmico?** Estático/institucional → SSG. Login, painel, e-commerce, dados em tempo real → framework full-stack ou backend.
3. **Hospedagem e orçamento?** Hospedagem compartilhada PHP → WordPress/HTML. Vercel/Netlify/Cloudflare → frameworks JS.
4. **Quem mantém?** Escolha o que a pessoa ou equipe que vai manter domina.

## Opções

### HTML + CSS + JavaScript (com Vite opcional)
- **Ideal para:** landing pages e sites pequenos, sem CMS, mantidos por desenvolvedor.
- **Vantagens:** zero dependência de framework, máxima performance, hospedagem em qualquer lugar, longevidade.
- **Desvantagens:** repetição sem componentes (mitigável com Vite + partials ou web components), sem CMS.
- **Manutenção:** baixa complexidade; escala mal para muitas páginas.

### Astro
- **Ideal para:** sites de conteúdo, institucionais, blogs, documentação, marketing.
- **Vantagens:** zero JS por padrão, excelente performance e SEO, Content Collections tipadas, aceita componentes React/Vue/Svelte em ilhas, integra com qualquer CMS headless.
- **Desvantagens:** menos indicado para aplicações muito interativas; ecossistema menor que o do Next.js.
- **Hospedagem:** estática em qualquer CDN, ou SSR em Vercel/Netlify/Cloudflare/Node.

### Next.js (React)
- **Ideal para:** sites com partes de aplicação (login, painel, e-commerce headless), times React.
- **Vantagens:** ecossistema enorme, SSR/SSG/ISR, Server Components, rotas de API, otimização de imagens e fontes integrada.
- **Desvantagens:** maior complexidade conceitual, mais JS no cliente se mal usado, melhor experiência na Vercel (self-host exige mais trabalho).
- **Hospedagem:** Vercel, Netlify, Cloudflare (via adaptador), Node/Docker.

### Nuxt (Vue)
- **Ideal para:** times Vue, sites com conteúdo e aplicação.
- **Vantagens:** convenções fortes, Nuxt Content, ótimo DX, SSR/SSG.
- **Desvantagens:** ecossistema menor que React.

### SvelteKit
- **Ideal para:** sites e apps interativos com foco em performance e simplicidade.
- **Vantagens:** pouco JS gerado, sintaxe enxuta, form actions com progressive enhancement.
- **Desvantagens:** ecossistema e mercado de profissionais menores.

### Remix / React Router (framework mode)
- **Ideal para:** aplicações web centradas em formulários e dados, times React que preferem padrões web.
- **Vantagens:** loaders/actions, progressive enhancement, roda em vários runtimes.
- **Desvantagens:** menos foco em sites estáticos de conteúdo.

### WordPress
- **Ideal para:** clientes que precisam editar tudo sozinhos, blogs grandes, orçamento de hospedagem baixo, equipes PHP.
- **Vantagens:** editor conhecido, ecossistema de plugins, hospedagem barata em qualquer lugar.
- **Desvantagens:** segurança e performance dependem de disciplina com plugins e atualizações; temas genéricos tendem a sites genéricos.
- **Variante headless:** WordPress como CMS + Astro/Next no frontend (mais complexo, melhor performance).

### Site builders (Webflow, Framer)
- **Ideal para:** equipes de marketing que querem autonomia visual sem código.
- **Vantagens:** edição visual, hospedagem inclusa.
- **Desvantagens:** lock-in, custo recorrente, controle de código limitado. Nesta Skill, o trabalho seria de direção, estrutura e revisão, não de código.

### CMS headless (combinável com Astro, Next, Nuxt, SvelteKit)
- **Sanity:** modelagem flexível, editor em tempo real, plano gratuito generoso.
- **Payload:** open source, TypeScript, pode rodar dentro do próprio app Next.js.
- **Strapi:** open source, self-hosted, painel tradicional.
- **Contentful:** enterprise, robusto, caro em escala.
- **Decap CMS / Keystatic / TinaCMS:** conteúdo em arquivos no Git, sem servidor, bom para sites pequenos.

### Estilização
- **Tailwind CSS:** rápido, consistente com tokens, ótimo para times; markup mais verboso.
- **CSS Modules / CSS puro com variáveis:** sem dependência, controle total, exige disciplina.
- **Sass:** útil em projetos legados que já o usam.
- **CSS-in-JS:** evite em projetos novos com Server Components (custo em runtime).

## Modelo de apresentação ao usuário

```markdown
Com base no que você descreveu (<resumo dos requisitos>), estas são as opções mais adequadas:

**1. <Opção A> (recomendada)** — <para que serve>.
- Prós: …
- Contras: …
- Manutenção/custo: …

**2. <Opção B>** — …

**3. <Opção C>** — …

Recomendo <A> porque <motivo ligado aos requisitos>. Qual prefere?
```
