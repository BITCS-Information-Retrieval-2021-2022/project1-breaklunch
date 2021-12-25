import pymongo
import json
from tqdm import tqdm
from pymongo.errors import DuplicateKeyError


class MyMongo(object):
    MONGODB_URI = "mongodb://localhost:27017"
    MONGODB_DB = "breaklunch"

    def __init__(self):
        self.client = pymongo.MongoClient(self.MONGODB_URI)
        self.db = self.client[self.MONGODB_DB]
        self.db['total'].create_index('doi', unique=True)

    def close(self):
        self.client.close()

    def insert_one(self, item):
        try:
            self.db['total'].insert_one(item)
        except DuplicateKeyError as e:
            # just don't insert
            pass
        except Exception as e:
            print("unexpected error:", str(e))



class PaperReader(object):
    '''
    Read Json files of papers
    '''

    def __init__(self, papers, paper_path, paper_read_func):
        for p in papers:
            if p not in paper_path.keys():
                raise ValueError("exist unspecified paper path.")
            if p not in paper_read_func.keys():
                raise ValueError("exist unspecified read paper func.")
        self.papers = papers
        self.paper_path = paper_path
        self.paper_read_func = paper_read_func

    def read_paper(self, paper):
        if paper not in self.papers:
            raise ValueError("unsupported paper")
        for item in self.paper_read_func[paper](self.paper_path[paper]):
            yield item

    @staticmethod
    def paper_read_func1(paper_path):
        '''
        used for `springer_paper_2.json`
        '''
        with open(paper_path, 'r', encoding='utf-8') as f:
            while 1:
                line = f.readline()
                if not line:
                    break
                yield json.loads(line, encoding='utf-8')

    @staticmethod
    def paper_read_func2(paper_path):
        '''
        used for `acm.json`
        '''
        tmp = ''
        with open(paper_path, 'r', encoding='utf-8') as f:
            while 1:
                line = f.readline()
                if not line:
                    break
                if line.strip() == '}':
                    tmp += line
                    item = json.loads(tmp, encoding='utf-8')
                    if 'checksum' in item:
                        item.pop('checksum')
                    yield item
                    tmp = ''
                    continue
                if line.strip() == '{':
                    assert tmp == ''
                    tmp += line
                    continue
                if "ObjectId" in line:
                    continue
                else:
                    tmp += line

    @staticmethod
    def paper_read_func3(paper_path):
        '''
        used for `acm_paper.json`, `science_direct.json`, `springer_paper_0.json`, `springer_paper_1.json`
        '''
        with open(paper_path, 'r', encoding='utf-8') as f:
            item_list = json.load(f)
            for item in item_list:
                yield item



class FieldProcessor(object):
    default_fields = {
        "title": "unavailable",
        "abstract": "",
        "authors": [],
        "doi": "",
        "url": "",
        "year": "",
        "month": "",
        "type": "",
        "venue": "",
        "source": "",
        "video_url": "",
        "video_path": "",
        "thumbnail_url": "",
        "pdf_url": "",
        "pdf_path": "",
        "inCitations": "",
        "outCitations": "",
    }

    @staticmethod
    def count_exist_field(item_iter):
        print("start counting fields...")
        field_cnt = dict()
        for item in tqdm(item_iter):
            for k in item:
                if k not in field_cnt:
                    field_cnt[k] = {
                        'count': 0,
                        'type2count': dict()
                    }
                field_cnt[k]['count'] += 1
                val = item[k]
                type_ = str(type(val))
                if type_ not in field_cnt[k]['type2count']:
                    field_cnt[k]['type2count'][type_] = 0
                field_cnt[k]['type2count'][type_] += 1

        return field_cnt

    def clean_fields(self, item: dict):
        for k in self.default_fields:
            if k not in item:
                item[k] = self.default_fields[k]
            if item[k] is None:
                item[k] = self.default_fields[k]
        if '_id' in item:
            item.pop('_id')
        if isinstance(item['month'], int):
            item['month'] = str(item['month'])
        if len(item['month']) == 1:
            item['month'] = '0'+item['month']
        if isinstance(item['year'], int):
            item['year'] = str(item['year'])
        if isinstance(item['inCitations'], int):
            item['inCitations'] = str(item['inCitations'])
        if isinstance(item['outCitations'], int):
            item['outCitations'] = str(item['outCitations'])

        return item
