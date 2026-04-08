# Tích hợp với AI Agents khác

Hầu hết MCP client dùng chung schema `mcpServers`. Copy block dưới vào file config tương ứng.

## Schema chung

```json
{
  "mcpServers": {
    "timgiup": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/timgiup/timgiup-mcp-server",
        "timgiup-mcp"
      ]
    }
  }
}
```

## File config theo từng agent

| Agent | OS | Path |
|-------|----|------|
| **Claude Desktop** | macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| | Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| | Linux | `~/.config/Claude/claude_desktop_config.json` |
| **Claude Code (CLI)** | mọi OS | `~/.claude.json` (mục `mcpServers`) hoặc dùng `claude mcp add` |
| **Cursor** | mọi OS | Settings → MCP, hoặc `~/.cursor/mcp.json` |
| **Cline (VS Code)** | mọi OS | `~/.cline/mcp_settings.json` (Settings → MCP Servers) |
| **Continue (VS Code/JetBrains)** | mọi OS | `~/.continue/config.json` (mục `mcpServers`) |
| **Windsurf** | mọi OS | `~/.codeium/windsurf/mcp_config.json` |
| **Zed** | mọi OS | `~/.config/zed/settings.json` (mục `context_servers`) |
| **Gemini CLI** | mọi OS | `~/.gemini/settings.json` (mục `mcpServers`) |
| **OpenCode** | mọi OS | `~/.config/opencode/config.json` (mục `mcp`) |
| **Antigravity (Google)** | mọi OS | Settings → MCP Servers (UI) |

## Cách dùng nhanh — Claude Code CLI

```bash
claude mcp add timgiup uvx -- --from git+https://github.com/timgiup/timgiup-mcp-server timgiup-mcp
```

## Cách dùng nhanh — Cursor

1. Mở Cursor Settings (`Cmd/Ctrl + ,`)
2. Tìm "MCP" → "Add new MCP server"
3. Nhập:
   - Name: `timgiup`
   - Command: `uvx`
   - Args: `--from git+https://github.com/timgiup/timgiup-mcp-server timgiup-mcp`

## Test kết nối

Sau khi config xong, restart agent. Trong chat thử prompt:

> "Tìm bài đăng mất CCCD ở TP HCM trên timgiup.com"

Agent sẽ tự gọi tool `search_lost_items` của MCP server.

## Lưu ý

- **`uvx` phải có sẵn**. Cài: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Một số MCP client (Claude Code, Claude Desktop) không load PATH của user shell** → phải dùng **absolute path** trong `command`, vd `/home/<user>/.local/bin/uvx` (Linux/macOS) hoặc `C:\Users\<user>\.local\bin\uvx.exe` (Windows). Tìm path bằng `which uvx`.
- Lần đầu chạy `uvx` sẽ tải code từ GitHub (~2-5s)
- Không cần biến môi trường — domain `https://timgiup.com` đã hardcoded

## Tham khảo mẫu

- [`claude-desktop-config.json`](claude-desktop-config.json) — Claude Desktop
- [`claude-code-config.json`](claude-code-config.json) — Claude Code CLI
