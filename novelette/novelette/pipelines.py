# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
class NovelettePipeline:
    def __init__(self):
        self.f = open(r'.\novels\穿成人鱼后我又穿了回来.txt', 'w+', encoding='utf-8')
        self.data = {}
        pass

    def process_item(self, item, spider):
        self.data[item['chapter_id']] = ''
        self.data[item['chapter_id']] += f"第{item['chapter_id'] + 1}章 {item['title']}"
        self.data[item['chapter_id']] += '\n'
        self.data[item['chapter_id']] += item['text']
        self.data[item['chapter_id']] += '\n\n'
        return item

    def close_spider(self, spider):
        for i in range(len(self.data.keys())):
            self.f.write(self.data[i])
        self.f.close()
        pass
