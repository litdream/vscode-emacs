# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a VSCode extension that brings Emacs keybindings and features to Visual Studio Code. Currently implements `dabbrev-expand` (dynamic abbreviation expansion) with plans to add more Emacs features.

## Development Commands

```bash
# Install dependencies
npm install

# Compile TypeScript to JavaScript (outputs to ./out directory)
npm run compile

# Watch mode - automatically recompile on file changes
npm run watch

# Prepare for publishing (runs compile)
npm run vscode:prepublish
```

## Running and Testing the Extension

Press `F5` in VSCode to launch the Extension Development Host with the extension loaded. This uses the launch configuration in `.vscode/launch.json` which automatically runs the default build task before launching.

## Architecture

### Extension Entry Point

The extension is activated via `src/extension.ts`, which exports the standard VSCode extension lifecycle functions:
- `activate(context: vscode.ExtensionContext)` - registers commands and event handlers
- `deactivate()` - cleanup function

### Command Registration

Commands are registered in `package.json` under `contributes.commands` and bound to keybindings in `contributes.keybindings`. The current implementation registers:
- `emacs.dabbrevExpand` - bound to `Ctrl+Shift+R` then `Alt+/`

**Keybinding Strategy**: This extension uses a prefix-based keybinding system to avoid conflicts with existing VSCode shortcuts. All Emacs features use `Ctrl+Shift+R` as a prefix key, followed by a second key. This is implemented using VSCode's built-in chord support (space-separated keys in the keybinding definition).

### Dabbrev-Expand Implementation (src/extension.ts)

The `dabbrevExpand` function implements stateful abbreviation expansion:

1. **State Management**: Uses a global `dabbrevState` object to track:
   - The original prefix being expanded
   - All matching words found in the document
   - Current position in the match list
   - The document version to detect external changes

2. **Match Finding**: `findMatches()` scans the entire document for words starting with the prefix that appear before the cursor position, returning them in reverse order (most recent first)

3. **Cycling Behavior**: Repeated invocations cycle through matches if the prefix and document version haven't changed

4. **State Reset**: Selection change listeners reset state when the cursor moves away from the expansion position

### TypeScript Configuration

- Target: ES2020
- Module: CommonJS (required for VSCode extensions)
- Strict mode enabled
- Output directory: `./out`
- Source directory: `./src`

## Extension Manifest (package.json)

Key configurations:
- `main`: Points to `./out/extension.js` (compiled output)
- `engines.vscode`: Minimum VSCode version `^1.80.0`
- `activationEvents`: Empty array means the extension activates immediately on VSCode startup
- Category: "Keymaps"
