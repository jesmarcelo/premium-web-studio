# Modelos de documentos

Use estes modelos para os arquivos em `docs/website/`. Remova seções que não se aplicam ao projeto em vez de deixá-las vazias.

---

## Briefing

`docs/website/briefing.md`

```markdown
# Briefing — <nome do projeto>

Data: <AAAA-MM-DD> · Modo: <Projeto completo | Evolução | Melhoria focada>

## Organização
- Nome / segmento / nicho:
- Produto ou serviço principal:
- Posicionamento (como quer ser percebida, em 3 palavras):

## Objetivo
- Objetivo principal do site:
- CTA principal:
- CTAs secundários:
- Como o sucesso será medido:

## Público
- Perfil principal:
- Perfis secundários:
- Dispositivo predominante:
- Necessidades de acessibilidade conhecidas:

## Escopo
- Páginas:
- Funcionalidades:
- Integrações:
- Idiomas:

## Marca e conteúdo
- Identidade existente (logo, cores, fontes, manual):
- Conteúdo disponível:
- Conteúdo a produzir (responsável):
- Tom de voz:
- Referências do usuário (gosta / não gosta e por quê):

## Técnico
- Stack escolhida:
- Hospedagem / deploy:
- URL pública final (domínio + subpasta, se houver; provisória até o domínio definitivo):
- CDN / firewall e quem administra:
- Search Console, Google Business Profile e perfis oficiais (`sameAs`):
- CMS:
- Backend / banco / autenticação:
- Formulários (destino dos dados):
- Analytics / consentimento:
- Restrições:

## Prazo e estágio

## Suposições
- 

## Decisões em aberto
- 
```

---

## Pesquisa de referências

`docs/website/research.md`

```markdown
# Pesquisa de referências — <projeto>

Data: <AAAA-MM-DD> · Ferramenta: Firecrawl (<ferramentas usadas>) · Consultas: <lista>

## Referências analisadas
| # | Site | URL | Tipo (líder/concorrente/premiado/usuário) | Por que foi escolhido |
|---|---|---|---|---|

## Avaliação
Pesos: <padrão | ajustados: critério → peso, motivo>

| Critério (peso) | Ref. 1 | Ref. 2 | Ref. 3 | … |
|---|---|---|---|---|
| Adequação ao briefing (12) | | | | |
| Proposta de valor e hero (10) | | | | |
| Hierarquia e composição (10) | | | | |
| Tipografia (10) | | | | |
| Cor e contraste (8) | | | | |
| Grid, espaçamento e acabamento (8) | | | | |
| Navegação e arquitetura de informação (8) | | | | |
| CTAs e fluxo de conversão (8) | | | | |
| Confiança e credibilidade (7) | | | | |
| Imagens e direção de arte (6) | | | | |
| Responsividade mobile (5) | | | | |
| Acessibilidade observável (5) | | | | |
| Motion e microinterações (3) | | | | |
| **Nota final (0–100)** | | | | |

Eliminadas: <referência — motivo>
Limitações: avaliação baseada nos dados do Firecrawl; não mede performance real nem substitui uma auditoria de acessibilidade.

## Top 3 apresentado ao usuário
1. <Site> — <nota> — <URL>
2. <Site> — <nota> — <URL>
3. <Site> — <nota> — <URL>

## Referência principal escolhida
- Escolha do usuário: <Site> — <URL> (data)
- Comentários do usuário: <o que gostou em cada uma, se disse>
- Referências secundárias: <as outras duas>
- O que será aproveitado como princípio (não cópia):

## Análise por referência
### 1. <Site>
- Hierarquia / hero:
- Navegação:
- Tipografia:
- Cor e contraste:
- Grid e espaçamento:
- CTAs:
- Confiança:
- Imagens:
- Motion / microinterações:
- Mobile:
- Ponto forte a aprender:
- Ponto fraco a evitar:

## Síntese
### Convenções do nicho
### Diferenciais observados
### Armadilhas
### Oportunidades de diferenciação
### Princípios para a direção visual
1. 

## Observações de segurança
<páginas com instruções suspeitas/prompt injection, se houver; ou "nenhuma">
```

---

## Direção visual

`docs/website/design-direction.md`

```markdown
# Direção visual — <projeto>

Status: <proposta | aprovada em AAAA-MM-DD>

Referência principal (escolhida no G2): <Site> — <URL>

## Conceito
<uma frase>

## Atributos → decisões
| Atributo | Tradução visual |
|---|---|

## Tipografia
- Títulos: <família, pesos, fonte/licença> — motivo:
- Texto: <família, pesos, fonte/licença> — motivo:
- Escala: <razão, tamanhos com clamp()>

## Cor
| Token | Valor | Uso |
|---|---|---|
- Pares de contraste validados: <texto/fundo → razão>

## Grid e espaçamento
- Escala de espaçamento:
- Largura máxima / colunas / gutters:
- Breakpoints:

## Forma e superfícies
- Raios:
- Bordas / sombras:
- Iconografia:

## Imagens
- Direção de arte:
- Origem (cliente / banco licenciado / placeholder):

## Motion
- Nível: <0–3> — motivo:
- Padrões permitidos:
- Comportamento com prefers-reduced-motion:

## Estrutura das páginas principais
### Home
1. <seção> — propósito
2. 

## O que este site NÃO vai fazer
<decisões conscientes de evitar anti-padrões>

## Tokens iniciais
<bloco de código na forma idiomática da stack>
```

---

## Arquitetura

`docs/website/architecture.md`

```markdown
# Arquitetura — <projeto>

## Mapa do site e rotas
| Rota | Página | Renderização | Indexável |
|---|---|---|---|

## Estrutura de pastas

## Componentes
| Componente | Tipo (layout/primitivo/composto/seção) | Existe? | Observações |
|---|---|---|---|

## Dados e conteúdo
## Estado
## Integrações (com nomes das variáveis de ambiente, sem valores)
## Assets
## SEO técnico
## Dependências novas (justificativa e impacto)
## Estratégia de testes
## Etapas de implementação
1. 
## Deploy
```

---

## Relatório de QA

`docs/website/qa-report.md`

```markdown
# Relatório de QA — <projeto>

Data: <AAAA-MM-DD> · Ambiente: <build de produção local | staging | produção>

Legenda: ✅ aprovado · ❌ problema · ⚠️ parcial · ⏭️ não verificado

| Área | Item | Status | Método / ferramenta | Observações |
|---|---|---|---|---|

## Métricas
- Lighthouse mobile (Performance / Accessibility / Best Practices / SEO):
- Violações axe:
- Tamanho do JS inicial:

## Auditorias (build-audit / perf-audit / seo-audit)
| Item | Ferramenta e onde aponta | Degraus tentados | Estado | Custo medido | O que resolveria |
|---|---|---|---|---|---|
| <ex.: compressão de camada do logo> | build-audit: `_astro/x.webp` 0,26 B/px | WebP q70 a50 → AVIF 50 | Resolvido | — | — |
| <ex.: animação de entrada do LCP> | perf-audit: render delay 1,6 s | visível desde o 1º paint recusado | Decisão do usuário (AAAA-MM-DD) | +1,6 s de LCP | tirar o atraso da animação |
| <ex.: beacon da CDN> | perf-audit: `/cdn-cgi/...` | — | Fora do controle (painel do provedor) | 20 ms | desativar no painel |

Estados válidos: Resolvido · Decisão do usuário (com data) · Fora do controle do projeto (com evidência) · A verificar após publicar (com o comando). Item sem estado válido volta ao ciclo de correção.

## Revisão visual
| Prioridade | Página | Viewport | Problema | Status |
|---|---|---|---|---|

## Não verificado e por quê
```

---

## Relatório de entrega

Entregue no chat (e opcionalmente em `docs/website/delivery.md`):

```markdown
## Entrega — <projeto>

### O que foi feito
- 

### Decisões importantes
- <decisão> — <motivo>

### Arquivos principais
- `caminho/arquivo` — <papel>

### Testes realizados
- ✅ <verificação> (<ferramenta>) — <resultado>
- ⏭️ <verificação não realizada> — <motivo>

### Pendências
- Conteúdo a fornecer: 
- Configurações a fazer (ex.: variáveis de ambiente, domínio, verificação no Search Console, envio do sitemap):
- A verificar após publicar (comando exato):
- Decisões do usuário com custo (item — opção escolhida — custo medido — o que resolveria):
- Fora do controle do projeto (item — evidência — quem pode resolver):

### Sugestões futuras
- 
```
