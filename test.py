from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import cmd
import time
import threading

WAIT = 2

class BrowserNavigator:
    def __init__(self):
        self.__driver = webdriver.Chrome()
        self.__driver_lock = threading.Lock()
        self.__exit_lock = threading.Lock()
        self.__exit_threads = False
    
    def __del__(self):
        self.__driver.close()

    def exit_threads(self):
        with self.__exit_lock:
            self.__exit_threads = True

    def go_to(self, page_url):
        with self.__driver_lock:
            self.__driver.get(page_url)
            time.sleep(5)
    
    def start_timer(self, page_url, text_cmd, frequency_s):
        print("Running cmd: ")
        while(not self.__exit_threads):
            with self.__driver_lock:
                self.__driver.get(page_url)
                time.sleep(5)

                elem = self.__driver.find_elements_by_class_name("slateTextArea-1Mkdgw")
                time.sleep(2)
                print("text_cmd:", text_cmd, "\n")
                elem[0].send_keys(text_cmd)
                elem[0].send_keys(Keys.RETURN)

            start_time = time.time()
            while time.time() - start_time < float(frequency_s) and not self.__exit_threads:
                time.sleep(5)

class myThread(threading.Thread):
    def __init__(self, driver, page_url, text_cmd, frequency_s):
        threading.Thread.__init__(self)
        self.driver = driver
        self.page_url = page_url
        self.text_cmd = text_cmd
        self.frequency_s = frequency_s
    def run(self):
        self.driver.start_timer(self.page_url, self.text_cmd, self.frequency_s)

nav = BrowserNavigator()
nav.go_to("https://discord.com")

print("\n\n\n\n\n\n\n")
threads = []
while(True):
    text = input("Enter Cmd (exit or <url> <text> <freq s>): \n")
    if text == "exit":
        nav.exit_threads()
        break
    else:
        info = text.split()
        print("hi")
        thread = myThread(nav, info[0], info[1], info[2])
        thread.start()
        threads.append(thread)
    
    time.sleep(1)
    print("\n\n")

for t in threads:
    t.join()

print("Exiting")
# waifu:
# https://discord.com/channels/127538186804002816/782486500730208328



# shack:
# https://discord.com/channels/127538186804002816/783418628309254164