@echo off
TITLE USBL 3-Team Subset Test Auto-Update
echo ====================================================================
echo   USBL 3-Team Subset Test Auto-Update
echo ====================================================================
echo.

cd /d "C:\Users\johnh\OneDrive\Desktop\USBL\USBL"

echo [1/3] Running Targeted 3-Team Data Extractor...
python export_league_data_v29_subset.py "C:\Users\johnh\OneDrive\Documents\Out of the Park Developments\OOTP Baseball 27\saved_games\Armada.lg\news\almanac_2017"

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Data extraction failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Staging updated web files for GitHub...
git add usbl_league_data.json index.html styles.css app.js

echo.
echo [3/3] Committing and pushing 3-Team test subset to GitHub Pages...
git commit -m "3-Team Subset Test Update - %DATE% %TIME%"
git push origin main

echo.
echo ====================================================================
echo   SUCCESS! 3-Team test update pushed to GitHub.
echo ====================================================================
pause
