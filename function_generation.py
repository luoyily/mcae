import os
import setblock


class Function:
    def __init__(self):
        self.cmds_list = []
        self.index = 0

    def get_seq_duration(self, cmds):
        """
        获取命令列表最大持续时长
        :param cmds: 命令列表
        :return: 最大Tick
        """
        tick = 0
        for cmd in cmds:
            if cmd.tick > tick:
                tick = cmd.tick
        return tick

    def create_null_sequence(self, cmds):
        """
        由命令列表创建能够存下它的空序列
        :param cmds: 命令列表
        :return: None
        """
        seq_duration = self.get_seq_duration(cmds)
        dx = seq_duration - len(self.cmds_list)
        if dx >= 0:
            for i in range(0, dx+1):
                self.cmds_list.append([])

    def add_cmd(self, cmds):
        """
        添加命令列表中的命令到总序列
        :param cmds: 命令列表
        :return: None
        """
        self.create_null_sequence(cmds)
        for cmd in cmds:
            index = cmd.tick
            self.cmds_list[index].append(cmd)

    def add_custom_loop_cmds(self, loop_cmds):
        """
        在每tick添加自定义的指令。如 每tick TP玩家一次
        :param loop_cmds: 命令列表
        :return: None
        """
        for cmds in self.cmds_list:
            cmds += loop_cmds

    def save_seq_file(self, folder, is_debug=False, build_schedule=True, namespace=''):
        """
        导出function序列
        :param folder:文件夹
        :param is_debug: 是否调试模式（聊天栏回显当前命令）
        :param build_schedule: 是否生成schedule
        :param namespace: 数据包命名空间
        :return: None
        """
        try:
            os.mkdir(f'./{folder}')
        except FileExistsError:
            pass
        schedule_tick = []
        for cmds in self.cmds_list:
            if cmds:
                f = open(f"./{folder}/{self.index}.mcfunction", "w")
                for cmd in cmds:
                    f.write(str(cmd) + "\n")
                    if is_debug:
                        f.write(f'tellraw @p {{"text":"Debug:{str(cmd)}","color":"aqua"}}\n')
                schedule_tick.append(cmds[0].tick)
            self.index += 1
        self.index = 0
        if build_schedule:
            f = open(f"./{folder}/schedule.mcfunction", "w")
            for st in schedule_tick:
                schedule = f'schedule function {namespace}:{folder}/{st} {st}\n'
                f.write(schedule)

    def save_single_file(self, folder, filename):
        """
        将所有指令保存为一个文件
        :param folder: 文件夹
        :param filename: 文件名
        :return: None
        """
        try:
            os.mkdir(f'./{folder}')
        except FileExistsError:
            pass

        f = open(f"./{folder}/{filename}.mcfunction", "w")
        for cmds in self.cmds_list:
            for cmd in cmds:
                f.write(str(cmd) + "\n")

    def output_cb_seq_function(self, namespace, folder, x, y, z, facing, max_length, max_width):
        """
        导出调用函数序列的命令方块序列生成函数, 并在cmds_list中写入调用下一个函数用的命令
        :param namespace: 命名空间
        :param folder: 文件夹名
        :param z: 起始z
        :param y: 起始y
        :param x: 起始x
        :param facing: 朝向
        :param max_length: 最大长度
        :param max_width: 最大宽度
        :return:None
        """
        cmds = []
        cb_x = x
        cb_y = y
        cb_z = z
        for i in range(len(self.cmds_list)):
            # /setblock 7 4 7 minecraft:command_block{Command:"say 1"} replace
            cmds.append(setblock.Command(0, cb_x, cb_y, cb_z, 'minecraft:command_block{Command:"function %s:%s/%s"}'
                                         % (namespace, folder, i)))
            if facing == 'x+':
                # 添加一条清除当前命令方块前的红石块的命令
                self.cmds_list[i].append(setblock.Command(i, cb_x - 1, cb_y, cb_z, 'air'))
                # 计算下一个cb的坐标
                cb_z = z + (i + 1) % max_length
                cb_y = y + int((i + 1) / max_length) % max_width
                cb_x = x + int(int((i + 1) / max_length) / max_width) * 3
                self.cmds_list[i].append(setblock.Command(i, cb_x - 1, cb_y, cb_z, 'minecraft:redstone_block'))
            elif facing == 'y+':
                self.cmds_list[i].append(setblock.Command(i, cb_x, cb_y - 1, cb_z, 'air'))
                cb_x = x + (i + 1) % max_length
                cb_z = z + int((i + 1) / max_length) % max_width
                cb_y = y + int(int((i + 1) / max_length) / max_width) * 3
                self.cmds_list[i].append(setblock.Command(i, cb_x, cb_y - 1, cb_z, 'minecraft:redstone_block'))
            elif facing == 'z+':
                self.cmds_list[i].append(setblock.Command(i, cb_x, cb_y, cb_z - 1, 'air'))
                cb_x = x + (i + 1) % max_length
                cb_y = y + int((i + 1) / max_length) % max_width
                cb_z = z + int(int((i + 1) / max_length) / max_width) * 3
                self.cmds_list[i].append(setblock.Command(i, cb_x, cb_y, cb_z - 1, 'minecraft:redstone_block'))
        try:
            os.mkdir(f'./{folder}')
        except FileExistsError:
            pass

        f = open(f"./{folder}/build_cb_seq.mcfunction", "w")
        for cmd in cmds:
            f.write(str(cmd) + "\n")
