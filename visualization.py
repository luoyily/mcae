from timeit import repeat
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation, projections


def show_static(points, color='blue', size=10, axr='equal', ax=None, show='on'):
    """
    展示静态图像
    param points:点列表
    param color:颜色
    param size:点大小
    param axr:坐标比例
    param ax:matplotlib3d类型图
    param show:是否立即显示，'on'则立即输出
    return:matplotlib3d类型图
    
    example:
    figure=show_static(points1,show='off')
    show_static(points2,ax=figure,color='red')
    将points1、points2在图中显示出来,且points2为红色
    """
    if not ax:
        ax = Axes3D(plt.figure())
    x = []
    y = []
    z = []
    for p in points:
        x.append(p[2])
        y.append(p[0])
        z.append(p[1])
    if axr == 'equal':
        dx = max(x) - min(x)
        dy = max(y) - min(y)
        dz = max(z) - min(z)
        r = 0.1
        rx = ax.get_xlim3d()
        ry = ax.get_ylim3d()
        rz = ax.get_zlim3d()
        d = max((0.5 + r) * max([dx, dy, dz]), (rx[1] - rx[0]) / 2, (ry[1] - ry[0]) / 2, (rz[1] - rz[0]) / 2)
        ax.set_xlim3d(left=min(x) + 0.5 * dx - d, right=max(x) - 0.5 * dx + d)
        ax.set_ylim3d(bottom=min(y) + 0.5 * dy - d, top=max(y) - 0.5 * dy + d)
        ax.set_zlim3d(bottom=min(z) + 0.5 * dz - d, top=max(z) - 0.5 * dz + d)
        # 此功能需要较高版本matplotlib，如果报错请升级matplotlib或者将下行注释
        ax.set_box_aspect((1, 1, 1))
    ax.scatter(x, y, z, c=color, s=size)
    # ax.set_xticks(())
    # ax.set_yticks(())
    # ax.set_zticks(())

    if show == 'on':
        plt.show()
    return ax


def get_max_frame(cmds):
    seq_duration = 0
    for cmd in cmds:
        if cmd.tick > seq_duration:
            seq_duration = cmd.tick
    return seq_duration


def get_frames(cmds):
    """
    添加命令列表中的粒子坐标到时序列
    :param cmds: 命令列表
    :return: 时序列
    """
    frame_list = []
    seq_duration = get_max_frame(cmds)

    dx = seq_duration - len(frame_list)
    if dx >= 0:
        for i in range(0, dx + 1):
            frame_list.append([])
    for cmd in cmds:
        index = cmd.tick
        frame_list[index].append([cmd.x, cmd.y, cmd.z])
    return frame_list


def show_animation(cmds, interval=0.05, t0=0, t1=-1, color='blue', size=1, repeat=False):
    """
    动态3d展示
    param cmds: 总命令集（未按时序处理的）
    param interval:每帧间隔时间，单位 秒，default=0.05与实际播放一致
    param t0:起始tick，默认0
    param t1:终止tick，默认-1,-1代表到识别的最后tick
    param color:颜色
    param size:点大小
    param repeat:是否重复播放（重复播放则无轨迹点）
    """

    fig = plt.figure()
    ax = Axes3D(fig)

    frame_list = get_frames(cmds)
    if t1 == -1:
        f = len(frame_list) - t0
    else:
        f = t1 - t0 + 1
    x = []
    y = []
    z = []

    for frame in frame_list[t0:t1]:
        for p in frame:
            x.append(p[2])
            y.append(p[0])
            z.append(p[1])

    dx = max(x) - min(x)
    dy = max(y) - min(y)
    dz = max(z) - min(z)
    r = 0.1
    rx = ax.get_xlim3d()
    ry = ax.get_ylim3d()
    rz = ax.get_zlim3d()
    d = max((0.5 + r) * max([dx, dy, dz]), (rx[1] - rx[0]) / 2, (ry[1] - ry[0]) / 2, (rz[1] - rz[0]) / 2)
    xmin = min(x) + 0.5 * dx - d
    xmax = max(x) - 0.5 * dx + d
    ymin = min(y) + 0.5 * dy - d
    ymax = max(y) - 0.5 * dy + d
    zmin = min(z) + 0.5 * dz - d
    zmax = max(z) - 0.5 * dz + d
    ax.set_xlim3d(left=xmin, right=xmax)
    ax.set_ylim3d(bottom=ymin, top=ymax)
    ax.set_zlim3d(bottom=zmin, top=zmax)
    ax.set_box_aspect((1, 1, 1))

    def frames(i):
        if repeat:
            plt.cla()
        ax.set_xlim3d(xmin=xmin, xmax=xmax)
        ax.set_ylim3d(ymin=ymin, ymax=ymax)
        ax.set_zlim3d(zmin=zmin, zmax=zmax)
        for p in frame_list[i + t0]:
            ax.scatter(p[2], p[0], p[1], c=color, s=size)
        return ax

    ani = animation.FuncAnimation(fig=fig, func=frames, frames=f, interval=interval * 1000, blit=False, repeat=repeat)
    plt.show()
