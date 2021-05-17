import selenium.common.exceptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait

from driver_set_up import driver_set_up
from info_getters import *


def __get_info():
    with open('conf.json') as json_file:
        return json.load(json_file)


def __create_user_dir(name, debug=False):
    if not os.path.isdir('./' + name):
        os.mkdir(name)
        if debug:
            print('users_info_dir se ha creado')
    else:
        if debug:
            print('users_info_dir ya se habia creado')


def cookie_agree(debug=False):
    try:
        driver.find_element_by_xpath("/html/body/div[2]/div/div/button[1]").click()
        if debug:
            print("Cookies aceptadas")
    except NoSuchElementException:
        print("No hay Cookies")


def fill_user_data(debug=False):
    try:
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.NAME, "username")))
        driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input").send_keys(
            inf_user['our_user'])
        driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input").send_keys(
            inf_user['password'])
        if debug:
            print("Usuario aceptado")
        driver.implicitly_wait(100)
    except NoSuchElementException:
        try:
            driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(
                inf_user['our_user'])
            driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input").send_keys(
                inf_user['password'])
            driver.implicitly_wait(100)
        except NoSuchElementException:
            print("No hay login")


def session_start(debug=False):
    try:
        driver.implicitly_wait(300)
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button")))
        driver.implicitly_wait(500)
        driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button').click()
        if debug:
            print("Usuario aceptado")
        driver.implicitly_wait(100)
    except NoSuchElementException:
        try:
            driver.implicitly_wait(300)
            driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div').click()
            driver.implicitly_wait(100)
        except NoSuchElementException:
            print("No se puede iniciar sesion")


def save_session_info_agree(decision, debug=False):
    try:
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/section/div/button')))
        if decision:
            driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/section/div/button').click()
            if debug:
                print("Salvar la info de inicio de sesion")
        else:
            driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
            if debug:
                print("No salvar la info de inicio de sesion")
    except NoSuchElementException:
        print("Falta la pantalla de salvar la informacion")


def go_user_profile(username, debug=False):
    try:
        if debug:
            print("Vamos al perfil del usuario: " + username)
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[1]')))
        driver.get("https://www.instagram.com/" + username)  # TODO NO BORRAR ESTO ES PARA PEDIR UN USUARIO
    except NoSuchElementException:
        print("No se encuentra usuario")


def get_dict_json(cookies, debug=False):
    aux_dict = {}
    for cookie in cookies:
        aux_dict[cookie['name']] = cookie['value']
    if debug:
        print(aux_dict)
    return aux_dict


def set_initial_conf():
    dictionary = dict()
    print("------------------------------------------------------")
    dictionary["our_user"] = input('Escriba su usuario: \n')
    dictionary["password"] = input('Escriba su contraseña: \n')
    print("------------------------------------------------------")
    print('¿Cuantas fotos va a querer extraer? (-1 para todas) ')
    print("Nota: La extraccion de fotos puede ser un proceso lento le recomendamos MAX 200")
    max_photos = input()
    dictionary["max_photos"] = max_photos

    print("------------------------------------------------------")
    print("La extraccion de los follower/following no esta recomendada para cuentas con más de 10.000 personas en "
          "estos apartados")
    q_followers = input('¿Quieres extraer los followers? S/n  \n')
    dictionary["extraer_follow_ers"] = "True"
    if q_followers.lower() == 'n' or q_followers.lower() == 'no':
        dictionary["extraer_follow_ers"] = "False"
    q_following = input('¿Quieres extraer los following? S/n  \n')
    dictionary["extraer_follow_ing"] = "True"
    if q_following.lower() == 'n' or q_following.lower() == 'no':
        dictionary["extraer_follow_ing"] = "False"
    print("------------------------------------------------------")
    dictionary["dir_name"] = input('¿Que nombre le quieres poner a la carpeta principal? \n')
    if dictionary["dir_name"] == "":
        dictionary["dir_name"] = "users_info_dir"
    print("------------------------------------------------------")
    dictionary['login_url'] = 'https://www.instagram.com/accounts/login/?source=deactivate'
    dictionary['save_session_info'] = "True"
    dictionary['main_page'] = 'https://www.instagram.com/'
    dictionary['first_time'] = 'False'

    with open(os.path.join("conf.json"), 'w+') as file:
        json.dump(dictionary, file, indent=1)


def __parse_boolean(boolean_):
    return boolean_.lower() == "true"


def __parse_max_photos(num_photos):
    if num_photos == "-1" or num_photos == "":
        return math.inf
    return int(num_photos)


def __menu(inf):
    salir_app = False
    salir_ext = False
    while not salir_app:
        print("------------------------------------------------------")
        print("Seleccione una opcion:")
        print("1) Extraer informacion")
        print("2) Modificar configuración de extracción")
        print("3) Salir")
        sel = input()
        if sel == "1":
            while not salir_ext:
                user_wnt = input("Introduce un nombre de usuario o -1 para salir: \n")
                if user_wnt == "-1" or user_wnt == "":
                    salir_ext = True
                else:
                    get_user_info(user_wnt, inf['dir_name'], cookies_dict['sessionid'],
                                  __parse_boolean(inf['extraer_follow_ers']),
                                  __parse_boolean(inf['extraer_follow_ing']), __parse_max_photos(inf['max_photos']),
                                  debug=True)
            salir_ext = False
        elif sel == "2":
            set_initial_conf()
            inf = __get_info()
        elif sel == "3":
            salir_app = True
        else:
            print("Introduce una opción valida")


if __name__ == '__main__':
    driver = None
    inf_user = __get_info()
    try:
        # Inicializacion de la info
        if __parse_boolean(inf_user['first_time']):
            set_initial_conf()
            inf_user = __get_info()
        # Inicializacion del driver
        print("Cargando información...")
        driver = driver_set_up()

        # Creacion de la carpeta raiz
        __create_user_dir(inf_user['dir_name'])
        # Iniciar las pantallas
        cookie_agree()
        fill_user_data()
        session_start()
    except (TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
        driver.implicitly_wait(500)
        driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/div/div[1]/div/form/div[1]/div[3]/button/div').click()

    save_session_info_agree(inf_user['save_session_info'])
    # Creacion de las cookies para evitar el cierrre de sesion
    cookies_dict = get_dict_json(driver.get_cookies())
    # Llamar al menu
    print("------------------------------------------------------")
    print("Bienvenido al extrator de información de instagram")
    __menu(inf_user)
