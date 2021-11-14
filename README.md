# 21-levenshtein-exercise
This repository contains files relating to a practice implementation of a program for calculation of the Levenshtein edit distance between two strings.

## Requirements
Requires numpy. All requirements can be installed from `requirements.txt` from the command line:
```
$ pip install -r requirements.txt
```

## Usage
Enter two strings as command line arguments.

The program prints the edit distance and the alignment (minimum edit path) as a list of strings:
```
$ py edit_distance.py hello world
Distance: 4
['hello', 'wello', 'wollo', 'worlo', 'worlo', 'world']
```