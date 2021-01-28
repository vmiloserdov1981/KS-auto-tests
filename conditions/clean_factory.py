from abc import ABC, abstractmethod
from api.api_models import ApiModels


class Creator(ABC):
    def __init__(self, driver, uuid, delete_anyway=False):
        self.driver = driver
        self.uuid = uuid
        self.delete_anyway = delete_anyway

    @abstractmethod
    def factory_method(self):
        pass


class DatasetCreator(Creator):
    def factory_method(self):
        return DatasetProduct(self.driver, self.uuid, self.delete_anyway)


class Product(ABC):
    """
    Интерфейс Продукта объявляет операции, которые должны выполнять все
    конкретные продукты.
    """

    def __init__(self, driver, uuid, delete_anyway):
        self.driver = driver
        self.uuid = uuid
        self.delete_anyway = delete_anyway

    @abstractmethod
    def delete_entity(self):
        pass


class DatasetProduct(Product):
    def delete_entity(self):
        api = ApiModels(None, None, self.driver.project_uuid, token=self.driver.token)
        api.delete_dataset(self.uuid)


def delete(creator: Creator):
    entity = creator.factory_method()
    if entity.delete_anyway:
        entity.delete_entity()
    else:
        if not entity.driver.is_test_failed:
            entity.delete_entity()
