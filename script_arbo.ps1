# Dossiers à exclure complètement (avec leur contenu)
$exclusions = @('.git', 'venv', '__pycache__', '.pytest_cache', '.vscode', 'staticfiles', 'node_modules')

function Afficher-Arborescence ($chemin, $prefixe = '') {
    # Liste les dossiers sauf exclusions
    Get-ChildItem -Path $chemin -Directory |
        Where-Object { $exclusions -notcontains $_.Name } |
        ForEach-Object {
            # Affiche le dossier actuel avec indentation
            $ligne = $prefixe + '├── ' + $_.Name
            Add-Content -Path "arborescence.txt" -Value $ligne

            # Appelle récursivement la fonction pour afficher les sous-dossiers
            Afficher-Arborescence $_.FullName ($prefixe + '│   ')
        }

    # Affiche les fichiers du dossier courant
    Get-ChildItem -Path $chemin -File |
        ForEach-Object {
            $ligne = $prefixe + '├── ' + $_.Name
            Add-Content -Path "arborescence.txt" -Value $ligne
        }
}

# Supprime l'ancien fichier s'il existe
if (Test-Path arborescence.txt) {
    Remove-Item arborescence.txt
}

# Démarre l'affichage de l'arborescence depuis le dossier courant
'.' | Add-Content -Path "arborescence.txt"
Afficher-Arborescence "."

Write-Host "Arborescence complète générée dans 'arborescence.txt'"


