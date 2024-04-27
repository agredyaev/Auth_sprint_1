from elasticsearch import Elasticsearch

elastic_client = Elasticsearch(hosts=["http://localhost:9200"])


def test_match_all():
    search_query = {"query": {"match_all": {}}}
    response = elastic_client.search(index="movies", body=search_query)
    assert "hits" in response
    assert "total" in response["hits"]
    assert response["hits"]["total"]["value"] == 999


def test_search_na():
    search_query = {"query": {"query_string": {"query": "N//A"}}}
    response = elastic_client.search(index="movies", body=search_query)
    assert "hits" in response
    assert "total" in response["hits"]
    assert response["hits"]["total"]["value"] == 7


def test_search_specific_value_for_id():
    search_query = {
        "query": {
            "multi_match": {
                "query": "camp",
                "fuzziness": "auto",
                "fields": [
                    "actors_names",
                    "writers_names",
                    "title",
                    "description",
                    "genres",
                ],
            }
        }
    }
    response = elastic_client.search(index="movies", body=search_query)
    assert "hits" in response
    assert "total" in response["hits"]
    assert response["hits"]["total"]["value"] == 24
    assert response["hits"]["hits"][0]["_id"] == "6764dd98-6546-4ccf-95c5-74a63e980768"


def test_search_by_actor_name():
    search_query = {
        "query": {
            "nested": {
                "path": "actors",
                "query": {"bool": {"must": [{"match": {"actors.name": "Greg Camp"}}]}},
            }
        }
    }
    response = elastic_client.search(index="movies", body=search_query)
    assert "hits" in response
    assert "total" in response["hits"]
    assert response["hits"]["total"]["value"] == 6


def test_search_by_writer():
    search_query = {
        "query": {"term": {"id": {"value": "24eafcd7-1018-4951-9e17-583e2554ef0a"}}}
    }
    response = elastic_client.search(index="movies", body=search_query)
    assert "hits" in response
    assert "total" in response["hits"]
    assert response["hits"]["total"]["value"] == 1
    assert response["hits"]["hits"][0]["_source"]["writers_names"] == [
        "Craig Hutchinson"
    ]


def test_no_director_for_specific_movie():
    search_query = {
        "query": {"term": {"id": {"value": "479f20b0-58d1-4f16-8944-9b82f5b1f22a"}}}
    }

    response = elastic_client.search(index="movies", body=search_query)
    assert "hits" in response
    assert "total" in response["hits"]
    assert response["hits"]["total"]["value"] == 1
    assert len(response["hits"]["hits"][0]["_source"]["directors_names"]) == 0


def test_unique_genres():
    search_query = {
        "size": 0,
        "aggs": {"uniq_genres": {"terms": {"field": "genres", "size": 100}}},
    }

    response = elastic_client.search(index="movies", body=search_query)
    assert "aggregations" in response
    assert "uniq_genres" in response["aggregations"]
    assert len(response["aggregations"]["uniq_genres"]["buckets"]) == 26
