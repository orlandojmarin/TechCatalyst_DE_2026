# Advanced Track A5: A Decorator (@timer)

**Optional, for fast finishers. Targets Python 3.13.**

A decorator wraps a function to add behavior without changing the function itself.
This is how teams add timing, logging, caching, and retries to pipeline steps. You
will build the classic one: a timer.

## How a decorator works

```python
@timer
def total_paid(claims):
    ...
```

`@timer` is shorthand for `total_paid = timer(total_paid)`. `timer` returns a new
function (`wrapper`) that runs your function, times it, and returns the result. The
`*args, **kwargs` let the wrapper accept any arguments the wrapped function takes.

## Instructions

Copy `Unsolved/decorator_demo.py` into your project.

### Core

1. Write `timer(func)` that returns a `wrapper(*args, **kwargs)`. The wrapper:
   - records `time.perf_counter()` before and after calling `func`,
   - prints `"{name} took {elapsed:.4f}s"`,
   - returns the function's result.
2. Use `@wraps(func)` from `functools` on the wrapper so the original name and
   docstring survive.
3. Decorate `total_paid` with `@timer` and call it.

## Expected Output

```text
  total_paid took 0.0000s
total: 50050000.0
function name preserved: total_paid
```

The timing value varies; the total and the preserved name do not.

## Success Criteria

- `@timer` works on the function without changing its body.
- `*args, **kwargs` let the wrapper pass through any arguments.
- `functools.wraps` preserves `total_paid.__name__`.

## Hint

<details>
<summary>Why use functools.wraps?</summary>

Without `@wraps(func)`, the decorated function reports the wrapper's name
(`wrapper`) and loses its docstring, which breaks debugging and help text.
`@wraps` copies that metadata across.

</details>
