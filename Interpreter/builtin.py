
class Builtins(object):

    def __init__(self):
        self.names = {
            'print': self.print_func,
            'max': self.max_func,
            'min': self.min_func
        }

    def call(self, name, visited_params):
        return self.names[name](visited_params)

    def print_func(self, visited_params):
        for idx, par in enumerate(visited_params):
            if len(visited_params) > 1:
                if idx == len(visited_params) - 1:
                    ret = print(par, end='')
                else:
                    print(par, end=' ')
            else:
                ret = print(par)
        if len(visited_params) > 1:
            print()

        return ret

    def max_func(self, visited_params):
        if type(visited_params[0]) is list:
            return max(visited_params[0])
        m = visited_params[0]
        for par in visited_params:
            if m < par:
                m = par
        return m

    def min_func(self, visited_params):
        if type(visited_params[0]) is list:
            return min(visited_params[0])
        m = visited_params[0]
        for par in visited_params:
            if m > par:
                m = par
        return m

    def sum_func(self, visited_params):
        if type(visited_params[0]) is list:
            return sum(visited_params[0])
        sum = 0
        for par in visited_params:
            sum += par
        return sum

    def int_func(self, visited_params):
        if len(visited_params) == 1:
            return int(visited_params[0])

    def str_func(self, visited_params):
        if len(visited_params) == 1:
            return str(visited_params[0])

    def exit_func(self, visited_params):
        exit()

    def abs(self, visited_params):
        if len(visited_params) == 1:
            return abs(visited_params[0])

    def input(self, visited_params):
        return input(visited_params[0])
