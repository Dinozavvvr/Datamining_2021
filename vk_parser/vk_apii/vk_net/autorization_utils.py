# Created by dinar at 01.03.2021
from urllib.request import urlopen
from vk_api.vk_api import VkApi
import json


class AuthorizationHelper:
    VERSION = 5.59

    @staticmethod
    def get_api_by_secret(client_id, client_secret, timeout):
        token = AuthorizationHelper.get_token(client_id, client_secret, timeout)
        return VkApi(token=token).get_api()

    @staticmethod
    def get_api(client_id, scope, timeout, version=VERSION):
        token = AuthorizationHelper.get_token(client_id, timeout, version, scope)
        return VkApi(token=token).get_api()

    @staticmethod
    def get_token_by_secret(client_id, client_secret, timeout=5000, version=VERSION):
        url_request = "https://oauth.vk.com/access_token?client_id={client_id}&client_secret={client_secret}&v=" \
                      "{version}&grant_type=client_credentials".format(client_id=client_id,
                                                                       version=version,

                                                                       client_secret=client_secret)
        response = urlopen(url=url_request, timeout=timeout).read().decode("utf-8")
        return json.loads(response)['access_token']

    @staticmethod
    def get_token(client_id, timeout=5000, version=VERSION, scope=None):
        url_request = "https://oauth.vk.com/authorize?client_id={client_id}" \
                      "&display=page&redirect_uri=https://oauth.vk.com/blank.com&scope={scope}" \
                      "&response_type=token&v={version}".format(client_id=client_id, scope=scope, version=version)
        response = urlopen(url=url_request, timeout=timeout) \
            .add_header('User-agent',
                        'Mozilla/5.0 (Windows NT 6.1; rv:52.0) '
                        'Gecko/20100101 Firefox/52.0') \
            .read().decode("utf-8")
        return json.loads(response)['access_token']
