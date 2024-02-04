from flask import Flask, request

app = Flask(__name__)

@app.route('/print_headers', methods=['GET'])
def print_headers():
    # Get all headers from the incoming request
    all_headers = request.headers

    # Print headers to the console
    print("Received Headers:")
    for header, value in all_headers.items():
        print(f"{header}: {value}")

    return all_headers.__str__()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
