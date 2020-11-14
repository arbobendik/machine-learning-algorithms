from numpy import linspace
import matplotlib.pyplot as plt
from prediction_library import Prediction_Library

x = [-21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
y = [98.18, 97.44, 99.6, 99.57, 97.23, 97.65, 97.99, 97.69, 98.32, 105.4, 102.46, 102.54, 102.9, 102.64, 100.2, 100.4, 98.58, 98, 96.9, 96.65, 98.41, 95.99, 99.28, 93.06, 92.5, 94, 97.82, 100.3, 100.08, 101.26, 99.48, 101.4, 100.58]
desired_value_in_work_days = 1

for i in range(0, desired_value_in_work_days):
    len_d = len(x)-5
    len_m = len(x)-21
    len_t = len(x)-120

    dx = x[len_d:]
    dy = y[len_d:]

    mx = x[len_m:]
    my = y[len_m:]

    tx = x[len_t:]
    ty = y[len_t:]

    xp = len(x)-21

    pm_d = Prediction_Library(dx, dy)
    reg_d = pm_d.get_regression()
    pat_d = pm_d.get_pattern(reg_d)
    d_yp_info = pm_d.predict(reg_d, pat_d, xp)
    d_yp = d_yp_info[1]

    pm_m = Prediction_Library(mx, my)
    reg_m = pm_m.get_regression()
    pat_m = pm_m.get_pattern(reg_m)
    m_yp_info = pm_m.predict(reg_m, pat_m, xp)
    m_yp = m_yp_info[1]

    pm_t = Prediction_Library(tx, ty)
    reg_t = pm_t.get_regression()
    pat_t = pm_t.get_pattern(reg_t)
    t_yp_info = pm_d.predict(reg_t, pat_t, xp)
    t_yp = t_yp_info[1]

    minimum = min(tx)
    maximum = max(tx)
    # get x width
    m_x = linspace(xp+1, xp-len(x), 5000)
    d_x = linspace(xp+1, xp-0.5*len(x), 5000)
    t_x = linspace(xp+1, xp-len(x), 5000)
    # set formulas
    d = [reg_d.formula(d) for d in d_x]
    m = [reg_m.formula(m) for m in m_x]
    t = [reg_t.formula(t) for t in t_x]

    # draw points
    dx.append(xp)
    mx.append(xp)
    tx.append(xp)
    res = (m_yp+d_yp+t_yp)/3
    px = tx
    py = ty+[res]
    dy.append(d_yp)
    my.append(m_yp)
    ty.append(t_yp)
    x.append(xp)
    y.append(res)

    if i == desired_value_in_work_days-1:
        print(reg_d.factors)
        print(reg_m.factors)
        print(reg_t.factors)
        # draw lines once in the last cycle
        plt.plot(d_x, d)
        plt.plot(m_x, m)
        plt.plot(t_x, t)
        plt.scatter(xp, d_yp)
        plt.scatter(xp, m_yp)
        plt.scatter(xp, t_yp)
        plt.scatter(xp, res)
        plt.plot(dx, dy)
        plt.plot(mx, my)
        plt.plot(tx, ty)
        plt.plot(px, py)
        print((m_yp + d_yp + t_yp) / 3)
        # show window
test = 3
x = x[:(len(x)-test-desired_value_in_work_days)]
y = y[:(len(y)-test-desired_value_in_work_days)]
desired_value_in_work_days += test
for i in range(0, desired_value_in_work_days):
    len_d = len(x)-5
    len_m = len(x)-21
    len_t = len(x)-120

    dx = x[len_d:]
    dy = y[len_d:]

    mx = x[len_m:]
    my = y[len_m:]

    tx = x[len_t:]
    ty = y[len_t:]

    xp = len(x)-21

    pm_d = Prediction_Library(dx, dy)
    reg_d = pm_d.get_regression()
    pat_d = pm_d.get_pattern(reg_d)
    d_yp_info = pm_d.predict(reg_d, pat_d, xp)
    d_yp = d_yp_info[1]

    pm_m = Prediction_Library(mx, my)
    reg_m = pm_m.get_regression()
    pat_m = pm_m.get_pattern(reg_m)
    m_yp_info = pm_m.predict(reg_m, pat_m, xp)
    m_yp = m_yp_info[1]

    pm_t = Prediction_Library(tx, ty)
    reg_t = pm_t.get_regression()
    pat_t = pm_t.get_pattern(reg_t)
    t_yp_info = pm_d.predict(reg_t, pat_t, xp)
    t_yp = t_yp_info[1]

    minimum = min(tx)
    maximum = max(tx)
    # get x width
    m_x = linspace(xp+1, xp-len(x), 5000)
    d_x = linspace(xp+1, xp-0.1*len(x), 5000)
    t_x = linspace(xp+1, xp-len(x), 5000)
    # set formulas
    d = [reg_d.formula(d) for d in d_x]
    m = [reg_m.formula(m) for m in m_x]
    t = [reg_t.formula(t) for t in t_x]

    # draw points
    dx.append(xp)
    mx.append(xp)
    tx.append(xp)
    res = (m_yp+d_yp+t_yp)/3
    px = tx
    py = ty+[res]
    dy.append(d_yp)
    my.append(m_yp)
    ty.append(t_yp)
    x.append(xp)
    y.append(res)

    if i == desired_value_in_work_days-1:
        print(reg_d.factors)
        print(reg_m.factors)
        print(reg_t.factors)
        # draw lines once in the last cycle
        plt.plot(d_x, d)
        plt.plot(m_x, m)
        plt.plot(t_x, t)
        plt.scatter(xp, d_yp)
        plt.scatter(xp, m_yp)
        plt.scatter(xp, t_yp)
        plt.scatter(xp, res)
        plt.plot(dx, dy)
        plt.plot(mx, my)
        plt.plot(tx, ty)
        plt.plot(px, py)
        print((m_yp + d_yp + t_yp) / 3)
plt.show()
