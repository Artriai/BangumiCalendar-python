import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from pojo import project, ep


class data:
    def __init__(self, userid) -> None:
        self.userid = userid
        self.preUrl = "Https://api.bgm.tv"
        self.epsUrl = self.preUrl + "/v0/episodes"
        self.projectUrl = self.preUrl + "/v0/users/" + userid + "/collections"
        self.headers = {
            "User-Agent": "Artriai/BangumiCalendar-python(https://github.com/Artriai/BangumiCalendar-python)"
        }
        self.subjects = []
        self.epdict = {}

        # Setup session with retry logic
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def getsubjects(self):
        params = {
            "type": 3,# 表示在看
            "subject_type": 2 # 限定番剧
        }
        page = self.session.get(url=self.projectUrl, headers=self.headers, params=params, timeout=10)
        projects = page.json()["data"]
        for i in projects:
            self.subjects.append(
                project(i["subject"]["name"], i["subject"]["name_cn"], i["subject"]["short_summary"], i["subject_id"]))

    def geteps(self):
        for i in self.subjects:
            temp = []
            params = {
                "subject_id": i.id
            }
            page = self.session.get(url=self.epsUrl, headers=self.headers, params=params, timeout=10)
            eps = page.json()["data"]
            for j in eps:
                temp.append(ep(j["airdate"], j["name"], j["name_cn"], j["ep"]))
            self.epdict[i.id] = temp
