import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def __set_options():
    options = Options()
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream_mic": 1,
                                              "profile.default_content_setting_values.media_stream_camera": 1,
                                              "profile.default_content_setting_values.geolocation": 1,
                                              "profile.default_content_setting_values.notifications": 1
                                              })
    return options


def driver_set_up():
    driverAux = webdriver.Chrome(options=__set_options(), executable_path=r"C:\dchrome\chromedriver.exe")
    driverAux.set_window_size(1280, 1000)
    driverAux.minimize_window()

    driverAux.get('https://www.instagram.com/accounts/login/?source=deactivate')

    return driverAux
