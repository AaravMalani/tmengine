# tmengine: A TextMate grammar engine in Python.
## Installation
```sh
python -m pip install tmengine
# or
python -m pip install git+https://github.com/AaravMalani/tmengine
```

## Usage
```python
import tmengine
import json

engine = tmengine.load_folder('grammars/') # Load all grammars in the grammars/ folder
print(engine.languages) # Returns a tuple of scopeNames
print(engine.parse('source.akbs', 'compile($FILES)')) # Parse 'compile($FILES)' using language with `scopeName` as `source.akbs` 
# [TextMateExpression(name='variable.other', range=(8, 14)), TextMateExpression(name='expression.inner', range=(8, 14)), TextMateExpression(name='punctuation.paren.open', range=(7, 8)), TextMateExpression(name='punctuation.paren.close', range=(14, 15)), TextMateExpression(name='expression.group', range=(7, 15)), TextMateExpression(name='keyword.function', range=(0, 7))]

with open('grammars/akbs.json', 'r') as f:
    engine2 = tmengine.TextMateEngine(json.load(f)) # or tmengine.TextMateEngine([json.load(f)])
```

## Tasklist
- [ ] Accept YAML
- [ ] Accept XML
- [ ] Make code ignore errors