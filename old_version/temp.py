import xmltodict
import gzip
import io
def handle(path,item):
    if 'author' in item:
        for a in item['author']:
            if 'Angela Dai' in a:
                print(item)
                for a2 in item['author']:
                    print(a2)
        #print(item['author'])
    return True
#xmltodict.parse(io.TextIOWrapper(gzip.GzipFile('./dblp-2019-01-01.xml.gz'),encoding='unicode_internal',errors='strict'),item_depth=2 ,item_callback=handle)
xmltodict.parse(gzip.open('./dblp-2019-01-01.xml.gz','rt'),item_depth=2, item_callback=handle,disable_entities=False)
