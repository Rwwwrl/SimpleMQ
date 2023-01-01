from .follower import Follower


class ConnectionToFollowerHasLost(BaseException):
    def __init__(self, *args, follower: Follower, **kwargs):
        super().__init__(*args, **kwargs)
        self.follower = follower
