# Wordle Solver Assistant

A simple command-line assistant to help you solve Wordle puzzles more efficiently!  
Automatically manages a 5-letter word list and guides you through the process of narrowing down possible solutions based on your guesses and feedback.

---

## Features

- **Automatic Word List Management:** Downloads and updates the official Wordle word list.
- **Interactive Filtering:** Input your guesses and feedback; the script will show you all possible remaining words.
- **Easy Feedback Format:** Use simple symbols (`g`, `y`, `.`, `_`) for green, yellow, and gray feedback.

---

## Usage

```sh
python wordle_solver.py --begin
```

### Options

- `--begin`  
  Start the Wordle assistant. Downloads the word list if it's missing.
- `--update`  
  Force-download the latest word list and exit.
- `--help` or `-h`  
  Show help message.
