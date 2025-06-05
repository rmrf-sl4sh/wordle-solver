#!/usr/bin/env python3
import os
import sys
import urllib.request

WORD_LIST_URL = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"
WORD_LIST_LOCAL = "words.txt"

HELP_TEXT = """
Wordle Solver Assistant

Usage:
  python wordle_solver.py --begin              Run the assistant (downloads word list if needed)
  python wordle_solver.py --update             Force-download the latest word list and exit
  python wordle_solver.py --help | -h          Show this help message

Options:
  --begin     Start the game
  --update    Force download the latest word list, save as words.txt, and exit
  --help, -h  Show this help message

Gameplay:
  - Enter your 5-letter guess when prompted
  - Enter feedback using:
      g/G = green (correct letter, correct position)
      y/Y = yellow (correct letter, wrong position)
      . or _ = gray (letter not in word)
  - Example: For a guess of 'crane' with feedback gray, green, gray, yellow, gray, enter: .g.y.
"""

def download_word_list(force=False):
    if not os.path.exists(WORD_LIST_LOCAL) or force:
        print("Downloading latest word list...")
        urllib.request.urlretrieve(WORD_LIST_URL, WORD_LIST_LOCAL)
        print("Word list downloaded and saved as 'words.txt'.")
    else:
        print("Local word list found.")

def load_words(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if len(line.strip()) == 5]

def feedback_to_letters(feedback):
    return "".join({
        "g": "G", "G": "G",
        "y": "Y", "Y": "Y",
        ".": ".", "_": "."
    }.get(c, ".") for c in feedback)

def filter_words(words, guess, feedback):
    feedback = feedback_to_letters(feedback)
    assert len(guess) == 5 and len(feedback) == 5

    new_words = []
    must_have = set()
    cannot_have = set()
    misplaced = [set() for _ in range(5)]
    confirmed = [None for _ in range(5)]

    for i, (g, f) in enumerate(zip(guess, feedback)):
        if f == "G":
            confirmed[i] = g
            must_have.add(g)
        elif f == "Y":
            misplaced[i].add(g)
            must_have.add(g)
        else:
            cannot_have.add(g)

    for g in must_have:
        cannot_have.discard(g)

    for word in words:
        if any(confirmed[i] and word[i] != confirmed[i] for i in range(5)):
            continue
        if any(word[i] in misplaced[i] for i in range(5)):
            continue
        if not all(g in word for g in must_have):
            continue
        invalid = False
        for c in cannot_have:
            must_count = sum(1 for i in range(5) if guess[i] == c and feedback[i] in "GY")
            if word.count(c) > must_count:
                invalid = True
                break
        if invalid:
            continue
        for i in range(5):
            for c in misplaced[i]:
                if c not in word or word[i] == c:
                    invalid = True
                    break
            if invalid:
                break
        if invalid:
            continue
        new_words.append(word)
    return new_words

def main():
    args = sys.argv[1:]
    if not args or "--help" in args or "-h" in args:
        print(HELP_TEXT)
        sys.exit(0)
    if "--update" in args:
        download_word_list(force=True)
        sys.exit(0)
    if "--begin" in args:
        download_word_list(force=False)
        words = load_words(WORD_LIST_LOCAL)
        print(f"Loaded {len(words)} 5-letter words.")
        round_num = 1
        while True:
            print(f"\nRound {round_num}")
            guess = input("Enter your guess: ").lower()
            feedback = input("Feedback (g=green, y=yellow, . or _=gray, e.g. .g.y.): ")
            if len(guess) != 5 or len(feedback) != 5:
                print("Please enter a 5-letter guess and feedback of length 5 (g/y/./_).")
                continue
            words = filter_words(words, guess, feedback)
            print(f"Remaining possible words: {len(words)}")
            print(", ".join(words[:20]) + ("..." if len(words) > 20 else ""))
            if len(words) == 1:
                print(f"Solution is likely: {words[0]}")
                break
            round_num += 1
        sys.exit(0)
    # If none of the above, show help
    print(HELP_TEXT)
    sys.exit(0)

if __name__ == "__main__":
    main()
