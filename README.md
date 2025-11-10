# VSCode Emacs

Emacs keybindings and features for Visual Studio Code.

## Features

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
| `Ctrl+Shift+R` `Ctrl+Space` | select-line | Select the entire current line |
| `Ctrl+Shift+R` `Alt+/` | dabbrev-expand | Dynamic abbreviation expansion |

## Roadmap

More Emacs features coming soon!
