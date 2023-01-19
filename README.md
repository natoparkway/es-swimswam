# es-swimswam
Learning Elastic Search by reading the SwimSwam RSS feed.


### GENERAL LEARNING
1. Elastic Search doesn't like text aggregation

### DEV OPS
```
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```


#### Elastic Search
https://www.elastic.co/downloads/elasticsearch
```
./elasticsearch-8.6.0/bin/elasticsearch
```

*INSERT A SINGLE DOC*
```
curl -X PUT "localhost:9200/swimswam/_doc/user-text" -H 'Content-Type: application/json' -d'
{
    "first_name" : "John",
    "last_name" :  "Smith",
    "age" :        25,
    "about" :      "I love to go rock climbing",
    "interests": [ "sports", "music" ]
}
'
```

*EXAMINE SCHEMA*
`curl -XGET 'http://localhost:9200/swimswam_articles/_mapping' | python -m json.tool`


curl -X GET "localhost:9200/swimswam_articles/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "index": "swimswam_articles",
  "aggs": {
    "genres": {
      "terms": { "field": "genre" }
    }
  }
}
'
