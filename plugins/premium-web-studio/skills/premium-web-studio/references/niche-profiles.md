# Perfis de nicho

Esta Skill atende **qualquer** nicho, mercado, país e idioma. Este arquivo oferece:

1. um **método** para derivar o perfil de qualquer segmento (use sempre);
2. **exemplos ilustrativos** de segmentos comuns (use como ponto de partida, nunca como regra).

O perfil final de cada projeto vem do briefing e da pesquisa de referências (fases 1, 3 e 4). Um mesmo nicho pode ter posicionamentos opostos (ex.: um escritório tradicional x uma lawtech), e um nicho ausente da lista é tratado com o mesmo método.

---

## 1. Método: derivar o perfil de qualquer nicho

Responda às perguntas abaixo com base no briefing e na pesquisa. O resultado alimenta a direção visual ([DESIGN.md](../DESIGN.md)).

| Dimensão | Pergunta | Exemplo de impacto |
|---|---|---|
| **Risco percebido** | Quanto o visitante arrisca ao escolher este fornecedor (dinheiro, saúde, liberdade, reputação)? | Risco alto → mais provas de confiança, sobriedade, transparência |
| **Frequência de decisão** | Compra por impulso, decisão recorrente ou decisão rara e ponderada? | Decisão rara → conteúdo mais profundo, comparativos, contato humano |
| **Tarefa principal** | O que o visitante veio fazer (comprar, agendar, encontrar informação, avaliar, se inscrever)? | Define a hierarquia e o CTA |
| **Perfil do público** | Idade, familiaridade digital, dispositivo, conectividade, necessidades de acessibilidade | Público amplo ou vulnerável → motion 0–1, alto contraste, linguagem simples |
| **Expectativa estética do mercado** | O que os líderes do segmento fazem e o que o público entende como "profissional" aqui? | Convenções a respeitar antes de diferenciar |
| **Regulação** | Há regras legais ou de órgãos de classe sobre publicidade, informações obrigatórias, dados, acessibilidade? | Restringe promessas, depoimentos, imagens e exige avisos |
| **Provas de confiança disponíveis** | Registros profissionais, certificações, clientes, casos, avaliações, imprensa, tempo de mercado — quais são reais e verificáveis? | Define seções de credibilidade (nunca invente) |
| **Natureza do produto** | Tangível (o produto é a estrela) ou serviço/intangível (pessoas, processo e resultados são a estrela)? | Direção de imagem e estrutura das páginas |
| **Conteúdo** | Volume, frequência de atualização e quem edita | Arquitetura, CMS e templates de página |
| **Contexto cultural e local** | Idioma, convenções de contato (telefone, e-mail, mensageiros), formatos de data, moeda e endereço, simbologia de cores | Microcopy, formulários, CTAs e paleta |

Resuma o perfil em 5 linhas no `design-direction.md`: **Prioridades · Tom visual · Nível de motion · Provas de confiança · O que evitar**.

### Regulação: como tratar sem presumir um país
- Pergunte no discovery em qual país/mercado o site opera e se o setor é regulado.
- Exemplos de setores com regras de comunicação frequentes: jurídico, saúde, finanças e investimentos, imobiliário, educação, alimentos e bebidas, farmacêutico, seguros, setor público.
- Se não souber a regra local com segurança, **não invente**: sinalize ao usuário que o conteúdo precisa de revisão por quem conhece a norma do setor.

---

## 2. Exemplos ilustrativos

Formato: **Prioridades** · **Tom visual** · **Motion** (nível de [DESIGN.md](../DESIGN.md#7-motion)) · **Confiança** · **Evitar**. Órgãos e normas citados são exemplos de categoria; confirme os equivalentes do país do projeto.

### Governo e serviços públicos
- **Prioridades:** clareza, acessibilidade (normalmente obrigatória por lei), navegação previsível, busca, linguagem simples, páginas leves, funcionamento em dispositivos antigos e conexões lentas.
- **Tom visual:** sóbrio, tipografia altamente legível, alto contraste, hierarquia funcional. Verifique se existe um design system governamental oficial no país (ex.: GOV.UK Design System, U.S. Web Design System, padrões digitais nacionais) e se seu uso é obrigatório.
- **Motion:** 0.
- **Confiança:** informação oficial, datas de atualização, canais de atendimento, transparência.
- **Evitar:** carrosséis, efeitos decorativos, jargão, PDFs como única forma de conteúdo.

### Serviços jurídicos
- **Prioridades:** credibilidade, áreas de atuação claras, perfis dos profissionais, contato facilitado.
- **Tom visual:** elegante e contido; tipografia de alta qualidade; paleta restrita; espaço em branco generoso; fotografia profissional real.
- **Motion:** 1.
- **Confiança:** formação e registro profissional na entidade de classe do país, publicações, casos (respeitando sigilo e as regras de publicidade profissional locais), endereço físico.
- **Evitar:** clichês (martelos, balanças, colunas gregas), promessas de resultado, linguagem comercial vedada pela regulação local.

### Finanças e investimentos
- **Prioridades:** segurança percebida, clareza de taxas e produtos, conformidade regulatória, acessibilidade.
- **Tom visual:** preciso, estruturado, dados bem apresentados, números tabulares.
- **Motion:** 1 (2 para produtos voltados a público jovem).
- **Confiança:** autorização do regulador financeiro do país, segurança, transparência de custos, suporte, avisos de risco obrigatórios.
- **Evitar:** gráficos decorativos sem dados reais, promessas de rentabilidade.

### Saúde
- **Prioridades:** agendamento, especialidades, localização, cobertura/planos aceitos, acolhimento, acessibilidade (público amplo e idoso).
- **Tom visual:** calmo, humano, legível; fotografia real da equipe e do espaço.
- **Motion:** 0–1.
- **Confiança:** registros profissionais, credenciais, estrutura, conformidade com as regras de publicidade dos conselhos de saúde locais (muitas vedam antes/depois e promessas).
- **Evitar:** imagens genéricas de banco, ícones médicos clichês, excesso de efeitos.

### SaaS e produtos de tecnologia
- **Prioridades:** proposta de valor clara em segundos, demonstração do produto, preços, prova social, conversão para trial/demo.
- **Tom visual:** contemporâneo, pode ser ousado; screenshots/vídeos reais do produto; tipografia expressiva.
- **Motion:** 2 (3 em lançamentos).
- **Confiança:** clientes reais, casos com números reais, segurança e compliance (certificações efetivamente obtidas), changelog, página de status.
- **Evitar:** gradiente roxo genérico, mockups abstratos sem produto real, hero vago ("A plataforma do futuro").

### E-commerce
- **Prioridades:** descoberta de produtos (busca, filtros, categorias), páginas de produto completas, velocidade, checkout simples, confiança, mobile.
- **Tom visual:** o produto é o protagonista; interface discreta e consistente; fotografia de produto de alta qualidade.
- **Motion:** 1 (microinterações de carrinho e feedback).
- **Confiança:** avaliações reais, política de troca, frete e prazos claros, meios de pagamento, identificação legal da empresa, contato.
- **Evitar:** pop-ups agressivos, carrosséis automáticos no hero, custos escondidos até o checkout. Consulte pesquisas de UX de e-commerce (ex.: Baymard Institute).

### Gastronomia e hospitalidade
- **Prioridades:** cardápio legível em HTML (não PDF), reservas, localização, horário, atmosfera.
- **Tom visual:** sensorial, fotografia autoral, tipografia com personalidade coerente com a casa.
- **Motion:** 1–2.
- **Confiança:** avaliações, equipe, imprensa.
- **Evitar:** cardápio em PDF ou imagem, áudio automático, vídeos pesados no mobile.

### Imobiliário e arquitetura
- **Prioridades:** busca e filtros, galerias de alta qualidade, plantas, localização, contato rápido pelo canal culturalmente preferido no mercado.
- **Tom visual:** editorial, grandes imagens, grid limpo.
- **Motion:** 1–2.
- **Confiança:** registro profissional local, histórico de projetos, documentação.
- **Evitar:** galerias lentas, imagens sem otimização.

### Educação
- **Prioridades:** cursos e grades, processo de inscrição, calendário, públicos distintos (alunos, responsáveis, docentes), acessibilidade.
- **Tom visual:** de institucional (universidade) a energético (cursos livres), conforme o posicionamento.
- **Motion:** 0–2 conforme o público.
- **Confiança:** credenciamento oficial, resultados reais, corpo docente, depoimentos verificáveis.

### Organizações sem fins lucrativos
- **Prioridades:** causa clara, impacto mensurável, doação simples, voluntariado, transparência.
- **Tom visual:** humano, histórias reais, fotografia autêntica com consentimento.
- **Motion:** 1.
- **Confiança:** prestação de contas, registro legal, parceiros, relatórios.

### Indústria e B2B
- **Prioridades:** catálogo técnico, especificações, certificações, contato comercial, downloads.
- **Tom visual:** robusto, técnico, objetivo; fotografia real de processos e produtos.
- **Motion:** 1.
- **Confiança:** certificações (ex.: ISO), clientes, tempo de mercado, capacidade produtiva.

### Agências, estúdios e portfólios criativos
- **Prioridades:** trabalho em destaque, personalidade, cases com processo, contato.
- **Tom visual:** autoral, experimental quando coerente; é o segmento com mais liberdade.
- **Motion:** 2–3, preservando performance e acessibilidade.
- **Evitar:** experimentação que esconda o trabalho ou bloqueie a navegação.

### Eventos e lançamentos
- **Prioridades:** data, local, programação, inscrição/ingressos, urgência real.
- **Tom visual:** identidade forte do evento.
- **Motion:** 2–3.
- **Evitar:** contadores falsos de escassez.

### Turismo e hotelaria
- **Prioridades:** reserva direta, galerias, localização, disponibilidade, avaliações, múltiplos idiomas.
- **Tom visual:** imersivo, fotografia de alta qualidade.
- **Motion:** 1–2.
