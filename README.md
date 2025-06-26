<div align="center">

# MuffinScript

Delectable little programming language.

[![Build Status](https://github.com/justintime50/muffinscript/workflows/build/badge.svg)](https://github.com/justintime50/muffinscript/actions)
[![Coverage Status](https://coveralls.io/repos/github/justintime50/muffinscript/badge.svg?branch=main)](https://coveralls.io/github/justintime50/muffinscript?branch=main)
[![PyPi](https://img.shields.io/pypi/v/muffinscript)](https://pypi.org/project/muffinscript)
[![Licence](https://img.shields.io/github/license/justintime50/muffinscript)](LICENSE)

<img src="https://raw.githubusercontent.com/justintime50/assets/main/src/muffinscript/showcase.png" width="256px" alt="Showcase">

</div>

## Why MuffinScript

We should probably start with what it's not. It's NOT fast (built on Python), it's NOT safe (built on Python), it's NOT sexy (built on Python)... so why?

It IS dead simple, it IS robust, it IS delectably little.

I built MuffinScript as a POC (mostly without AI) to see if I could even build a programming language. I don't have intentions for it to become very useful, but it was super fun to build some basic programming language concepts into.

So what's it used for? Building tiny little scripts and tools.

## Features

- Data types: `str`, `int`, `float`, `bool`, `null`
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison operators: `==`, `!=`, `>`, `>=`, `<`, `<=`
- Variable assignment: `foo = "hello world"`
- Comments (inline and alone): `// This is a comment`
- Clear, colored error messages: `ERROR - Invalid expression | line: 3`
- REPL: Use `muffin` to enter
- Standard library
  - Print to console: `p("hello world")`
  - String concatenation: `cat("hello ", bar)`

## Usage

Create a `filename.ms` file and start coding with `muffin filename.ms`.

- Everything must be assigned to a variable to evaluate (forces explicit self-documenting code).

```ms
// Variable assignment and printing
foo = "hello world"
p(foo)

// Simple arithmetic (add, subtract, multiply, divide, modulo)
p(2 + 2.5)

// Concatenate strings
p(cat("I say ", foo))
```

Commands:

```sh
# REPL
muffin

# Help
muffin --help

# Version
muffin --version
```

## Development

### Abstract Syntax Tree (AST)

Defines the abstract supported syntax of the programming language (what is a string, what is a variable, etc).

### Lexer (Tokenizer)

Takes raw text and turns it into a list of tokens which are structured pieces of the programming language (keywords, numbers, strings, symbols).

- Takes `print("hello world")` and converts it into `print`, `(`, `"hello world"`, and `)`
- Detects errors in characters
- Should convert tokens to their most appropriate types

### Parser

Parses the tokens from the Lexer.

- Grammar rules, defines what combos of tokens are valid
- Syntax errors detect issues

### Interpreter

Actually executes the program by traversing the AST.

- Prints values, assigns variables, etc

### TODO

- `str`, `int`, `float` functions
- Control flow (if, else, elseif?)
- For loops
- Lists
- Functions
- Errors
- String interpolation
