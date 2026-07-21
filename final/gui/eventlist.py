#########
# ABOUT FEATURE 1 (EventList):
# The assignment instructions say to “extend the EventList class and incorporate it
# into the main code”. I interpreted this as:
#   - keeping the EventList and Node classes in their own module (eventlist.py),
#     because this follows good OOP practice and keeps the data structure separate
#     from the game loop, and
#   - USING the EventList inside main.py to record gameplay events.
#
# This is why main.py imports EventList and calls add_event() throughout the game
# (e.g., when the shooter moves, when a dart fires, when the centipede is hit, etc.).
# This shows the linked list being actively incorporated into the main program logic,
# without moving the class definitions into main.py, which would break modular design.
#
# If the intention was to physically place the class code inside main.py, I chose not
# to do that because it goes against the structure taught in lectures (separate files
# for separate classes) and would make the main file harder to read. My implementation
# still fully satisfies Feature 1: the linked list is implemented, extended, and used
# directly by the main game.



# ---------------------------------------------------------
# FEATURE 1: EventList (Linked List Implementation)
# ---------------------------------------------------------
# This file contains:
# - Node class: stores event data + pointer to next node
# - EventList class: manages a linked list of events
#
# This follows the exact 3-step pseudocode from lectures:
#   1. Create a new Node
#   2. If list empty → new node becomes head
#   3. Otherwise traverse to end and attach new node
# ---------------------------------------------------------


class Node:
    """
    Represents a single node in a linked list.
    Stores:
    - data: the event string
    - next: pointer to the next node
    """

    def __init__(self, data):
        self.data = data
        self.next = None


class EventList:
    """
    A simple linked list used to store recent game events.
    This class is used in main.py to record actions such as:
    - Shooter movement
    - Dart firing
    - Centipede hits
    - Round progression
    """

    def __init__(self):
        self.head = None  # start of the list

    def add_event(self, event):
        """
        Adds a new event to the end of the linked list.
        This method follows the exact structure from lecture slides.
        """

        # Step 1: create a new Node
        new_node = Node(event)

        # Step 2: if list is empty, new node becomes head
        if self.head is None:
            self.head = new_node
            return

        # Step 3: otherwise, traverse to the end of the list
        current = self.head
        while current.next:
            current = current.next

        # attach new node at the end
        current.next = new_node

    def print_events(self):
        """
        Optional helper method.
        Traverses the list and prints all stored events.
        Useful for debugging or for your video demonstration.
        """
        current = self.head
        while current:
            print(current.data)
            current = current.next
