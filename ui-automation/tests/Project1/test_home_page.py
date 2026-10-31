import pytest
import allure

from playwright.sync_api import Page, expect


BASE_URL = "https://www.saucedemo.com/"
INVENTORY_URL = "https://www.saucedemo.com/inventory.html"

@allure.feature("Login Functionality")

class TestLogin:

    @allure.title("User login validation")
    @allure.description("Verify that user can log in.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login1(self, page: Page):
        page.goto(BASE_URL)
        page.get_by_role("textbox", name="Username").fill("standard_user")
        page.get_by_placeholder("Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()
        expect(page).to_have_url(INVENTORY_URL)


    @allure.title("Successful login with problem_user")
    @allure.description("Verify that problem_user can log in.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login2(self, page: Page):
        page.goto(BASE_URL)

        page.get_by_role("textbox", name="Username").fill("problem_user")
        page.get_by_placeholder("Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()

        expect(page).to_have_url(INVENTORY_URL)

    @allure.title("Locked out user login validation")
    @allure.description("Verify that locked_out_user cannot log in.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login3(self, page: Page):
        page.goto(BASE_URL)

        page.get_by_role("textbox", name="Username").fill("locked_out_user")
        page.get_by_placeholder("Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()

        expect(page).to_have_url(BASE_URL)
        expect(page.locator('[data-test="error"]')).to_be_visible()

    @allure.title("Performance glitch user login")
    @allure.description("Verify that performance_glitch_user can log in.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login4(self, page: Page):
        page.goto(BASE_URL)

        page.get_by_role("textbox", name="Username").fill("performance_glitch_user")
        page.get_by_placeholder("Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()

        expect(page).to_have_url(INVENTORY_URL)

    @allure.title("Error user login validation")
    @allure.description("Verify error_user login behavior.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login5(self, page: Page):
        page.goto(BASE_URL)

        page.get_by_role("textbox", name="Username").fill("error_user")
        page.get_by_placeholder("Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()

        expect(page).to_have_url(INVENTORY_URL)

    @allure.title("Visual user login validation")
    @allure.description("Verify visual_user can log in.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login6(self, page: Page):
        page.goto(BASE_URL)

        page.get_by_role("textbox", name="Username").fill("visual_user")
        page.get_by_placeholder("Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()

        expect(page).to_have_url(INVENTORY_URL)
