from employee import Employee


class OrderedArray:
    def __init__(self):
        self.records: list[Employee] = []

    def insert(self, employee: Employee):
        # index = self._binary_search(employee.employee_id)
        self.records.append(employee)

    def _binary_search(self, target_id: int):
        low, high = 0, len(self.records) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.records[mid].employee_id == target_id:
                return mid
            elif self.records[mid].employee_id < target_id:
                low = mid + 1
            else:
                high = mid - 1
        return low

    def search(self, target_id: int):
        index = self._binary_search(target_id)
        if index < len(self.records) and self.records[index].employee_id == target_id:
            return self.records[index]
        else:
            return None

    def delete(self, target_id: int):
        index = self._binary_search(target_id)
        if index < len(self.records) and self.records[index].employee_id == target_id:
            del self.records[index]

    def is_sorted(self):
        return all(
            self.records[i].employee_id <= self.records[i + 1].employee_id
            for i in range(len(self.records) - 1)
        )
