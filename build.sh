source ~/miniconda/etc/profile.d/conda.sh
conda activate mcaatracker
rm -rf ./dist
mkdir dist
cd dist
pyinstaller ../run.py --name "MC AA Tracker" --onefile --icon icon.ico
cp ../settings.txt ./dist/settings.txt
cp ../readme.md ./dist/readme.txt
cp ../credentials.json ./dist/credentials.json
