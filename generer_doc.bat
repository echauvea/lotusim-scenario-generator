@echo off
chcp 65001 >nul
setlocal

set "SCRIPT_DIR=%~dp0"
set "ONT_FILE=%SCRIPT_DIR%lotusim naval maritime ontology v1.1-draft"
set "OUT_DIR=%SCRIPT_DIR%docs"
set "JAVA_EXE=C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot\bin\java.exe"
set "WIDOCO_JAR=C:\Users\chauv\tools\widoco\widoco-1.4.25.jar"
set "PORT=8743"

if not exist "%JAVA_EXE%" (
    echo ERREUR : Java introuvable a "%JAVA_EXE%"
    pause
    exit /b 1
)

if not exist "%WIDOCO_JAR%" (
    echo ERREUR : WIDOCO introuvable a "%WIDOCO_JAR%"
    pause
    exit /b 1
)

if not exist "%ONT_FILE%" (
    echo ERREUR : Fichier d'ontologie introuvable a "%ONT_FILE%"
    pause
    exit /b 1
)

echo Generation de la documentation HTML...
echo.

"%JAVA_EXE%" -jar "%WIDOCO_JAR%" -ontFile "%ONT_FILE%" -outFolder "%OUT_DIR%" -rewriteAll -webVowl -lang en-fr

if errorlevel 1 (
    echo.
    echo La generation a echoue. Voir les messages ci-dessus.
    pause
    exit /b 1
)

echo.
echo Documentation generee dans : %OUT_DIR%
echo Demarrage du serveur local sur le port %PORT% (necessaire pour WebVOWL)...

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
