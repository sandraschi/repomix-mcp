"""
Repomix MCP Server
==================

A Model Context Protocol server that provides AI assistants with the ability to pack
entire repositories into AI-friendly formats using Repomix.

Features:
- Pack local repositories into XML, Markdown, JSON, or plain text
- Intelligent code compression (70% token reduction)
- Search and analyze packed repository content
- Support for remote repositories
- Custom include/exclude patterns

Requirements:
- Node.js and npm (for Repomix)
- Python 3.9+
- fastmcp library

Usage:
    python server.py
"""

__version__ = "0.1.0"
__author__ = "FlowEngineer sandraschi"