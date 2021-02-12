from notification_config import NotificationConfig

class Bar(object):

    _bar = 1
    def __init__(self, val):
        self._bar =val

    @classproperty
    def bar(self):
        return self._bar


# test instance instantiation
foo = Bar(1)
assert foo.bar == 1
print(foo.bar)
print(foo.bar == 1)

baz = Bar(1)
assert baz.bar == 1
print(baz.bar )
print(baz.bar == 1)

