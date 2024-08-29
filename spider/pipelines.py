# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from spider.items import DoubanItem


class DoubanPipeline:
    def process_item(self, item, spider):
        if not isinstance(item, DoubanItem):
            return item
        data_json = json.dumps(dict(item), ensure_ascii=False)
        print(data_json)
        return data_json
