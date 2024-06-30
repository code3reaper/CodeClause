# calculator_backend.py

def evaluate_expression(expression):
    try:
        result = eval(expression)
    except Exception:
        raise ValueError("Invalid expression")
    return result
