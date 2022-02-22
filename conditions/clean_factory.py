from abc import ABC, abstractmethod
from api.api_models import ApiModels
from api.api_classes import ApiClasses
from api.api_bpms import ApiBpms
import allure


class Creator(ABC):
    def __init__(self, driver, uuid, delete_anyway=False, force=None, entity_uuid=None):
        self.driver = driver
        self.uuid = uuid
        self.delete_anyway = delete_anyway
        self.force = force
        self.entity_uuid = entity_uuid

    @abstractmethod
    def factory_method(self):
        pass


class DatasetCreator(Creator):
    def factory_method(self):
        return DatasetEntity(self.driver, self.uuid, self.delete_anyway)


class ClassNodeCreator(Creator):
    def factory_method(self):
        return ClassNode(self.driver, self.uuid, self.delete_anyway, force=self.force)


class ModelNodeCreator(Creator):
    def factory_method(self):
        return ModelNode(self.driver, self.uuid, self.delete_anyway)


class BpmsNodeCreator(Creator):
    def factory_method(self):
        return BpmsNode(self.driver, self.uuid, self.delete_anyway, force=self.force, entity_uuid=self.entity_uuid)


class FormulaEntityCreator(Creator):
    def factory_method(self):
        return FormulaEntity(self.driver, self.uuid, self.delete_anyway)


class Product(ABC):

    def __init__(self, driver, uuid, delete_anyway, force=None, entity_uuid=None):
        self.driver = driver
        self.uuid = uuid
        self.delete_anyway = delete_anyway
        self.force = force
        self.entity_uuid = entity_uuid

    @abstractmethod
    def delete_entity(self):
        pass


class DatasetEntity(Product):
    def delete_entity(self):
        with allure.step(f'Удалить набор данных'):
            api = ApiModels(None, None, self.driver.project_uuid, token=self.driver.token)
            api.delete_dataset(self.uuid)


class FormulaEntity(Product):
    def delete_entity(self):
        with allure.step(f'Удалить формулу'):
            api = ApiClasses(None, None, self.driver.project_uuid, token=self.driver.token)
            api.delete_formula(self.uuid)


class ModelNode(Product):
    def delete_entity(self):
        with allure.step(f'Удалить модель'):
            api = ApiModels(None, None, self.driver.project_uuid, token=self.driver.token)
            api.delete_model_node(self.uuid)


class BpmsNode(Product):
    def delete_entity(self):
        with allure.step(f'Удалить bpms'):
            api = ApiBpms(None, None, self.driver.project_uuid, token=self.driver.token)
            api.delete_bpms_node(self.uuid, self.entity_uuid, force=self.force)


class ClassNode(Product):
    def delete_entity(self):
        with allure.step(f'Удалить класс'):
            api = ApiClasses(None, None, self.driver.project_uuid, token=self.driver.token)
            api.delete_class_node(self.uuid, force=self.force)


def delete(creator: Creator):
    entity = creator.factory_method()
    if entity.delete_anyway:
        try:
            entity.delete_entity()
        except ZeroDivisionError:
            pass
    else:
        if not entity.driver.is_test_failed:
            try:
                entity.delete_entity()
            except ZeroDivisionError:
                pass
