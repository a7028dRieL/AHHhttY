# 代码生成时间: 2025-09-17 03:52:27
import quart
from random import randint

"""
A Quart application that provides a random number generator API.
"""

app = quart.Quart(__name__)

@app.route('/generate', methods=['GET'])
async def generate_random_number():
    """
    Generates a random number between 1 and 100 and returns it as a JSON response.
    If no parameters are provided, the default range is 1 to 100.
    If parameters are provided, it uses the provided parameters to set the range.
    Parameters:
        - min (optional): The minimum value of the range, defaults to 1.
        - max (optional): The maximum value of the range, defaults to 100.
    """
    try:
        min_value = int(quart.request.args.get('min', 1))
        max_value = int(quart.request.args.get('max', 100))
        if min_value > max_value:
            return {
                "error": "Minimum value cannot be greater than maximum value."
            }, 400
        random_number = randint(min_value, max_value)
        return {
            "random_number": random_number
        }
    except ValueError:
        return {
            "error": "Invalid input. Please ensure that min and max are integers."
        }, 400

if __name__ == '__main__':
    app.run(debug=True)