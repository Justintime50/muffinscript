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

I built **MuffinScript** as a POC (mostly without AI) to see if I could even build a **Turing Complete** programming language. I don't have intentions for it to become very useful, but it was super fun to build some basic programming language concepts into.

So what's it used for? Building tiny little scripts and tools.

## Features

- Data types: `str` (either `"` or `'` work), `int`, `float`, `bool`, `list`, `null`
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison operators: `==`, `!=`, `>`, `>=`, `<`, `<=`
- Variable assignment: `foo = "hello world"`
- String interpolation: `foo = "hello #{bar}"`
- Type coercion: `str(2)`, `int("2")`, `float("2.5")`
- If statements: `if (foo == bar) { ... }`
- Else statements `{ ... } else { ... }`
- Comments (inline and alone): `// This is a comment`
- Clear, colored error messages: `ERROR - Invalid expression | line: 3`
- REPL: Use `muffin` to enter
- Standard library
  - Print to console: `p("hello world")`
  - Type checking: `type("hello world")`
  - String concatenation: `cat("hello ", foo)`
  - Sleep: `sleep(10.5)`
- Debug mode by passing `MUFFIN_DEBUG=true`

## Usage

- Variables are global
- Functions are public

```ms
// Variable assignment and printing
foo = "hello world"
p(foo)

// Simple arithmetic (add, subtract, multiply, divide, modulo)
p(2 + 2.5)

// Concatenate strings
p(cat("I say ", foo))

// If statements
if (foo == bar) {
    p(true)
}
```

Commands:

```sh
# Run the Muffin interpreter on a Muffinscript file
muffin filename.ms

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

#### v0.1.0

- BUG: line numbers for errors are off in `if` statements due to us buffering the entire block together
- Muffinscript is Turing Complete
  - For loops

#### Future

- Functions
- Error handling
- Imports
- Package manager (StudMuffin)
  - Call the directory packages are stored `oven` and the packages `ingredients`
  - Use GitHub as source of packages
