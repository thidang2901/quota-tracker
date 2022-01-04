class QuotaOptions(object):
    def __init__(
            self,
            start_quota: int = 0,
            refresh_by: str = "month",
            warning_rate: float = 0.8
    ):
        self.start_quota = start_quota
        self.refresh_by = refresh_by
        self.warning_rate = warning_rate
