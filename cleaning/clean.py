from cleaning.utils import MyMongo, PaperReader, FieldProcessor
from tqdm import tqdm


def main():
    papers = ['acm', 'acm_paper', 'science_direct', 'springer_paper_0', 'springer_paper_1', 'springer_paper_2']
    paper_path = {key: "cleaning/data/" + key + ".json" for key in papers}
    paper_read_func = {
        'acm': PaperReader.paper_read_func2,
        'acm_paper': PaperReader.paper_read_func3,
        'science_direct': PaperReader.paper_read_func3,
        'springer_paper_0': PaperReader.paper_read_func3,
        'springer_paper_1': PaperReader.paper_read_func3,
        'springer_paper_2': PaperReader.paper_read_func1,
    }
    reader = PaperReader(papers=papers, paper_path=paper_path, paper_read_func=paper_read_func)
    fieldp = FieldProcessor()
    mongo = MyMongo()

    for p in papers:
        paper_iter = reader.read_paper(p)
        for item in tqdm(paper_iter):
            if 'thumbnail_path' in item:
                item['thumbnail_url'] = item['thumbnail_path']
                item.pop('thumbnail_path')
            item = fieldp.clean_fields(item)
            mongo.insert_one(item)


if __name__ == '__main__':
    main()
