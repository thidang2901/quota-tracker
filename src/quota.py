from time import time, localtime
from utils import read_json, write_to_json


class QuotaTracker(object):
    def __init__(self, filename, dir_path="./", refresh_by="month"):
        self.dir_path = dir_path
        self.filename = filename

        try:
            read_json(f"{self.dir_path}/{self.filename}")
        except FileNotFoundError as e:
            write_to_json(
                _dir=self.dir_path,
                filename=self.filename,
                data={"timestamp": int(time()), "count": 0},
                mode='w'
            )

        self.refresh_by = refresh_by
        self.max_quota = None
        self._check_new_quota()
        self.count = self._load_request_count()

    def set_max_quota(self, max_quota):
        self.max_quota = max_quota

    def exceed_quota(self):
        current_quota = self._load_request_count()
        if current_quota >= self.max_quota:
            return True
        return False

    def _load_request_count(self):
        log = read_json(f"{self.dir_path}/{self.filename}")
        return log["count"]

    def _save_request_count(self):
        log = {"timestamp": int(time()), "count": self.count}
        write_to_json(self.dir_path, self.filename, log)

    def get_count(self):
        return self.count

    def count_request(self, num=1):
        self.count += num
        self._save_request_count()

    def _check_new_quota(self):
        log = read_json(f"{self.dir_path}/{self.filename}")
        log_time = localtime(log["timestamp"])
        now_time = localtime(time())
        if self.refresh_by == "month" and (now_time.tm_mon > log_time.tm_mon) or \
                self.refresh_by == "day" and (now_time.tm_mday > log_time.tm_mday):
            self.count = 0
            self._save_request_count()
