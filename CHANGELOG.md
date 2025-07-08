# CHANGELOG

## Next Release

- Data types: `str` (either `"` or `'` work), `int`, `float`, `bool`, `null`
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison operators: `==`, `!=`, `>`, `>=`, `<`, `<=`
- Variable assignment: `foo = "hello world"`
- Type coercion: `str(2)`, `int("2")`, `float("2.5")`
- If statements: `if (foo == bar) { ... }`
- Else statements `{ ... } else { ... }`
- Comments (inline and alone): `// This is a comment`
- Clear, colored error messages: `ERROR - Invalid expression | line: 3`
- REPL: Use `muffin` to enter
- Standard library
  - Print to console: `p("hello world")`
  - Type checking: `type("hello world")`
  - String concatenation: `cat("hello ", bar)`
  - Sleep: `sleep(10.5)`
