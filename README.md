# eo
Machine Readable Corpus of Executive Orders

## Installation
Install `eo` from PyPI:
```
pip install eo
```

## Usage
Get an updated corpus of Executive Orders

```python
In [1]: import eo
In [2]: eos = eo.corpus.update()

# Let's see how many EOs we have records of for each president
In [3]: from collections import Counter
In [4]: Counter([eo.get('president') for eo in eos])
Out[4]:
Counter({'Barack Obama': 106,
         'Donald J. Trump': 12,
         'Dwight D. Eisenhower': 484,
         'Franklin D. Roosevelt': 1905,
         'George Bush': 166,
         'George W. Bush': 102,
         'Gerald R. Ford': 169,
         'Harry S. Truman': 908,
         'Jimmy Carter': 243,
         'John F. Kennedy': 125,
         'Lyndon B. Johnson': 325,
         'Richard Nixon': 346,
         'Ronald Reagan': 270,
         'William J. Clinton': 234})
```

Obviously to make meaningful comparisons across presidents we'd need to
normalized based on time as president, but this is simply meant to illustrate
what executive orders are recorded in the data.

Unfortunatly we don't have access to the text of each EO. I've only found
digital access to EOs after President Clinton from the [archives](https://www.archives.gov).

```python
In [5]: Counter([eo.get('president') for eo in eos if eo.get('text')])
Out[5]:
Counter({'Barack Obama': 102,
         'Donald J. Trump': 12,
         'George W. Bush': 102,
         'William J. Clinton': 234})
```

While this is only 3 complete presidencies it is the text of executive orders
for more than 20 years.
