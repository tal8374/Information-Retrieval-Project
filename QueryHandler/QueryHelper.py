class QueryHelper(object):

    @staticmethod
    def cosine_similarity(idf, tf, size, query_weight, total_weight):
        return (idf * (tf / size)) / (query_weight * total_weight)
