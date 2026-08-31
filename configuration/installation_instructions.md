# Repomix MCP Server Installation

This extension integrates Repomix as a Model Context Protocol (MCP) server for Zed's Assistant, allowing you to pack and analyze codebases for AI consumption.

## What is Repomix?

Repomix is a tool that packs your entire repository into a single AI-friendly file. It's particularly useful for:
- Providing comprehensive codebase context to AI assistants
- Analyzing repository structure and dependencies
- Creating shareable codebase snapshots for AI analysis

## Installation

1. **Install the extension** from the Zed extension marketplace
2. **Install Repomix globally** (required):
   ```bash
   npm install -g repomix
   ```

## Configuration

### Basic Setup

After installing the extension, enable it in your Zed settings:

1. Open Zed settings (Cmd+, on macOS or Ctrl+, on Linux/Windows)
2. Add the following to your settings:

```json
{
  "context_servers": {
    "mcp-server-repomix": {}
  }
}
```

### Custom Repomix Path (Optional)

If you have Repomix installed in a custom location, you can specify the path:

```json
{
  "context_servers": {
    "mcp-server-repomix": {
      "settings": {
        "repomix_path": "/custom/path/to/repomix"
      }
    }
  }
}
```

## Remote Repositories

Repomix can pack remote repositories by providing a repository URL using either:
- **HTTPS**: `https://github.com/user/repo`
- **SSH**: `git@github.com:user/repo.git`

Simply pass the repository URL to the pack repository tool.

## Usage

### Agent Mode

To use Repomix in agent mode:

1. Enable the MCP server in your assistant settings
2. The assistant will have access to Repomix tools for packing repositories

### Available Tools

The MCP server provides the following tools:

- **pack_repository**: Pack a local or remote repository into a single file
- **read_packed_output**: Read and analyze the packed repository output
- **search_packed_output**: Search for specific patterns in the packed output

## Verification

To verify the extension is working:

1. Open the Zed Assistant panel
2. Check that "Repomix MCP Server" appears in the list of available context servers
3. Try using the Repomix tools in your conversation

## Troubleshooting

### Server Not Starting

If the server fails to start:

1. Ensure Repomix is installed globally: `npm list -g repomix`
2. Check that Node.js is installed: `node --version`
3. Verify the extension is enabled in your settings
4. Restart Zed after making configuration changes

### Permission Issues

If you encounter permission errors:

1. Ensure you have write permissions in the project directory
2. Check that Repomix can execute: `which repomix`
3. Verify Node.js permissions



## Learn More

- [Repomix Documentation](https://repomix.com)
- [Repomix GitHub Repository](https://github.com/yamadashy/repomix)
- [Repomix Remote Repository Processing](https://repomix.com/guide/remote-repository-processing)
- [MCP Documentation](https://modelcontextprotocol.io)
- [Zed Extensions Guide](https://zed.dev/docs/extensions)

## Support

For issues and questions:
- Extension issues: [Report on GitHub](https://github.com/mlopezgez/zed-mcp-server-repomix/issues)
- Repomix issues: [Report on Repomix GitHub](https://github.com/yamadashy/repomix/issues)
