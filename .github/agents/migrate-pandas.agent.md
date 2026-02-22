# Pandas to Polars Migration Guide

## Purpose

This agent will automate or guide the migration from using **pandas** DataFrames to **polars** DataFrames in the codebase. Polars is a faster, more memory-efficient DataFrame library that provides similar functionality to pandas with a more intuitive API.

## Scope

- Identify all imports and usages of `pandas` (e.g., `import pandas as pd`, `pd.DataFrame`, `pd.Series`, etc.).
- Replace them with equivalent `polars` implementations (e.g., `import polars as pl`, `pl.DataFrame`, etc.).
- Ensure all DataFrame operations, aggregations, merges, and transformations use Polars syntax and types.
- Update dependencies from `pandas` to `polars` in `requirements.txt` and `pyproject.toml`.
- Validate all tests pass and functionality remains unchanged.

## Migration Steps

### 1. **Update Imports**

Replace pandas imports with polars:

```python
# Before
import pandas as pd

# After
import polars as pl
```

...TBD...
