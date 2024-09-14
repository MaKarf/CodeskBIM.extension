class Hello:
    my_list = []

    def __init__(self):
        # self.my_list = []
        pass

    def set_list(self):
        m = [i for i in range(10)]
        # print m
        self.my_list = m


mk = Hello()
mk.set_list()
ny = mk.my_list

print ny

