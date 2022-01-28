import particle
import function_generation
import points


# 粒子相关
# 初始化形状，粒子命令生成器，函数生成器
shape = points.Shapes()
particle_cmd = particle.CmdBuilder()
ani_func = function_generation.Function()

# 用粒子绘制一张彩色图片
particle_cmd.color_particle_img('test2.png', 0, 32, 0, 7, 0, 0, 1)
ani_func.add_cmd(particle_cmd.cmds)
ani_func.save_single_file('pimg', 'img2')
# 旋转并绘制这张图片
# 这里为了单独演示每个动画，对粒子命令生成器，以及函数生成器的命令列表进行了清空
particle_cmd.cmds = []
ani_func.cmds_list = []

particle_cmd.color_particle_img('test2.png', 0, 32, 0, 7, 0, 0, 1,
                                is_rotate=True, vec1=[0, 32, 0], vec2=[0, 32, 1], degree=45)
ani_func.add_cmd(particle_cmd.cmds)
ani_func.save_single_file('pimg', 'img3')

# 绘制一条三阶贝塞尔曲线
particle_cmd.cmds = []
ani_func.cmds_list = []
curve = shape.bezier3x_xyz([[21, 20, 20], [38, 28, 8], [46, 19, 10], [45, 23, -8]], 0.2)
particle_cmd.static_particle(0, 40, curve, 'end_rod', 0, 0, 0, 0, 1)
ani_func.add_cmd(particle_cmd.cmds)
# ani_func.output_cb_seq_function('mcae', 'curve', -10, 7, -10, 'x+', 64, 64)
# ani_func.save_seq_file('curve')
ani_func.save_seq_file('ani', build_schedule=True, namespace='mcae')

# 围绕上面的贝塞尔曲线绘制螺线
particle_cmd.cmds = []
ani_func.cmds_list = []
helix = shape.helix([21, 20, 20], [45, 23, -8], 3, 0.1,
                    degree=0, path_type='custom', custom_points=curve, add=True, deg_d=7)
# 这次换点不一样子粒子
particle_cmd.static_particle(0, 40, helix, 'end_rod', 0.1, 0.1, 0.1, 0.03, 3)
ani_func.add_cmd(particle_cmd.cmds)
# ani_func.output_cb_seq_function('mcae', 'helix', -10, 9, -10, 'x+', 64, 64)
# ani_func.save_seq_file('helix')
ani_func.save_seq_file('ani', build_schedule=True, namespace='mcae')

# 单独绘制一条围绕抛物线的螺线
particle_cmd.cmds = []
ani_func.cmds_list = []
helix = shape.helix([21, 20, 20], [100, 20, 100], 7, 0.1,
                    degree=0, path_type='parabola', add=True, deg_d=7)

particle_cmd.static_particle(0, 40, helix, 'firework', 0.2, 0.2, 0.2, 0.1, 7)
ani_func.add_cmd(particle_cmd.cmds)
# ani_func.output_cb_seq_function('mcae', 'helix2', -10, 11, -10, 'x+', 64, 64)
# ani_func.save_seq_file('helix2')
ani_func.save_seq_file('ani', build_schedule=True, namespace='mcae')
