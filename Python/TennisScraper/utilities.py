def find_utr_ids(soup_data, data_type):
    import re
    """
    Returns the player id and the UTR (Universal Tennis Ranking)
    ranking of a tennis player.

    Args:
        soup_data (obj): A beautiful soup object.
        data_type (str): The string to search for in the beautiful soup object.

    Returns:
        player_id: An integer of the associated player id
        utr_id: A float of the Universal Tennis Ranking (UTR)
    """
    try:
        data = soup_data.find_all(data_type)
        potential_utr_ids = []
        for item in data:
            id = re.findall('id":[\d+]+', str(item))
            if len(id) > 0:
                potential_utr_ids.append(id)
                player_id = int(potential_utr_ids[0][0].split(":")[1])
                utr_id = int(potential_utr_ids[0][2].split(":")[1])
                        
        return player_id, utr_id
    except:
        return "error", "error"



def find_utr_rating(login_url, url, utr_id, utr_username, utr_password):
    from bs4 import BeautifulSoup
    import html5lib
    import selenium
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    import re
    import time
    """
    Returns a dictionary of player ids and the UTR (Universal Tennis Ranking)
    ranking of the player.

    Args:
        login_url (str): The login URL of the UTR tennis page.
        url (str): The base URL of the UTR website to pull the rating
                   from.
        utr_id (int): The UTR id of the player to concatenate with the
                      url passed

    Returns:
        The player id and associated UTR id
        example: (1234: 5678).
    """
    try:
        options = Options()
        # options.add_argument("start-maximized")
        # options.add_argument("enable-automation")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-infobars")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-gpu")
        # options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(login_url)

        time.sleep(1)
        username = driver.find_element_by_id("emailInput")
        password = driver.find_element_by_id("passwordInput")
        username.send_keys(utr_username)
        password.send_keys(utr_password)
        driver.find_element_by_xpath("//*[@id='myutr-app-body']/div/div/div/div/div[1]/form/div[3]/button").click()
        time.sleep(5)

        driver.get(url + str(utr_id))
        time.sleep(5)
        html = driver.page_source
        driver.close()

        page = BeautifulSoup(html, "html5lib")
        item = page.find_all(class_=re.compile("ratingCircle__utrValue__L_LHa"))
        for id in item:
            rating_digit = re.findall(r"(\d+)", str(id))[0]
            rating_decimal = re.findall(r"(.\d+)", str(id))[2]
            rating = rating_digit + rating_decimal
            time.sleep(1)
            print(rating)
        return utr_id, rating
        driver.close()
    
    except:
        return utr_id, "error"
        driver.close()

def find_utr_rating_by_name(login_url, url, player_name, utr_username, utr_password):
    import selenium
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.common.exceptions import TimeoutException
    import re
    import time
    """
    Returns a dictionary of player ids and the UTR (Universal Tennis
    Ranking) ranking of the player.

    Args:
        soup_data (obj): A beautiful soup object.
        data_type (str): The string to search for in the beautiful soup
                         object.

    Returns:
        The player name and associated UTR id example: (1234: 5678).
    """
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    #driver = webdriver.Firefox()
    driver.get(login_url)

    time.sleep(5)
    try:
        username = driver.find_element_by_id("emailInput")
        password = driver.find_element_by_id("passwordInput")
        username.send_keys(utr_username)
        password.send_keys(utr_password)
        driver.find_element_by_xpath("//*[@id='myutr-app-body']/div/div/div/div/div[1]/form/div[3]/button").click()
        time.sleep(7)
        #driver.get(url)
        #driver.implicitly_wait(3)
        search = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/nav/div[1]/div[2]/div/div[1]/div/input")
        time.sleep(5)
        search.click()
        driver.implicitly_wait(3)
        search.send_keys(player_name)
        driver.implicitly_wait(3)
    except NoSuchElementException:
        driver.stop_client()
        driver.close()
        return "error on login"
    except UnboundLocalError:
        driver.stop_client()
        driver.close()
        return "UnboundLocalError"
    except StaleElementReferenceException:
        driver.stop_client()
        driver.close()
        return "StaleElementReferenceException"
    except TimeoutException:
        driver.stop_client()
        driver.close()
        return "TimeoutException"

    try:
        name = driver.find_element_by_class_name("globalSearch__name__3LzQY")
        name.click()
        driver.implicitly_wait(2)
        utr_url = driver.current_url
        utr_id = utr_url.split("/")[4]
        time.sleep(1)
        driver.stop_client()
        driver.close()
        return player_name, utr_id
    except NoSuchElementException:
        driver.stop_client()
        driver.close()
        return player_name, "No UTR id found"
    except UnboundLocalError:
        driver.stop_client()
        driver.close()
        return "UnboundLocalError"
    except StaleElementReferenceException:
        driver.stop_client()
        driver.close()
        return "StaleElementReferenceException"
    except TimeoutException:
        driver.stop_client()
        driver.close()
        return "TimeoutException"
