from collections import namedtuple
class Serialization:
    def __init__(self, query_result, item_name, item_colmns):
        self.query_result=query_result
        self.item_name=item_name
        self.item_colmns=item_colmns
        print("this is serialization test: ", self.__serialization_to_json(self.query_result, self.item_name, self.item_colmns))
    
    # serilzed the item in form of dict {"item_title": title, etc...}
    def __serialization_to_json(self, query_result, item_name: str, item_columns: list[str]):
        tupled_data = namedtuple(item_name, item_columns) # Item(*"Item Data")
        items = [tupled_data(*row) for row in query_result] #query array will be tupled
        items_list = [product._asdict() for product in items] #dict of the tupled data
        return items_list
    
    # get serialzed data
    def get_data(self):
        data = self.__serialization_to_json(self.query_result, self.item_name, self.item_colmns)
        return data