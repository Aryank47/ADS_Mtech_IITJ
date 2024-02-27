from employee import Employee


class BTreeNode:
    def __init__(self, order: int, leaf=True):
        self.leaf = leaf
        self.employees: list[Employee] = []
        self.children: list["BTreeNode"] = []
        self.order = order

    def insert_non_full(self, employee: Employee):
        i = len(self.employees) - 1

        if self.leaf:
            # Case 1: Node is a leaf, insert the employee
            self.insert_key(employee)
        else:
            # Case 2: Node is not a leaf
            while i >= 0 and employee.employee_id < self.employees[i].employee_id:
                i -= 1

            i += 1
            if len(self.children[i].employees) == (2 * self.order - 1):
                # Case 2a: Child is full, split the child
                self.split_child(i)

                # Determine which child to descend into
                if employee.employee_id > self.employees[i].employee_id:
                    i += 1

            # Descend into the appropriate child
            self.children[i].insert_non_full(employee)

    def insert_key(self, employee: Employee):
        i = len(self.employees) - 1

        # Find the correct position to insert the key
        while i >= 0 and employee.employee_id < self.employees[i].employee_id:
            i -= 1

        # Insert the key at the appropriate position
        self.employees.insert(i + 1, employee)

    def split_child(self, i: int):
        new_node = BTreeNode(order=self.order, leaf=self.children[i].leaf)
        split_node = self.children[i]

        # Insert the middle key of the split_node to the current node
        self.employees.insert(i, split_node.employees[self.order - 1])

        # Insert the new_node as the child after the middle key
        self.children.insert(i + 1, new_node)

        # Move keys and children from split_node to new_node
        new_node.employees = split_node.employees[self.order :]
        split_node.employees = split_node.employees[: self.order - 1]

        if not split_node.leaf:
            # If split_node is not a leaf, move children as well
            new_node.children = split_node.children[self.order :]
            split_node.children = split_node.children[: self.order]

    def search(self, employee_id: int):
        i = 0
        while i < len(self.employees) and employee_id > self.employees[i].employee_id:
            i += 1

        if i < len(self.employees) and employee_id == self.employees[i].employee_id:
            return self.employees[i]

        if self.leaf:
            return f"Employee with id {employee_id} not found"

        return self.children[i].search(employee_id)

    def find_predecessor(self, i: int):
        current = self.children[i]

        # Traverse to the rightmost child until a leaf is reached
        while not current.leaf:
            current = current.children[-1]

        # Return the rightmost leaf and its index
        return current, len(current.employees) - 1

    def find_successor(self, i: int):
        current = self.children[i + 1]

        # Traverse to the leftmost child until a leaf is reached
        while not current.leaf:
            current = current.children[0]

        # Return the leftmost leaf and its index
        return current, 0

    def merge(self, i: int):
        child = self.children[i]
        sibling = self.children[i + 1]

        # Move the key from the current node to the child node
        child.employees.append(self.employees[i])

        # Move all employees and children from the sibling to the child
        child.employees.extend(sibling.employees)
        child.children.extend(sibling.children)

        # Remove the key from the current node
        del self.employees[i]

        # Remove the merged sibling from the children list
        del self.children[i + 1]

    def borrow_from_prev(self, i: int):
        child = self.children[i]
        sibling = self.children[i - 1]

        child.employees.insert(0, self.employees[i - 1])
        self.employees[i - 1] = sibling.employees.pop()

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def borrow_from_next(self, i: int):
        child = self.children[i]
        sibling = self.children[i + 1]

        child.employees.append(self.employees[i])
        self.employees[i] = sibling.employees.pop(0)

        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def delete(self, employee: Employee):
        i = 0
        while (
            i < len(self.employees)
            and employee.employee_id > self.employees[i].employee_id
        ):
            i += 1

        if (
            i < len(self.employees)
            and employee.employee_id == self.employees[i].employee_id
        ):
            # Case 1: Key is in this node and node is a leaf
            if self.leaf:
                del_idx = self.employees.index(employee)
                del self.employees[del_idx]
                print("Deleted Successfully")
            else:
                # Find predecessor (largest key in the subtree)
                if len(self.children[i].employees) >= self.order:
                    predecessor, pred_index = self.find_predecessor(i)
                    # Replace key with predecessor's key
                    self.employees[i] = predecessor.employees[pred_index]
                    # Delete predecessor in the subtree
                    self.children[i].delete(self.employees[i])
                elif len(self.children[i + 1].employees) >= self.order:
                    # Case 3: Key is in this node, but in a child which has
                    # fewer than order keys
                    # Find successor (smallest key in the subtree)
                    successor, successor_index = self.find_successor(i)
                    # Replace key with successor's key
                    self.employees[i] = successor.employees[successor_index]
                    # Delete successor in the subtree
                    self.children[i + 1].delete(self.employees[i])
                else:
                    # Case 4: Key is in this node, but in a child with fewer
                    # than order keys,
                    # and the next sibling has fewer than order keys
                    self.merge(i)
                    # Delete the key in the merged child
                    self.children[i].delete(employee)
        else:
            # Case 5: Key is not present in this node
            if self.leaf:
                print("probably already deleted or employee does not exists")
                return
            else:
                # If the child has fewer than order keys, try to borrow or merge
                if len(self.children[i].employees) < self.order:
                    if i > 0 and len(self.children[i - 1].employees) >= self.order:
                        self.borrow_from_prev(i)
                    elif (
                        i < len(self.employees)
                        and len(self.children[i + 1].employees) >= self.order
                    ):
                        self.borrow_from_next(i)
                    elif i > 0:
                        self.merge(i - 1)
                        self.children[i - 1].delete(employee)
                    else:
                        self.merge(i)
                        self.children[i].delete(employee)
                    # Adjust the index if necessary
                    if employee.employee_id > self.employees[i].employee_id:
                        i += 1

                self.children[i].delete(employee)


class BTree:
    def __init__(self, order: int):
        self.root = BTreeNode(order=order, leaf=True)
        self.order = order

    def insert(self, employee: Employee):
        root = self.root

        # Case 1: Root is full, create a new root and split the old root
        if len(root.employees) == (2 * self.order - 1):
            new_node = BTreeNode(order=self.order, leaf=False)
            new_node.children.append(self.root)
            self.root = new_node
            new_node.split_child(0)

            # Determine which of the two children is now the correct one to
            # insert into
            if employee.employee_id < new_node.employees[0].employee_id:
                new_node.children[0].insert_non_full(employee)
            else:
                new_node.children[1].insert_non_full(employee)
        else:
            # Case 2: Root is not full, insert into the root
            root.insert_non_full(employee)

    def search(self, employee_id: int):
        return self.root.search(employee_id)

    def delete(self, employee: Employee):
        root = self.root

        if not root.employees:
            print("Tree is empty. Nothing to delete.")
            return

        root.delete(employee)

        # If the root has no keys and has a child, make the child as the new root
        if not root.employees and root.children:
            self.root = root.children[0]

    def print_btree(self):
        self._print_btree(self.root)

    def _print_btree(self, node: BTreeNode, level=0, child_no=0):
        if node is not None:
            print(f"Level --> {level}")
            print(f"Child No --> {child_no}")
            print(f"No of employees --> {len(node.employees)}")
            print(f"No of children --> {len(node.children)}")
            print(
                {
                    ", ".join(
                        map(
                            lambda e: "id:" + str(e.employee_id) + "-> name:" + e.name,
                            node.employees,
                        )
                    )
                }
            )
            level += 1
            for child in node.children:
                child_no += 1
                self._print_btree(child, level, child_no)
