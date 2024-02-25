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
            self.insert_key(employee)
        else:
            while i >= 0 and employee.employee_id < self.employees[i].employee_id:
                i -= 1

            i += 1
            if len(self.children[i].employees) == (2 * self.order - 1):
                self.split_child(i)

                if employee.employee_id > self.employees[i].employee_id:
                    i += 1

            self.children[i].insert_non_full(employee)

    def insert_key(self, employee: Employee):
        i = len(self.employees) - 1

        while i >= 0 and employee.employee_id < self.employees[i].employee_id:
            i -= 1

        self.employees.insert(i + 1, employee)

    def split_child(self, i: int):
        new_node = BTreeNode(order=self.order, leaf=self.children[i].leaf)
        split_node = self.children[i]

        self.employees.insert(i, split_node.employees[self.order - 1])
        self.children.insert(i + 1, new_node)

        new_node.employees = split_node.employees[self.order :]
        split_node.employees = split_node.employees[: self.order - 1]

        if not split_node.leaf:
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
        while not current.leaf:
            current = current.children[-1]
        return current, len(current.employees) - 1

    def find_successor(self, i: int):
        current = self.children[i + 1]
        while not current.leaf:
            current = current.children[0]
        return current, 0

    def merge(self, i: int):
        child = self.children[i]
        sibling = self.children[i + 1]

        child.employees.append(self.employees[i])
        child.employees.extend(sibling.employees)
        child.children.extend(sibling.children)

        del self.employees[i]
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
            if self.leaf:
                del self.employees[i]
            else:
                if len(self.children[i]) >= self.order:
                    predecessor, pred_index = self.find_predecessor(i)
                    self.employees[i] = predecessor.employees[pred_index]
                    self.children[i].delete(self.employees[i])
                elif len(self.children[i + 1]) >= self.order:
                    successor, successor_index = self.find_successor(i)
                    self.employees[i] = successor.employees[successor_index]
                    self.children[i + 1].delete(self.employees[i])
                else:
                    self.merge(i)
                    self.children[i].delete(employee)
        else:
            if self.leaf:
                print("Key not found:", employee)
            else:
                if len(self.children[i]) < self.order:
                    if i > 0 and len(self.children[i - 1]) >= self.order:
                        self.borrow_from_prev(i)
                    elif (
                        i < len(self.employees)
                        and len(self.children[i + 1]) >= self.order
                    ):
                        self.borrow_from_next(i)
                    elif i > 0:
                        self.merge(i - 1)
                    else:
                        self.merge(i)
                    if employee.employee_id > self.employees[i].employee_id:
                        i += 1
                self.children[i].delete(employee)


class BTree:
    def __init__(self, order: int):
        self.root = BTreeNode(order=order, leaf=True)
        self.order = order

    def insert(self, employee: Employee):
        root = self.root

        if len(root.employees) == (2 * self.order - 1):
            new_node = BTreeNode(order=self.order, leaf=False)
            new_node.children.append(self.root)
            self.root = new_node
            new_node.split_child(0)

            if employee.employee_id < new_node.employees[0].employee_id:
                new_node.children[0].insert_non_full(employee)
            else:
                new_node.children[1].insert_non_full(employee)
        else:
            root.insert_non_full(employee)

    def search(self, employee_id: int):

        return self.root.search(employee_id)

    def delete(self, employee: Employee):
        self.root.delete(employee)
