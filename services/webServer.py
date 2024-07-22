import sys
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass,fields, asdict
from flet import Page
import flet as ft
@dataclass
class WinairRespose:
    uid:str = None
    name: str = None
    total_lt: str = "00:00"
    task_lt: str = "00:00"
    page_title: str = None
    work_on: str = None
    work_on_code: str = None

    def to_dict(self):
        print("returning")
        return asdict(self)


class ScanUser:
    def __init__(self, page: Page):
        self.winairRespose = WinairRespose()
        self.page = page
        self.uid = None
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        self.session.get("https://winair.transmaldivian.com/maintenance/timetracking/home")
        print(self.session.cookies)

    def login(self, uid):
        print(" 0 Login in user:", uid)
        try:
            # del self.user
            print("Login in user:",uid)
            self.winairRespose.uid = uid
            self.uid = uid
            response = self.session.get(f"https://winair.transmaldivian.com/maintenance/timetracking/userScan.rpc?ajaxRequest=true&username=EC{uid}")
            # print(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup.title.string)
            self.winairRespose.page_title = soup.title.string
            if self.winairRespose.page_title != "User Scan":
                # Find all span elements with class "page_title"
                page_title_spans = soup.find_all('span', class_='page_title')
                self.winairRespose.name = page_title_spans[0].string
                self.winairRespose.total_lt = page_title_spans[1].string.strip()

                if self.winairRespose.page_title == "Started tracking time":
                    working_task_name_obj = soup.find_all('span', class_='system_response_value')
                    working_task_name: list[str] = working_task_name_obj[0].string.split(",")
                    self.winairRespose.work_on_code = working_task_name[1].strip()
                    self.winairRespose.work_on = working_task_name[0].strip()
                    #This task time
                    timecard_span = soup.find('span', text='This Timecard:')

                    if timecard_span:
                        # Get the next sibling span (which should contain the time)
                        time_span = timecard_span.find_next_sibling('span', class_='page_title_alt')

                        if time_span:
                            timecard_value = time_span.text.strip()
                            # print(f"This Timecard: {timecard_value}")
                            self.winairRespose.task_lt = timecard_value
                        else:
                            print("Could not find the time value for 'This Timecard'")
                    else:
                        print("Could not find 'This Timecard' span")

                print("Savin....local machin")
                self.page.client_storage.set("winair_response", self.winairRespose)
                return self.winairRespose
            else:
                raise IndexError


        except Exception as e:
            print(f'user logging error : {e}')
            return False

    def start_task(self, tid):
        data = self.get_saved()
        self.login(data['uid'])
        url = f"https://winair.transmaldivian.com/maintenance/timetracking/woTaskScan.rpc?ajaxRequest=true&username={self.winairRespose.uid}&wotask=TC{tid}"
        tc = self.session.post(url)
        soup = BeautifulSoup(tc.text, 'html.parser')
        # Find the div with class "error_area"
        if tc.status_code == 200:
            print("Task started")
            error_div = soup.find('div', class_='error_area')
            if error_div:
                error_tc = error_div.text.strip()

                return False, error_tc
            return True, "Saved"

        else:
            return False, "False"

    def update_work_on(self, ans:str):
        ws = self.session.post(f"https://winair.transmaldivian.com/maintenance/timetracking/isTaskComplete.rpc?ajaxRequest=true&username={self.winairRespose.uid}&completed={ans.upper()}")
        if ws.status_code == 200:
            away = self.session.post(f"https://winair.transmaldivian.com/maintenance/timetracking/woTaskScan.rpc?ajaxRequest=true&username={self.winairRespose.uid}&wotask=AWAY")
            if away.status_code == 200:
                print("Task completed and is away")
                return True
            else:
                return False
        else:
            return False

    def on_break_start(self):
        ob = self.session.post(f"https://winair.transmaldivian.com/maintenance/timetracking/woTaskScan.rpc?ajaxRequest=true&username={self.winairRespose.uid}&wotask=BREAK")
        if ob.status_code == 200:
            return True
        else:
            return False

    def on_close(self):
        del self.winairRespose
        self.session.close()
        print("Session closed")

    def save_response(self, obj):
        self.page.client_storage.set("winair_response", obj)
    def get_saved(self):
        if self.page.client_storage.contains_key("winair_response"):
            s = self.page.client_storage.get("winair_response")
            return s
        else:
            return False


