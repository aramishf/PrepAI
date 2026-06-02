#!/usr/bin/env bash
set -euo pipefail

# Install OpenClaw (Node 24 base image). SHARP_IGNORE_GLOBAL_LIBVIPS avoids a known native-dep build failure.
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest

# Configure OpenClaw to use Anthropic Claude.
# It reads ANTHROPIC_API_KEY from the environment (injected as a Codespaces secret), so we only
# need to set the model. Writing the config directly is the documented headless path — it avoids
# the interactive `openclaw onboard` wizard (which is interactive-by-default; see issue #1950).
mkdir -p "$HOME/.openclaw"
cat > "$HOME/.openclaw/openclaw.json" <<'EOF'
{
  agents: { defaults: { model: { primary: "anthropic/claude-sonnet-4-6" } } },
}
EOF

echo "OpenClaw installed. Verify with:"
echo "  openclaw --version"
echo "  openclaw models list --provider anthropic   # empty list = ANTHROPIC_API_KEY missing/wrong"
