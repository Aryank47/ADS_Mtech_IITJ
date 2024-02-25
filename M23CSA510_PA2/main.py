import random
import time

from Btree import BTree
from employee import Employee
from faker import Faker
from ordered_array import OrderedArray

faker = Faker()


# Inserting Records and Measuring Time
def benchmark(func):
    def wrapper(*args, **kwargs):
        fn_name = func.__name__
        print(f"Benchmarking loops in {fn_name}")

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
        f"Successful Ordered Array Search Result:"
        f" {ordered_array.search(employee.employee_id)}"
    )


@benchmark
def successful_Btree_search(b_tree: BTree, employee: Employee):
    print(f"Successful B-Tree Search Result: {b_tree.search(employee.employee_id)}")


@benchmark
def unsuccessful_oa_search(ordered_array: OrderedArray):
    print(
        f"UnSuccessful Ordered Array Search Result:" f" {ordered_array.search(4534354)}"
    )


@benchmark
def unsuccessful_Btree_search(b_tree: BTree):
    print(f"UnSuccessful B-Tree Search Result: {b_tree.search(4534354)}")


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


main()
