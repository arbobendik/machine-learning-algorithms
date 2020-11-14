# This class was created by Bendik Arbogast at the 17.10.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
from regression import Regression
from typing import Callable


class Regression_Library:
    xs: list = []
    ys: list = []

    def __init__(self, x_values, y_values):
        self.xs = x_values
        self.ys = y_values

    def get_flat(self) -> Regression:
        try:
            xs = self.xs
            ys = self.ys
            a = sum(ys) / len(ys)
            # get residuals
            res = [y - a for y in ys]
            # calculate precision
            if max(xs) - min(xs) == 0:
                precision = 0.0
            else:
                precision = 1 / (sum([abs(r) for r in res]) / (max(xs) - min(xs)) + 1)
            formula: Callable[[float], float] = lambda x: a
            standard_deviation = (sum([r ** 2 for r in res]) / len(res)) ** 0.5
            # return everything in the form of a Regression_Object
            return Regression([a], res, formula, standard_deviation, precision)
        except ZeroDivisionError:
            return Regression([0], [0], lambda x: 0, 0.0, 0.0)

    def get_linear(self) -> Regression:
        try:
            # get global variables
            xs = self.xs
            ys = self.ys
            # the algorithm uses the linear formula f(x) = ax + b
            # and the linear regression formula:
            #
            #                      n         _         _
            #                      E   (x  - x) * (y  -y)
            #                     i=1    i          i
            #               a = ________________________________
            #                           n          _  2
            #                           E    (x  - x)
            #                          i=1     i
            #
            #                    _       _
            #               b =  y - a * x
            #
            #
            #               _     _
            # ax and ay are x and y and the average value of xs and ys
            ax = sum(xs) / len(xs)
            ay = sum(ys) / len(ys)
            # calculates a with the regression formula for a
            a = sum(list(map(lambda x, y: (x - ax)*(y - ay), xs, ys))) / sum([(x - ax)**2 for x in xs])
            # calculates b with the regression formula for b out of a
            b = ay - a * ax
            # get x and y coordinates of the interceptions between th regression line
            # and a corresponding orthogonal for each point in (xs | ys)
            ixs: list = list(map(lambda x, y: (x / a + y - b) / (a + 1 / a), xs, ys))
            iys: list = [a * x + b for x in ixs]
            # get the total deviation of all points from the regression line
            td = sum(list(map(lambda x, y, xi, yi: ((x - xi) ** 2 + (y - yi) ** 2) ** 0.5, xs, ys, ixs, iys)))
            # calculate the distance between the first and last orthogonal interception
            # with the regression line as a factor of scale
            mx = [min(ixs), max(ixs)]
            my = [a * x + b for x in mx]
            sf = ((mx[0] - mx[1]) ** 2 + (my[0] - my[1]) ** 2)**0.5
            # calculate precision where 1 is perfectly accurate and 0 the unreachable maximum of inaccuracy
            precision = 1 / (td / sf + 1)
            # get residuals
            res = list(map(lambda x, y: y - (a*x + b), xs, ys))
            # return everything in the form of a Regression_Object
            formula: Callable[[float], float] = lambda x: a*x + b
            standard_deviation = (sum([r ** 2 for r in res]) / len(res)) ** 0.5
            return Regression([b, a], res, formula, standard_deviation, precision)
        except ZeroDivisionError:
            return Regression([0], [0], lambda x: 0, 0.0, 0.0)

    def get_quadratic(self) -> Regression:
        try:
            # get global variables
            xs = self.xs
            ys = self.ys
            # the algorithm uses the quadratic formula f(x) = ax^2 + bx + c
            # and the quadratic regression formula:
            #
            #                       ______    _ _        ____   _2      ___   _   _       ____   _   ____
            #                     ( y*x**x  - y*x  ) * ( x**2 - x ) - ( y*x - y * x ) * ( x**3 - x * x**2 )
            #               a =  ___________________________________________________________________________
            #                               ____   ____2      ____    _2      ____   _   ____  2
            #                             ( x**4 - x**2 ) * ( x**2  - x ) - ( x**3 - x * x**2 )
            #
            #
            #                      ___   _   _         ____   _   ____
            #                      y*x - y * x - a * ( x**3 - x * x**2 )
            #               b =  _________________________________________
            #                                 ____   _2
            #                                 x**2 - x
            #
            #
            #                     _       ____       _
            #               c =   y - a * x**2 - b * x
            #
            #
            #               _     _
            # ax and ay are x and y and the average value of xs and ys
            ax = sum(xs) / len(xs)
            ay = sum(ys) / len(ys)
            #        ___
            # ayx is y*x and the average value of xs*ys
            ayx = sum(list(map(lambda x, y: x*y, xs, ys))) / len(xs)
            a2x = sum([x**2 for x in xs]) / len(xs)
            a3x = sum([x**3 for x in xs]) / len(xs)
            a4x = sum([x**4 for x in xs]) / len(xs)
            ay2x = sum(list(map(lambda x, y: y*x**2, xs, ys))) / len(xs)
            # calculates a with the regression formula for a
            a = ((ay2x-ay*a2x)*(a2x-ax**2)-(ayx-ay*ax)*(a3x-ax*a2x)) / ((a4x-a2x**2)*(a2x-ax**2)-(a3x-ax*a2x)**2)
            # calculates b with the regression formula for b with a
            b = (ayx-ay*ax-a*(a3x-ax*a2x))/(a2x-ax**2)
            # calculates c with the regression formula for c with a and b
            c = ay-a*a2x-b*ax
            # the shortest distance between each point and f(x)
            process_shortest_distance = self.__quadratic_process_shortest_distance(a, b, c)
            sd_and_xv = list(map(process_shortest_distance, xs, ys))
            # get x-values of the interceptions
            ixs = [xv[1] for xv in sd_and_xv]
            # get total deviation of all points from f(x)
            td = sum([sd[0] for sd in sd_and_xv])
            # calculate the distance of f(x) between the first and last orthogonal interception
            # with the regression curve as a scale factor
            mi = min(ixs)
            # process the curve length between lowest and highest x-value of the interception points (scale factor)
            clx = [mi + (i + 1) * ((max(ixs) - mi) / 512) for i in range(0, 512)]
            cly = [a * x**2 + b * x + c for x in clx]
            clx1 = clx[0:]
            cly1 = cly[0:]
            clx1.insert(0, 0)
            cly1.insert(0, 0)
            # get scale factor
            sf = sum(list(map(lambda x, y, x1, y1: ((x-x1)**2+(y-y1)**2)**0.5 if x1 != 0 else 0, clx, cly, clx1, cly1)))
            # calculate precision where 1 is perfectly accurate and 0 the unreachable maximum of inaccuracy
            precision = 1 / (td / sf + 1)
            # get residuals
            res = list(map(lambda x, y: y - (a * x**2 + b * x + c), xs, ys))
            # return everything in the form of [max_exponent, precision, residuals, factors[i] = [factors of x**i]]
            formula: Callable[[float], float] = lambda x: a * x**2 + b * x + c
            standard_deviation = (sum([r ** 2 for r in res]) / len(res)) ** 0.5
            return Regression([c, b, a], res, formula, standard_deviation, precision)
        except ZeroDivisionError:
            return Regression([0], [0], lambda x: 0, 0.0, 0.0)

    @staticmethod
    def __quadratic_process_shortest_distance(a, b, c) -> Callable[[float, float], list]:
        def __quadratic_process_this_shortest_distance(x, y) -> list:
            # calculate the x-spectrum where the interception of the orthogonal of f(x) through each point could be
            # the interception point lays on f(x) between the points x value and xi
            if (a > 0 and origin_y > y) or (a < 0 and origin_y < y):
                xi = origin_x
            else:
                x1 = (- b + (b ** 2 - 4 * a * (c - y)) ** 0.5) / (2 * a)
                x2 = (- b - (b ** 2 - 4 * a * (c - y)) ** 0.5) / (2 * a)
                if abs(x - x1) < abs(x - x2):
                    xi = x1
                else:
                    xi = x2
            # calculate the corresponding y value for x on f(x), the variable a represents the points y value
            yi = a * x**2 + b * x + c
            if x > xi:
                dist = [xi, y, x, yi, abs(x - xi), abs(y - yi)]
            else:
                dist = [x, yi, xi, y, abs(xi - x), abs(yi - y)]
            # get approximately x value on f(x) with the shortest distance to the point
            # by recursively halving the x-spectrum and reusing the shorter half
            for i in range(0, 32):
                mix = (dist[2] + dist[0]) / 2
                miy = a * mix**2 + b * mix + c
                if (dist[4] > dist[5] and x > xi) or (dist[5] > dist[4] and xi > x):
                    dist[0] = mix
                    dist[1] = miy
                else:
                    dist[2] = mix
                    dist[3] = miy
            # get shortest distance out of the calculated x value and return it
            return [((x - dist[0]) ** 2 + (y - dist[1]) ** 2)**0.5, dist[0]]
        # find origin of regression parabola with it's derivative f'(x) = 0
        origin_x = -b / (2 * a)
        origin_y = a * origin_x ** 2 + b * origin_x + c
        # return function __quadratic_process_this_shortest_distance to be used in map()
        return __quadratic_process_this_shortest_distance
