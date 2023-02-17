import allure
import pytest
import users
from pages.main.projects_po import ProjectsPage
from pages.login_po import LoginPage
from pages.components.modals import ChangePasswordModal
import time
from selenium import webdriver

'''

@allure.feature('Таблицы')
@allure.story('Логин/Логаут')
@allure.title('Отработка входящих событий и подмена сущности для таблиц')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_incoming_events_and_entity_substitution_for_tables(driver, parameters):
    #данные
    projects_page = ProjectsPage(driver)
    Project_name = "AUTOTEST BASIC"
    Class_name = "Данные спортсмена"
    Index1 = "Страна"
    Index2 = "Вес"
    Index3 = "Оценка"
    Table_name1 = "Сводная по команде 1"
    Table_name2 = "Сводная по команде 2"
    Interface_name = "Передача по событию"
    Model_name = 'Команды'
    Event_tag = '1таблица'
    Button_name = 'Передать сущность'
    Entity_name = 'Сводная по команде 2'

    with allure.step('Перейти на вкладку "Проекты"'):
        projects_page.click_to_page_project()

    with allure.step('Зайти в подготовленный проект AUTOTEST BASIC'):
        projects_page.search_test_project(Project_name)

#    with allure.step('Создание класса и показателей'):
#        projects_page.create_class_and_metrics(Class_name, Index1, Index2, Index3)

#    with allure.step('Создание таблицы 1 и таблицы 2'):
#        projects_page.create_first_table()

#    with allure.step('Конструируем таблицу 1'):
#        projects_page.made_first_table()

#    with allure.step('Конструируем таблицу 2'):
#        projects_page.made_two_table()

    with allure.step('Создание интерфейса'):
        projects_page.create_interface(Interface_name)

    with allure.step('Создание связанной сущности - таблица'):
        projects_page.create_related_entity_table(Model_name, Table_name1)

    with allure.step('Настройка собитий для таблицы'):
        projects_page.set_events_for_table(Event_tag)

    with allure.step('Создание связанной сущности - кнопка'):
        projects_page.create_related_entity_button(Button_name, Entity_name)

    with allure.step('Настройка собитий для кнопки'):
        projects_page.set_events_for_button(Event_tag)
'''

@allure.feature('Интерфейсы')
@allure.story('Логин/Логаут')
@allure.title('Добавление, настройка и удаление ячеек')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_add_edit_and_delete_cells(driver, parameters):
    #данные
    projects_page = ProjectsPage(driver)
    Project_name = "AUTOTEST BASIC"
    Interface_name = "Ячейки"


    with allure.step('Перейти на вкладку "Проекты"'):
        projects_page.click_to_page_project()

    with allure.step('Зайти в подготовленный проект AUTOTEST BASIC'):
        projects_page.search_test_project(Project_name)

    with allure.step('Создание интерфейса с двумя ячейками'):
        projects_page.create_interface(Interface_name)