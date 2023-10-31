import generate
import time
import main


class test_class(object):

    def __init__(self, name, time_limit, test_method, evaluate):
        self.name = name
        self.time_limit = time_limit
        self.test_method = test_method
        self.time_count = 0
        self.pass_count = 0
        self.evaluate = evaluate

    def test(self, state):
        base = time.time()
        ans = self.test_method(state,
                               evaluate=self.evaluate,
                               time_limit=self.time_limit)
        used = time.time() - base
        if used < time_limit:
            self.time_count += used
            self.pass_count += 1
            return ans, used
        else:
            self.time_count += time_limit
            return -1, -1.0

    def count(self):
        return self.time_count, self.pass_count


if __name__ == '__main__':
    pass_count = 0
    time_count = 0
    n = int(input('Test number: '))
    time_limit = float(input('Time limit(s): '))

    methods = [
        test_class('A*   with weighted manhattan', time_limit, main.A_star,
                   main.evaluate),
        test_class('A*   with euclid', time_limit, main.A_star,
                   main.evaluate_euclid),
        test_class('A*   with manhattan', time_limit, main.A_star,
                   main.evaluate_manhattan),
        test_class('IDA* with weighted manhattan', time_limit, main.IDA_star,
                   main.evaluate),
        test_class('IDA* with euclid', time_limit, main.IDA_star,
                   main.evaluate_euclid),
        test_class('IDA* with manhattan', time_limit, main.IDA_star,
                   main.evaluate_manhattan),
    ]

    for test in range(n):
        state, expectation = generate.generate(step_limit=200)

        for method in methods:
            ans, used = method.test(state)
            if used == -1:
                str = ("Test %-4d    %-4d Timeout     " + method.name) % (test,
                                                                          ans)
            else:
                str = ("Test %-4d    %-4d %-10f  " + method.name) % (test, ans,
                                                                     used)
            print(str)

        print('')

    for method in methods:
        time_count, pass_count = method.count()
        str = ('Average Time = %-10f Pass Rate = %-10f  ' +
               method.name) % (time_count / n, pass_count / n)
        print(str)
