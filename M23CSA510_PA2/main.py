import random
import time

from Btree import BTree
from employee import Employee
from faker import Faker
from ordered_array import OrderedArray

faker = Faker()


def benchmark(func):
    def wrapper(*args, **kwargs):
        fn_name = func.__name__
        print(f"Benchmarking {fn_name}")

        # Start time
        start_time = time.time()

        # Call the function
        result = func(*args, **kwargs)

        # End time
        end_time = time.time()

        elapsed_time = end_time - start_time

        print(f"Time taken: {elapsed_time} seconds \n\n")

        return result

    return wrapper


@benchmark
def oa_insert(ordered_array: OrderedArray, employee_records: list[Employee]):
    for employee in employee_records:
        ordered_array.insert(employee)


@benchmark
def Btree_insert(b_tree: BTree, employee_records: list[Employee]):
    for employee in employee_records:
        b_tree.insert(employee)


@benchmark
def successful_oa_search(ordered_array: OrderedArray, employee: Employee):
    print(
        f"Successful Ordered Array Search Result for 10000 employees records:"
        f" {ordered_array.search(employee.employee_id)}"
    )


@benchmark
def successful_Btree_search(b_tree: BTree, employee: Employee):
    print(
        f"Successful B-Tree Search Result for 10000 employees records: {b_tree.search(employee.employee_id)}"
    )


@benchmark
def unsuccessful_oa_search(ordered_array: OrderedArray):
    print(
        f"UnSuccessful Ordered Array Search Result for 10000 employees records: {ordered_array.search(4534354)}"
    )


@benchmark
def unsuccessful_Btree_search(b_tree: BTree):
    print(
        f"UnSuccessful B-Tree Search Result for 10000 employees records: {b_tree.search(4534354)}"
    )


@benchmark
def successful_oa_delete(ordered_array: OrderedArray, employee: Employee):
    ordered_array.delete(employee.employee_id)


@benchmark
def successful_Btree_delete(b_tree: BTree, employee: Employee):
    b_tree.delete(employee)


def main():
    # Initializing Data Structures
    ordered_array = OrderedArray()
    b_tree = BTree(order=100)

    # Generating Employee Records
    employee_records: list[Employee] = []
    for i in range(0, 10000):
        employee_records.append(
            Employee(
                employee_id=i,
                name=faker.name(),
                department=faker.name(),
                salary=random.randint(100000, 10000000),
            )
        )

    oa_insert(ordered_array, employee_records)
    Btree_insert(b_tree, employee_records)

    search_employee = employee_records[1343]
    successful_oa_search(ordered_array, search_employee)
    successful_Btree_search(b_tree, search_employee)

    unsuccessful_oa_search(ordered_array)
    unsuccessful_Btree_search(b_tree)

    successful_oa_delete(ordered_array, search_employee)
    successful_oa_search(ordered_array, search_employee)
    print(f"Is Array sorted after deleting employee? -> {ordered_array.is_sorted()} \n")

    # print("\n\n")
    # b_tree.print_btree()

    successful_Btree_search(b_tree, search_employee)
    successful_Btree_delete(b_tree, search_employee)

    successful_Btree_delete(b_tree, search_employee)

    successful_Btree_delete(b_tree, employee_records[1344])
    successful_Btree_search(b_tree, employee_records[1344])

    successful_Btree_delete(b_tree, employee_records[1344])


main()
