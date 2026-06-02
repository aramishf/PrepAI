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

echo "Hermes installed at ~/.local/bin/hermes."
echo "Open a NEW terminal (so PATH picks up ~/.local/bin), then verify with:"
echo "  hermes --help"
echo "  hermes            # then ask it something, e.g. 'Summarize this repo in 5 bullets'"
