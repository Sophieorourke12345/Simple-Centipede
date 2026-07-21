class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class EventList:
    def __init__(self):
        self.head = None

    def add_event(self, event):
        new_node = Node(event)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node

    def print_events(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next
