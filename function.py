import os


class Function:
    def __init__(self):
        self.cmds_list = []
        self.index = 0

    def get_seq_duration(self, cmds):
        tick = 0
        for cmd in cmds:
            if cmd.tick > tick:
                tick = cmd.tick
        return tick

    def create_null_sequence(self, cmds):
        seq_duration = self.get_seq_duration(cmds)
        dx = seq_duration - len(self.cmds_list)
        if dx >= 0:
            for i in range(0, dx+1):
                self.cmds_list.append([])

    def add_cmd(self, cmds):
        self.create_null_sequence(cmds)
        for cmd in cmds:
            index = cmd.tick
            self.cmds_list[index].append(str(cmd))

    def add_custom_loop_cmds(self, loop_cmds):
        for cmds in self.cmds_list:
            cmds += loop_cmds

    def save_seq_file(self, folder, is_debug=False):
        try:
            os.mkdir(f'./{folder}')
        except FileExistsError:
            pass

        for cmds in self.cmds_list:
            f = open(f"./{folder}/{self.index}.mcfunction", "w")
            for cmd in cmds:
                if cmd:
                    f.write(str(cmd) + "\n")
                    if is_debug:
                        f.write(f'tellraw @p {{"text":"Debug:{str(cmd)}","color":"aqua"}}\n')
            self.index += 1

    def save_single_file(self, folder, filename):
        try:
            os.mkdir(f'./{folder}')
        except FileExistsError:
            pass

        f = open(f"./{folder}/{filename}.mcfunction", "w")
        for cmds in self.cmds_list:
            for cmd in cmds:
                f.write(str(cmd) + "\n")

