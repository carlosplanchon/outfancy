# outfancy

*Table printing and Line plotting in Terminal*

<img src='https://raw.githubusercontent.com/carlosplanchon/outfancy/refs/heads/master/examples/chart_auto.png'>

## What is it?

Outfancy is a Python library for printing tables and charts in the terminal. It's a quick way to visualize data when you don't have a GUI, and it integrates easily into your programs. You can install it with uv or pip and use it anywhere.

This was the first library I ever built when I was 16 :). It's been modernized to support Python 3.10+, fix bugs, add type hints, improve logging, and enhance performance, but the original style is still there: raw, exploratory teenage code.

## Documentation

- **[DeepWiki Docs](https://deepwiki.com/carlosplanchon/outfancy)** - Comprehensive documentation
- **[LOGGING.md](LOGGING.md)** - Logging system configuration and usage
- **[logging_example.py](logging_example.py)** - Practical logging examples

## Installation

### Install with uv
```bash
pip install outfancy
```

### Install with pip
```bash
pip install outfancy
```

## Features

- **Quick table printing** - Print formatted tables in the terminal with automatic column width detection
- **LineChart plotting** - Create line charts with linear interpolation
- **Customizable formatting** - Configure separators, widths, and column priorities
- **Real-time column rearrangement** - Dynamically reorder columns
- **Auto-generated labels** - Automatic label creation above tables
- **Oneline printing** - Single-line updates for real-time applications
- **Color support** - Add ANSI colors to table fields
- **Type hints** - Full type annotation support for better IDE integration
- **Configurable logging** - Flexible logging system with multiple severity levels
- **Data type auto-detection** - Automatic detection of ID, name, date, time, value, and description columns

## Quick Start

### Basic Table
```python
import outfancy.table

table = outfancy.table.Table()
dataset = [(1, 'Marie'), (2, 'Joseph')]
print(table.render(dataset))
```

### Line Chart
```python
import outfancy.chart
from math import sin

line_chart = outfancy.chart.LineChart()
dataset = [(i, sin(i)) for i in range(10)]
line_chart.plot(dataset)
print(line_chart.render(color=True))
```

### Large Table with Pagination
```python
from outfancy.table import LargeTable

large_table = LargeTable()
large_dataset = [(i, f'User {i}', f'user{i}@example.com') for i in range(100)]
print(large_table.render(large_dataset))
```

## Development

### Development installation (pip)
```bash
git clone https://github.com/carlosplanchon/outfancy.git
cd outfancy
pip install -e .
```

### Development installation (uv)
```bash
git clone https://github.com/carlosplanchon/outfancy.git
cd outfancy
uv venv
uv pip install -e ".[dev]"
```

### Running tests

The project includes a comprehensive test suite covering all major functionality:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_table.py

# Run tests with coverage
pytest --cov=outfancy
```

The test suite includes:
- **79 test functions** covering Table, Oneline, and LargeTable classes
- Unit tests for initialization, configuration, and rendering
- Integration tests for complex workflows
- Regression tests for documented bug fixes
- Edge case validation for data integrity

### Logging Configuration

Outfancy uses a configurable logging system. By default, only WARNING and above messages are shown:

```python
import logging
import outfancy.table

# Enable debug logging
logging.getLogger('outfancy').setLevel(logging.DEBUG)

# Create table with debug output
table = outfancy.table.Table()
```

See [LOGGING.md](LOGGING.md) for detailed logging configuration options.

## Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** - Open an issue describing the problem
2. **Suggest features** - Share your ideas for improvements
3. **Submit pull requests** - Fix bugs or implement features
4. **Improve documentation** - Help make the docs clearer
5. **Write tests** - Add test coverage for edge cases

### Code style
- Follow existing code patterns
- Add type hints to new functions
- Include tests for new features
- Update documentation as needed

## Examples & Demos

- **[Funny demo with colors](https://gist.github.com/carlosplanchon/986c7c11a932a7206bb3)** - Colorful table demonstration

### Line Chart Example
<img src='https://raw.githubusercontent.com/carlosplanchon/outfancy/refs/heads/master/examples/sin_little_2.png'>

## License

MIT License - see [LICENSE](LICENSE) file for details
