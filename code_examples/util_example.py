import sys
import os

# Add parent directory to sys.path if not there
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redeal.util import create_func, reify

def test_create_func():
    print("Testing create_func...")
    
    # Define a simple function body as a string
    body = "return a + b"
    
    # Dynamically create the function
    # Passing the current module's globals (as the module argument is often sys.modules[__name__])
    current_module = sys.modules[__name__]
    add_func = create_func(current_module, "add", "(a, b)", body)
    
    # Use the created function
    result = add_func(10, 20)
    print(f"Created function 'add(10, 20)': {result}")
    
    # You can also pass a lambda
    lambda_func = create_func(current_module, "multiply", "(a, b)", lambda a, b: a * b)
    print(f"Created function from lambda 'multiply(10, 20)': {lambda_func(10, 20)}")

class ExampleClass:
    def __init__(self):
        self.count = 0

    @reify
    def expensive_property(self):
        self.count += 1
        print(f"Calculating expensive_property (Calculation #{self.count})...")
        return 42

def test_reify():
    print("\nTesting reify...")
    obj = ExampleClass()
    
    print("First access:")
    val1 = obj.expensive_property
    print(f"Result: {val1}")
    
    print("Second access (should be cached):")
    val2 = obj.expensive_property
    print(f"Result: {val2}")
    
    print(f"Calculation count: {obj.count}")
    assert val1 == val2 == 42
    assert obj.count == 1

if __name__ == "__main__":
    test_create_func()
    test_reify()
