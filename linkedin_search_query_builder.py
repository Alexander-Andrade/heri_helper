class LinkedinSearchQueryBuilder:
    def __init__(self, query_param):
        self.query_param = query_param

    def build(self):
        return f"site:linkedin.com/in/ AND {self.query_param}"
