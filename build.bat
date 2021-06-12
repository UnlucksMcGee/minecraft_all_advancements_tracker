powershell -Command "Get-ChildItem .\dist -Recurse | rmdir -Recurse"
mkdir dist
cd .\dist
pyinstaller ../run.py --name "MC AA Tracker" --onefile --noconsole --icon ..\icon.ico
powershell -Command "Copy-Item ..\readme.md -Destination .\dist\readme.txt"
powershell -Command "Copy-Item ..\settings.txt -Destination .\dist\settings.txt"
powershell -Command "Copy-Item ..\credentials.json -Destination .\dist\credentials.json"
cd ..