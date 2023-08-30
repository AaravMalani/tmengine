# tmengine: A TextMate grammar engine in Python.
## Installation
```sh
python -m pip install tmengine
# or
python -m pip install git+https://github.com/AaravMalani/tmengine
```

## Usage
```python
from tmengine import TextMateEngine
import json

engine = TextMateEngine.load_folder('grammars/') # Load all grammars in the grammars/ folder
print(engine.languages) # Returns a tuple of scopeNames
print(engine.parse('source.akbs', 'compile($FILES)')) # Parse 'compile($FILES)' using language with `scopeName` as `source.akbs` 
# [TextMateExpression(name='punctuation.paren.open', range=(7, 8)), TextMateExpression(name='expression.group', range=(7, 15)), TextMateExpression(name='keyword.function', range=(0, 7)), TextMateExpression(name='expression.inner', range=(8, 14)), TextMateExpression(name='punctuation.paren.close', range=(14, 15)), TextMateExpression(name='variable.other', range=(8, 14))]

with open('grammars/akbs.json', 'r') as f: # Found at https://github.com/akbs-org/akbs-vscode/blob/main/syntaxes/akbs.tmGrammar.json
    engine2 = TextMateEngine(json.load(f)) # or tmengine.TextMateEngine([json.load(f)])
```

## Tasklist
- [ ] Accept YAML
- [ ] Accept XML
- [ ] Make code ignore errors

## Changelog
### Version 1.0.1
- Fixed bug which returned indices/a range less than expected when there were multiple `match` expressions satisfied on separate lines
- Fixed only a single `begin`/`end` expression of a type being selected
  