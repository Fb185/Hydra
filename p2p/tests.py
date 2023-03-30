import unittest
import threading
import time
from newnode import Node

class TestNode(unittest.TestCase):
    def setUp(self):
        self.host = "127.0.0.1"
        self.port1 = 8000
        self.port2 = 8001
        self.node1 = Node(self.host, self.port1)
        self.node2 = Node(self.host, self.port2)
        threading.Thread(target=self.node1.start).start()
        threading.Thread(target=self.node2.start).start()
        time.sleep(1)  # wait for nodes to start up

    def test_connection(self):
        self.node1.connect_to_node(self.host, self.port2)
        time.sleep(1)  # wait for connection to establish
        self.assertEqual(len(self.node1.connections), 1)
        self.assertEqual(len(self.node2.connections), 1)

    def test_task_assignment(self):
        self.node1.connect_to_node(self.host, self.port2)
        time.sleep(1)  # wait for connection to establish
        self.node2.request_task("1")
        time.sleep(1)  # wait for task request to propagate
        self.node1.broadcast("YES:1")
        time.sleep(2)  # wait for task acceptance to propagate
        self.assertEqual(len(self.node1.task_acceptors), 1)
        self.assertEqual(len(self.node2.task_acceptors), 1)
        self.assertEqual(len(self.node1.task_acceptors["1"]), 1)

    def tearDown(self):
        self.node1.close()
        self.node2.close()

if __name__ == "__main__":
    unittest.main()
