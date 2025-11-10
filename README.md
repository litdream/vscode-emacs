# VSCode Emacs

Emacs keybindings and features for Visual Studio Code.

## Features

### Center Cursor in View (recenter)

Press `Ctrl+Shift+R` then `Ctrl+L` to center the current line in the editor viewport. This is useful for bringing context into view when working at the top or bottom of the screen.

### Center Cursor in Other Window

Press `Ctrl+Shift+R` then `Ctrl+Shift+L` to center the cursor in the other visible editor window. Useful when working with side-by-side editors to bring context into view in the non-active window without switching focus.

### Select Current Line

Press `Ctrl+Shift+R` then `Ctrl+Space` to select the entire current line. The line will be highlighted and ready for copy (`Ctrl+C`) or cut (`Ctrl+X`) operations.

### Dynamic Abbreviation Expansion (dabbrev-expand)

Press `Ctrl+Shift+R` then `Alt+/` to autocomplete based on words that appear earlier in the current document.

**How it works:**
- Type a few characters of a word
- Press `Ctrl+Shift+R` followed by `Alt+/` to expand to the most recent matching word in the document
- Press the same key sequence repeatedly to cycle through other matches (going backwards through the document)

**Example:**
```
function calculateTotal() { ... }
function calculateAverage() { ... }

calc<Ctrl+Shift+R Alt+/> → calculateAverage
calc<Ctrl+Shift+R Alt+/> → calculateTotal (press again to cycle)
```

## Installation

### For Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Compile the extension:
   ```bash
   npm run compile
   ```

3. Press `F5` to open a new VSCode window with the extension loaded

### For Use

1. Compile the extension:
   ```bash
   npm run compile
   ```

2. Copy this folder to your VSCode extensions directory:
   - Linux/Mac: `~/.vscode/extensions/`
   - Windows: `%USERPROFILE%\.vscode\extensions\`

3. Reload VSCode

## Keybindings

| Key | Command | Description |
|-----|---------|-------------|
| `Ctrl+Shift+R` `Ctrl+L` | recenter | Center cursor in active window |
| `Ctrl+Shift+R` `Ctrl+Shift+L` | recenter-other | Center cursor in other window |
| `Ctrl+Shift+R` `Ctrl+Space` | select-line | Select the entire current line |
| `Ctrl+Shift+R` `Alt+/` | dabbrev-expand | Dynamic abbreviation expansion |

## Roadmap

More Emacs features coming soon!
