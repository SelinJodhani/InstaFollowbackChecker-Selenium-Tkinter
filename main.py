from tkinter.constants import *
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import tkinter as tk
import os
import time
import ctypes
 
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class InstaBot(tk.Tk):

    def __init__(self):

        super().__init__()
        self.geometry("444x344")
        self.maxsize(444, 444)
        self.minsize(444, 444)
        self.wm_iconbitmap("icon/3721672-instagram_108066.ico")
        self.title("Instagram Followback Checker")
        self.configure(background="grey20")
        self.widgets()

    def widgets(self):

        self.label = tk.Label(text="Login to your instagram account", background="pink", fg="black", font=("Arial", 13))
        self.label.pack(side=TOP, fill=X)

        self.varRadio = tk.IntVar()
        self.selectBrowser1 = tk.Radiobutton(self, text="Chrome", variable=self.varRadio, value=1, bg="grey20", foreground="white", activebackground="grey20", activeforeground="white", selectcolor="grey20")
        self.selectBrowser2 = tk.Radiobutton(self, text="Edge", variable=self.varRadio, value=2, bg="grey20", foreground="white", activebackground="grey20", activeforeground="white", selectcolor="grey20")
        self.selectBrowser1.place(relx=0.39, rely=0.18)
        self.selectBrowser2.place(relx=0.6, rely=0.18)

        self.lableUsername = tk.Label(self, text="Username : ", background="grey20", foreground="white")
        self.lablePassword = tk.Label(self, text="Password : ", background="grey20", foreground="white")
        self.lableUsername.place(relx=0.2, rely=0.3)
        self.lablePassword.place(relx=0.2, rely=0.4)

        self.userValue = tk.StringVar()
        self.passValue = tk.StringVar()

        self.entryUsername = tk.Entry(self, textvariable=self.userValue)
        self.entryPassword = tk.Entry(self, textvariable=self.passValue, show="*")
        self.entryUsername.place(relx=0.4, rely=0.3)
        self.entryPassword.place(relx=0.4, rely=0.4)

        self.errorValue = tk.StringVar()
        self.errorLable = tk.Label(self, textvariable=self.errorValue, background="gray20", foreground="red")
        self.errorLable.pack(side=BOTTOM, fill=X)

        self.buttonLogin = tk.Button(self, text="Login", relief="raised", bg="grey60", command=lambda: self.login(self.userValue.get(), self.passValue.get()))
        self.buttonLogin.place(relx=0.4, rely=0.5)

    def otp(self):

        if not self.otpValue.get():
            self.errorValue.set("OTP can not be empty.")
        elif len(self.otpValue.get()) != 6:
            self.errorValue.set("Length Mismatch (Expected: 6 digits).")
        else:
            # OTP Button
            self.driver.find_element_by_name('verificationCode').send_keys(int(self.otpValue.get()))
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[2]/button').click()
            time.sleep(5)

        try:
            if self.driver.find_element_by_id('twoFactorErrorAlert'):
                self.errorValue.set("Please check the security code.")
                self.driver.find_element_by_name('verificationCode').send_keys(Keys.CONTROL + u'\ue003')
        except:
            self.errorValue.set(" ")
            self.noOTP()
               
    def noOTP(self):

        time.sleep(5)

        # Save info/not now button
        self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        time.sleep(5)

        # Turn on/off notification button
        self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        time.sleep(5)

        self.get_unfollowers()

    def login(self, username, password):

        if not self.varRadio.get():
            self.errorValue.set("Select browser.")
        elif not self.userValue.get():
            self.errorValue.set("Username can not be empty.")
        elif not self.passValue.get():
            self.errorValue.set("Password can not be empty.")
        else:
            self.errorValue.set(" ")

            if self.varRadio.get() == 1:
                self.driver = webdriver.Chrome(ChromeDriverManager().install())
            elif self.varRadio.get() == 2:
                self.driver = webdriver.Edge(EdgeChromiumDriverManager().install())

            self.driver.get('https://www.instagram.com/')
            time.sleep(5)

            # Username, Password and Login button
            self.driver.find_element_by_xpath('//input[@name = "username"]').send_keys(username)
            self.driver.find_element_by_xpath('//input[@name = "password"]').send_keys(password)
            self.driver.find_element_by_xpath('//button[@type = "submit"]').click()
            time.sleep(5)

            try:
                if self.driver.find_element_by_id('slfErrorAlert'):
                    self.errorValue.set("Your email/password was incorrect.")
                    self.driver.find_element_by_xpath('//input[@name = "username"]').send_keys(Keys.CONTROL + u'\ue003')
                    self.driver.find_element_by_xpath('//input[@name = "password"]').send_keys(Keys.CONTROL + u'\ue003')
            except:

                self.errorValue.set(" ")

                self.selectBrowser1.destroy()
                self.selectBrowser2.destroy()
                self.lableUsername.destroy()
                self.lablePassword.destroy()
                self.entryUsername.destroy()
                self.entryPassword.destroy()
                self.buttonLogin.destroy()

                self.lableOTP = tk.Label(self, text="OTP : ", background="grey20", foreground="white")
                self.lableOTP.place(relx=0.2, rely=0.3)

                self.otpValue = tk.StringVar()
                self.entryOTP = tk.Entry(self, textvariable=self.otpValue)
                self.entryOTP.place(relx=0.3, rely=0.3)

                self.buttonSubmit = tk.Button(self, text="Submit", relief="raised", bg="grey60", command=self.otp)
                self.buttonSubmit.place(relx=0.3, rely=0.4)

                self.noOtp = tk.Button(self, text="Don't have 2-step verification enabled?", bd=0, bg="grey20", fg="pink", command=self.noOTP)
                self.noOtp.place(relx=0.29, rely=0.5)
        
    def get_unfollowers(self):

        # Profile Button
        self.driver.find_element_by_xpath(f'//a[contains(text(), "{self.userValue.get()}")]').click()
        time.sleep(4)

        # Following Button
        self.driver.find_element_by_xpath(f'//a[contains(@href, "following")]').click()
        time.sleep(4)
        following = self._get_names()

        # Followers Button
        self.driver.find_element_by_xpath('//a[contains(@href,"followers")]').click()
        time.sleep(4)
        followers = self._get_names()
        time.sleep(5)

        not_following_back = [user for user in following if user not in followers]

        path = os.getcwd()
        now = datetime.now()
        file = now.strftime("%b-%d-%Y, %M")

        with open(os.path.join(path, file + '.txt'), 'a') as f:
            f.write(f'------------------------- {now.strftime("%b-%d-%Y, %H:%M:%S")} -------------------------\n\n')
            for i in not_following_back:
                f.write(f'--> @{i}\n')

    def _get_names(self):

        #Scrolling in view
        scroll_box = self.driver.find_element_by_xpath('//div[@class = "isgrP"]')

        last_ht = 0
        ht = 1

        while last_ht != ht:
            last_ht = ht
            time.sleep(2)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)

        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']

        # close button
        self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button/div').click()

        return names

if __name__ == '__main__':
    root = InstaBot()
    root.mainloop()

