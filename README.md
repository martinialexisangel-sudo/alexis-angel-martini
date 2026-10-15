# alexis-angel-martini
## Utiliser Claude Code via OpenRouter (machine locale)

1. Copier le modèle de configuration : `cp .env.example .env`
2. Renseigner la vraie clé dans `.env` (clé : <https://openrouter.ai/settings/keys>).
   `.env` est exclu de git par `.gitignore` — ne jamais versionner la clé.
3. Charger les variables dans le shell courant, puis lancer Claude Code :
   ```bash
   source scripts/openrouter-env.sh
   claude
   ```
4. Vérifier avec `/status` dans Claude Code et sur <https://openrouter.ai/activity>.

Variables définies par le script : `ANTHROPIC_BASE_URL=https://openrouter.ai/api`,
`ANTHROPIC_AUTH_TOKEN=$OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY=""` (doit rester vide).
Les modèles par défaut peuvent être fixés dans `.env` ; vérifier les identifiants
exacts sur <https://openrouter.ai/models>.

Remarque : cela ne concerne que Claude Code lancé localement, pas les sessions cloud.
