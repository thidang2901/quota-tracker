import logging
from time import time, localtime
from utils import read_json, write_to_json

from options import QuotaOptions


class QuotaTracker(object):
    def __init__(self,
                 filename: str,
                 max_quota: int,
                 dir_path: str = "./",
                 options: QuotaOptions = QuotaOptions(),
                 logger=None):

        if not logger:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger('QuotaTracker')
        else:
            self.logger = logger

        self.options = options
        self.dir_path = dir_path
        self.filename = filename
        try:
            read_json(f"{self.dir_path}/{self.filename}")
        except FileNotFoundError:
            write_to_json(
                _dir=self.dir_path,
                filename=self.filename,
                data={"timestamp": int(time()), "count": 0},
                mode='w'
            )

        self._refresh_quota()
        self.count = self._load_count()
        self.max_quota = max_quota
        self.exceed_quota = False

    def is_exceeded_quota(self):
        current_quota = self._load_count()
        if current_quota >= self.max_quota:
            return True
        return False

    def _load_count(self):
        log = read_json(f"{self.dir_path}/{self.filename}")
        return log["count"]

    def _save_count(self):
        log = {"timestamp": int(time()), "count": self.count}
        write_to_json(self.dir_path, self.filename, log)

    def get_count(self):
        return self.count

    def count_request(self, num=1):
        self.count += num
        self._save_count()

    def _refresh_quota(self):
        log = read_json(f"{self.dir_path}/{self.filename}")
        log_time = localtime(log["timestamp"])
        now_time = localtime(time())
        if self.options.refresh_by == "month" and (now_time.tm_mon > log_time.tm_mon) or \
                self.options.refresh_by == "day" and (now_time.tm_mday > log_time.tm_mday):
            self.count = 0
            self._save_count()

    def validate_quota(self):
        if self.get_count() < self.options.warning_rate * float(self.max_quota):
            self.logger.info("QuotaStatus: OK")
        elif self.get_count() <= self.max_quota:
            self.logger.info(f"QuotaStatus: WARNING - Exceeded {self.options.warning_rate * 100}% of quota requests")
        else:
            self.logger.info(f"QuotaStatus: STOPPING - Exceeded 100% of quota requests")
            self.exceed_quota = True
        return self.exceed_quota

    def show_quota(self):
        self.logger.info(f'CurrentQuota: {self.get_count()}/{self.max_quota}')
