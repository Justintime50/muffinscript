# CHANGELOG

## v0.2.0 (2026-01-11)

- Upgraded Python to 3.14 under the hood

## v0.1.0 (2025-08-25)

- Data types: `str` (either `"` or `'` work), `int`, `float`, `bool`, `list`, `null`
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison operators: `==`, `!=`, `>`, `>=`, `<`, `<=`
- Variable assignment: `foo = "hello world"`
- String interpolation: `foo = "hello #{bar}"`
- Type coercion: `str(2)`, `int("2")`, `float("2.5")`
- If statements: `if (foo == bar) { ... }`
  - Else statements: `if (...) { ... } else { ... }`
- Foor loops: `for (item in myList) { ... }`
  - Lists: `[1, 2, 3]`
- Comments (inline and standalone): `// This is a comment`
- Clear, colored error messages: `ERROR - Invalid expression | line: 3`
- REPL: Use `muffin` to enter
- Standard library
  - Print to console: `p("hello world")`
  - Type checking: `type("hello world")`
  - String concatenation: `cat("hello ", foo)`
  - Sleep: `sleep(10.5)`
- Debug mode by passing `MUFFIN_DEBUG=true`
