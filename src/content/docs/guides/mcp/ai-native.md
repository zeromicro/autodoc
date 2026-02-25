---
title: AI-Assisted go-zero Development
description: Make AI coding assistants (Copilot, Claude, Cursor) experts in go-zero using ai-context, zero-skills, and mcp-zero
sidebar:
  order: 3
---

import { Card, CardGrid, Aside } from '@astrojs/starlight/components';


In the AI-assisted coding era, how do you make your AI coding assistant truly understand your framework and generate spec-compliant code? The go-zero team has built a complete AI tooling ecosystem around three projects:

<CardGrid>
  <Card title="ai-context" icon="document">
    A concise instruction layer (~5KB). Tells AI **what to do** — workflows, tool usage, quick-reference patterns.
  </Card>
  <Card title="zero-skills" icon="open-book">
    A detailed knowledge base (~40KB+). Tells AI **how to do it well** — patterns, best practices, troubleshooting.
  </Card>
  <Card title="mcp-zero" icon="rocket">
    A runtime MCP server. Lets AI **actually do it** — create services, generate models, validate specs.
  </Card>
</CardGrid>

## How They Work Together

```
┌─────────────────────────────────────┐
│ AI Assistant (Claude/Copilot/Cursor) │
└────────────┬────────────────────────┘
             │
    ┌────────┴──────────┐
    │                   │
    ▼                   ▼
┌──────────┐       ┌──────────┐
│ai-context│       │ mcp-zero │
│          │       │          │
│ Workflows│       │  Tools   │
│ Patterns │       │  Code    │
└────┬─────┘       └────┬─────┘
     │                  │
     │    ┌─────────────┘
     │    │
     ▼    ▼
┌──────────────┐
│ zero-skills  │
│              │
│  Patterns    │
│  Examples    │
│ Troubleshoot │
└──────────────┘
```

**Example: Create a REST API**
1. AI reads `ai-context` → learns to use `create_api_service` tool
2. AI calls `mcp-zero` → generates the project structure
3. AI references `zero-skills` → produces Handler/Logic/Model code following go-zero conventions

## Setup by Tool

### GitHub Copilot

```bash
# Add ai-context as a submodule (tracks upstream updates automatically)
git submodule add https://github.com/zeromicro/ai-context.git .github/ai-context

# Create symlink for Copilot
ln -s ai-context/00-instructions.md .github/copilot-instructions.md

# Update to latest
git submodule update --remote .github/ai-context
```

### Cursor

```bash
git submodule add https://github.com/zeromicro/ai-context.git .cursorrules
git submodule update --remote .cursorrules
```

Cursor auto-reads all `.md` files in `.cursorrules/` as project rules.

### Windsurf (Codeium)

```bash
git submodule add https://github.com/zeromicro/ai-context.git .windsurfrules
git submodule update --remote .windsurfrules
```

### Claude Desktop + mcp-zero

**1. Build mcp-zero:**

```bash
git clone https://github.com/zeromicro/mcp-zero.git
cd mcp-zero
go build -o mcp-zero main.go
```

**2. Configure Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "mcp-zero": {
      "command": "/path/to/mcp-zero",
      "env": {
        "GOCTL_PATH": "/Users/yourname/go/bin/goctl"
      }
    }
  }
}
```

**3.** Restart Claude Desktop. Claude will now use `mcp-zero` tools to generate go-zero code.

### Claude Code (CLI)

```bash
claude mcp add \
  --transport stdio \
  mcp-zero \
  --env GOCTL_PATH=/Users/yourname/go/bin/goctl \
  -- /path/to/mcp-zero

claude mcp list     # verify
```

## Project Descriptions

### ai-context

**Repo:** https://github.com/zeromicro/ai-context

A lightweight instruction file (~5KB) that provides:
- **Workflows**: When to use which tool
- **Tool usage**: How to call mcp-zero
- **Quick patterns**: Short code snippets for common tasks

Example decision tree from ai-context:
```markdown
User Request →
├─ New API? → create_api_service → generate_api_from_spec
├─ New RPC? → create_rpc_service
├─ Database? → generate_model
└─ Modify? → Edit .api → generate_api_from_spec
```

### zero-skills

**Repo:** https://github.com/zeromicro/zero-skills

A comprehensive knowledge base (~40KB+):
- **Patterns**: REST API, RPC, database, resilience
- **Best practices**: Production-grade code standards with ✅ correct vs ❌ common mistakes
- **Troubleshooting**: Solutions to frequent issues
- **Getting started**: End-to-end examples

### mcp-zero

**Repo:** https://github.com/zeromicro/mcp-zero

A [Model Context Protocol](./index.md) server with 10+ tools:
- Create API / RPC services
- Generate model code from SQL
- Validate `.api` specs and `.proto` definitions
- Query go-zero documentation
- Analyze existing project structure

## Before vs After

**Without the AI tool ecosystem:**
```
Developer: Create a user API

AI: Here's a basic HTTP handler...
[generates generic Go HTTP code, not go-zero conventions]

Developer: That's not how go-zero works — handlers should call the logic layer

AI: Sorry, here's the updated code...
[multiple rounds needed to get correct code]
```

**With the AI tool ecosystem:**
```
Developer: Create a user API

AI: I'll follow go-zero's three-layer architecture...
[immediately generates correct Handler → Logic → Model structure]
[includes proper error handling, context propagation, validation]

Developer: Perfect! ✅
```

## Design Principles

| Principle | Benefit |
|-----------|---------|
| **Layered** — ai-context (5KB) for speed, zero-skills (40KB+) for depth | Fast responses + deep knowledge |
| **Single source of truth** — zero-skills is the canonical reference | Update once, affects all tools |
| **AI-optimized structure** — ✅/❌ examples, structured Markdown | Better AI parsing and output |
| **Full lifecycle coverage** | Create → generate → debug → optimize |

<Aside type="tip">
Using submodules ensures your project automatically tracks upstream updates to ai-context and zero-skills. Run `git submodule update --remote` to pull the latest.
</Aside>

## Related

- [MCP Server Overview](./index.md)
- [MCP Servers Reference](./servers.md)
