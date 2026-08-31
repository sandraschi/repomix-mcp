# Cursor MCP Configuration for Repomix MCP

## Configuration

Add this to your Cursor MCP settings. You can access Cursor MCP settings through:

1. **Cursor Settings UI**: `Settings > MCP > Add Server`
2. **Manual Configuration**: Edit `.cursor/mcp.json` in your workspace or user settings

### Recommended Configuration

```json
{
  "mcpServers": {
    "repomix": {
      "command": "python",
      "args": ["src/repomix_mcp/server.py"],
      "cwd": "${workspaceFolder}/repomix-mcp",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/repomix-mcp/src",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Alternative: Absolute Path Configuration

If you prefer absolute paths or have the repo in a fixed location:

```json
{
  "mcpServers": {
    "repomix": {
      "command": "python",
      "args": ["D:/Dev/repos/repomix-mcp/src/repomix_mcp/server.py"],
      "env": {
        "PYTHONPATH": "D:/Dev/repos/repomix-mcp/src",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

## Prerequisites

### 1. Install Repomix
Repomix must be installed globally for the MCP server to work:

```bash
npm install -g repomix
```

Verify installation:
```bash
repomix --version
```

### 2. Install Python Dependencies

```bash
cd D:\Dev\repos\repomix-mcp
pip install -r requirements.txt
```

### 3. Verify Server Startup

Test that the server starts manually:
```bash
cd D:\Dev\repos\repomix-mcp
python src/repomix_mcp/server.py
```

The server should start and show tool listings.

## Troubleshooting

### Server Won't Start

1. **Check Repomix Installation:**
   ```bash
   repomix --version
   ```
   If this fails, reinstall: `npm install -g repomix`

2. **Check Python Dependencies:**
   ```bash
   cd D:\Dev\repos\repomix-mcp
   pip install -r requirements.txt
   ```

3. **Test Manual Server Startup:**
   ```bash
   python src/repomix_mcp/server.py
   ```
   Should show tool registration without errors.

### MCP Tools Not Available

1. **Check Cursor MCP Settings:**
   - Open Cursor Settings
   - Navigate to MCP section
   - Verify the repomix server is listed and enabled

2. **Check Cursor Logs:**
   - Open Developer Tools (Help > Toggle Developer Tools)
   - Look for MCP-related errors in Console
   - Check for Python path issues

3. **Verify Configuration:**
   - Ensure paths are correct for your system
   - Check that PYTHONPATH includes the src directory
   - Verify the server.py file exists at the specified path

### Permission Issues

If you get permission errors:
1. Ensure you have read/write access to the workspace directory
2. Check that Node.js/npm can execute repomix
3. Verify Python can import the required modules

### Repository Access Issues

When packing repositories:
- Ensure the repository path exists and is accessible
- For remote repositories, ensure internet connectivity
- Check that git is available for remote repo operations

## Usage Examples

Once configured, you can use natural language commands like:

- "Pack this repository and analyze its structure"
- "Pack the src/ directory as markdown with compression"
- "Find all authentication-related code in the current repository"
- "Search for 'API_KEY' patterns in the packed output"

## Performance Notes

- **Large repositories**: May take time to pack - be patient
- **Compression**: Enabled by default for ~70% token reduction
- **Caching**: Packed outputs are saved to disk for reuse
- **Memory**: Large repos may require significant RAM

## Advanced Configuration

### Custom Repomix Options

You can modify the server code to add custom repomix options or change defaults.

### Multiple Instances

You can run multiple repomix MCP servers with different configurations by using different server names in Cursor settings.

## Related Documentation

- [Repomix Official Site](https://repomix.com/)
- [Cursor MCP Documentation](https://cursor.sh/docs/mcp)
- [FastMCP Framework](https://fastmcp.com/)