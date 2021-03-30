# Created by dinar at 24.03.2021

# parsers
import configparser
# system
import time
from math import ceil
# multiprocessing
from multiprocessing import Pool

from more_itertools import grouper
# database
from psycopg2 import connect

# my files
from html_parser import PageParser

c = configparser.ConfigParser()
c.read('configuration.ini')


def get_connection():
    global c
    db = c['DB']
    return connect(dbname=db['NAME'],
                   user=db['USER'],
                   password=db['PASSWORD'],
                   host=db['HOST'],
                   port=int(db['PORT']))


def search_in_new_thread(ids, is_last):
    conn = get_connection()
    for id in ids:
        if id is None:
            conn.close()
            return
        id = int(id)
        with conn.cursor() as cursor:
            cursor.execute(f'select link from link where id = {id}')
            link = cursor.fetchone()[0]
            try:
                page_parser = PageParser(link)
                child_links = page_parser.get_all_href(delete_anchor=True,
                                                       add_domain=True,
                                                       remove_files=True)
                for lin in child_links:
                    lin = lin.replace("'", "\\'")
                    cursor.execute(f"select id from link where link = '{lin}'")
                    return_item = cursor.fetchone()
                    if return_item is None:
                        if is_last:
                            continue
                        try:
                            sql = f"insert into link(link) values ('{lin}') returning id"
                            cursor.execute(sql)
                            return_id = cursor.fetchone()[0]
                            conn.commit()
                        except Exception:
                            pass
                    else:
                        return_id = return_item[0]

                    # if you want to create an non repeatable pairs between two pages use it:
                    # cursor.execute(f"select * from relation where from_id={id} and to_id={return_id}")
                    # return_item = cursor.fetchone()
                    # if return_item is None:
                    # if return_id != id:
                    cursor.execute(f"insert into relation(from_id, to_id) values ({id}, {return_id})")
                    conn.commit()

            except Exception as e:
                print(e)
                continue
            finally:
                cursor.close()
    conn.close()


def search_and_fill(nesting: int,
                    pool_size: int,
                    key):
    conn = get_connection()

    last_iteration_id = 1

    while nesting > 0:
        print('nesting: ' + str(nesting))
        thread_pool = Pool(pool_size)

        with conn.cursor() as cursor:
            cursor.execute('select id from link order by id desc limit 1')
            temp_id = cursor.fetchone()[0]
            links = list(range(last_iteration_id, temp_id + 1))
            last_iteration_id = temp_id
            cursor.close()

        count_of_links = len(links)
        is_last = True if nesting == key else False
        if pool_size < count_of_links:
            [thread_pool.apply_async(search_in_new_thread, (group, is_last)) for group in
             grouper(ceil(count_of_links / pool_size), links)]
        else:
            [thread_pool.apply_async(func=search_in_new_thread, args=([link], is_last)) for link in links]
        thread_pool.close()
        thread_pool.join()
        nesting -= 1
    conn.close()


def refresh_tables():
    global c
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute('drop table if exists relation')
        conn.commit()
        cursor.execute('drop table if exists page_rank')
        conn.commit()
        cursor.execute('drop table if exists link')
        conn.commit()
        cursor.execute('create table link('
                       'id bigserial primary key,'
                       'link varchar not null unique)')
        conn.commit()
        cursor.execute('create table page_rank('
                       'link_id bigint,'
                       'page_rank numeric(10, 8),'
                       'foreign key (link_id) references link(id))')
        cursor.execute('create table relation('
                       'from_id bigint,to_id bigint,'
                       'foreign key (from_id) references link (id),'
                       'foreign key (to_id) references link (id))')
        conn.commit()
        cursor.execute(f"insert into link(link)"
                       f"values ('{c['HTML']['URL']}')")
        conn.commit()
        cursor.close()
    conn.close()


def create_graph():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select max(id) from link')
    length = cursor.fetchone()[0]

    g = [[0] * length for i in range(length)]

    for i in range(length):
        id = i + 1
        cursor.execute(f'select to_id from relation where from_id = {id}')
        res = cursor.fetchall()
        links = len(res)
        children = dict(map(lambda l: (l[0], list.count(res, l)), res))

        for (key, value) in children.items():
            g[key - 1][i] = int(value) / links
    cursor.close()
    conn.close()
    return g


def initialize_vector(len):
    v = [0] * len
    for i in range(len):
        v[i] = 1 / len
    return v


def initialize_vector_e(len, d_factor):
    e = [0] * len
    for i in range(len):
        e[i] = (1 - d_factor) / len
    return e


def get_page_rank_matrix(g, d_factor, iterations):
    v = initialize_vector(len(g))
    e = initialize_vector_e(len(g), d_factor)

    for i in range(iterations):
        v = sum_vectors(multiple_matrix_on_vector(g, v, d_factor), e)
        print(v)
        print(sum(v))
    return v


def sum_vectors(v, e):
    for i in range(len(v)):
        v[i] = v[i] + e[i]
    return v


def multiple_matrix_on_vector(x, y, d_factor):
    result = [0] * len(y)

    for i in range(len(x)):
        for j in range(len(x[0])):
            result[i] += (x[i][j] * y[j])
        result[i] = result[i] * d_factor
    return result


def save_page_rank_to_db(page_rank):
    conn = get_connection()

    cursor = conn.cursor()
    id = 1
    for pr in page_rank:
        cursor.execute(f'insert into page_rank(link_id, page_rank) values ({id}, {pr})')
        id += 1
    cursor.close()
    conn.commit()
    conn.close()


def start():
    refresh_tables()
    before_execution = time.time()
    search_and_fill(
        nesting=int(c['HTML']['NESTING']),
        pool_size=12,
        key=1
    )

    g = create_graph()

    page_rank = get_page_rank_matrix(g, 0.85, 20)
    save_page_rank_to_db(page_rank)

    print(sum(page_rank))

    after_execution = time.time()
    print(str(after_execution - before_execution))


if __name__ == '__main__':
    start()
