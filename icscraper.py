from dotenv import load_dotenv, dotenv_values
import json
import os
import re
import requests
import time

BASE = "https://dcsdk12.infinitecampus.org/campus"

LOGIN_PAGE = f"{BASE}/portal/students/douglas.jsp?status=logoff"
LOGIN_POST = f"{BASE}/verify.jsp"
TARGET = f"{BASE}/nav-wrapper/student/portal/student/grades"
PRISM_API_CALL = f"{BASE}/prism"
GRADES_API_CALL = f"{BASE}/resources/portal/grades"
GPA_API_CALL = f"{BASE}/api/campus/grading/gpas/my/gpa"

def main():
    p = Page()
    p.login(create_login_info())
    p.get_user_info()
    p.get_notifications()
    p.get_gpa()
    p.get_grades()

    p.output()

def create_login_info() -> dict:
    load_dotenv()

    data = {
        "username":  os.getenv("USER_NAME"),
        "password": os.getenv("PASSWORD"),
        "appName": "douglas",
        "url": "nav-wrapper",
        "lang": "en",
        "portalLoginPage": "students",
    }

    return data

class Page:
    def __init__(self):
        self.session = requests.Session()
        self.r = self.session.get(LOGIN_PAGE)
    
    def login(self, data: dict):
        html = self.r.text

        match = re.search(r'name="portalUrl" value="([^"]+)"', html)
        if not match:
            raise Exception("portalUrl not found in login page")

        data["portalUrl"] = match.group(1)

        headers = {
            "Origin": BASE,
            "Referer": LOGIN_PAGE,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        self.r = self.session.post(LOGIN_POST, data=data, headers=headers, allow_redirects=True)
        self.r = self.session.get(TARGET, allow_redirects=True)

        assert("grades" in self.r.url)
    
    def get_user_info(self):
        self.user_info = self.call_api(PRISM_API_CALL, {
            "x": "user.UserAccount-loadFromUser",
            "header": "true"
        })["data"]["Header"]["User"]
        
        print(f"{self.user_info["firstName"]} {self.user_info["lastName"]}")
    
    def get_notifications(self):
        self.notifications = self.call_api(PRISM_API_CALL, {
            "x": "notifications.Notification-retrieve",
            "limitCount": "200",
            "urlFilter": "portal"
        })["data"]["NotificationList"]["Notification"]
    
    def get_gpa(self):
        self.gpa = self.call_api(GPA_API_CALL)
    
    def get_grades(self):
        self.grades = self.call_api(GRADES_API_CALL)

    def call_api(self, target: str, params: dict = {}):
        headers = {
            "Accept": "application/json",
            "Referer": TARGET
        }

        self.r = self.session.get(target, params=params, headers=headers)

        return json.loads(self.r.text)
    
    def output(self):
        if not os.path.exists("out"):
            os.mkdir("out")

        with open("out/user_info.json", mode="w+", encoding="utf-8") as info_file:
            json.dump(self.user_info, info_file, indent=4)
        
        with open("out/notifications.json", mode="w+", encoding="utf-8") as notifs_file:
            json.dump(self.notifications, notifs_file, indent=4)
        
        with open("out/gpa.json", mode="w+", encoding="utf-8") as gpa_file:
            json.dump(self.gpa, gpa_file, indent=4)
        
        with open("out/grades.json", mode="w+", encoding="utf-8") as grades_file:
            json.dump(self.grades, grades_file, indent=4)

if __name__ == "__main__":
    main()

