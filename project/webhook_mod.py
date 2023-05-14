from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pyngrok import ngrok
from selenium.webdriver.common.keys import Keys


def initial():
    def connNgrok():
        ngrok.kill()
        port = 80
        ngrok.connect(port)
        public_url = ngrok.get_tunnels()[0].public_url
        print(" * ngrok tunnel \"{}\" -> \http://127.0.0.1:{}/\"".format(public_url, port))
        return public_url
    url = connNgrok()
    driver = webdriver.Chrome("chromedriver.exe")
    channelID="1660935653"
    driver.get("https://developers.line.biz/console/channel/"+channelID)
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div[3]/div/div[3]/div[2]/a").click()
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div[3]/div/div[3]/div[2]/form/div/div[1]/input").send_keys("hakkalinebot6@gmail.com")
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div[3]/div/div[3]/div[2]/form/div/div[2]/input").send_keys("hakka0523")
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div[3]/div/div[3]/div[2]/form/div/div[5]/button").click()
    time.sleep(3)
    driver.find_element(
        By.XPATH, "//*[@id=\"app\"]/section/div/div/div[1]/nav/ul/li[2]/button").click()
    driver.find_element(
        By.XPATH, "//*[@id=\"app\"]/section/div/div/section/div/section[2]/div[1]/aside/div/div[2]/button[2]").click()
    textarea = driver.find_element(
        By.XPATH, "//*[@id=\"app\"]/section/div/div/section/div/section[2]/div[1]/section/div/div/textarea")
    textarea.send_keys(Keys.CONTROL + 'a')
    textarea.send_keys(Keys.DELETE)
    textarea.send_keys(str(url)+'/callback')
    driver.find_element(
        By.XPATH, "//*[@id=\"app\"]/section/div/div/section/div/section[2]/div[1]/aside/div/div[2]/button[1]").click()
    return driver


def verify(driver):
    time.sleep(5)
    driver.find_element(
        By.XPATH, "/html/body/div/div/div/section/div/div/section/div/section[2]/div[1]/aside/div/div[2]/button[1]").click()
    time.sleep(3)
    driver.quit()