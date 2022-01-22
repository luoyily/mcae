import points as pt


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

    def average_cmd_count(self, count, tick):
        """计算平均每tick指令数"""
        count_list = []
        # 整除计算每tick需要的数量
        i = count // tick
        # 计算余数，之后平均插入
        r = count % tick
        for n in range(0, tick):
            count_list.append(i)
        # 将余下的点平均插入
        for n in range(0, int(r)):
            if round(tick / r) * n < len(count_list):
                count_list[round(tick / r) * n] = count_list[round(tick / r) * n] + 1
        return count_list

    def cmds_to_seq(self, t0, t1, cmds):
        """
        将指令列表转为t0-t1 Tick的序列并添加到总列表中
        :param t0: 起始刻
        :param t1: 结束刻
        :param cmds: 指令列表
        :return: None
        """
        if t0 == t1:
            for cmd in cmds:
                cmd.tick = t0
                self.cmds.append(cmd)
        else:
            count_list = self.average_cmd_count(len(cmds), int(t1-t0+1))
            # 按每tick粒子数量切片列表
            index1, index2 = 0, 0
            for i, c in enumerate(count_list):
                index2 += c
                for cmd in cmds[index1:index2]:
                    cmd.tick = t0 + i
                    self.cmds.append(cmd)
                index1 = index2

    def static_particle(self, t0, t1, points, name, dx, dy, dz, speed, amount):
        """生成普通粒子序列"""
        self.temp_cmds = []
        for p in points:
            x, y, z = p[0], p[1], p[2]
            cmd = Command(t0, name, x, y, z, dx, dy, dz, speed, amount)
            self.temp_cmds.append(cmd)
        self.cmds_to_seq(t0, t1, self.temp_cmds)

    def motion_particle(self, points, motions, t0, t1, name, speed):
        """生成带初速度的粒子序列，每个粒子具有指定初速度"""
        self.temp_cmds = []
        for p, m in zip(points, motions):
            x, y, z = p[0], p[1], p[2]
            dx, dy, dz = m[0], m[1], m[2]
            cmd = Command(t0, name, x, y, z, dx, dy, dz, speed, 0)
            self.temp_cmds.append(cmd)
        self.cmds_to_seq(t0, t1, self.temp_cmds)

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
        self.motion_particle([x, y, z]*len(motions), motions, t0, t1, name, speed)

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

    def color_particle_img(self, points, color, size, t0, t1):
        """生成彩色粒子画（1.13+）"""
        # particle minecraft:dust 1 1 1 1 ~ ~ ~ 0 0 0 0 1
        # self.temp_cmds = []
        # for p, c in zip(points, color):
        #     name = 'dust '
        #     x, y, z = p[0], p[1], p[2]
        #     dx, dy, dz = c[0], c[1], c[2]
        #     cmd = Command(t0, name, x, y, z, dx, dy, dz, 0, 1)
        #     self.temp_cmds.append(cmd)
        # self.cmds_to_seq(t0, t1, self.temp_cmds)





