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
        # Eliminem el mode headless per mostrar el navegador
        # opts.headless = True  # Mode headless desactivat
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        
        # Creem el superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        # Tanquem el navegador
        cls.selenium.quit()
        super().tearDownClass()

    def test_crear_preguntes_i_choices(self):
        # Iniciem sessió com a superusuari
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        self.assertEqual(self.selenium.title, "Log in | Django site admin")

        # Introduïm nom d'usuari i contrasenya
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        # Obtenim la data d'avui per assignar-la a les preguntes
        today_date = datetime.today().strftime('%Y-%m-%d')  # format: '2024-11-19'

        # Creem la Pregunta 1
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/question/add/'))
        self.assertEqual(self.selenium.title, "Add question | Django site admin")

        question_text_input = self.selenium.find_element(By.NAME, "question_text")
        question_text_input.send_keys('Pregunta 1')

        # Afegim la data de publicació d'avui
        pub_date_input = self.selenium.find_element(By.NAME, 'pub_date_0')
        pub_date_input.send_keys(today_date)
        pub_date_input = self.selenium.find_element(By.NAME, 'pub_date_1')
        pub_date_input.send_keys('12:00:00')

        save_button = self.selenium.find_element(By.NAME, "_addanother")
        save_button.click()

        self.assertIn(' was added successfully. You may add another question below.', self.selenium.page_source)

        # Creem la Pregunta 2
        question_text_input = self.selenium.find_element(By.NAME, "question_text")
        question_text_input.send_keys('Pregunta 2')

        # Afegim la data de publicació d'avui
        pub_date_input = self.selenium.find_element(By.NAME, 'pub_date_0')
        pub_date_input.send_keys(today_date)
        pub_date_input = self.selenium.find_element(By.NAME, 'pub_date_1')
        pub_date_input.send_keys('12:30:00')

        save_button = self.selenium.find_element(By.NAME, "_save")
        save_button.click()

        self.assertIn(' was added successfully.', self.selenium.page_source)

        # Creem les Choices per la Pregunta 1
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/question/'))
        question1_edit_link = self.selenium.find_element(By.LINK_TEXT, "Pregunta 1")
        question1_edit_link.click()

        # Afegim la primera opció per la Pregunta 1
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/choice/add/'))
        choice_text_field = self.selenium.find_element(By.NAME, 'choice_text')
        choice_text_field.send_keys('Choice 1 per Pregunta 1')

        # Associem la Pregunta 1 a aquesta opció
        question_dropdown = self.selenium.find_element(By.NAME, 'question')
        question_dropdown.send_keys('Pregunta 1')

        save_button = self.selenium.find_element(By.NAME, "_addanother")
        save_button.click()

        # Afegim la segona opció per la Pregunta 1
        choice_text_field = self.selenium.find_element(By.NAME, 'choice_text')
        choice_text_field.send_keys('Choice 2 per Pregunta 1')

        # Associem la Pregunta 1 a aquesta opció
        question_dropdown = self.selenium.find_element(By.NAME, 'question')
        question_dropdown.send_keys('Pregunta 1')

        save_button = self.selenium.find_element(By.NAME, "_save")
        save_button.click()

        # Creem les Choices per la Pregunta 2
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/question/'))
        question2_edit_link = self.selenium.find_element(By.LINK_TEXT, "Pregunta 2")
        question2_edit_link.click()

        # Afegim la primera opció per la Pregunta 2
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/choice/add/'))
        choice_text_field = self.selenium.find_element(By.NAME, 'choice_text')
        choice_text_field.send_keys('Choice 1 per Pregunta 2')

        # Associem la Pregunta 2 a aquesta opció
        question_dropdown = self.selenium.find_element(By.NAME, 'question')
        question_dropdown.send_keys('Pregunta 2')

        save_button = self.selenium.find_element(By.NAME, "_addanother")
        save_button.click()

        # Afegim la segona opció per la Pregunta 2
        choice_text_field = self.selenium.find_element(By.NAME, 'choice_text')
        choice_text_field.send_keys('Choice 2 per Pregunta 2')

        # Associem la Pregunta 2 a aquesta opció
        question_dropdown = self.selenium.find_element(By.NAME, 'question')
        question_dropdown.send_keys('Pregunta 2')

        save_button = self.selenium.find_element(By.NAME, "_save")
        save_button.click()

        # Comprovem que les Choices s'han creat correctament
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/choice/'))
        self.assertEqual(self.selenium.title, "Select choice to view | Django site admin")

        # Comprovem que totes les opcions estan visibles
        choices = self.selenium.find_elements(By.LINK_TEXT, "Choice 1 per Pregunta 1")
        self.assertTrue(choices)
        choices = self.selenium.find_elements(By.LINK_TEXT, "Choice 2 per Pregunta 1")
        self.assertTrue(choices)
        choices = self.selenium.find_elements(By.LINK_TEXT, "Choice 1 per Pregunta 2")
        self.assertTrue(choices)
        choices = self.selenium.find_elements(By.LINK_TEXT, "Choice 2 per Pregunta 2")
        self.assertTrue(choices)
