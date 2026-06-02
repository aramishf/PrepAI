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
if [ -n "${OPENAI_API_KEY:-}" ]; then
  codex login --api-key "$OPENAI_API_KEY" || echo "⚠ codex login failed — check the OPENAI_API_KEY secret value."
else
  echo "⚠ OPENAI_API_KEY not set. Add it as a Codespaces secret, then rebuild — or run:  codex login --api-key <key>"
fi

# Show the start command in every new interactive terminal so interns can't miss it. Idempotent.
if ! grep -qF "Start it with:  codex" "$HOME/.bashrc" 2>/dev/null; then
  cat >> "$HOME/.bashrc" <<'EOF'

# Intern reminder
if [[ $- == *i* ]]; then echo "👋 Your AI agent is ready. Start it with:  codex"; fi
EOF
fi

echo "Codex installed. Use it with:  codex"
