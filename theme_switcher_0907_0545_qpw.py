# 代码生成时间: 2025-09-07 05:45:59
# theme_switcher.py

"""
A simple theme switcher application using Quart framework.
This application allows users to switch between themes.
"""

from quart import Quart, request, jsonify, abort
from werkzeug.exceptions import BadRequestKeyError

app = Quart(__name__)

# Define available themes
AVAILABLE_THEMES = {'light', 'dark'}

# Define the default theme
DEFAULT_THEME = 'light'

# Store the current theme in the session
@app.before_serving
async def before_serving():
    app.session_interface.new = lambda: { 'theme': DEFAULT_THEME }

@app.route('/theme/<theme_name>')
async def switch_theme(theme_name: str):
    """
    Endpoint to switch themes.
    :param theme_name: The name of the theme to switch to.
    :return: A JSON response with the current theme.
    """
    if theme_name not in AVAILABLE_THEMES:
        # If the theme is not available, abort with a 400 error.
        abort(BadRequestKeyError('Invalid theme name'))
    else:
        # Set the theme in the session
        app.session['theme'] = theme_name
        return jsonify({'theme': app.session['theme']})

@app.route('/theme')
async def get_current_theme():
    """
    Endpoint to get the current theme.
    :return: A JSON response with the current theme.
    """
    try:
        # Get the current theme from the session
        current_theme = app.session['theme']
    except KeyError:
        # If the theme is not set, return the default theme
        current_theme = DEFAULT_THEME
    return jsonify({'theme': current_theme})

if __name__ == '__main__':
    # Run the application
    app.run(debug=True)
