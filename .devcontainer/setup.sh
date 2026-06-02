#!/usr/bin/env bash
set -euo pipefail

# Install Claude Code (Anthropic). The ANTHROPIC_API_KEY Codespaces secret is read automatically
# at runtime; the default model is set via ANTHROPIC_MODEL in devcontainer.json.
npm install -g @anthropic-ai/claude-code

# Show the start command in every new interactive terminal so interns can't miss it. Idempotent.
if ! grep -qF "Start it with:  claude" "$HOME/.bashrc" 2>/dev/null; then
  cat >> "$HOME/.bashrc" <<'EOF'

# Intern reminder
if [[ $- == *i* ]]; then echo "👋 Your AI agent is ready. Start it with:  claude"; fi
EOF
fi

echo "Claude Code installed. Use it with:  claude"
