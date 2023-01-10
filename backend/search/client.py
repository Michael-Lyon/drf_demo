from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client


def get_index(index_name='cfe_Product'):
    client = get_client()
    index = client.init_index('cfe_Product')
    return index



def perform_search(query, **kwargs):
    index = get_index()
    tags = ""
    params = {}
    if "tags" in kwargs:
        tags = kwargs.pop("tags") or []
        if len(tags) != 0:
            params["tagFilters"] = tags
    
    # Futher filter the queryset by any given kwargs that we might have
    index_filters = [f"{k}:{v}" for k,v in kwargs.items() if v]
    if len(index_filters) != 0:
        params['facetFilters'] = index_filters
    results = index.search(query, params)
    return results


