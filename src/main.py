import elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A, Q
import feedparser
import json
import random
import ssl  # https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed

def print_hits(es_result):
    for elem in es_result:
        print(elem)

def parse_schema(elem):
    schema = {}
    if isinstance(elem, dict):
        for k, v in elem.items():
            schema[k] = parse_schema(v)
    elif isinstance(elem, list):
        if elem:
            return [parse_schema(elem[0])]
        else:
            return []
    else:
        return type(elem).__name__

    return schema



def pretty_print(elem):
    print(json.dumps(elem, indent=4))

def load_rss_feed(url):
    # https://github.com/kurtmckee/feedparser/issues/84
    original_ss_https_context = ssl._create_default_https_context
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        parse = feedparser.parse(url)
    finally:
        ssl._create_default_https_context = original_ss_https_context
    

    feed_entries = parse.entries
    return feed_entries

def bulk_insert(es, index, data):
    actions = [{**{
        "_index": index,
    }, **doc} for doc in data]
    bulk(es, actions)


def main():
    ARTICLE_INDEX = 'swimswam_articles'

    es = Elasticsearch()
    s = Search(using=es)

    try:
        es.indices.delete(index=ARTICLE_INDEX)
    except elasticsearch.exceptions.NotFoundError as e:
        print(f'Index {ARTICLE_INDEX} could not be deleted')


    data = load_rss_feed('https://swimswam.com/feed/')
    bulk_insert(es, ARTICLE_INDEX, data)
    es.indices.refresh(index=ARTICLE_INDEX)

    # query = s.index(ARTICLE_INDEX).query()
    # query.aggs.bucket('author_counts', A('terms', field='title'))
    # response = query.execute()

    # Find all articles where Caeleb Dressel or College is tagged
    responses = (
        s.index(ARTICLE_INDEX)
        .query("match", **{"content.value": "swim"})
    ).execute()
    for response in responses:
        print(response)

    # print(response)



if __name__ == '__main__':
    main()