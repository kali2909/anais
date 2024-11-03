from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

class AdminPanelTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = False  # Executar en mode amb finestra visible
        cls.selenium = WebDriver(service=Service(), options=options)
        cls.selenium.implicitly_wait(10)

        # Creació d'un superusuari per al test
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_create_questions_and_choices(self):
        # Login to admin panel
        self.selenium.get(f'{self.live_server_url}/admin/')
        self.selenium.find_element(By.NAME, "username").send_keys("isard")
        self.selenium.find_element(By.NAME, "password").send_keys("pirineus")
        self.selenium.find_element(By.XPATH, "//input[@type='submit']").click()

        # Assertions to verify login was successful
        assert "Site administration" in self.selenium.page_source

        # Creació de 2 Questions
        for i in range(1, 3):  # Crea 2 Questions
            self.selenium.find_element(By.LINK_TEXT, "Questions").click()
            self.selenium.find_element(By.LINK_TEXT, "Add question").click()
            self.selenium.find_element(By.NAME, "question_text").send_keys(f"Pregunta {i}")
            self.selenium.find_element(By.XPATH, "//input[@type='submit']").click()

            # Creació de 2 Choices per a cada Question
            for j in range(1, 3):  # Crea 2 Choices per cada Question
                # Esperem que el formulari de Choices estigui visible
                time.sleep(1)  # Potser necessites ajustar el temps d'espera
                self.selenium.find_element(By.LINK_TEXT, "Add choice").click()
                self.selenium.find_element(By.NAME, "choice_text").send_keys(f"Opció {j} per Pregunta {i}")
                self.selenium.find_element(By.XPATH, "//input[@type='submit']").click()

        # Comprovem que les 4 Choices s'han creat
        self.selenium.find_element(By.LINK_TEXT, "Choices").click()
        for j in range(1, 5):  # Comprovem que les 4 Choices existeixen
            try:
                self.selenium.find_element(By.XPATH, f"//td[contains(text(), 'Opció {j}')]")
            except NoSuchElementException:
                assert False, f"L'element 'Opció {j}' no existeix."

        # Si arribes aquí, significa que les 4 Choices existeixen
        assert True

