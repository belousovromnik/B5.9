import time

""" кол-во циклов запуска в самой функции"""
CNT_ITER = 10000
""" кол-во первых элементов в последовательности Фибоначчи"""
MAX_ITEM = 150
""" кол-во запусков в декораторе """
NUM_RUNS = 10


def sum_fib(max_item):
    """ вычисление суммы элементов последовательность Фибоначчи,
        max_item - кол-во первых элементов  """
    sum_itog = 0
    item_prev = 0
    item_now = 0
    for i in range(max_item):
        if not item_now:
            item_now = 1
        sum_iter = item_prev + item_now
        item_prev = item_now
        item_now = sum_iter
        sum_itog += sum_iter
    # print(sum_itog)
    return sum_itog


def fib_in_range(cnt_iter, max_item):
    """ запуск вычисления последовательности Фибоначчи в цикле
        cnt_iter - кол-во циклов запуска
        max_item - кол-во первых элементов
        возвращаем сумму сумм каждой итерации   """
    t = 0
    for j in range(cnt_iter):
        t += sum_fib(max_item)
    return t


def decor_def(num_runs):
    """ декоратор-функция """

    def decorator(func):
        def run_func(cnt_iter, max_item):
            avg_time = 0
            for i in range(num_runs):
                t0 = time.time()
                rez = func(cnt_iter, max_item)
                t1 = time.time()
                avg_time_item = t1 - t0
                avg_time += avg_time_item
                print("%s - Выполнение цикла заняло %.5f секунд" % (i, avg_time_item))
            avg_time /= num_runs
            print("Выполнение заняло %.5f секунд" % avg_time)

        return run_func

    return decorator


@decor_def(num_runs=NUM_RUNS)
def decor_def_fib_in_range(cnt_iter, max_item):
    """ оборачиваем исходную функцию в функцию с декоратором
        такое усложнение нужно для того, чтобы одну исходную функцию fib_in_range
        можно было использовать и в примере с декоратором-функцией и с остальными декораторами """
    fib_in_range(cnt_iter, max_item)


class DecorClass:
    def __init__(self, num_runs=10):
        self.num_runs = num_runs

    def __call__(self, fn):
        def new_func(*args):
            avg_time = 0
            for i in range(self.num_runs):
                t0 = time.time()
                fn(*args)
                t1 = time.time()
                avg_time_item = t1 - t0
                avg_time += avg_time_item
                print("%s - Выполнение цикла заняло %.5f секунд" % (i, avg_time_item))
            avg_time /= self.num_runs
            print("Выполнение заняло %.5f секунд" % avg_time)

        return new_func


@DecorClass(num_runs=NUM_RUNS)
def decor_class_fib_in_range(cnt_iter, max_item):
    """ оборачиваем исходную функцию в функцию с декоратором
        такое усложнение нужно для того, чтобы одну исходную функцию fib_in_range
        можно было использовать и в примере с декоратором-функцией и с остальными декораторами """
    fib_in_range(cnt_iter, max_item)


class ContextDecorator(object):
    def __init__(self, num_runs=10):
        self.num_runs = num_runs
        self.start = 0

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        avg_time_item = time.time() - self.start
        print("Кол-во циклов %s" % self.num_runs)
        print("Среднее время выполнения одного цикла заняло %.5f секунд"
              % (avg_time_item / self.num_runs))
        print("Общее время выполнения всех циклов заняло %.5f секунд" % avg_time_item)


print('запуск с применением декоратора-функции')
""" запуск с применением декоратора-функции """
decor_def_fib_in_range(CNT_ITER, MAX_ITEM)

print('запуск с применением декоратора-класса')
""" запуск с применением декоратора-класса """
decor_class_fib_in_range(CNT_ITER, MAX_ITEM)

print('запуск с применением менеджера контекста')
""" запуск с применением менеджера контекста """
with ContextDecorator(NUM_RUNS) as cd:
    for i in range(NUM_RUNS):
        fib_in_range(CNT_ITER, MAX_ITEM)
