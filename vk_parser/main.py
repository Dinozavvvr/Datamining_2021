# -*- coding: utf-8 -*-
import vk_api
import xlsxwriter
import configparser

from vk_apii.vk_analyzer.analyzer_utils import *
from vk_apii.vk_parser import *
from vk_parser.db.db_utils import PostgreSql


def write_dict_to_xlsx_file(dictionary: dict):
    workbook = xlsxwriter.Workbook('WordsRating.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0
    for item in dictionary:
        worksheet.write(row, col, item)
        worksheet.write(row, col + 1, dictionary[item])
        row += 1

    workbook.close()


def print_dict(dictionary: dict):
    for k, v in dictionary.items():
        try:
            print("{key:_<50}{value:_>5}".format(key=str(k).strip(), value=v))
        except UnicodeError:
            pass


def start():
    config = configparser.ConfigParser()
    config.read('configuration.ini')

    vk_api_config = config['VK_API']

    vk_parser = VkParser(vk_api.VkApi(token=str(vk_api_config['TOKEN'])).get_api())
    posts = vk_parser.get_posts_by_id(owner_id=vk_api_config['ITIS_ID'], count=int(vk_api_config['COUNT']),
                                      offset=int(vk_api_config['OFFSET']))

    common_text = ''
    for post in posts:
        common_text += post.get("text")

    uniq_dict = TextAnalyzerUtil \
        .get_unique_words_from_posts_as_dict(common_text,
                                             clean_text=True,
                                             language=["english", "russian"],
                                             stemming=False,
                                             lemmatization=True)

    uniq_dict = {k: v for k, v in sorted(uniq_dict.items(),
                                         key=lambda item: item[1],
                                         reverse=True)}

    db_config = config['DB']

    db = PostgreSql(db_name=db_config['DB_NAME'], user=db_config['DB_USER'],
                    password=db_config['DB_PASSWORD'], host=db_config['DB_HOST'],
                    schema_name=db_config['DB_SCHEME'])

    # saving into db
    for (key, value) in uniq_dict.items():
        db.save(table_name='count_of_word',
                return_id=True,
                generated_columns=['id'],
                word=key, count=value)

    # print_dict(uniq_dict)
    # write_dict_to_xlsx_file(uniq_dict)


if __name__ == '__main__':
    start()
    print('end')
