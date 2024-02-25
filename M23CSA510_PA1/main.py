import time

from hash_ds import HashTable
from inputs import (element_to_delete, element_to_insert, element_to_search,
                    input_array)
from RBT import RedBlackTree

hash_vs_rbt_creation_time = {}
hash_vs_rbt_insertion_time = {}
hash_vs_rbt_search_time = {}
hash_vs_rbt_deletion_time = {}


def benchmark(func):
    def wrapper(*args, **kwargs):
        fn_name = func.__name__
        # print(f"Benchmarking loops in {fn_name}")

        # Start time
        start_time = time.time()

        # Call the function
        result = func(*args, **kwargs)

        # End time
        end_time = time.time()

        elapsed_time = end_time - start_time

        if "create" in fn_name and "hash" in fn_name:
            hash_vs_rbt_creation_time["hash"] = elapsed_time
        elif "insert" in fn_name and "hash" in fn_name:
            hash_vs_rbt_insertion_time["hash"] = elapsed_time
        elif "search" in fn_name and "hash" in fn_name:
            hash_vs_rbt_search_time["hash"] = elapsed_time
        elif "delete" in fn_name and "hash" in fn_name:
            hash_vs_rbt_deletion_time["hash"] = elapsed_time
        elif "create" in fn_name and "rbt" in fn_name:
            hash_vs_rbt_creation_time["rbt"] = elapsed_time
        elif "insert" in fn_name and "rbt" in fn_name:
            hash_vs_rbt_insertion_time["rbt"] = elapsed_time
        elif "search" in fn_name and "rbt" in fn_name:
            hash_vs_rbt_search_time["rbt"] = elapsed_time
        elif "delete" in fn_name and "rbt" in fn_name:
            hash_vs_rbt_deletion_time["rbt"] = elapsed_time
        # print(f"Time taken: {elapsed_time} seconds \n\n")

        return result

    return wrapper


@benchmark
def delete_keys_from_rbt(rb_tree: RedBlackTree):
    for key in element_to_delete:
        rb_tree.delete(key)


@benchmark
def search_keys_in_rbt(rb_tree: RedBlackTree):
    for search_key in element_to_search:
        # rb_tree.search(search_key)
        (
            print(f"{search_key} --> FOUND")
            if rb_tree.search(search_key)
            else print(f"{search_key} --> NOT FOUND")
        )


@benchmark
def insert_new_keys_in_rbt(rb_tree: RedBlackTree):
    for key in element_to_insert:
        rb_tree.insert(key)


@benchmark
def create_initial_rbt(rb_tree: RedBlackTree):
    for key in input_array:
        rb_tree.insert(key)


@benchmark
def delete_keys_from_hash(hash_table: HashTable):
    for key in element_to_delete:
        hash_table.delete(key)


@benchmark
def search_keys_in_hash(hash_table: HashTable):
    for search_key in element_to_search:
        # hash_table.search(search_key)
        (
            print(f"{search_key} --> FOUND")
            if hash_table.search(search_key)
            else print(f"{search_key} --> NOT FOUND")
        )


@benchmark
def insert_new_keys_in_hash(hash_table: HashTable):
    for key in element_to_insert:
        hash_table.insert(key, f"value_{key}")


@benchmark
def create_initial_hash(hash_table: HashTable):
    for key in input_array:
        hash_table.insert(key, f"value_{key}")

    # for search_key in element_to_delete:
    #     (
    #         print(f"{search_key} --> FOUND")
    #         if rb_tree._search(search_key)
    #         else print(f"{search_key} --> NOT FOUND")
    #     )


def main():
    hash_table = HashTable(initial_size=1000, load_factor_threshold=0.7)

    # Creating the DS.
    create_initial_hash(hash_table)
    # print("COLLISION COUNT --> ",hash_table.collision_count)
    # inserting
    insert_new_keys_in_hash(hash_table)

    # searching
    search_keys_in_hash(hash_table)

    # deleting
    delete_keys_from_hash(hash_table)

    rb_tree = RedBlackTree()

    # Creating the DS.
    create_initial_rbt(rb_tree)

    # inserting
    insert_new_keys_in_rbt(rb_tree)

    # searching
    search_keys_in_rbt(rb_tree)

    # deleting
    delete_keys_from_rbt(rb_tree)


main()
print(hash_vs_rbt_creation_time)
print("Did creating a hash take less time than RBT?")
print(hash_vs_rbt_creation_time["hash"] < hash_vs_rbt_creation_time["rbt"])
print(f"By {hash_vs_rbt_creation_time["rbt"] - hash_vs_rbt_creation_time["hash"]} seconds \n")

print(hash_vs_rbt_insertion_time)
print("Did inserting into hash take less time than RBT?")
print(hash_vs_rbt_insertion_time["hash"] < hash_vs_rbt_insertion_time["rbt"])
print(f"By {hash_vs_rbt_insertion_time["rbt"] - hash_vs_rbt_insertion_time["hash"]} seconds \n")

print(hash_vs_rbt_search_time)
print("Did searching a hash take less time than RBT?")
print(hash_vs_rbt_search_time["hash"] < hash_vs_rbt_search_time["rbt"])
print(f"By {hash_vs_rbt_search_time["rbt"] - hash_vs_rbt_search_time["hash"]} seconds \n")

print(hash_vs_rbt_deletion_time)
print("Did deleting from a hash take less time than RBT?")
print(hash_vs_rbt_deletion_time["hash"] < hash_vs_rbt_deletion_time["rbt"])
print(f"By {hash_vs_rbt_deletion_time["rbt"] - hash_vs_rbt_deletion_time["hash"]} seconds \n")
