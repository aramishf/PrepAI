#!/usr/bin/env bash
set -euo pipefail

# Install OpenAI Codex CLI (Node 22 base image satisfies the Node 22+ requirement).
npm install -g @openai/codex

# Force API-key auth so Codex never falls back to the ChatGPT browser/OAuth login (bad in a container).
mkdir -p "$HOME/.codex"
cat > "$HOME/.codex/config.toml" <<'EOF'
forced_login_method = "api"
EOF

# Cache the API key so interactive `codex` works without a browser. The OPENAI_API_KEY Codespaces
# secret is in the environment. (Interactive Codex does NOT auto-read OPENAI_API_KEY — it needs this
# login step to write ~/.codex/auth.json.)
# Cache the API key + greet on the first interactive terminal. Done at RUNTIME (not build) because
# the OPENAI_API_KEY Codespaces secret is reliably present in the terminal env (but not always at
# build), and Codex's interactive mode doesn't auto-read it. Current Codex pipes the key via stdin
# (the old `--api-key` flag was removed). Guarded so the login runs only once. Idempotent.
if ! grep -qF "Start it with:  codex" "$HOME/.bashrc" 2>/dev/null; then
  cat >> "$HOME/.bashrc" <<'EOF'

# Codex: cache the API key on first interactive shell, then show the start command.
if [[ $- == *i* ]]; then
  if [ ! -f "$HOME/.codex/auth.json" ] && [ -n "${OPENAI_API_KEY:-}" ]; then
    printenv OPENAI_API_KEY | codex login --with-api-key >/dev/null 2>&1 && echo "✅ Codex authenticated."
  fi
  echo "👋 Your AI agent is ready. Start it with:  codex"
fi
EOF
fi

echo "Codex installed. Use it with:  codex"
