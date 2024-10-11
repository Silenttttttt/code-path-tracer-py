import ast
import graphviz
import os
import sys

class CodePathTracer(ast.NodeVisitor):
    def __init__(self):
        self.graph = graphviz.Digraph()
        self.graph.attr(rankdir='TB', nodesep='0.5', ranksep='0.7')  # Set layout to vertical
        self.current_function = None
        self.current_class = None
        self.defined_functions = set()  # Track functions defined in the file
        self.edges = set()  # Track edges to avoid duplicates

    def visit_ClassDef(self, node):
        # Set the current class
        self.current_class = node.name
        # Add class to the graph
        self.graph.node(node.name, shape='box')
        # Visit all methods in the class
        self.generic_visit(node)
        # Reset current class after processing
        self.current_class = None

    def visit_FunctionDef(self, node):
        # Set the current function
        self.current_function = f"{self.current_class}.{node.name}" if self.current_class else node.name
        # Add function to the graph
        self.graph.node(self.current_function)
        # Add to the set of defined functions
        self.defined_functions.add(self.current_function)
        # Visit all statements in the function
        self.generic_visit(node)

    def visit_Call(self, node):
        # Handle method calls
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            # Check if the method is defined in the current class
            if self.current_class:
                full_method_name = f"{self.current_class}.{method_name}"
                if full_method_name in self.defined_functions:
                    edge = (self.current_function, full_method_name)
                    if edge not in self.edges:
                        self.graph.edge(*edge)
                        self.edges.add(edge)
            # Check if the method is defined in any class
            for defined_function in self.defined_functions:
                if defined_function.endswith(f".{method_name}"):
                    edge = (self.current_function, defined_function)
                    if edge not in self.edges:
                        self.graph.edge(*edge)
                        self.edges.add(edge)
        # Handle function calls
        elif isinstance(node.func, ast.Name) and node.func.id in self.defined_functions:
            # Ensure the function is not the entry point 'main' unless explicitly called
            if node.func.id != 'main' or self.current_function != 'main':
                edge = (self.current_function, node.func.id)
                if edge not in self.edges:
                    self.graph.edge(*edge)
                    self.edges.add(edge)
        self.generic_visit(node)

    def trace(self, code):
        tree = ast.parse(code)
        self.visit(tree)
        return self.graph



def main():
    # Take the filename from sys input, default to "graph_maker.py"
    filename = sys.argv[1] if len(sys.argv) > 1 else "graph_maker.py"

    # Convert to absolute path if necessary
    filename = os.path.abspath(filename)

    # Check if the file exists
    if not os.path.isfile(filename):
        print(f"File '{filename}' not found.")
        return

    # Read the file content
    with open(filename, 'r') as file:
        code = file.read()

    # Trace the code and generate the flowchart
    tracer = CodePathTracer()
    flowchart = tracer.trace(code)
    flowchart.render('flowchart', format='png', view=True)
    
if __name__ == "__main__":
    main()
    