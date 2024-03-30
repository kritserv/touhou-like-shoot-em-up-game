# Pygame Touhou-like shoot-em-up

This branch is made specifically for exporting the game.

## Clone
```
git clone -b onescript --single-branch https://github.com/kritsev/touhou-like-shoot-em-up-game.git
```

```
pip install -r requirements.txt
```

# Export to web

#### Go to parent directory of directory including game file

```
cd ..
```

#### Export to web with pygbag

```
pygbag touhou-like-shoot-em-up-game
```

#### Play test

http://localhost:8000

#### Archive game

```
pygbag --archive touhou-like-shoot-em-up-game
```


# Export to desktop

#### Go to root directory that include game file

```
cd touhou-like-shoot-em-up-game
```

#### Export to desktop with pyinstaller

```
pyinstaller --noconsole main.py --onefile
```