const vscode = require('vscode');

function activate()
{
    console.log("SCM16 Extension Activated");
}

function deactivate()
{
    console.log("SCM16 Extension Deactivated");
}

module.exports = {
    activate,
    deactivate
}