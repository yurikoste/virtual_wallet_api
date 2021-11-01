# Virtual wallet API
This API will allow you to manage you virtual wallet

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install count-unique.

```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps count-unique-chars-yurikoste
```

## Usage

Count-unique can be used as a script with command-line interface and as an imported module. User can specify with options which type of input data should be processed - string (--string) of file (--file). If both options are specified then --file has higher priority.

CLI:
```python
python -m count_uniq.collect_framework --string "test_string"
python -m count_uniq.collect_framework --file "/home/my_test_file.txt"
python -m count_uniq.collect_framework --string "test_string" --file "/home/my_test_file.txt"
```
Imported module:
```python
from count_uniq.collect_framework import count_unique_chars

count_unique_chars(("--string", "test_string"))
count_unique_chars(("--file", "/home/my_test_file.txt"))
count_unique_chars(("--string", "test_string", "--file", "/home/my_test_file.txt"))
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## References
[Count-unique at test.pypi](https://test.pypi.org/project/count-unique-chars-yurikoste/)
