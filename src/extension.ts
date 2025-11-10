import * as vscode from 'vscode';

// State for tracking dabbrev expansions across multiple invocations
let dabbrevState: {
    prefix: string;
    matches: string[];
    currentIndex: number;
    startPosition: vscode.Position;
    documentVersion: number;
} | null = null;

export function activate(context: vscode.ExtensionContext) {
    console.log('vscode-emacs extension is now active');

    const dabbrevExpandCommand = vscode.commands.registerCommand(
        'emacs.dabbrevExpand',
        async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                return;
            }

            await dabbrevExpand(editor);
        }
    );

    const selectLineCommand = vscode.commands.registerCommand(
        'emacs.selectLine',
        () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                return;
            }

            selectLine(editor);
        }
    );

    const centerCursorCommand = vscode.commands.registerCommand(
        'emacs.centerCursor',
        () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                return;
            }

            centerCursor(editor);
        }
    );

    const centerCursorOtherCommand = vscode.commands.registerCommand(
        'emacs.centerCursorOther',
        () => {
            centerCursorOther();
        }
    );

    // Reset state when document changes or cursor moves
    vscode.window.onDidChangeTextEditorSelection((e) => {
        if (dabbrevState && e.textEditor === vscode.window.activeTextEditor) {
            const currentPos = e.selections[0].active;
            // Reset if cursor moved away from the expansion area
            if (!currentPos.isEqual(dabbrevState.startPosition)) {
                dabbrevState = null;
            }
        }
    });

    context.subscriptions.push(dabbrevExpandCommand, selectLineCommand, centerCursorCommand, centerCursorOtherCommand);
}

async function dabbrevExpand(editor: vscode.TextEditor) {
    const document = editor.document;
    const position = editor.selection.active;

    // Get the word prefix before cursor
    const lineText = document.lineAt(position.line).text;
    const textBeforeCursor = lineText.substring(0, position.character);
    const wordMatch = textBeforeCursor.match(/(\w+)$/);

    if (!wordMatch) {
        vscode.window.showInformationMessage('No word prefix to expand');
        return;
    }

    const prefix = wordMatch[1];
    const prefixStart = new vscode.Position(position.line, position.character - prefix.length);

    // Check if we're continuing a previous expansion
    const isContinuation =
        dabbrevState !== null &&
        dabbrevState.prefix === prefix &&
        dabbrevState.documentVersion === document.version &&
        prefixStart.isEqual(dabbrevState.startPosition);

    if (!isContinuation) {
        // New expansion - find all matches
        const matches = findMatches(document, position, prefix);

        if (matches.length === 0) {
            vscode.window.showInformationMessage('No expansion found');
            return;
        }

        dabbrevState = {
            prefix,
            matches,
            currentIndex: 0,
            startPosition: prefixStart,
            documentVersion: document.version
        };
    } else {
        // Cycle to next match
        dabbrevState!.currentIndex = (dabbrevState!.currentIndex + 1) % dabbrevState!.matches.length;
    }

    // Replace the prefix with the current match
    const replacement = dabbrevState!.matches[dabbrevState!.currentIndex];
    const range = new vscode.Range(prefixStart, position);

    await editor.edit(editBuilder => {
        editBuilder.replace(range, replacement);
    });

    // Update document version after edit
    dabbrevState!.documentVersion = document.version;
}

function findMatches(
    document: vscode.TextDocument,
    position: vscode.Position,
    prefix: string
): string[] {
    const text = document.getText();
    const matches: string[] = [];
    const seen = new Set<string>();

    // Word boundary regex - matches words starting with prefix
    const regex = new RegExp(`\\b(${escapeRegex(prefix)}\\w+)\\b`, 'g');

    let match;
    while ((match = regex.exec(text)) !== null) {
        const word = match[1];
        const matchPos = document.positionAt(match.index);

        // Skip the current prefix itself and words we've already found
        if (matchPos.isBefore(position) && !seen.has(word) && word !== prefix) {
            seen.add(word);
            matches.push(word);
        }
    }

    // Return matches in reverse order (most recent first)
    return matches.reverse();
}

function escapeRegex(str: string): string {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function selectLine(editor: vscode.TextEditor) {
    const position = editor.selection.active;
    const line = editor.document.lineAt(position.line);

    // Create selection from start to end of line
    const start = new vscode.Position(line.lineNumber, 0);
    const end = new vscode.Position(line.lineNumber, line.text.length);

    // Set the selection with anchor at start and active at end
    editor.selection = new vscode.Selection(start, end);
}

function centerCursor(editor: vscode.TextEditor) {
    const position = editor.selection.active;

    // Use VSCode's built-in revealLine command with 'InCenter' option
    // This centers the current line in the viewport
    editor.revealRange(
        new vscode.Range(position, position),
        vscode.TextEditorRevealType.InCenter
    );
}

function centerCursorOther() {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor) {
        return;
    }

    // Get all visible text editors
    const visibleEditors = vscode.window.visibleTextEditors;

    // Find the "other" editor - first visible editor that's not the active one
    const otherEditor = visibleEditors.find(editor => editor !== activeEditor);

    if (!otherEditor) {
        vscode.window.showInformationMessage('No other visible editor found');
        return;
    }

    // Center the cursor in the other editor
    const position = otherEditor.selection.active;
    otherEditor.revealRange(
        new vscode.Range(position, position),
        vscode.TextEditorRevealType.InCenter
    );
}

export function deactivate() {}
