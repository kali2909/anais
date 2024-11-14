from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # Crear superusuario
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # Ir a la página de acceso al panel de administración
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # Comprobar que el título de la página es el esperado
        self.assertEqual(self.selenium.title, "Log in | Django site admin")

        # Introducir datos de inicio de sesión y hacer clic en "Log in"
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        # Verificar que hemos ingresado al panel de administración
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")
def test_login_and_create_questions(self):
    # Ir a la página de acceso al panel de administración
    self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

    # Comprobar que el título de la página es el esperado
    self.assertEqual(self.selenium.title, "Log in | Django site admin")

    # Introducir datos de inicio de sesión y hacer clic en "Log in"
    username_input = self.selenium.find_element(By.NAME, "username")
    username_input.send_keys('isard')
    password_input = self.selenium.find_element(By.NAME, "password")
    password_input.send_keys('pirineus')
    self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

    # Verificar que hemos ingresado al panel de administración
    self.assertEqual(self.selenium.title, "Site administration | Django site admin")

    # Ahora vamos a crear una pregunta
    self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/question/add/'))
    
    # Comprobar que estamos en la página de creación de preguntas
    self.assertEqual(self.selenium.title, "Add question | Django site admin")
    
    # Llenar el formulario para la pregunta
    question_input = self.selenium.find_element(By.NAME, "question_text")
    question_input.send_keys("Pregunta de prueba")

    # Hacer clic en el botón para guardar la pregunta
    self.selenium.find_element(By.XPATH, '//input[@value="Save"]').click()
    
    # Verificar que la pregunta se ha guardado
    self.assertEqual(self.selenium.title, "Change question | Django site admin")
def test_login_and_create_questions_and_choices(self):
    # Ir a la página de acceso al panel de administración
    self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

    # Comprobar que el título de la página es el esperado
    self.assertEqual(self.selenium.title, "Log in | Django site admin")

    # Introducir datos de inicio de sesión y hacer clic en "Log in"
    username_input = self.selenium.find_element(By.NAME, "username")
    username_input.send_keys('isard')
    password_input = self.selenium.find_element(By.NAME, "password")
    password_input.send_keys('pirineus')
    self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

    # Verificar que hemos ingresado al panel de administración
    self.assertEqual(self.selenium.title, "Site administration | Django site admin")

    # Crear una pregunta
    self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/question/add/'))
    self.assertEqual(self.selenium.title, "Add question | Django site admin")

    question_input = self.selenium.find_element(By.NAME, "question_text")
    question_input.send_keys("Pregunta de prueba")
    self.selenium.find_element(By.XPATH, '//input[@value="Save"]').click()

    # Comprobar que hemos regresado a la lista de preguntas
    self.assertEqual(self.selenium.title, "Change question | Django site admin")
def test_login_and_create_questions_and_choices(self):
    # Ir a la página de acceso al panel de administración
    self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

    # Comprobar que el título de la página es el esperado
    self.assertEqual(self.selenium.title, "Log in | Django site admin")

    # Introducir datos de inicio de sesión y hacer clic en "Log in"
    username_input = self.selenium.find_element(By.NAME, "username")
    username_input.send_keys('isard')
    password_input = self.selenium.find_element(By.NAME, "password")
    password_input.send_keys('pirineus')
    self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

    # Verificar que hemos ingresado al panel de administración
    self.assertEqual(self.selenium.title, "Site administration | Django site admin")

    # Crear una pregunta
    self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/question/add/'))
    self.assertEqual(self.selenium.title, "Add question | Django site admin")

    question_input = self.selenium.find_element(By.NAME, "question_text")
    question_input.send_keys("Pregunta de prueba")
    self.selenium.find_element(By.XPATH, '//input[@value="Save"]').click()

    # Comprobar que hemos regresado a la lista de preguntas
    self.assertEqual(self.selenium.title, "Change question | Django site admin")

    # Añadir opciones a la pregunta
    self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/choice/add/?question=1'))  # Asegúrate de que el ID de la pregunta sea correcto
    self.assertEqual(self.selenium.title, "Add choice | Django site admin")

    # Llenar el formulario para la opción
    choice_input = self.selenium.find_element(By.NAME, "choice_text")
    choice_input.send_keys("Opción 1 para Pregunta de prueba")
    self.selenium.find_element(By.XPATH, '//input[@value="Save"]').click()

    # Repetir para añadir otra opción
    self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/choice/add/?question=1'))
    choice_input = self.selenium.find_element(By.NAME, "choice_text")
    choice_input.send_keys("Opción 2 para Pregunta de prueba")
    self.selenium.find_element(By.XPATH, '//input[@value="Save"]').click()

    # Comprobar que hemos regresado a la página de opciones
    self.assertEqual(self.selenium.title, "Change choice | Django site admin")
