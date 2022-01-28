"""
静态点列表库
"""
import math
import numpy as np

np.set_printoptions(suppress=True)


class Utils:
    def array_tran(self, *points, t="list"):
        """
        转换坐标格式
        :param: t:转换类别，默认为list，可选向量vec，或输出单个点points
        """
        out = []
        if type(points[0]) != list and len(points) == 3:
            out = [list(points)]
        elif type(points[0][0]) == list:
            out = points[0]
        else:
            out = list(points)
        if t == "list":
            return out
        if t == "vec":
            return out[0]
        if t == "points":
            return out[0][0], out[0][1], out[0][2]

    def get_distance(self, p1, p2):
        """
        求两点距离
        :param p1: 点1
        :param p2: 点2
        :return: 两点距离
        """
        d = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2) ** 0.5
        return d

    def move(self, points, x, y, z):
        """
        整体移动点列表
        :param points:点列表
        :param x: x方向移动量
        :param y: y方向移动量
        :param z: z方向移动量
        :return: 移动后的点列表
        """
        point_list = []
        for p in points:
            point = [p[0] + x, p[1] + y, p[2] + z]
            point_list.append(point)
        return point_list

    def get_midpoint(self, points_list):
        """
        获取点列中点
        :param points_list: 点列表
        :return: 中点
        """
        x, y, z = 0, 0, 0
        for point in points_list:
            x += point[0]
            y += point[1]
            z += point[2]
        x = x / len(points_list)
        y = y / len(points_list)
        z = z / len(points_list)
        return x, y, z

    def vec_unit(self, p1, p2):
        """
        单位化向量
        :param p1: 向量起点
        :param p2: 向量终点
        :return: 单位化向量
        """
        x1, y1, z1 = p1[0], p1[1], p1[2]
        x2, y2, z2 = p2[0], p2[1], p2[2]
        dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
        d = self.get_distance(p1, p2)
        x, y, z = dx * 1 / d, dy * 1 / d, dz * 1 / d
        return x, y, z

    def rotate(self, u, v, w, a, x, y, z):
        """
        通过旋转矩阵绕单位向量旋转点
        :param u: 旋转轴单位向量 x
        :param v: 旋转轴单位向量 y
        :param w: 旋转轴单位向量 z
        :param a: 角度
        :param x: 被旋转的的点 x
        :param y: 被旋转的的点 y
        :param z: 被旋转的的点 z
        :return: 旋转后的点 x,y,z 坐标
        """
        a = math.radians(a)
        rm = np.array([[math.cos(a) + (1 - math.cos(a)) * u ** 2, (1 - math.cos(a)) * u * v - math.sin(a) * w,
                        (1 - math.cos(a)) * u * w + math.sin(a) * v],
                       [(1 - math.cos(a)) * u * v + math.sin(a) * w, math.cos(a) + (1 - math.cos(a)) * v ** 2,
                        (1 - math.cos(a)) * v * w - math.sin(a) * u],
                       [(1 - math.cos(a)) * u * w - math.sin(a) * v, (1 - math.cos(a)) * w * v + math.sin(a) * u,
                        math.cos(a) + (1 - math.cos(a)) * w ** 2]]
                      )
        pm = np.transpose(np.array([[x, y, z]]))
        fm = np.dot(rm, pm)
        rx, ry, rz = round(fm[0][0], 4), round(fm[1][0], 4), round(fm[2][0], 4)
        return rx, ry, rz

    def rotate_by_vec(self, u1, v1, w1, u2, v2, w2, degree, x, y, z):
        """
        通过旋转矩阵绕任意向量旋转点
        :param u1: 旋转轴向量 x1
        :param v1: 旋转轴向量 y1
        :param w1: 旋转轴向量 z1
        :param u2: 旋转轴向量 x2
        :param v2: 旋转轴向量 y2
        :param w2: 旋转轴向量 z2
        :param degree: 角度
        :param x: 被旋转的的点 x
        :param y: 被旋转的的点 y
        :param z: 被旋转的的点 z
        :return: 旋转后的点 x,y,z 坐标
        """
        uu, uv, uw = self.vec_unit([u1, v1, w1], [u2, v2, w2])
        x1, y1, z1 = x - u1, y - v1, z - w1
        tx, ty, tz = self.rotate(uu, uv, uw, degree, x1, y1, z1)
        rx, ry, rz = tx + u1, ty + v1, tz + w1
        return rx, ry, rz

    def rotate_points_by_vec(self, u1, v1, w1, u2, v2, w2, degree, points):
        r_points = []
        for p in points:
            x, y, z = p[0], p[1], p[2]
            rx, ry, rz = self.rotate_by_vec(u1, v1, w1, u2, v2, w2, degree, x, y, z)
            r_points.append([rx, ry, rz])
        return r_points

    def coordinate_transformation(self, e1, e2, *points, er1=[1, 0, 0], er2=[0, 1, 0], er3=[0, 0, 1]):
        """
        :param e1:基坐标1
        :param e2:基坐标2
        :param points:点
        """
        points = self.array_tran(*points, t="list")
        pr = []
        e1 = self.vec_unit([0, 0, 0], e1)
        e2 = self.vec_unit([0, 0, 0], e2)
        if np.dot(e1, e2) != 0:
            print("Error:坐标构建失败")
            return
        e3 = np.cross(e1, e2)
        A = np.inner([er1, er2, er3], [e1, e2, e3])
        for p in points:
            pr.append(list(np.matmul(A, p)))
        return pr


class Shapes(Utils):
    def __init__(self):
        Utils.__init__(self)

    def line(self, p1, p2, step):
        """
        给出两点生成直线
        :param step: 步长
        :return: 点列表
        """
        points = []
        x, y, z = x1, y1, z1 = p1[0], p1[1], p1[2]
        x2, y2, z2 = p2[0], p2[1], p2[2]
        d = self.get_distance([x1, y1, z1], [x2, y2, z2])
        # 计算需要的粒子数
        count = int(d / step)
        dx = (x2 - x1) / count
        dy = (y2 - y1) / count
        dz = (z2 - z1) / count
        for i in range(0, count + 1):
            points.append([x, y, z])
            x += dx
            y += dy
            z += dz
        return points

    def line_link(self, point_list, step):
        """
        首位相连多个点
        :param point_list: 点列表
        :param step: 步长
        :return: 点列表
        """
        points = []
        for n in range(0, len(point_list)):
            # 到最后一个点时连接第一个点
            if n == len(point_list) - 1:
                x1, y1, z1 = point_list[n][0], point_list[n][1], point_list[n][2]
                x2, y2, z2 = point_list[0][0], point_list[0][1], point_list[0][2]
            else:
                x1, y1, z1 = point_list[n][0], point_list[n][1], point_list[n][2]
                x2, y2, z2 = point_list[n + 1][0], point_list[n + 1][1], point_list[n + 1][2]
            # 函数line会返回一条直线上的所有点，将它添加到points中
            points += self.line([x1, y1, z1], [x2, y2, z2], step)
        return points

    def line_link_one_to_n(self, x, y, z, points_list, step):
        """
        一个点连接多个点
        :param points_list: 点列表
        :param step: 步长
        :return: 点列表
        """
        points = []
        for p in points_list:
            points += self.line([x, y, z], p, step)
        return points

    def solve_parabola(self, x1, x2, x3, y1, y2, y3):
        """
        给出经过三点求抛物线参数
        """
        # 系数矩阵
        coe = np.array([[x1 ** 2, x1, 1], [x2 ** 2, x2, 1], [x3 ** 2, x3, 1]])
        # 结果矩阵
        sol = np.transpose(np.array([[y1, y2, y3]]))
        # 返回系数
        abc = np.linalg.solve(coe, sol)
        a = abc.tolist()[0][0]
        b = abc.tolist()[1][0]
        c = abc.tolist()[2][0]
        return a, b, c

    def get_3rdpoint_parabola(self, x1, y1, z1, x2, y2, z2):
        """
        抛物线求出第三个点
        """
        dy = y2 - y1
        d = self.get_distance([x1, y1, z1], [x2, y2, z2])
        y3 = (y2 * (d - dy) / 2 / d + y1 * (d + dy) / 2 / d + y2 + (d - dy) / 2) / 2
        x3 = x2 * (d - dy) / 2 / d + x1 * (d + dy) / 2 / d
        z3 = z2 * (d - dy) / 2 / d + z1 * (d + dy) / 2 / d
        return x3, y3, z3

    def parabola(self, p1, p2, step):
        """
        给出两点生成竖直平面内抛物线,xz平面内投影疏密均匀
        """

        points = []
        x, y, z = x1, y1, z1 = p1[0], p1[1], p1[2]
        x2, y2, z2 = p2[0], p2[1], p2[2]
        x3, y3, z3 = self.get_3rdpoint_parabola(x1, y1, z1, x2, y2, z2)
        d = self.get_distance([x1, 0, z1], [x2, 0, z2])
        d3 = self.get_distance([x1, 0, z1], [x3, 0, z3])
        count = int(d / step)
        px = 0
        a, b, c = self.solve_parabola(0, d3, d, 0, y3 - y1, y2 - y1)
        dx = (x2 - x1) / count
        dz = (z2 - z1) / count
        for i in range(0, count + 1):
            points.append([x, y, z])
            px += step
            py = a * px ** 2 + b * px + c
            x += dx
            y = y1 + py
            z += dz
        return points

    # 贝塞尔曲线相关
    def bezier3x(self, t, p0, p1, p2, p3):
        """
        三阶贝塞尔曲线方程
        """
        return p0 * (1 - t) ** 3 + 3 * p1 * t * (1 - t) ** 2 + 3 * p2 * t ** 2 * (1 - t) + p3 * t ** 3

    def bezier3x_get_c1(self, i, i_p1, i_n1, a=1 / 4):
        """
        计算控制点1(i, a*((i+1)-(i-1)))
        """
        return i + a * (i_p1 - i_n1)

    def bezier3x_get_c2(self, i_p1, i_p2, i, a=1 / 4):
        """
        计算控制点2(i+1, a*((i+2)-(i)))
        """
        return i_p1 - a * (i_p2 - i)

    def bezier_get_count_list(self, points_list, step):
        """
        计算每两个点间需要的点数
        """
        count_list = []
        for n in range(0, len(points_list) - 1):
            x1, x2 = points_list[n][0], points_list[n + 1][0]
            y1, y2 = points_list[n][1], points_list[n + 1][1]
            z1, z2 = points_list[n][2], points_list[n + 1][2]
            d = self.get_distance([x1, y1, z1], [x2, y2, z2])
            count = int(d / step)
            count_list.append(count)
        return count_list

    def bezier3x_get_points(self, n, p0, p1, p2, p3):
        """
        三阶贝塞尔曲线取点
        """
        t = 0
        b_points = []
        for i in range(1, n + 1):
            point = self.bezier3x(t, p0, p1, p2, p3)
            b_points.append(point)
            t += 1 / n
        return b_points

    def bezier_link(self, points, counts, take=0):
        """
        连接多点
        """
        b_points = []
        if len(points) < 4:
            print('Error: Bezier3x requires at least four points')
        for n in range(0, len(points) - 1):
            # 第一个点与第二个点连接，第n-1个点选第一个点
            if n == 0:
                i = points[n][take]
                i_p1 = points[n + 1][take]
                i_p2 = points[n + 2][take]
                i_n1 = points[0][take]
            # 最后两点连接， 第n+2个点选最后一个
            elif n == len(points) - 2:
                i = points[n][take]
                i_p1 = points[n + 1][take]
                i_p2 = points[-1][take]
                i_n1 = points[n - 1][take]
            else:
                i = points[n][take]
                i_p1 = points[n + 1][take]
                i_p2 = points[n + 2][take]
                i_n1 = points[n - 1][take]
            c1 = self.bezier3x_get_c1(i, i_p1, i_n1)
            c2 = self.bezier3x_get_c2(i_p1, i_p2, i)
            p0 = points[n][take]
            p3 = points[n + 1][take]
            # 每两点间生成点列
            b_point = self.bezier3x_get_points(counts[n], p0, c1, c2, p3)
            b_points.append(b_point)
        return b_points

    def bezier3x_xyz_points(self, points_list, step):
        points_lists = []
        points_temp = []
        counts = self.bezier_get_count_list(points_list, step)
        # 返回值为每两点中的点列表集（每两点中的点作为单独列表，返回这个单独列表的列表
        x_lists = self.bezier_link(points_list, counts, take=0)
        y_lists = self.bezier_link(points_list, counts, take=1)
        z_lists = self.bezier_link(points_list, counts, take=2)
        for x_list, y_list, z_list in zip(x_lists, y_lists, z_lists):
            for x, y, z in zip(x_list, y_list, z_list):
                points_temp.append([x, y, z])
            points_lists.append(points_temp)
            points_temp = []
        # 返回打包为xyz的点列表集
        return points_lists

    def bezier3x_xyz(self, points_list, step):
        """
        给出至少四个点，生成三阶贝塞尔曲线
        """
        points = []
        bezier_lists = self.bezier3x_xyz_points(points_list, step)
        for points_list in bezier_lists:
            # for point in points_list:
            #     points.append(point)
            points += points_list
        return points

    def circle_vec_point(self, x0, y0, z0, r, n, t):
        """
        给出圆心，半径，单位法向量，角度，求空间圆上一点
        :param x0: 圆心x
        :param y0: 圆心y
        :param z0: 圆心z
        :param r: 半径
        :param n: 列表，单位化的法向量
        :param t: 角度
        :return: 点
        """
        n = np.array(n)
        j = np.array([1, 0, 0])
        k = np.array([0, 1, 0])
        a = np.cross(n, j)
        if a.tolist() == [0, 0, 0]:
            a = np.cross(n, k)
        b = np.cross(n, a)
        a1, a2, a3 = self.vec_unit([0, 0, 0], a)
        b1, b2, b3 = self.vec_unit([0, 0, 0], b)
        x = x0 + r * math.cos(t) * a1 + r * math.sin(t) * b1
        y = y0 + r * math.cos(t) * a2 + r * math.sin(t) * b2
        z = z0 + r * math.cos(t) * a3 + r * math.sin(t) * b3
        point = [x, y, z]
        return point

    def circle_vec(self, x0, y0, z0, r, n, step):
        """
        给出圆心，半径，单位法向量，角度，求空间圆
        :param x0: 圆心x
        :param y0: 圆心y
        :param z0: 圆心z
        :param r: 半径
        :param n: 列表，单位化的法向量
        :param step: 步长
        :return: 点列表
        """
        points = []
        d = math.pi * 2 * r
        count = int(d / step)
        for i in range(0, count + 1):
            t = math.radians(360 * (i / count))
            point = self.circle_vec_point(x0, y0, z0, r, n, t)
            points.append(point)
        return points

    def circle(self, x, y, z, r, step):
        """
        给出圆心，半径，生成xz平面上的圆
        :param step: 步长
        :param x: 圆心x
        :param y: 圆心y
        :param z: 圆心z
        :param r: 半径
        :return: 点列表
        """
        points = self.circle_vec(x, y, z, r, [0, 1, 0], step)
        return points

    def ellipse(self, x0, y, z0, a, b, step):
        """
        给出圆心，长轴及短轴长度，生成xz平面椭圆
        :param x0: 圆心x
        :param y: 圆心y
        :param z0: 圆心z
        :param a: 长轴长度
        :param b: 短轴长度
        :param step: 步长
        :return: 点列表
        """
        points = []
        l = 2 * math.pi * b + 4 * (a - b)
        count = int(l / step)
        for i in range(0, count + 1):
            x = x0 + a * math.cos(2 * math.pi * (i / count))
            z = z0 + b * math.sin(2 * math.pi * (i / count))
            points.append([x, y, z])
        return points

    def rectangle(self, x0, y, z0, a, b, step):
        """
        给出一个顶点和长宽，生成xz平面矩形
        :param x0: 顶点x
        :param y: 顶点y
        :param z0: 顶点z
        :param a: 长
        :param b: 宽
        :param step:步长
        :return: 点列表
        """
        points = []
        points += self.line([x0 - (a / 2), y, z0 + (b / 2)], [x0 + (a / 2), y, z0 + (b / 2)], step)
        points += self.line([x0 + (a / 2), y, z0 + (b / 2)], [x0 + (a / 2), y, z0 - (b / 2)], step)
        points += self.line([x0 + (a / 2), y, z0 - (b / 2)], [x0 - (a / 2), y, z0 - (b / 2)], step)
        points += self.line([x0 - (a / 2), y, z0 - (b / 2)], [x0 - (a / 2), y, z0 + (b / 2)], step)
        return points

    def square(self, x0, y, z0, a, step):
        """
        给出顶点，边长，生成xz平面正方形
        """
        points = []
        points += self.rectangle(x0, y, z0, a, a, step)

    def delta(self, x0, y, z0, a, step):
        """给出中心，边长，生成xz平面正三角形"""
        points = []
        r = a / (2 * math.sin(math.pi / 3))
        points += self.line([x0 - a / 2, y, z0 - r * math.sin(math.pi / 6)], [x0, y, z0 + r], step)
        points += self.line([x0, y, z0 + r], [x0 + a / 2, y, z0 - r * math.sin(math.pi / 6)], step)
        points += self.line([x0 + a / 2, y, z0 - r * math.sin(math.pi / 6)], [x0 - a / 2, y,
                                                                              z0 - r * math.sin(math.pi / 6)], step)
        return points

    def polygon_apex(self, x0, y, z0, n, r, step):
        """给出中心，边数，半径，生成xz平面正多边形的各个顶点"""
        apexes = []
        ex_angle = math.radians(360 / n)
        a1 = (x0 - r * math.cos(ex_angle / 2), y, z0 + r * math.sin(ex_angle / 2))
        apexes.append(a1)
        for t in range(1, n):
            ap = self.rotate_by_vec(x0, y, z0, x0, y + 1, z0, t * 360 / n, a1[0], a1[1], a1[2])
            apexes.append(ap)
        return apexes

    def polygon(self, x0, y, z0, n, r, step):
        """给出中心，边数，半径，生成xz平面正多边形"""
        apexes = self.polygon_apex(x0, y, z0, n, r, step)
        points = self.line_link(apexes, step)
        return points

    def regular_pyramid(self, x0, y, z0, n, r, h, step):
        """给出中心，边数，半径，高度，生成底面为正多边形的棱锥"""
        apexes = self.polygon_apex(x0, y, z0, n, r, step)
        points = self.line_link(apexes, step)
        # 棱锥顶点
        ah = (x0, y + h, z0)
        points += self.line_link_one_to_n(ah[0], ah[1], ah[2], apexes, step)
        return points

    def helix(self, p1, p2, r, step, degree=0, path_type='line', custom_points=None, add=True, deg_d=3):
        """
        生成半径不变，轨迹支持自定义的螺线
        :param p1: 点1
        :param p2: 点2
        :param r: 半径
        :param step: 步长
        :param degree: 起始角度
        :param path_type: 螺线轨迹类型，
        内置直线（line），抛物线(parabola)，也可自定义(custom),自定义时需填写custom_points参数为你的点列表
        :param custom_points: 点列表，自定义轨迹时会将此列表中的点作为轨迹
        :param add: 是否附加轨迹点，False时将只返回螺线上的点
        :param deg_d: 螺线旋转速度，单位 度
        :return: 点列表
        """
        x1, y1, z1 = p1[0], p1[1], p1[2]
        x2, y2, z2 = p2[0], p2[1], p2[2]
        points = []
        # 轨迹上的点列表
        lp = []
        if path_type == 'line':
            lp = self.line([x1, y1, z1], [x2, y2, z2], step)
        elif path_type == 'parabola':
            lp = self.parabola([x1, y1, z1], [x2, y2, z2], step)
        elif path_type == 'custom':
            lp = custom_points
        # 绘制圆的点先放这
        cp1 = []
        # 遍历轨迹点列
        for i in range(0, len(lp) - 1):
            # 圆心
            x0, y0, z0 = lp[i][0], lp[i][1], lp[i][2]
            # 圆平面法向量
            n = list(self.vec_unit(lp[i], lp[i + 1]))
            # 用圆心，法向量，半径绘制圆上一点
            cp = self.circle_vec_point(x0, y0, z0, r, n, math.radians(degree))
            cp1.append(cp)
            degree += deg_d
        if add:
            points += lp
        points += cp1
        return points

    def cuboid(self, x0, y0, z0, n1, n2, step, a=1, b=1, c=1):
        """
        生成长方体
        """
        a /= 2
        b /= 2
        c /= 2

        relative_p = []
        relative_p += self.line([a, b, c], [a, b, -c], step)
        relative_p += self.line([a, b, c], [-a, b, c], step)
        relative_p += self.line([-a, b, c], [-a, b, -c], step)
        relative_p += self.line([a, b, -c], [-a, b, -c], step)
        relative_p += self.line([a, b, c], [a, -b, c], step)
        relative_p += self.line([-a, b, c], [-a, -b, c], step)
        relative_p += self.line([a, b, -c], [a, -b, -c], step)
        relative_p += self.line([-a, b, -c], [-a, -b, -c], step)
        relative_p += self.line([a, -b, c], [a, -b, -c], step)
        relative_p += self.line([a, -b, c], [-a, -b, c], step)
        relative_p += self.line([-a, -b, c], [-a, -b, -c], step)
        relative_p += self.line([a, -b, -c], [-a, -b, -c], step)
        p = self.coordinate_transformation(n1, n2, relative_p)
        points = []
        for itm in p:
            points.append(list(np.array([x0, y0, z0] + np.array(itm))))
        return points

    def cube(self, x0, y0, z0, step=0.1, a=1, n1=[1, 0, 0], n2=[0, 1, 0]):
        """
        生成正方体
        :param x0: 中心点
        :param y0: 中心点
        :param z0: 中心点
        :param n1: 一个面的法向量
        :param n2: 另个面的法向量
        :param step:步长
        :param a: 边长 default=1
        :return: 点列表
        """
        return self.cuboid(x0, y0, z0, n1, n2, step, a, a, a)
