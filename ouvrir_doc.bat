@echo off
chcp 65001 >nul
setlocal

set "SCRIPT_DIR=%~dp0"
set "OUT_DIR=%SCRIPT_DIR%doc"
set "PORT=8743"

if not exist "%OUT_DIR%\index-en.html" (
    echo ERREUR : Aucune documentation trouvee dans "%OUT_DIR%"
    echo Lance d'abord generer_doc.bat
    pause
    exit /b 1
)

echo Demarrage du serveur local sur le port %PORT%...

start "Serveur doc LOTUSim - fermer cette fenetre pour arreter" cmd /k "cd /d "%OUT_DIR%" && python -m http.server %PORT%"

timeout /t 2 /nobreak >nul

start "" "http://localhost:%PORT%/index-en.html"

echo.
echo Documentation servie sur http://localhost:%PORT%/
echo Visualisation graphique : clique sur "Visualization" dans la doc,
echo ou ouvre directement http://localhost:%PORT%/webvowl/index.html
echo.
echo NE FERME PAS la fenetre "Serveur doc LOTUSim" tant que tu consultes la doc.
pause
