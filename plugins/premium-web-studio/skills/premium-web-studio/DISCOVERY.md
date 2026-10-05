# Discovery

## Regras de condução

- **Antes de perguntar, colete.** Leia a mensagem, arquivos anexos, o repositório e o site atual (se houver URL, leia via Firecrawl se já estiver configurado, ou via navegador/fetch web). Não pergunte o que já está respondido.
- **Agrupe.** No máximo 2 rodadas. Cada rodada com até ~8 perguntas organizadas por tema. Evite interrogatório.
- **Ofereça opções.** Sempre que possível, dê alternativas concretas com uma recomendação marcada, em vez de perguntas abertas. Use a ferramenta AskUserQuestion quando disponível (até 4 perguntas por chamada).
- **Proporcionalidade.** Uma melhoria focada pede 2–4 perguntas; um projeto completo pede o roteiro inteiro.
- **"Não sei" é uma resposta válida.** Nesse caso, proponha um padrão sensato e registre como suposição.
- **Não invente.** Se o usuário não forneceu conteúdo, não crie fatos sobre a empresa. Use placeholders explícitos.
- **Feche com um briefing.** Apresente o resumo consolidado e peça confirmação (gate G1).

## Rodada 1 — Essencial (sempre)

**Negócio e objetivo**
1. Que tipo de website é (institucional, landing page, e-commerce, portal, blog/conteúdo, SaaS/produto, portfólio, outro)?
2. Qual é o produto, empresa ou organização, e o nicho/segmento?
3. Qual é o objetivo principal do site (gerar leads, vender, informar, captar inscrições, credibilidade, recrutamento)?
4. Qual é a ação principal (CTA) que o visitante deve realizar?

**Público**
5. Quem é o público-alvo (perfil, nível técnico, faixa etária, B2B/B2C, região, dispositivo predominante)?

**Escopo**
6. Quais páginas e funcionalidades são necessárias? (Ofereça uma lista sugerida para o tipo de site.)

**Stack e estágio**
7. Já existe código, site ou stack definida? Se não, há preferência de tecnologia, hospedagem ou CMS? (Se "não sei", vá para o bloco "Escolha de stack".)
8. Em que estágio está o projeto e há prazo ou restrição importante?

## Rodada 2 — Detalhamento (quando relevante)

**Marca e conteúdo**
- Existe identidade visual (logotipo, cores, tipografia, manual de marca)? Em que formato estão os arquivos?
- Há referências de sites que o usuário admira ou rejeita? O que agrada/desagrada em cada um?
- Qual conteúdo já existe (textos, fotos, vídeos, depoimentos, cases, dados)? Quem vai produzir o restante?
- Tom de voz desejado (técnico, acolhedor, institucional, ousado, sofisticado)?
- Qual é a percepção desejada em 3 palavras?

**Funcionalidades e integrações**
- Formulários (contato, orçamento, inscrição)? Para onde vão os dados (e-mail, CRM, planilha, banco)?
- Backend, banco de dados, autenticação, área logada?
- Integrações (pagamento, agenda, chat, newsletter, mapas, ERP, APIs)?
- CMS para o cliente editar conteúdo? Quem editará e com que frequência?
- Analytics e consentimento de cookies (conforme a lei de privacidade aplicável — ex.: GDPR, LGPD, CCPA)?

**Alcance e qualidade**
- Idiomas e mercados atendidos?
- Requisitos de acessibilidade (obrigação legal do país/setor, setor público, público com necessidades específicas)?
- Regulamentações do setor que afetam o conteúdo (ex.: regras de publicidade de conselhos profissionais, informações legais obrigatórias da empresa, avisos financeiros ou de saúde)?
- Prioridades de SEO (palavras-chave, SEO local, migração de URLs existentes)?
- Restrições técnicas (hospedagem compartilhada, sem Node no servidor, políticas de TI, navegadores legados)?
- Domínio e deploy (onde será publicado, quem administra)? **Qual é a URL pública final**, com subpasta se houver (`https://www.exemplo.com/` ou `https://host.com/projeto/`)? Sem ela não há canonical nem imagem na prévia de compartilhamento ([SEO-PERFORMANCE.md](SEO-PERFORMANCE.md#url-pública-final-pré-requisito)). Se o domínio definitivo ainda não existe, onde o site ficará no ar enquanto isso? Há CDN ou firewall na frente (ex.: proteção contra bots) e quem tem acesso ao painel?
- Google e redes: já existe conta no Search Console (ou quem pode verificar o domínio), perfil no Google Business Profile e perfis oficiais nas redes (para `sameAs`)? Qual frase e qual imagem devem aparecer quando o link for compartilhado?

## Escolha de stack (quando o usuário não sabe)

1. Pergunte os requisitos que determinam a stack:
   - Quem vai editar o conteúdo e com que frequência?
   - Haverá funcionalidades dinâmicas (login, painel, e-commerce, busca, dados em tempo real)?
   - Quantas páginas e qual expectativa de crescimento?
   - Onde será hospedado e qual orçamento de infraestrutura?
   - Quem vai manter o código depois (o próprio usuário, uma equipe, uma agência)? Qual linguagem essa pessoa domina?
2. Apresente **2 ou 3 opções** adequadas a partir de [references/stack-options.md](references/stack-options.md), cada uma com: para que serve, vantagens, desvantagens, custo/complexidade de manutenção.
3. Indique qual recomenda e por quê, mas **deixe o usuário decidir** antes de prosseguir.

## Suposições

Quando faltar informação não crítica, siga com padrões sensatos e liste-os numa seção explícita:

```markdown
### Suposições
- Idioma único: o mesmo idioma usado pelo usuário nesta conversa.
- Público majoritariamente mobile.
- Formulário de contato enviará e-mail (serviço a definir).
```

Decisões **críticas** nunca viram suposição — viram pergunta:
- stack/framework, hospedagem, CMS;
- identidade visual (cores, logo, tipografia de marca);
- funcionalidades e escopo de páginas;
- arquitetura de dados, autenticação, pagamentos;
- remoção ou reescrita de partes existentes.

## Saída

Briefing consolidado em `docs/website/briefing.md` (modelo em [references/templates.md](references/templates.md#briefing)), resumido no chat, aguardando confirmação.
