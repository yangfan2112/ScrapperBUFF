from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver import ActionChains
import random
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def configure_driver_with_profile(settings, user_agent):
    
    # Path del perfil de Chrome
    chrome_profile_path = 'C:\\Users\\ivan\\AppData\\Local\\Google\\Chrome\\User Data'  # Ruta a tu perfil de Chrome

    service = Service(settings.chromedriver_path)

    options = Options()

    # Configurar la ruta del perfil
    options.add_argument("user-data-dir=" + chrome_profile_path)

    # Más configuraciones como el user agent, etc.
    options.add_argument("start-maximized")
    options.add_argument('user-agent={user_agent}')
    options.add_argument('disable-blink-features')
    options.add_argument('disable-blink-features=AutomationControlled')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('log-level=3')
    options.binary_location = settings.binary_location

    driver = webdriver.Chrome(service=service, options=options)
    # overwrite the webdriver property
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

    #
    driver.execute_cdp_cmd("Network.enable", {})

    # overwrite the User-Agent header
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": user_agent}})

    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    return driver


def set_download_path(driver, new_path):

    params = {'cmd': 'Page.setDownloadBehavior',
                  'params': {
                      'behavior': 'allow',
                      'downloadPath': new_path
                  }
              }

    driver.execute("send_command", params)


def solve_wait_recaptcha(driver):

    # Move to reCAPTCHA Iframe
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor?']")
    ))

    check_selector = "span.recaptcha-checkbox.goog-inline-block.recaptcha-checkbox-unchecked.rc-anchor-checkbox"

    captcha_check = driver.find_element_by_css_selector(
        check_selector
    )

    # Click the checkbox
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable(
    #         (By.CSS_SELECTOR,
    #          check_selector)
    #     ))

    # Random delay before hover & click the checkbox
    sleep(random.uniform(3, 6))
    ActionChains(driver).move_to_element(captcha_check).perform()

    # Hover it
    sleep(random.uniform(0.5, 1))
    hov = ActionChains(driver).move_to_element(captcha_check).perform()

    # Random delay before click the checkbox
    sleep(random.uniform(0.5, 1))
    driver.execute_script("arguments[0].click()", captcha_check)

    # Wait for recaptcha to be in solved state
    elem = None
    while elem is None:
        try:
            elem = driver.find_element_by_class_name("recaptcha-checkbox-checked")
        except:
            pass
        sleep(5)


#Hacemos el login despues el captcha
def site_login(driver, settings):

    driver.find_element_by_id("numcontacontrato").send_keys(settings.num_contrato)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cmdEnviar"))).click()

    try:

        driver.execute_script("$('#divModalCampana')[0].remove();")

        driver.execute_script("$('#divModalCampanaBak')[0].remove();")

        # WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
        #     (By.ID, "ifrVCE")
        # ))
        #
        # WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, "dijitDialogCloseIcon"))).click()
        #
        # WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, "continuarSinRegistrarBtn_label"))).click()

    except:
        pass

    # TODO: Check if we did log-in successfully
    return True


def show_progress(driver, progress_message):

    driver.execute_script(
        """
                    rex_bar = document.getElementById('rex_progress_bar');
                    if (rex_bar === null) {{

                        var newDiv = document.createElement("div");

                        var newContent = document.createTextNode("{0}");

                        newDiv.appendChild(newContent);

                        newDiv.setAttribute( 'style',
                            'z-index: 1000; top: 10px; left: 10px; position: absolute; background: black; color: white; padding: 5px 10px; border-radius: 5px;');

                        newDiv.setAttribute( 'id', 'rex_progress_bar');

                        document.getElementsByTagName('body')[0].appendChild(newDiv);

                    }} else {{

                        rex_bar.innerText = "{0}";

                    }}

                """.format(progress_message)
    )
