class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # Height of the node


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def update_height(self, node):
        if node is not None:
            node.height = 1 + max(
                self.height(node.left),
                self.height(node.right),
            )

    def balance(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y

    def balance_node(self, node):
        if node is None:
            return node

        # Update height of the current node
        self.update_height(node)

        # Get the balance factor
        balance = self.balance(node)

        # Left heavy
        if balance > 1:
            # Left-Right case
            if self.balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Right heavy
        if balance < -1:
            # Right-Left case
            if self.balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def insert(self, root, key):
        if root is None:
            return AVLNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            # Duplicate keys are not allowed
            return root

        # Update height and balance of the current node
        return self.balance_node(root)

    def insert_key(self, key):
        self.root = self.insert(self.root, key)

    def delete(self, root, key):
        if root is None:
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            # Node with two children: Get the inorder successor
            temp = self.get_min_value_node(root.right)

            # Copy the inorder successor's key to this node
            root.key = temp.key

            # Delete the inorder successor
            root.right = self.delete(root.right, temp.key)

        # Update height and balance of the current node
        return self.balance_node(root)

    def delete_key(self, key):
        self.root = self.delete(self.root, key)

    def get_min_value_node(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current

    def preorder_traversal(self, root):
        result = []
        if root:
            result.append(root.key)
            result.extend(self.preorder_traversal(root.left))
            result.extend(self.preorder_traversal(root.right))
        return result

    def preorder(self):
        return self.preorder_traversal(self.root)

    def search(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def search_key(self, key):
        return self.search(self.root, key)


# no_of_oprn=int(input())
operations = []
keys = [9, 5, 10, 0, 6, 11, -1, 1, 2, 10, 6, 1, 53]
for key in keys:
    operations.append(("INSERT", key))
operations.append(("SEARCH", 10))
operations.append(("DELETE", 10))
operations.append(("DELETE", 10))
operations.append(("DELETE", 1))
# operations.append(("SEARCH",10))
# operations.append(("SEARCH",10))

# for i in range(0,no_of_oprn):
#     operation=input()
#     type,value=operation.split(" ")
#     operations.append((str(type),int(value)))

# print(no_of_oprn)
# print(operations)

avl_tree = AVLTree()
for oprn in operations:
    type, value = oprn
    if type == "INSERT":
        avl_tree.insert_key(value)
    elif type == "DELETE":
        all_instance_deleted = False
        while not all_instance_deleted:
            found = avl_tree.search_key(value)
            if not found:
                all_instance_deleted = True
            avl_tree.delete_key(value)
    elif type == "SEARCH":
        found = avl_tree.search_key(value)
        if found:
            print("FOUND")
        else:
            print("NOT FOUND")
    else:
        print("INVALID OPERATION")

print(" ".join(map(str, avl_tree.preorder())))
