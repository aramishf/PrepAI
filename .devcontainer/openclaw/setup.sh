#!/usr/bin/env bash
set -euo pipefail

# postCreateCommand runs from the repo root — capture it so OpenClaw's agent operates IN the
# project files, not its default ~/.openclaw/workspace sandbox. Works for any team repo name.
WORKSPACE="$(pwd)"

# Install OpenClaw (Node 24 base image). SHARP_IGNORE_GLOBAL_LIBVIPS avoids a known native-dep build failure.
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest

# Configure OpenClaw to use Anthropic Claude and work inside the repo.
# - Reads ANTHROPIC_API_KEY from the environment (a Codespaces secret) — no key stored here.
# - Writing config directly is the documented headless path (skips the interactive onboard wizard).
# - gateway.mode=local is required for the gateway to start in a container.
# - agents.defaults.workspace points the agent at the repo so it edits the actual project.
# Note: unquoted heredoc so $WORKSPACE expands.
mkdir -p "$HOME/.openclaw"
cat > "$HOME/.openclaw/openclaw.json" <<EOF
{
  gateway: { mode: "local" },
  agents: { defaults: {
    workspace: "$WORKSPACE",
    model: { primary: "anthropic/claude-sonnet-4-6" }
  } },
}
EOF

# Keep OpenClaw's agent-workspace scaffolding out of git — it's local agent state, not project
# code, and would otherwise get committed via Commit & Sync. Uses .git/info/exclude (local, never
# committed/pushed), so the shared .gitignore stays clean. Idempotent.
EXCLUDE="$WORKSPACE/.git/info/exclude"
if [ -f "$EXCLUDE" ]; then
  for pat in ".openclaw/" "AGENTS.md" "SOUL.md" "IDENTITY.md" "HEARTBEAT.md" "TOOLS.md" "USER.md"; do
    grep -qxF "$pat" "$EXCLUDE" || echo "$pat" >> "$EXCLUDE"
  done
fi

echo "OpenClaw installed; agent workspace = $WORKSPACE"
echo "Use it with:  openclaw chat"
