# VSCode Emacs

Emacs keybindings and features for Visual Studio Code.

## Features

### Dynamic Abbreviation Expansion (dabbrev-expand)

Press `Alt+/` to autocomplete based on words that appear earlier in the current document.

**How it works:**
- Type a few characters of a word
- Press `Alt+/` to expand to the most recent matching word in the document
- Press `Alt+/` repeatedly to cycle through other matches (going backwards through the document)

**Example:**
```
function calculateTotal() { ... }
function calculateAverage() { ... }

calc<Alt+/> → calculateAverage
calc<Alt+/> → calculateTotal (press again to cycle)
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
| `Alt+/` | dabbrev-expand | Dynamic abbreviation expansion |

## Roadmap

More Emacs features coming soon!
