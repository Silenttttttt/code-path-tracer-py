# Code Path Tracer

## Overview

The Code Path Tracer is a tool designed to visualize the flow of function calls within a Python file. By leveraging Python's `ast` module and `graphviz`, it provides a graphical representation of how functions interact within your code. This project serves as a valuable resource for understanding code structure and flow, making it a useful tool for both learning and code analysis.

## Features

- Parses Python code to identify classes and functions.
- Visualizes the flow of function calls within the code.
- Generates a flowchart using Graphviz, aiding in code comprehension and debugging.

## Usage

To use this tool, run the script and provide either a relative or absolute path to a Python file (default is `graph_maker.py`). The script will parse the file and generate a flowchart of the function and method calls, which will be saved as a PNG file and opened for viewing.

```bash
python graph_maker.py /path/to/your/file.py
```

## Limitations

- The tool only visualizes functions and methods defined within the specified file. External calls to functions or methods in other files or libraries will not appear in the flowchart.

## Benefits

- Enhances understanding of code structure and function interactions.
- Useful for educational purposes, code reviews, and debugging.
- Provides a visual aid for complex codebases.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
