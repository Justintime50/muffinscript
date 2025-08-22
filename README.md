<div align="center">

# MuffinScript

Delectable little programming language.

[![Build Status](https://github.com/justintime50/muffinscript/workflows/build/badge.svg)](https://github.com/justintime50/muffinscript/actions)
[![Coverage Status](https://coveralls.io/repos/github/justintime50/muffinscript/badge.svg?branch=main)](https://coveralls.io/github/justintime50/muffinscript?branch=main)
[![PyPi](https://img.shields.io/pypi/v/muffinscript)](https://pypi.org/project/muffinscript)
[![Licence](https://img.shields.io/github/license/justintime50/muffinscript)](LICENSE)

<img src="https://raw.githubusercontent.com/justintime50/assets/main/src/muffinscript/showcase.png" width="256px" alt="Showcase">

</div>

## What is MuffinScript

MuffinScript is a delectably simple programming language baked for fun, not for fame. It’s not going to win any speed records (it’s built on Python), can't be used for integrated circuits, nor will it dazzle you with cutting-edge features. What it will do is make writing tiny scripts feel like a treat.

MuffinScript is all about the basics: variables, arithmetic, strings, lists, loops, and conditionals, served up with a syntax that’s easy to read and a parser that’s forgiving enough for beginners but robust enough for tinkerers. You get a REPL for instant feedback, clear error messages with a dash of color, and a standard library that covers the essentials (printing, type checking, string concatenation, sleeping, etc).

It’s a proof of concept, a playground, and a learning tool. If you want to see how a programming language is built from scratch, MuffinScript is your open kitchen.

## Features

- Data types: `str` (either `"` or `'` work), `int`, `float`, `bool`, `list`, `null`
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison operators: `==`, `!=`, `>`, `>=`, `<`, `<=`
- Variable assignment: `foo = "hello world"`
- String interpolation: `foo = "hello #{bar}"`
- Type coercion: `str(2)`, `int("2")`, `float("2.5")`
- If statements: `if (foo == bar) { ... }`
  - Else statements: `if (...) { ... } else { ... }`
- Foor loops: `for (item in myList) { ... }`
- Comments (inline and standalone): `// This is a comment`
- Clear, colored error messages: `ERROR - Invalid expression | line: 3`
- REPL: Use `muffin` to enter
- Standard library
  - Print to console: `p("hello world")`
  - Type checking: `type("hello world")`
  - String concatenation: `cat("hello ", foo)`
  - Sleep: `sleep(10.5)`
- Debug mode by passing `MUFFIN_DEBUG=true`

## Usage

NOTE: All variables are global (this includes `item` in foor loops).

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
} else {
    p(false)
}

// For loops
for (item in [1, 2, 3]) {
    p(item + 1)
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

The AST is the recipe book for MuffinScript. It defines the basic ingredients like what counts as a string, a number, or a variable.

### Lexer (Tokenizer)

The lexer is the kitchen assistant. It takes raw text and chops it up into tokens by identifying keywords, numbers, strings, and symbols.

- Example: p("hello world") becomes p, (, "hello world", )
- Spots errors in characters
- Converts tokens to their proper types

### Parser

The parser is the chef who checks the recipe. It looks at the tokens and makes sure they follow MuffinScript’s grammar rules.

- Decides which combinations of tokens are valid
- Catches syntax mistakes

### Interpreter

The interpreter is the baker. It reads the AST and actually runs your code by printing values, assigning variables, and more executing the code.

### TODO

- BUG: line numbers for errors are off in block statements (eg: `if`, `for`) due to us buffering the entire block and parsing it as one set of tokens instead of each line of tokens individually (the parser will only know the line number of the end of the block by the time it runs error checking)
- Functions
- Error handling
- Imports
- Package manager (StudMuffin)
  - Call the directory packages are stored `oven` and the packages `ingredients`
  - Use GitHub as source of packages
