#!/usr/bin/env bash
# Configure Claude Code pour passer par OpenRouter.
# Usage : source scripts/openrouter-env.sh   (doit être « sourcé », pas exécuté)

if [ "${BASH_SOURCE[0]}" = "$0" ] && [ -z "${ZSH_VERSION:-}" ]; then
  echo "Ce script doit être sourcé : source scripts/openrouter-env.sh" >&2
  exit 1
fi

_or_root="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"

# Charge .env s'il existe (clé et modèles facultatifs).
if [ -f "$_or_root/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$_or_root/.env"
  set +a
fi
unset _or_root

if [ -z "${OPENROUTER_API_KEY:-}" ] || [ "$OPENROUTER_API_KEY" = "sk-or-..." ]; then
  echo "OPENROUTER_API_KEY absente : définissez-la dans .env ou dans l'environnement." >&2
  return 1
fi

export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""   # doit rester vide

[ -n "${ANTHROPIC_DEFAULT_SONNET_MODEL:-}" ] && export ANTHROPIC_DEFAULT_SONNET_MODEL
[ -n "${ANTHROPIC_DEFAULT_HAIKU_MODEL:-}" ] && export ANTHROPIC_DEFAULT_HAIKU_MODEL

echo "Claude Code → OpenRouter configuré (clé ...${OPENROUTER_API_KEY: -4})."
