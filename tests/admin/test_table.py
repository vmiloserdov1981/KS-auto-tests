import allure
import pytest
import users
from pages.main.projects_po import ProjectsPage
from pages.login_po import LoginPage
from pages.components.modals import ChangePasswordModal
import time
from selenium import webdriver

@allure.feature('Таблицы')
@allure.story('Логин/Логаут')
@allure.title('Отработка входящих событий и подмена сущности для таблиц')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_create_new_project(driver, parameters):
    #данные
    projects_page = ProjectsPage(driver)
    Project_name = "AUTOTEST BASIC"
    Class_name = "Данные спортсмена"
    Index1 = "Страна"
    Index2 = "Вес"
    Index3 = "Оценка"
    Table_name1 = "Сводная по команде 1"
    Table_name2 = "Сводная по команде 2"

    with allure.step('Перейти на вкладку "Проекты"'):
        projects_page.click_to_page_project()

    with allure.step('Зайти в подготовленный проект AUTOTEST BASIC'):
        projects_page.search_test_project(Project_name)

#    with allure.step('Создание класса и показателей'):
#        projects_page.create_class_and_metrics(Class_name, Index1, Index2, Index3)

    with allure.step('Создание таблицы 1 и таблицы 2'):
        projects_page.create_first_table()

    with allure.step('Конструируем таблицу 1'):
        projects_page.made_first_table()

    with allure.step('Конструируем таблицу 2'):
        projects_page.made_two_table()