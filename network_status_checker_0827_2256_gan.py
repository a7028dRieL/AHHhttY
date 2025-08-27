# 代码生成时间: 2025-08-27 22:56:58
import quart
from quart import jsonify
import requests
import socket
from urllib.parse import urlparse

""" A Quart application for checking network connection status. """

app = quart.Quart(__name__)

"""
Check if the provided URL is accessible and returns its status code.

Args:
    url (str): The URL to check.

Returns:
    A JSON response with the HTTP status code and a message.
"""
@app.route("/check", methods=["GET"])
async def check_url():
    url = quart.request.args.get("url", "")
    try:
        # Parse the URL to ensure it is valid
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid URL")

        # Make a request to the URL and get the status code
        response = requests.get(url, timeout=10)
        return jsonify({
            "status_code": response.status_code,
            "message": "URL is accessible"
        })
    except requests.exceptions.RequestException as e:
        quart.abort(quart.http.SERVICE_UNAVAILABLE, description=str(e))
    except ValueError as e:
        quart.abort(quart.http.BAD_REQUEST, description=str(e))
    except Exception as e:
        quart.abort(quart.http.INTERNAL_SERVER_ERROR, description=str(e))

"""
Check if the provided hostname is reachable and returns a boolean.

Args:
    hostname (str): The hostname to check.

Returns:
    A JSON response indicating whether the hostname is reachable.
"""
@app.route("/ping", methods=["GET"])
async def ping_hostname():
    hostname = quart.request.args.get("hostname", "")
    if not hostname:
        quart.abort(quart.http.BAD_REQUEST, description="No hostname provided")
    try:
        # Use socket to check if the hostname is reachable
        # Set a timeout of 1 second
        socket.create_connection((hostname, 80), 1)
        return jsonify({
            "reachable": True,
            "message": "Hostname is reachable"
        })
    except socket.error as e:
        return jsonify({
            "reachable": False,
            "message": "Hostname is not reachable"
        })
    except Exception as e:
        quart.abort(quart.http.INTERNAL_SERVER_ERROR, description=str(e))

if __name__ == '__main__':
    app.run(debug=True)