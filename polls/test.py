from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from datetime import datetime


class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.headless = True  # Evitar que s'obri el navegador
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # Crear un superusuari per a les proves
        user = User.objects.create_user("isard", "isard@example.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_crear_questions_y_choices(self):
        # 1. Entrar a l'administració de Django
        self.selenium.get(f'{self.live_server_url}/admin/login/')
        self.assertEqual(self.selenium.title, "Log in | Django site admin")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("isard")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("pirineus")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")

        # 2. Crear la primera pregunta
        self.selenium.get(f'{self.live_server_url}/admin/polls/question/add/')
        question_text_input = self.selenium.find_element(By.NAME, "question_text")
        question_text_input.send_keys("Pregunta 1")
        today_date = datetime.today().strftime('%Y-%m-%d')
        pub_date_input = self.selenium.find_element(By.NAME, 'pub_date_0')
        pub_date_input.send_keys(today_date)
        pub_date_time = self.selenium.find_element(By.NAME, 'pub_date_1')
        pub_date_time.send_keys("10:00:00")
        self.selenium.find_element(By.NAME, "_save").click()

        # 3. Crear la segona pregunta
        self.selenium.get(f'{self.live_server_url}/admin/polls/question/add/')
        question_text_input = self.selenium.find_element(By.NAME, "question_text")
        question_text_input.send_keys("Pregunta 2")
        pub_date_input = self.selenium.find_element(By.NAME, 'pub_date_0')
        pub_date_input.send_keys(today_date)
        pub_date_time = self.selenium.find_element(By.NAME, 'pub_date_1')
        pub_date_time.send_keys("11:00:00")
        self.selenium.find_element(By.NAME, "_save").click()

        # 4. Crear les Choices per a cada pregunta
        # Choice 1 per Pregunta 1
        self.selenium.get(f'{self.live_server_url}/admin/polls/choice/add/')
        question_dropdown = self.selenium.find_element(By.NAME, "question")
        question_dropdown.send_keys("Pregunta 1")
        choice_text_input = self.selenium.find_element(By.NAME, "choice_text")
        choice_text_input.send_keys("Choice 1 per Pregunta 1")
        self.selenium.find_element(By.NAME, "_save").click()

        # Choice 2 per Pregunta 1
        self.selenium.get(f'{self.live_server_url}/admin/polls/choice/add/')
        question_dropdown = self.selenium.find_element(By.NAME, "question")
        question_dropdown.send_keys("Pregunta 1")
        choice_text_input = self.selenium.find_element(By.NAME, "choice_text")
        choice_text_input.send_keys("Choice 2 per Pregunta 1")
        self.selenium.find_element(By.NAME, "_save").click()

        # Choice 1 per Pregunta 2
        self.selenium.get(f'{self.live_server_url}/admin/polls/choice/add/')
        question_dropdown = self.selenium.find_element(By.NAME, "question")
        question_dropdown.send_keys("Pregunta 2")
        choice_text_input = self.selenium.find_element(By.NAME, "choice_text")
        choice_text_input.send_keys("Choice 1 per Pregunta 2")
        self.selenium.find_element(By.NAME, "_save").click()

        # Choice 2 per Pregunta 2
        self.selenium.get(f'{self.live_server_url}/admin/polls/choice/add/')
        question_dropdown = self.selenium.find_element(By.NAME, "question")
        question_dropdown.send_keys("Pregunta 2")
        choice_text_input = self.selenium.find_element(By.NAME, "choice_text")
        choice_text_input.send_keys("Choice 2 per Pregunta 2")
        self.selenium.find_element(By.NAME, "_save").click()

        # 5. Verificar que totes les Choices existeixen
        self.selenium.get(f'{self.live_server_url}/admin/polls/choice/')
        self.assertTrue(self.selenium.find_element(By.LINK_TEXT, "Choice 1 per Pregunta 1"))
        self.assertTrue(self.selenium.find_element(By.LINK_TEXT, "Choice 2 per Pregunta 1"))
        self.assertTrue(self.selenium.find_element(By.LINK_TEXT, "Choice 1 per Pregunta 2"))
        self.assertTrue(self.selenium.find_element(By.LINK_TEXT, "Choice 2 per Pregunta 2"))
