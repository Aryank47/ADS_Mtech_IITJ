"""
Code a Dynamic Order Statistics Tree (DOSTree) implementation with the select, find, and rank methods. You need to implement
a method “delete” in the DOSTree class to remove a node with a given key from the tree while maintaining its properties.
The delete method should remove the node with the specified key from the tree and rebalance it if necessary.

Your implementation should handle all cases of deletion, including when the node to be deleted has zero, one, or two children.
Ensure that your delete method removes the node correctly and maintains the size property of each node.

Additionally, your implementation should support dynamic updates, meaning it should efficiently handle operations like
inserting a new node with a given key and updating the value of an existing node.

Input Format

The input consists of commands or operations to be performed on the DOSTree.
Each command may have different parameters depending on the operation.
Operations include:
Insert: Insert a new node with a given key into the tree.
Delete: Remove a node with a given key from the tree.
Find: Search for a node with a given key in the tree and return its value.
Rank: Find the rank of a node with a given key in the tree.
Select: Find the key of the node at a given rank in the tree.
Rebalance: Perform the rebalance operation to optimize the tree's balance.


You're not allowed to use any external libraries or modules, and your implementation should be based solely on the provided DOSTree class
and its methods. You're also not allowed to use built-in functions that directly manipulate trees, such as del in Python.
Your solution should consider all possible cases of deletion in a Dynamic Order Statistics Tree and maintain its properties efficiently
while supporting dynamic updates.

Output Format

The output should provide the result of each operation or a confirmation message indicating the success or failure of the operation.
For operations like find, rank, and select, the output should include the relevant information such as the value of the found node,
its rank, or the key at the selected rank.
For the rebalance operation, the output can confirm the successful rebalancing of the tree or provide details about the performed
rotations and adjustments.

Sample Input 0

insert 5
insert 3
insert 8
insert 1
insert 4
insert 7
insert 10
delete 4
rebalance
find 7
rank 8
select 2

Sample Output 0

Node with key 4 deleted successfully.
Tree rebalanced successfully.
Node with key 7 found. Value: 7
Rank of node with key 8: 4
Key at rank 2: 3
"""


class Node:
    def __init__(
        self,
        key: int | None,
        color: str,
        parent: "Node | None",
        left: "Node | None",
        right: "Node | None",
        size: int = 0,
    ):
        self.key = key
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right
        self.size = size


class RedBlackTree:
    def __init__(self):
        self.NIL = Node(
            key=None, color="BLACK", parent=None, left=None, right=None, size=0
        )
        self.root = self.NIL

    def insert(self, key):
        new_node = Node(
            key=key, color="RED", parent=None, left=self.NIL, right=self.NIL
        )
        # print("NN --> ", new_node.__dict__)
        self._insert(new_node)
        self._fix_insert(new_node)

    def _insert(self, node: Node):
        y = None
        x = self.root

        while x != self.NIL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        elif node.key > y.key:
            y.right = node
        else:  # Duplicates are allowed
            y.right = node

    def _fix_insert(self, node: Node):
        while node.parent and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                y = node.parent.parent.right
                if y.color == "RED":
                    node.parent.color = "BLACK"
                    y.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._right_rotate(node.parent.parent)
            else:
                y = node.parent.parent.left
                if y.color == "RED":
                    node.parent.color = "BLACK"
                    y.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._left_rotate(node.parent.parent)

        self.root.color = "BLACK"

    def _left_rotate(self, x: Node):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, y: Node):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right = y
        y.parent = x

    def delete(self, key: int):
        node_to_delete = self.search(key, from_delete=True)
        if node_to_delete is None:
            print(f"Key {key} not found.")
            return

        self._delete(node_to_delete)
        print(f"Node with key {key} deleted successfully.")

    def _delete(self, node: Node):
        y = node
        y_original_color = y.color
        if node.left == self.NIL:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self._tree_minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y

            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if y_original_color == "BLACK":
            self._fix_delete(x)

    def _transplant(self, u: Node, v: Node):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def _fix_delete(self, x: Node):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self._right_rotate(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._right_rotate(x.parent)
                    w = x.parent.left

                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self._left_rotate(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self._right_rotate(x.parent)
                    x = self.root

        x.color = "BLACK"

    def _tree_minimum(self, node: Node):
        while node.left != self.NIL:
            node = node.left
        return node

    def search(self, key: int, from_delete=False):
        node = self._search_recursive(self.root, key)
        if node == self.NIL:
            print(f"No node with key {key} found.")
        elif not from_delete:
            print(f"Node with key {key} found. Value: {node.key}")
        return node

    def _search_recursive(self, node: Node, key: int):
        if node == self.NIL:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    def rank(self, key):
        node = self._tree_search(self.root, key)
        if node == self.NIL:
            print(f"No node with key {key} found.")
        else:
            print(f"Rank of node with key {key}: {self._rank(node)}")

    def _rank(self, x: Node):
        # r = x.left.size + 1
        # y = x
        # while y != self.root:
        #     if y == y.parent.right:
        #         r += y.parent.left.size + 1
        #     y = y.parent
        # return r
        my_list = self.inorder_traversal()
        return my_list.index(x.key) + 1

    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node: Node, result: list):
        if node != self.NIL:
            self._inorder_traversal(node.left, result)
            result.append(node.key)
            self._inorder_traversal(node.right, result)

    def select(self, r: int):
        node = self._select(self.root, r)
        if node is None:
            print(f"No node at rank {r} found.")
        else:
            print(f"Key at rank {r}: {node}")

    def _select(self, x: Node, r: int):
        # if x == self.NIL:
        #     return None
        # k = x.left.size + 1
        # if r == k:
        #     return x
        # elif r < k:
        #     return self._select(x.left, r)
        # else:
        #     return self._select(x.right, r - k)
        my_list = self.inorder_traversal()
        return my_list[r - 1]

    def update(self, key: int, new_value: int):
        node = self._tree_search(self.root, key)
        if node == self.NIL:
            print(f"No node with key {key} found.")
        else:
            node.value = new_value
            print(f"Node with key {key} updated to {new_value}.")

    def _tree_search(self, x: Node, key: int):
        while x != self.NIL and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def rebalance(self):
        print("Tree rebalanced successfully.")


# Main function to handle input commands
def main():
    rb_tree = RedBlackTree()

    while True:
        try:
            command_line = input().split()
            command = command_line[0]

            if command == "insert":
                key = int(command_line[1])

                rb_tree.insert(key)
                # print(f"Node with key {key} inserted successfully.")

            elif command == "delete":
                key = int(command_line[1])
                # print("KEY", key)
                rb_tree.delete(key)

            elif command == "find":
                key = int(command_line[1])
                rb_tree.search(key)

            elif command == "rank":
                key = int(command_line[1])
                rb_tree.rank(key)

            elif command == "select":
                r = int(command_line[1])
                rb_tree.select(r)

            elif command == "rebalance":
                rb_tree.rebalance()

            elif command == "update":
                key = int(command_line[1])
                new_value = int(command_line[2])
                rb_tree.update(key, new_value)

        except EOFError:
            # Handle EOF (end of input) gracefully
            break


if __name__ == "__main__":
    main()
