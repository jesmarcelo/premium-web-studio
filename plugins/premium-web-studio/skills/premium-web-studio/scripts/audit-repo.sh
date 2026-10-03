#!/usr/bin/env bash
# Panorama rápido de um repositório web existente. Somente leitura.
# Não lê nem exibe o conteúdo de arquivos .env.
# Uso: bash <SKILL_DIR>/scripts/audit-repo.sh [raiz-do-projeto]

set -u

ROOT="${1:-$(pwd)}"
cd "$ROOT" || { echo "Diretório inválido: $ROOT"; exit 1; }

IGNORE='node_modules|\.git|dist|build|\.next|\.nuxt|\.svelte-kit|\.astro|\.output|\.vercel|\.netlify|coverage|vendor|\.cache|tmp'

section() { printf '\n== %s ==\n' "$1"; }

section "Raiz"
pwd

section "Git"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Branch: $(git branch --show-current 2>/dev/null)"
  changes=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  echo "Arquivos com alterações não commitadas: $changes"
  git log --oneline -5 2>/dev/null
else
  echo "Não é um repositório git"
fi

section "Estrutura (até 3 níveis)"
find . -maxdepth 3 -not -path '*/.*' 2>/dev/null \
  | grep -Ev "/($IGNORE)(/|$)" \
  | sort | head -150

section "Manifestos e lockfiles"
for f in package.json pnpm-lock.yaml package-lock.json yarn.lock bun.lockb bun.lock \
         composer.json Gemfile pyproject.toml requirements.txt go.mod Cargo.toml; do
  [ -f "$f" ] && echo "$f"
done

if [ -f package.json ]; then
  section "package.json — nome, scripts e dependências"
  if command -v node >/dev/null 2>&1; then
    node -e '
      const p = require("./package.json");
      console.log("name:", p.name || "-", "| type:", p.type || "commonjs", "| engines:", JSON.stringify(p.engines || {}));
      console.log("\nscripts:"); for (const [k,v] of Object.entries(p.scripts || {})) console.log(`  ${k}: ${v}`);
      console.log("\ndependencies:"); for (const [k,v] of Object.entries(p.dependencies || {})) console.log(`  ${k}@${v}`);
      console.log("\ndevDependencies:"); for (const [k,v] of Object.entries(p.devDependencies || {})) console.log(`  ${k}@${v}`);
    '
  else
    cat package.json
  fi
fi

section "Indícios de framework e ferramentas"
for f in next.config.js next.config.mjs next.config.ts astro.config.mjs astro.config.ts \
         nuxt.config.ts nuxt.config.js svelte.config.js vite.config.ts vite.config.js \
         remix.config.js react-router.config.ts angular.json gatsby-config.js \
         tailwind.config.js tailwind.config.ts postcss.config.js postcss.config.mjs \
         tsconfig.json jsconfig.json eslint.config.js eslint.config.mjs .eslintrc.json .eslintrc.cjs \
         .prettierrc .prettierrc.json prettier.config.js biome.json \
         theme.json style.css functions.php wp-config.php \
         vercel.json netlify.toml wrangler.toml Dockerfile .github/workflows; do
  [ -e "$f" ] && echo "$f"
done

section "Possíveis tokens / estilos globais"
find . -type f \( -name 'globals.css' -o -name 'global.css' -o -name 'tokens.*' -o -name 'theme.*' \
  -o -name 'variables.*' -o -name '_variables.*' -o -name 'app.css' -o -name 'main.css' \) 2>/dev/null \
  | grep -Ev "/($IGNORE)/" | head -30

section "Componentes (diretórios)"
find . -type d \( -iname 'components' -o -iname 'ui' -o -iname 'sections' -o -iname 'layouts' \) 2>/dev/null \
  | grep -Ev "/($IGNORE)/" | head -30

section "Rotas / páginas (diretórios)"
find . -type d \( -name 'app' -o -name 'pages' -o -name 'routes' \) 2>/dev/null \
  | grep -Ev "/($IGNORE)/" | head -20

section "Variáveis de ambiente (apenas nomes de arquivo)"
ls -1a 2>/dev/null | grep -E '^\.env' || echo "nenhum arquivo .env*"
if [ -f .env.example ]; then
  echo "Variáveis esperadas (.env.example):"
  grep -Eo '^[A-Z0-9_]+' .env.example
fi
if [ -f .gitignore ]; then
  grep -qE '^\.env' .gitignore && echo ".gitignore cobre .env: sim" || echo ".gitignore cobre .env: NÃO VERIFICADO/AUSENTE"
else
  echo ".gitignore ausente"
fi

section "Documentação existente"
ls -1 README* CLAUDE.md AGENTS.md CONTRIBUTING* docs 2>/dev/null

echo
echo "Próximos passos: ler os arquivos de config relevantes e rodar build/lint/typecheck para registrar a linha de base."
