import ast
import operator
from collections.abc import Callable
from typing import Any

from keel.domain.exceptions import ToolExecutionError

_BINARY_OPERATORS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class CalculatorTool:

    """
    
    A safe arithmetic evaluator built on AST whitelisting.
    
    
    Usage
    -----
    The expression is parsed, never executed; only numeric literals, the four
    basic operations, floor division, modulo, exponentiation, and unary signs
    are admitted. Anything else — names, calls, attributes, subscripts — is
    rejected, which is what makes this demo tool safe to expose to a reasoner
    that may produce arbitrary input.
    ```python
    from keel.adapters.tools import CalculatorTool
    
    tool = CalculatorTool()
    result = await tool.execute({"expression": "(2 + 3) * 4"})
    print(result)
    ```
    
    """

    name: str = "calculator"
    description: str = "Evaluates a plain arithmetic expression (+, -, *, /, //, %, **, parentheses) and returns the numeric result."
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The arithmetic expression to evaluate, e.g. '(2 + 3) * 4'",
            }
        },
        "required": ["expression"],
    }


    async def execute(self, arguments: dict[str, Any]) -> str:

        """
        
        Evaluates the arithmetic expression in the arguments.
        
        
        Parameters
        ----------
        arguments : dict[str, Any]
            The tool arguments; requires an 'expression' string.
        
        
        Returns
        -------
        str
            The numeric result rendered as a string.
        
        
        Raises
        ------
        ToolExecutionError
            If the expression is missing, malformed, or uses a disallowed construct.
        
        """

        if not isinstance(arguments, dict):
            raise TypeError(f"arguments must be a dictionary. Received: {arguments} with type {type(arguments)}")


        expression = arguments.get("expression")
        if not isinstance(expression, str) or not expression.strip():
            raise ToolExecutionError(f"'expression' must be a non-empty string. Received: {expression}")

        try:
            tree = ast.parse(expression, mode="eval")
            value = self._evaluate(tree.body)
        except ToolExecutionError:
            raise
        except ZeroDivisionError as error:
            raise ToolExecutionError("Division by zero") from error
        except Exception as error:
            raise ToolExecutionError(f"Malformed arithmetic expression: '{expression}'") from error

        if isinstance(value, float) and value.is_integer():
            return str(int(value))

        return str(value)


    def _evaluate(self, node: ast.expr) -> float:

        """
        
        Recursively evaluates a whitelisted AST node.
        
        
        Parameters
        ----------
        node : ast.expr
            The AST node to evaluate.
        
        
        Returns
        -------
        float
            The numeric value of the node.
        
        
        Raises
        ------
        ToolExecutionError
            If the node type or operator is not whitelisted.
        
        """

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return float(node.value)

        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
            return _BINARY_OPERATORS[type(node.op)](self._evaluate(node.left), self._evaluate(node.right))

        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
            return _UNARY_OPERATORS[type(node.op)](self._evaluate(node.operand))

        raise ToolExecutionError(f"Disallowed construct in expression: {type(node).__name__}")
