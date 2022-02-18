## Battleship

Python console application for playing the classic Battleship game invented by Clifford von Wickler which became popular with French and Russian soldiers during World War I. It was published by various companies as a pad-and-pencil game in the 1930s, and was released as a plastic board game by Milton Bradley in 1967. This implementation follows the Milton Bradley rules.

Battleship uses pynput, pygame and pyinstaller
```apache
pip install pynput pygame pyinstaller
```

Start the game:
```apache
python .\app\main.py
# start the pygame version
python .\app\battleship.py
```

Build the game:
```apache
pyinstaller battleship.py
pyibstaller battleship.spec
```
You may need to replace the `datas` line in battleship.spec as follows:
```apache
datas: [('assets/images/*', 'assets/images/']
```
