class FakeScribbler(object):
    value = "something"

    def __init__(self, name, out_dir):
        self.name = name
        self.out_dir = out_dir


class FakeScribblerArgs(object):
    def __init__(self, name, out_dir, an_int, a_str, **other_args):
        self.name = name
        self.out_dir = out_dir
        self.an_int = an_int
        self.a_str = a_str
        self.other_args = other_args
