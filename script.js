// Fetch data from the server
function fetchData() {
  fetch('/nodes')
    .then(response => response.json())
    .then(data => {
      displayNodes(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Display nodes on the web page
function displayNodes(nodes) {
  const container = document.getElementById('nodeContainer');
  container.innerHTML = ''; // Clear previous content

  nodes.forEach(node => {
    const nodeElement = document.createElement('div');
    nodeElement.className = 'node';

    const ipAddress = document.createElement('p');
    ipAddress.innerText = `IP Address: ${node.ip}`;

    const portNumber = document.createElement('p');
    portNumber.innerText = `Port Number: ${node.port}`;

    nodeElement.appendChild(ipAddress);
    nodeElement.appendChild(portNumber);

    container.appendChild(nodeElement);
  });
}

// Fetch data initially when the page loads
fetchData();
