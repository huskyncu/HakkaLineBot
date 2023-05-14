def start():
    # from pyngrok import ngrok

    # https_tunnel = ngrok.connect(5000)

    # print(https_tunnel)
    
    from selenium import webdriver
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    import os
    from bs4 import BeautifulSoup
    # 指定Chrome瀏覽器的webdriver路徑，並開啟瀏覽器
    driver_path = './chromedriver' #/ 請將此路徑替換為實際的webdriver執行檔案路徑
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    driver = webdriver.Chrome(driver_path,chrome_options = option)
    # 打開評分網站
    driver.get('https://account.line.biz/login')
    # 等待網頁加載完成
    time.sleep(5)
    # 找到圖片上傳按鈕，點擊後彈出文件選擇對話框
    bus_login_button = driver.find_element_by_xpath("//div[@class='px-3 mb-4']/a")
    bus_login_button.click()
    #user_.send_keys('hakkalinebot6@gmail.com')
    # bus_login_button = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[3]/div[2]/a')
    # bus_login_button.click()
    time.sleep(5)
start()