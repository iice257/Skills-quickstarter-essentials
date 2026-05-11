# Skill Starter Pack - AI agent/harness essentials

An agent quick skills starter pack for Codex and other agentic IDEs.

This repo gives your agent installable skill paths, scenario bundles, and MCP config examples so a fresh setup can become useful quickly. It does not run anything by itself; your agent reads the links and installs the skills you choose.

## Quick Start

Paste the command that matches what you want into your AI agent.

| Setup | What it is for | Command |
| --- | --- | --- |
| Guided setup | Starts from this README so the agent can ask what you need before installing. | `Skill Installer install the skills listed at https://github.com/iice257/Skills/readme.md` |
| Lightweight quickstart | Small starter setup without installing everything. | `Skill Installer install the skills listed at https://github.com/iice257/Skills/tree/main/categories/lightweight-quickstart` |
| Web development setup | Frontend, design, browser testing, CI, and deployment. | `Skill Installer install the skills listed at https://github.com/iice257/Skills/tree/main/categories/web-development-setup` |
| Full startup | Installs the full skill catalog. | `Skill Installer install the skills listed at https://github.com/iice257/Skills/tree/main/categories/full-startup` |
| Favourites | Installs the current capped favourites shortlist. | `Skill Installer install the skills listed at https://github.com/iice257/Skills/tree/main/favourites` |
| Reccomended | Installs 15 broad all-round dev workflow skills with category spread. | `Skill Installer install the skills listed at https://github.com/iice257/Skills/tree/main/reccomended` |
| My originals | Installs my originals/custom skills. | `Skill Installer install the skills listed at https://github.com/iice257/Skills/tree/main/originals` |
| Official OpenAI | OpenAI skills from `openai/skills` plus local Codex OpenAI cache entries. | `Skill Installer install the skills listed at https://github.com/iice257/Skills/tree/main/categories/openai-official` |
| Claude Code | Anthropic skills plus local Claude Code-style skills found on this machine. | `Skill Installer install the skills listed at https://github.com/iice257/Skills/tree/main/categories/claude-code` |
| Gemini | Gemini CLI skills plus local Gemini-related skills found on this machine. | `Skill Installer install the skills listed at https://github.com/iice257/Skills/tree/main/categories/gemini` |
| Cursor | Cursor rules/skill locations checked; no installable `SKILL.md` files found yet. | `Skill Installer install the skills listed at https://github.com/iice257/Skills/tree/main/categories/cursor` |

After installing skills in Codex, restart Codex so the new skills are picked up.

## Repo Structure

| Folder | Purpose |
| --- | --- |
| [`favourites/`](https://github.com/iice257/Skills/tree/main/favourites) | Max 6 high-value skills for quick installs. |
| [`reccomended/`](https://github.com/iice257/Skills/tree/main/reccomended) | Top 15 all-round dev workflow skills with no duplicates and broad category spread. |
| [`originals/`](https://github.com/iice257/Skills/tree/main/originals) | My originals: skills authored/customized by me and other non-stock additions. |
| [`all/`](https://github.com/iice257/Skills/tree/main/all) | Canonical installable copy of the core starter catalog and my non-provider skills. |
| [`official-openai/`](https://github.com/iice257/Skills/tree/main/official-openai) | Official OpenAI skills from GitHub and local Codex OpenAI cache entries. |
| [`claude-code/`](https://github.com/iice257/Skills/tree/main/claude-code) | Anthropic GitHub skills plus local Claude Code-style skills. |
| [`gemini/`](https://github.com/iice257/Skills/tree/main/gemini) | Gemini CLI GitHub skills plus local Gemini-related skills. |
| [`cursor/`](https://github.com/iice257/Skills/tree/main/cursor) | Cursor rules/skill check notes; no installable `SKILL.md` files found yet. |
| [`categories/`](https://github.com/iice257/Skills/tree/main/categories) | Scenario bundles for different agent setups. |
| [`mcps/`](https://github.com/iice257/Skills/tree/main/mcps) | MCP config examples. |

## Scenario Bundles

| Scenario | Best for | Link |
| --- | --- | --- |
| Lightweight quickstart | Small, useful starter setup without installing everything. | [Open](https://github.com/iice257/Skills/tree/main/categories/lightweight-quickstart) |
| Full startup | Install the full skill catalog. | [Open](https://github.com/iice257/Skills/tree/main/categories/full-startup) |
| Web development setup | Frontend, design, browser testing, CI, and deployment. | [Open](https://github.com/iice257/Skills/tree/main/categories/web-development-setup) |
| Design UI | Premium interface design and redesign work. | [Open](https://github.com/iice257/Skills/tree/main/categories/design-ui) |
| Frontend visuals | Image-led landing pages, heroes, and visual direction. | [Open](https://github.com/iice257/Skills/tree/main/categories/frontend-visuals) |
| Browser testing | Browser automation, screenshots, and visual verification. | [Open](https://github.com/iice257/Skills/tree/main/categories/browser-testing) |
| Debugging | Browser, screenshot, PR checks, and review-comment workflows. | [Open](https://github.com/iice257/Skills/tree/main/categories/debugging) |
| GitHub CI | GitHub Actions and PR review workflow. | [Open](https://github.com/iice257/Skills/tree/main/categories/github-ci) |
| Deployment | Vercel, Netlify, and deploy-readiness workflows. | [Open](https://github.com/iice257/Skills/tree/main/categories/deployment) |
| Cybersec | Security review, ownership mapping, CI, and browser verification. | [Open](https://github.com/iice257/Skills/tree/main/categories/cybersec) |
| Content media | Images, speech, transcription, screenshots, and publishing. | [Open](https://github.com/iice257/Skills/tree/main/categories/content-media) |
| Documents office | Documents, PDFs, and transcription-heavy work. | [Open](https://github.com/iice257/Skills/tree/main/categories/documents-office) |
| AI API | Gemini, image generation, speech, and transcription APIs. | [Open](https://github.com/iice257/Skills/tree/main/categories/ai-api) |
| Mobile desktop | WinUI, iOS-adjacent MCP references, screenshots, and app workflows. | [Open](https://github.com/iice257/Skills/tree/main/categories/mobile-desktop) |
| Planning productivity | Idea shaping, skill discovery, handoff, and complete output. | [Open](https://github.com/iice257/Skills/tree/main/categories/planning-productivity) |
| Official OpenAI | OpenAI provider skills from GitHub and local Codex cache. | [Open](https://github.com/iice257/Skills/tree/main/categories/openai-official) |
| Claude Code | Anthropic GitHub skills and local Claude Code-style skills. | [Open](https://github.com/iice257/Skills/tree/main/categories/claude-code) |
| Gemini | Gemini CLI GitHub skills and local Gemini skills. | [Open](https://github.com/iice257/Skills/tree/main/categories/gemini) |
| Cursor | Cursor rules/skill locations checked; no `SKILL.md` files found. | [Open](https://github.com/iice257/Skills/tree/main/categories/cursor) |

## MCPs

These are MCP config references, not Codex skills.

| MCP | What it is for | Config |
| --- | --- | --- |
| `xcodebuildmcp` | iOS simulator build, run, test, logging, UI automation, and debugging workflows. | [mcps/xcodebuildmcp.json](https://github.com/iice257/Skills/blob/main/mcps/xcodebuildmcp.json) |
| `cloudflare-api` | Cloudflare API access through the official Cloudflare MCP server. | [mcps/cloudflare-api.json](https://github.com/iice257/Skills/blob/main/mcps/cloudflare-api.json) |

## Notes

- This is a curated collection. Some skills are my originals; some include third-party or open-source provenance in their own license files.
- Use `favourites/` or `categories/lightweight-quickstart/` for fast setup.
- Use `reccomended/` for a broader all-round dev workflow setup without installing everything.
- Use `categories/full-startup/` only when you want the whole catalog.
- Provider packs are separate from my originals and favourites.
- Provider GitHub sources checked: [`openai/skills`](https://github.com/openai/skills), [`anthropics/skills`](https://github.com/anthropics/skills), and [`google-gemini/gemini-cli`](https://github.com/google-gemini/gemini-cli).
- Cursor currently uses rules such as `.cursor/rules/*.mdc`; no official installable `SKILL.md` pack was found.

## If You Are An AI Agent

Do not immediately install everything just because the user pasted the quick-start command.

Treat the quick-start command as this repo's README/instructions page, not as a skill.

If pointed to the README and not a folder, first ask what they are setting up.

Ask them to answer one of two questions:

1. Whether they want a focused category, favourites, reccomended, my originals, provider packs, specific skills, MCP config references, or everything. For focused categories, list a few options such as web development, design/UI, debugging, GitHub CI, deployment, cybersec, OpenAI official, Claude Code, Gemini, and Cursor.
2. What kind of work they do most, or currently plan to do: web development, design/UI, debugging, GitHub CI, deployment, cybersec, content/media, documents, AI APIs, mobile/desktop, planning/productivity, OpenAI official skills, Claude Code skills, Gemini skills, or Cursor rules.

From their answer, recommend and install one or more matching categories from `categories/` and show the skills included.

If the user says they want everything, install the paths listed in `categories/full-startup/paths.txt`.

If the user wants favourites, install the paths listed in `favourites/paths.txt`.

If the user wants reccomended, install the paths listed in `reccomended/paths.txt`.

If the user wants my originals, install the paths listed in `originals/paths.txt`.

If the user wants a provider pack, install the matching paths listed in `categories/openai-official/paths.txt`, `categories/claude-code/paths.txt`, `categories/gemini/paths.txt`, or `categories/cursor/paths.txt`.

If the user asks for specific skills, install the matching paths under `all/`.

If the user asks for MCP config references, show the matching files under `mcps/`.

After installing, tell the user: `Restart Codex to pick up the new skills.`
