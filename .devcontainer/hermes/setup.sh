#!/usr/bin/env bash
set -euo pipefail

# Install Hermes Agent (Nous Research). The installer brings its own Python 3.11 via uv (no base
# image dependency), needs no sudo for Hermes itself, and auto-skips its setup wizard on non-TTY.
# Flags make it explicitly non-interactive and skip the slow optional Playwright/Chromium download.
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh \
  | bash -s -- --non-interactive --skip-setup --skip-browser

# Configure provider = Anthropic Claude. Hermes reads ANTHROPIC_API_KEY from the environment
# (injected as a Codespaces secret); config.yaml just pins the provider + model. claude-sonnet-4-6
# clears Hermes' >=64k context requirement.
mkdir -p "$HOME/.hermes"
cat > "$HOME/.hermes/config.yaml" <<'EOF'
model:
  provider: "anthropic"
  default: "claude-sonnet-4-6"
EOF

# Show the start command in every new interactive terminal so interns can't miss it.
# (Also why a fresh terminal matters here: PATH for ~/.local/bin only applies to new shells.)
# Idempotent.
if ! grep -qF "Start it with:  hermes" "$HOME/.bashrc" 2>/dev/null; then
  cat >> "$HOME/.bashrc" <<'EOF'

# Intern reminder
if [[ $- == *i* ]]; then echo "👋 Your AI agent is ready. Start it with:  hermes"; fi
EOF
fi

echo "Hermes installed at ~/.local/bin/hermes."
echo "Open a NEW terminal (so PATH picks up ~/.local/bin), then run:  hermes"
