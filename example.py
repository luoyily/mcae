import particle
import function_generation
import points


# 粒子相关
# 初始化形状，粒子命令生成器，函数生成器
shape = points.Shapes()
particle_cmd = particle.CmdBuilder()
ani_func = function_generation.Function()

# 创建一条由0Tick到20Tick的粒子直线动画
# 每个函数的详细参数都可以在相应代码的注释中查看（虽然还有部分注释未完善）
# 生成一条起点为0, 0, 0 终点为20, 20, 20的直线，每0.2格在这条直线上取一个点。返回所有产生的点
line = shape.line([0, 0, 0], [20, 20, 20], 0.2)
# 生成静态的粒子命令，动画从0Tick开始至20Tick结束，点使用上面生成的直线，粒子名为'end_rod'，
# 粒子运动范围为0, 0, 0， 速度为0， 每条指令产生1个粒子
particle_cmd.static_particle(0, 20, line, 'end_rod', 0, 0, 0, 0, 1)
# 将上面生成的粒子命令添加到function中，如果制作了多个粒子动画，每个都会保存在particle_cmd.cmds中，只需要在最后添加一次即可
ani_func.add_cmd(particle_cmd.cmds)
# 导出一个命令方块序列，用于执行以上制作的动画
# V1.0.1 可用schedule模式导出，schedule功能需要游戏版本1.14以上
# ani_func.output_cb_seq_function('mcae', 'ani', -10, 5, -10, 'x+', 64, 64)
# 导出函数文件序列
# ani_func.save_seq_file('ani')
# V1.0.1 注意，这里由原来的命令方块序列改为了schedule来执行function序列。
# 游戏中请使用 形如“/function mcae:ani/schedule”的指令运行你的动画
ani_func.save_seq_file('ani', build_schedule=True, namespace='mcae')
# 至此，你可以将目录下的 ani 文件下放入你存档中数据包的functions文件夹下。
# 例如：.minecraft\saves\新的世界\datapacks\example\data\mcae\functions
# 如果你不会使用datapack 可以去Wiki搜索相关条目。
