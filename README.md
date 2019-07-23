# Combinatorial Games

## Python module
The Combinatorial Games (`cg`) module can be found as the [cg directory](cg).

### Usage
Getting started is a simple as importing the `Game` class and creating a new game:
```python
from cg.game import Game
g = Game("*")
h = g + g
print(h.canonical_form())
```

See `cg/game.py` for more the available functions.

# Unit testing

## Run tests
Use the following command to run the tests:
```bash
python -m unittest discover -s tests
```

## Code coverage
To generate a code coverage report, run
```bash
coverage run -m unittest discover -s tests
```
An extensive report in `html` can then be generated using
```bash
coverage html
```
The report can then be found in the `coverage_html` directory.

For a simple report with percentages for each file, run
```bash
coverage report
```
This will show a small table in the terminal.

## C++ library
CBLib offers a basic C++ implementation. To compile the `main.cc` test file:

```bash
g++ -Wall -o game main.cc src/*.cc
```

