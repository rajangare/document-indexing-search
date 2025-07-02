

class DocumentSearchService:

    def __init__(self, elasticsearch):
        self.elasticsearch = elasticsearch

    # Search for documents in the document store based on a semantic query.
    def search_semantic(self, query, limit=10):
        """
        Search for documents in the document store based on a query.

        :param query: The search query string.
        :param limit: The maximum number of documents to return.
        :return: A list of documents matching the query.
        """
        search_query = {
            "query": {
                "match": {
                    "content": {
                        "query": query,
                        "fuzziness": "AUTO"
                    }
                }
            },
            "size": limit
        }
        results = self.elasticsearch.search(index="documents", body=search_query)

        return results