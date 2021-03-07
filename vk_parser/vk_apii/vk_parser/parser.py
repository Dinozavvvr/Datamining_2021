from operator import concat


class VkParser:
    def __init__(self, api=None, user_id=None):
        self.api = api
        self.user_id = user_id

    def set_api(self, api):
        self.api = api

    def get_posts_by_id(self, owner_id=None, count=100, offset=0):

        """ how many post will be returned - count
        owner_id - id from group or user
        offset - how many posts will skipped
        offset_100 - var for getting posts if count more then 100
        because api.get.wall() can return max 100 items
        result_list = list with result items
        """

        result_list = []
        get_posts = self.api.wall.get
        offset_100 = offset

        if owner_id is None and self.user_id is not None:
            owner_id = self.user_id

        # formatting for wall.get(). owner_id must starts with '-'
        owner_id = concat('-', str(owner_id))

        while count - 100 > 0:
            result_list.extend(get_posts(owner_id=owner_id, count=100, offset=offset_100)
                               .get("items"))
            count -= 100
            offset_100 += 100

        result_list.extend(get_posts(owner_id=owner_id, count=count, offset=offset_100)
                           .get("items"))

        return result_list
