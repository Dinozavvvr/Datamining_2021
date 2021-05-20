# Created by dinar at 19.05.2021
import random

max_items_in_bucket = 10
items = list(map(lambda item: 'item-' + str(item), range(10)))


def generate_random_dataset(count):
    global items, max_items_in_bucket
    dataset = []

    for i in range(count):
        bucket_len = random.randint(1, max_items_in_bucket)
        bucket = []
        for j in range(bucket_len):
            item = items[random.randint(0, len(items) - 1)]

            while item in bucket:
                item = items[random.randint(0, len(items) - 1)]

            bucket.append(item)
        dataset.append(bucket)
    return dataset


def find_singleton_frequent_items(dataset, mapping_table, support):
    singletons_map = {}

    for bucket in dataset:
        for item in bucket:
            singletons_map[item] = singletons_map.get(item, 0) + 1

    return {mapping_table.get(k): v for k, v in singletons_map.items() if v >= support}


def get_doubletons(dataset):
    doubletons = []
    for bucket in dataset:
        bucket_doubletons = []
        for i in range(len(bucket) - 1):
            for j in range(i + 1, len(bucket)):
                bucket_doubletons.append(sorted((bucket[i], bucket[j])))

        doubletons.extend(bucket_doubletons)
    return doubletons


def get_mapping_table(dataset):
    mapping_table = {}
    k = 0
    for bucket in dataset:
        for item in bucket:
            if mapping_table.get(item) is None:
                mapping_table[item] = k
                k += 1
    return mapping_table


def get_bit_map(hash_bucket, support):
    bit_map = []
    for hash_i in hash_bucket:
        if len(hash_i) >= support:
            bit_map.append(1)
        else:
            bit_map.append(0)
    return bit_map


def find_frequent_doubletons(dataset, support):
    # variables
    doubletons = get_doubletons(dataset)
    mapping_table = get_mapping_table(dataset)
    doubletons = list(map(lambda i: (mapping_table.get(i[0]), mapping_table.get(i[1])), doubletons))
    hash_bucket = [[] for _ in range(len(mapping_table))]
    hash_bucket_two = [[] for _ in range(len(mapping_table))]

    # pass 1
    result_set = find_singleton_frequent_items(dataset, mapping_table, support)

    # hash 1
    for (a, b) in doubletons:
        hash_of_pair = (a + b) % len(mapping_table)
        hash_bucket[hash_of_pair].append((a, b))

    bit_map_1 = get_bit_map(hash_bucket, support)

    frequent_doubletons = []
    for i in range(len(hash_bucket)):
        if bit_map_1[i] == 1:
            frequent_doubletons.extend(hash_bucket[i])

    # hash 2
    for (a, b) in frequent_doubletons:
        hash_of_pair = (a + 2 * b) % len(mapping_table)
        hash_bucket_two[hash_of_pair].append((a, b))

    bit_map_2 = get_bit_map(hash_bucket_two, support)

    frequent_doubletons_two = []
    for i in range(len(hash_bucket_two)):
        if bit_map_2[i] == 1:
            frequent_doubletons_two.extend(hash_bucket_two[i])

    for (a, b) in frequent_doubletons:
        if result_set.get(a) is not None and \
                result_set.get(b) is not None:
            if frequent_doubletons_two.count((a, b)) > 0:
                result_set[(a, b)] = result_set.get((a, b), 0) + 1

    return result_set


def start():
    support = 3
    dataset = generate_random_dataset(5)
    result_set = find_frequent_doubletons(dataset, support)

    print(f'support level = {support} \n\n')
    for item_id, count in result_set.items():
        print(f'{item_id} , count = {count}')


if __name__ == '__main__':
    start()
