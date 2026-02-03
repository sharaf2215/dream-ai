import ast

expr = '50 * 50'

def _validate(node):
    allowed = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
        ast.USub, ast.UAdd,
        ast.Constant,
        ast.Load,
        ast.Tuple,
    )
    if not isinstance(node, allowed):
        raise ValueError(f"Disallowed syntax: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _validate(child)

try:
    tree = ast.parse(expr, mode="eval")
    _validate(tree)
    result = eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, {})
    print(result)
except Exception as e:
    print(f"Error calculating '{expr}': {e}")
