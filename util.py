from threading import Lock


class LockedSet(object):

    def __init__(self):
        self.set = set()
        self.lock = Lock()

    def __contains__(self, obj):
        with self.lock:
            return obj in self.set

    def insert_if_not_contains(self, obj):
        with self.lock:
            if obj not in self.set:
                self.set.add(obj)
                return True

            return False

    def __len__(self):
        with self.lock:
            return len(self.set)
