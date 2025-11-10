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
- `emacs.centerCursor` - bound to `Ctrl+Shift+R` then `Ctrl+L`
- `emacs.centerCursorOther` - bound to `Ctrl+Shift+R` then `Ctrl+Shift+L`
- `emacs.selectLine` - bound to `Ctrl+Shift+R` then `Ctrl+Space`
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

### Select Line Implementation (src/extension.ts)

The `selectLine` function provides a simple way to select the entire current line:

1. Gets the current cursor position and line
2. Creates a selection from the beginning of the line (column 0) to the end of the line
3. Sets the editor selection, leaving the line highlighted for copy/cut operations

This mimics the Emacs behavior of selecting a line for subsequent operations.

### Center Cursor Implementation (src/extension.ts)

The `centerCursor` function centers the current line in the viewport (src/extension.ts:173):

1. Gets the current cursor position
2. Uses VSCode's built-in `editor.revealRange()` method with `TextEditorRevealType.InCenter`
3. This scrolls the viewport to center the current line

This is a wrapper around VSCode's native functionality, replicating Emacs' `recenter` command (Ctrl+L).

### Center Cursor Other Implementation (src/extension.ts)

The `centerCursorOther` function centers the cursor in the non-active editor window (src/extension.ts:184):

1. Gets the active editor and all visible editors
2. Finds the first visible editor that is not the active one
3. Centers that editor's cursor position using the same `revealRange()` method
4. Shows a message if no other visible editor is found

This is useful for split-screen editing where you want to center the view in the other pane without switching focus to it.

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
