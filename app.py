
from flask import Flask, jsonify

app = Flask(__name__)

# Route for serving the nodes data
@app.route('/nodes')
def nodes():
    nodes = get_nodes()  # Replace this with your logic to get the list of nodes
    return jsonify(nodes)

# Replace this with your logic to get the list of nodes
def get_nodes():
    nodes = [
        {"ip": "127.0.0.1", "port": 8000},
        {"ip": "127.0.0.1", "port": 8001},
        {"ip": "127.0.0.1", "port": 8002}
    ]
    return nodes

if __name__ == '__main__':
    app.run()
