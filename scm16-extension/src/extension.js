const vscode = require('vscode');

function activate(context) {
    const assemblyLanguage = {
        language: 'assembly',
        scheme: 'file',
        pattern: '**/*.assembly'
    };

    // Create decoration types for different colors
    const decorationTypes = [
        vscode.window.createTextEditorDecorationType({ color: 'orange' }),
        vscode.window.createTextEditorDecorationType({ color: 'yellow' }),
        vscode.window.createTextEditorDecorationType({ color: 'green' }),
        vscode.window.createTextEditorDecorationType({ color: 'blue' }),
    ];

    // Listen for changes in the text document
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(event => {
            const document = event.document;
            if (document.languageId === 'assembly') {
                const text = document.getText();
                const lines = text.split('\n');
                const decorations = [[], [], [], []]; // Store decorations for each color

                lines.forEach((line, lineIndex) => {
                    const words = line.split(/\s+/);
                    words.forEach((word, index) => {
                        if (index < 4) { // Only highlight the first four words
                            const startPos = line.indexOf(word);
                            const endPos = startPos + word.length;
                            const range = new vscode.Range(lineIndex, startPos, lineIndex, endPos);
                            decorations[index].push(range); // Add the range for the respective color
                        }
                    });
                });

                // Apply text decorations
                const editor = vscode.window.activeTextEditor;
                if (editor) {
                    for (let i = 0; i < decorations.length; i++) {
                        editor.setDecorations(decorationTypes[i], decorations[i]);
                    }
                }
            }
        })
    );
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
