#!/usr/bin/env python3
"""
Repomix MCP Server - Pack repositories into AI-friendly formats

This MCP server provides tools to pack entire repositories using Repomix,
making it easy for AI assistants to analyze and understand complete codebases.
"""

import os
import subprocess
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from pydantic import BaseModel, Field

# Create MCP server instance
mcp = FastMCP("repomix-mcp")


class PackRepositoryRequest(BaseModel):
    """Request to pack a repository using Repomix."""

    repository_path: str = Field(..., description="Path to the repository to pack")
    output_file: str | None = Field(None, description="Output file path (optional, defaults to repomix-output.xml)")
    style: str | None = Field("xml", description="Output format: xml, markdown, json, plain")
    include_patterns: list[str] | None = Field(None, description="Glob patterns to include")
    ignore_patterns: list[str] | None = Field(None, description="Glob patterns to ignore")
    compress: bool | None = Field(False, description="Use Tree-sitter compression for ~70% token reduction")


class SearchPackedOutputRequest(BaseModel):
    """Request to search within packed repository output."""

    packed_file_path: str = Field(..., description="Path to the packed output file")
    query: str = Field(..., description="Search query/pattern")
    case_sensitive: bool | None = Field(False, description="Case sensitive search")


class ReadPackedOutputRequest(BaseModel):
    """Request to read packed repository output."""

    packed_file_path: str = Field(..., description="Path to the packed output file")
    max_lines: int | None = Field(100, description="Maximum lines to return")


@mcp.tool()
async def pack_repository(request: PackRepositoryRequest) -> dict[str, Any]:
    """
    Pack a repository into an AI-friendly format using Repomix.

    This tool uses Repomix to convert entire repositories into single files
    optimized for AI consumption, supporting multiple output formats and
    intelligent code compression.

    Args:
        request: PackRepositoryRequest with repository details and options

    Returns:
        Dict containing success status, output file path, and metadata
    """
    try:
        # Check if repomix is installed
        try:
            subprocess.run(["repomix", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {"success": False, "error": "Repomix is not installed. Install with: npm install -g repomix"}

        # Build repomix command
        cmd = ["repomix"]

        # Add repository path
        repo_path = Path(request.repository_path).resolve()
        if not repo_path.exists():
            return {"success": False, "error": f"Repository path does not exist: {repo_path}"}
        cmd.append(str(repo_path))

        # Add output file
        output_file = request.output_file or "repomix-output.xml"
        cmd.extend(["--output", output_file])

        # Add style/format
        if request.style:
            cmd.extend(["--style", request.style])

        # Add include patterns
        if request.include_patterns:
            for pattern in request.include_patterns:
                cmd.extend(["--include", pattern])

        # Add ignore patterns
        if request.ignore_patterns:
            for pattern in request.ignore_patterns:
                cmd.extend(["--ignore", pattern])

        # Add compression
        if request.compress:
            cmd.append("--compress")

        # Run repomix
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())

        if result.returncode == 0:
            # Get file size
            output_path = Path(output_file)
            file_size = output_path.stat().st_size if output_path.exists() else 0

            return {
                "success": True,
                "message": f"Successfully packed repository {repo_path.name}",
                "output_file": str(output_path.absolute()),
                "file_size": file_size,
                "format": request.style,
                "compressed": request.compress,
                "repository": str(repo_path),
            }
        else:
            return {"success": False, "error": f"Repomix failed: {result.stderr}", "stdout": result.stdout}

    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


@mcp.tool()
async def read_packed_output(request: ReadPackedOutputRequest) -> dict[str, Any]:
    """
    Read and analyze packed repository output.

    This tool reads the content of packed repository files created by Repomix,
    providing insights into the codebase structure and content.

    Args:
        request: ReadPackedOutputRequest with file path and options

    Returns:
        Dict containing success status and file content/metadata
    """
    try:
        packed_file = Path(request.packed_file_path)

        if not packed_file.exists():
            return {"success": False, "error": f"Packed file does not exist: {packed_file}"}

        # Read file content
        with open(packed_file, encoding="utf-8", errors="replace") as f:
            content = f.read()

        lines = content.split("\n")
        total_lines = len(lines)

        # Limit content if requested
        if request.max_lines and total_lines > request.max_lines:
            content = "\n".join(lines[: request.max_lines])
            truncated = True
        else:
            truncated = False

        # Get file metadata
        file_size = packed_file.stat().st_size

        return {
            "success": True,
            "message": f"Read packed output: {packed_file.name}",
            "file_path": str(packed_file.absolute()),
            "file_size": file_size,
            "total_lines": total_lines,
            "content": content,
            "truncated": truncated,
            "max_lines_shown": request.max_lines if truncated else total_lines,
        }

    except Exception as e:
        return {"success": False, "error": f"Failed to read packed output: {e!s}"}


@mcp.tool()
async def search_packed_output(request: SearchPackedOutputRequest) -> dict[str, Any]:
    """
    Search for patterns within packed repository output.

    This tool searches through packed repository files to find specific
    code patterns, functions, or text matches.

    Args:
        request: SearchPackedOutputRequest with search parameters

    Returns:
        Dict containing success status and search results
    """
    try:
        packed_file = Path(request.packed_file_path)

        if not packed_file.exists():
            return {"success": False, "error": f"Packed file does not exist: {packed_file}"}

        # Read file content
        with open(packed_file, encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Perform search
        if request.case_sensitive:
            matches = content.count(request.query)
            found_lines = []
            for i, line in enumerate(content.split("\n"), 1):
                if request.query in line:
                    found_lines.append({"line_number": i, "content": line.strip()})
        else:
            query_lower = request.query.lower()
            matches = content.lower().count(query_lower)
            found_lines = []
            for i, line in enumerate(content.split("\n"), 1):
                if query_lower in line.lower():
                    found_lines.append({"line_number": i, "content": line.strip()})

        # Limit results to prevent overwhelming responses
        max_results = 50
        if len(found_lines) > max_results:
            found_lines = found_lines[:max_results]
            truncated = True
        else:
            truncated = False

        return {
            "success": True,
            "message": f"Found {matches} matches for '{request.query}'",
            "query": request.query,
            "case_sensitive": request.case_sensitive,
            "total_matches": matches,
            "results": found_lines,
            "truncated": truncated,
            "max_results_shown": max_results if truncated else len(found_lines),
        }

    except Exception as e:
        return {"success": False, "error": f"Failed to search packed output: {e!s}"}


@mcp.tool()
async def list_supported_formats() -> dict[str, Any]:
    """
    List supported output formats and compression options for Repomix.

    Returns:
        Dict containing available formats and their descriptions
    """
    return {
        "success": True,
        "formats": {
            "xml": "XML format with structured metadata (default)",
            "markdown": "GitHub Flavored Markdown with syntax highlighting",
            "json": "JSON format for programmatic processing",
            "plain": "Plain text format for simple reading",
        },
        "compression": {
            "enabled": "Tree-sitter based intelligent compression (~70% token reduction)",
            "disabled": "Full source code preservation",
        },
        "features": [
            "Automatic .gitignore respect",
            "Token counting for LLM context limits",
            "Security scanning with Secretlint",
            "Remote repository support",
            "Custom include/exclude patterns",
        ],
    }


# ASGI app for uvicorn: `uvicorn repomix_mcp.server:app`
app = mcp.http_app(path="/")

if __name__ == "__main__":
    import mcp.server.stdio

    mcp.server.stdio.run_server(mcp.to_server())
