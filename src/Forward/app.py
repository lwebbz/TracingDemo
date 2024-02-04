from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/forward', methods=['POST'])
def forward_request():
    # Define a list of headers to forward
    headers_to_forward = [
        'x-request-id',
        'x-b3-traceid',
        'x-b3-spanid',
        'x-b3-parentspanid',
        'x-b3-sampled',
        'x-b3-flags'
    ]

    # Get headers from the incoming request and filter only the specified headers
    incoming_headers = {key: value for key, value in request.headers.items() if key.lower() in headers_to_forward}

    # Get the URL from the request body
    request_data = request.get_json()
    if 'url' not in request_data:
        return "Error: 'url' not provided in the request body", 400

    outbound_url = request_data['url']

    print(f"Sending request to outbound url: {outbound_url}")
    # Make an outbound HTTP call with the filtered headers and specified URL
    outbound_response = requests.get(outbound_url, headers=incoming_headers)

    return f"Outbound Response: {outbound_response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
