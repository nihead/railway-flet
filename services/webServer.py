import sys
from bs4 import BeautifulSoup
import requests


class ScannedUser:
    uid: int = None
    name: str = None
    work_on: str = None
    work_on_code: str = None
    total_lt: str = None
    c_page: str = None


class ScanUser:
    def __init__(self):
        self.user = ScannedUser()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        # self.session.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;'})
        # self.session.headers.update({'Accept-Language': 'en-US,en;q=0.8'})
        # self.session.headers.update({'Accept-Encoding': 'gzip, deflate, br'})
        self.session.get("https://winair.transmaldivian.com/maintenance/timetracking/home")
        self.cookies = self.session.cookies.get_dict()
        print(self.cookies)

    def scan(self, uid) -> bool:
        try:
            print(uid)
            self.user.uid = uid
            response = self.session.get(f"https://winair.transmaldivian.com/maintenance/timetracking/userScan.rpc?ajaxRequest=true&username=EC{uid}")
            # print(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup.title.string)
            self.user.c_page = soup.title.string
            if self.user.c_page != "User Scan":
                # Find all span elements with class "page_title"
                page_title_spans = soup.find_all('span', class_='page_title')
                self.user.name = page_title_spans[0].string
                self.user.total_lt = page_title_spans[1].string

                if self.user.c_page == "Started tracking time":
                    working_task_name_obj = soup.find_all('span', class_='system_response_value')
                    working_task_name: list[str] = working_task_name_obj[0].string.split(",")
                    self.user.work_on_code = working_task_name[1].strip()
                    self.user.work_on = working_task_name[0].strip()

                return True
            else:
                raise IndexError


        except Exception as e:
            print(f'user logging error : {e}')
            return False

    def update_work_on(self, ans:str):
        ws = self.session.post(f"https://winair.transmaldivian.com/maintenance/timetracking/isTaskComplete.rpc?ajaxRequest=true&username={self.user.uid}&completed={ans.upper()}")
        print(ws.text)

    def get_user(self):
        print(f"Name: {self.user.name}")
        print(f"Time Lt: {self.user.total_lt}")
        print(f"Working on: {self.user.work_on}")
        print(f"Working on code: {self.user.work_on_code}")
        return self.user




if __name__ == '__main__':
    scans =ScanUser()
    scans.scan("11112")
    scans.get_user()