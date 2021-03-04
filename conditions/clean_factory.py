from abc import ABC, abstractmethod
from api.api_models import ApiModels
from api.api_classes import ApiClasses


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


class ClassNodeCreator(Creator):
    def factory_method(self):
        return ClassNode(self.driver, self.uuid, self.delete_anyway)


class ModelNodeCreator(Creator):
    def factory_method(self):
        return ModelNode(self.driver, self.uuid, self.delete_anyway)


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


class ModelNode(Product):
    def delete_entity(self):
        api = ApiModels(None, None, self.driver.project_uuid, token=self.driver.token)
        api.delete_model_node(self.uuid)


class ClassNode(Product):
    def delete_entity(self):
        api = ApiClasses(None, None, self.driver.project_uuid, token=self.driver.token)
        api.delete_class_node(self.uuid)


def delete(creator: Creator):
    entity = creator.factory_method()
    if entity.delete_anyway:
        try:
            entity.delete_entity()
        except AssertionError:
            pass
    else:
        if not entity.driver.is_test_failed:
            try:
                entity.delete_entity()
            except AssertionError:
                pass
