import points as pt
from PIL import Image


class Command:
    def __init__(self, tick, name, x, y, z, dx, dy, dz, speed, amount, mode='force'):
        self.tick = tick
        self.name = name
        self.x = round(x, 2)
        self.y = round(y, 2)
        self.z = round(z, 2)
        self.dx = round(dx, 2)
        self.dy = round(dy, 2)
        self.dz = round(dz, 2)
        self.speed = speed
        self.amount = amount
        self.mode = mode

    def __str__(self):
        text = 'particle %s %s %s %s %s %s %s %s %s %s' \
               % (self.name, self.x, self.y, self.z, self.dx, self.dy, self.dz, self.speed, self.amount, self.mode)
        return text


class CmdBuilder:
    def __init__(self):
        self.cmds = []
        self.temp_cmds = []

    def cls(self):
        self.cmds = []

    def average_cmd_count(self, count, t0, t1, fun):
        """计算每tick指令数"""
        count_list = []
        tick = int(t1 - t0 + 1)
        if fun:
            sum = 0
            for t in range(t0, t1 + 1):
                n = fun(t)
                count_list.append(n * count)
                sum += n
            for t in range(0, tick):
                count_list[t] //= sum

        else:
            # 整除计算每tick需要的数量
            i = count // tick
            # 计算余数，之后平均插入
            r = count % tick
            for n in range(0, tick):
                count_list.append(i)
            # 将余下的点平均插入
            for n in range(0, int(r)):
                if round(tick / r) * n < len(count_list):
                    count_list[round(tick / r) * n] += 1
        return count_list

    def cmds_to_seq(self, t0, t1, fun=None):
        """
        将指令列表转为t0-t1 Tick的序列并添加到总列表中
        :param t0: 起始刻
        :param t1: 结束刻
        :param cmds: 指令列表
        :return: None
        """
        cmds = self.temp_cmds
        if t0 == t1:
            for cmd in cmds:
                cmd.tick = t0
                self.cmds.append(cmd)
        else:
            count_list = self.average_cmd_count(len(cmds), t0, t1, fun)
            # 按每tick粒子数量切片列表
            index1, index2 = 0, 0
            for i, c in enumerate(count_list):
                index2 += c
                for cmd in cmds[index1:index2]:
                    cmd.tick = t0 + i
                    self.cmds.append(cmd)
                index1 = index2
        self.temp_cmds = []

    def static_particle(self, t0, t1, points, name, dx, dy, dz, speed, amount):
        """生成普通粒子序列"""
        self.temp_cmds = []
        for p in points:
            cmd = Command(t0, name, p[0], p[1], p[2], dx, dy, dz, speed, amount)
            self.temp_cmds.append(cmd)
        self.cmds_to_seq(t0, t1)

    def motion_particle(self, points, motions, t0, t1, name, speed):
        """生成带初速度的粒子序列，每个粒子具有指定初速度"""
        self.temp_cmds = []
        for p, m in zip(points, motions):
            x, y, z = p[0], p[1], p[2]
            dx, dy, dz = m[0], m[1], m[2]
            cmd = Command(t0, name, x, y, z, dx, dy, dz, speed, 0)
            self.temp_cmds.append(cmd)
        self.cmds_to_seq(t0, t1)

    def motion_move(self, points_1, points_2, t0, t1, name, speed, zoom=11):
        """生成粒子移动动画"""
        motions = []
        for p1, p2 in zip(points_1, points_2):
            motion = [(p2[0] - p1[0]) / zoom, (p2[1] - p1[1]) / zoom, (p2[2] - p1[2]) / zoom]
            motions.append(motion)
        self.motion_particle(points_1, motions, t0, t1, name, speed)

    def motion_spread_from_point(self, points, x, y, z, t0, t1, name, speed, zoom=11):
        """生成粒子扩散动画"""
        motions = []
        for point in points:
            motions.append([((point[0] - x) / zoom), ((point[1] - y) / zoom), ((point[2] - z) / zoom)])
        self.motion_particle([x, y, z] * len(motions), motions, t0, t1, name, speed)

    def motion_centre_spread(self, points, t0, t1, name, speed, zoom=11):
        """生成粒子中心扩散动画"""
        pu = pt.Utils()
        x, y, z = pu.get_midpoint(points)
        self.motion_spread_from_point(points, x, y, z, t0, t1, name, speed, zoom)

    def motion_shrink_to_point(self, points, x, y, z, t0, t1, name, speed, zoom=11):
        """生成粒子收缩动画"""
        motions = []
        for point in points:
            motions.append([((x - point[0]) / zoom), ((y - point[1]) / zoom), ((z - point[2]) / zoom)])
        self.motion_particle(points, motions, t0, t1, name, speed)

    def motion_centre_shrink(self, points, t0, t1, name, speed, zoom=11):
        """生成粒子中心收缩动画"""
        pu = pt.Utils()
        x, y, z = pu.get_midpoint(points)
        self.motion_shrink_to_point(points, x, y, z, t0, t1, name, speed, zoom)

    def particle_img(self, filename, x0, y0, z0, zoom_level, t0, t1, particle_name):
        """
        生成粒子画，仅读取黑色像素点
        :param filename: images文件下的图片名（注意带后缀）
        :param x0: 图片左上角坐标 x
        :param y0: 图片左上角坐标 y
        :param z0: 图片左上角坐标 z
        :param zoom_level: 缩放级别，整数（推荐5）
        :param t0: 起始Tick
        :param t1: 结束Tick
        :param particle_name: 粒子名
        :return: None
        """
        points = []
        im = Image.open(f'./images/{filename}')
        width, height = im.size[0], im.size[1]
        for w in range(0, width):
            for h in range(0, height):
                imgdata = (im.getpixel((w, h)))
                if imgdata == (0, 0, 0):
                    x = x0 + w / zoom_level
                    y = y0 - h / zoom_level
                    z = z0
                    points.append([x, y, z])
        self.static_particle(t0, t1, points, particle_name, 0, 0, 0, 0, 1)

    def color_particle_img(self, filename, x0, y0, z0, t0, t1, particle_size, zoom_level=7,
                           is_rotate=False, vec1=None, vec2=None, degree=None):
        """
        生成彩色粒子画（1.13+）
        :param filename: 带后缀的图片文件名
        :param x0: 图片左上角坐标 x
        :param y0: 图片左上角坐标 y
        :param z0: 图片左上角坐标 z
        :param t0: 起始Tick
        :param t1: 结束Tick
        :param particle_size: 粒子大小
        :param zoom_level: 缩放级别，整数（推荐7）
        :param is_rotate: 是否旋转
        :param vec1: 旋转轴起点
        :param vec2: 旋转轴终点
        :param degree: 旋转角度
        :return: None
        """
        # particle minecraft:dust 1 1 1 1 ~ ~ ~ 0 0 0 0 1
        self.temp_cmds = []
        pu = pt.Utils()
        im = Image.open(f'./images/{filename}')
        width, height = im.size[0], im.size[1]
        for w in range(0, width):
            for h in range(0, height):
                imgdata = (im.getpixel((w, h)))
                r, g, b = imgdata[0], imgdata[1], imgdata[2]
                name = f'dust {round(r / 255, 4)} {round(g / 255, 4)} {round(b / 255, 4)} {particle_size}'
                x = x0 + w / zoom_level
                y = y0 - h / zoom_level
                z = z0
                if is_rotate:
                    u1, v1, w1 = vec1[0], vec1[1], vec1[2]
                    u2, v2, w2 = vec2[0], vec2[1], vec2[2]
                    rx, ry, rz = pu.rotate_by_vec(u1, v1, w1, u2, v2, w2, degree, x, y, z)
                    cmd = Command(t0, name, rx, ry, rz, 0, 0, 0, 0, 1)
                    self.temp_cmds.append(cmd)
                else:
                    cmd = Command(t0, name, x, y, z, 0, 0, 0, 0, 1)
                    self.temp_cmds.append(cmd)
        self.cmds_to_seq(t0, t1)

    def cmds_fun(self, t0, t1, fun, name, dx, dy, dz, speed, amount, ppt=3, frags=None):
        """
        以参数方程形式生成命令
        :param t0:起始tick
        :param t1:终止tick
        :param fun:坐标函数，参数格式为（t，*frags），返回值为[p1,p2,p3……]或x,y,z或[x,y,z]
        :param frags:需要传入fun的参数，用元组表示，如fun的参数为（t,a,b,c），则frags=（a,b,c）
        :param ppt:每tick点数,default:3
        """
        pu = pt.Utils()
        dt = 1 / ppt
        for tick in range(t0, t1):
            for i in range(ppt):
                if not frags:
                    points = pu.array_tran(fun(tick + i * dt))
                else:
                    points = pu.array_tran(fun(tick + i * dt, *frags))
                for p in points:
                    cmd = Command(tick, name, p[0], p[1], p[2], dx, dy, dz, speed, amount)
                    self.cmds.append(cmd)

    def static_particle_fun(self, t0, t1, points, name, dx, dy, dz, speed, amount, fun):
        """
        生成普通粒子序列,时间的浓度方程版
        :param fun:时间浓度方程，参数为t，返回值为t时刻轨迹速度
        """
        self.temp_cmds = []
        for p in points:
            cmd = Command(t0, name, p[0], p[1], p[2], dx, dy, dz, speed, amount)
            self.temp_cmds.append(cmd)
        self.cmds_to_seq(t0, t1, fun)
