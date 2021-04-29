# Created by dinar at 29.04.2021

import math
import random
import mmh3
from urllib import request
from bs4 import BeautifulSoup


class CountableBloomFilter:
    """
        m is count of items in input set
        probability is false positive value
    """

    def __init__(self, probability, items_count):
        # probability is false positive value
        self.probability = probability
        # m is count of items in input set
        self.m = items_count
        # length of our countable bloom filter
        self.length = self.get_cbf_length()
        # k is amount of hash functions
        self.k = self.get_amount_of_hash_functions()
        # initialize a cbf array
        self.cbf_array = self.initialize_cbf_array()

    def get_cbf_length(self) -> int:
        # число полученное вычислением уравнения
        # используется в качестве основания для логорифма
        base = 0.62
        return math.ceil(math.log(self.probability, base) * self.m)

    def get_amount_of_hash_functions(self) -> int:
        return math.ceil((self.length / self.m) * math.log(2))

    def add_item(self, value):
        for i in range(self.k):
            hash_value = mmh3.hash128(value, i) % self.length
            self.cbf_array[hash_value] += 1

    def item_is_present(self, value) -> bool:
        for i in range(self.k):
            hash_value = mmh3.hash128(value, i, signed=False) % self.length

            if self.cbf_array[hash_value] == 0:
                return False
        return True

    def initialize_cbf_array(self) -> list:
        return [0 for i in range(self.length)]


def get_dataset() -> list:
    document = request.urlopen("https://military.wikireading.ru/28209", timeout=10000)

    soup = BeautifulSoup(document, 'html.parser')
    tags = soup.find_all('p')

    res = []
    for p in tags:
        res.extend(p.getText().split(' '))
    return list(filter(lambda w: w != '', res))


def start():
    probability = 0.0001
    dataset = get_dataset()
    countable_bloom_filter = CountableBloomFilter(probability, len(dataset))

    print('filter size: {}'.format(countable_bloom_filter.length))
    print('amount of hash functions: {}\n'.format(countable_bloom_filter.k))

    for item in dataset:
        countable_bloom_filter.add_item(item)

    for i in range(10):
        word = dataset[random.randint(0, len(dataset))]
        print('checking a word "{}" returned "{}"'
              .format(word, countable_bloom_filter.item_is_present(word)))


if __name__ == '__main__':
    start()
