
import matplotlib.pyplot as plt
from pylab import mpl
#plt.rcParams['font.sans-serif'] = ['YaHei Consolas Hybrid'] # 用来正常显示中文标签
#plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
import mpl_toolkits.axisartist.axislines as axislines

fig = plt.figure(1, figsize=(10, 6))
fig.subplots_adjust(bottom=0.2)

# 子图1
ax1 = axislines.Subplot(fig, 131)
fig.add_subplot(ax1)
# for axis in ax1.axis.values():
#     axis.major_ticks.set_tick_out(True) # 标签全部在外部
ax1.axis[:].major_ticks.set_tick_out(True) # 这句和上面的for循环功能相同
ax1.axis["left"].label.set_text("子图1 -left标签")  # 显示在左边
# 设置刻度
ax1.set_yticks([2,4,6,8])
ax1.set_xticks([0.2,0.4,0.6,0.8])

# 子图2
ax2 = axislines.Subplot(fig, 132)
fig.add_subplot(ax2)
ax2.set_yticks([1,3,5,7])
ax2.set_yticklabels(('one','two','three', 'four', 'five'))   # 不显示‘five’
ax2.set_xlim(5, 0) # X轴刻度
ax2.axis["left"].set_axis_direction("right")
ax2.axis["left"].label.set_text("子图2 -left标签")  # 显示在右边
ax2.axis["bottom"].set_axis_direction("top")
ax2.axis["right"].set_axis_direction("left")
ax2.axis["top"].set_axis_direction("bottom")

# 子图3
ax3 = axislines.Subplot(fig, 133)
fig.add_subplot(ax3)
# 前两位表示X轴范围，后两位表示Y轴范围
ax3.axis([40, 160, 0, 0.03])
ax3.axis["left"].set_axis_direction("right")
ax3.axis[:].major_ticks.set_tick_out(True)

ax3.axis["left"].label.set_text("Long Label Left")
ax3.axis["bottom"].label.set_text("Label Bottom")
ax3.axis["right"].label.set_text("Long Label Right")
ax3.axis["right"].label.set_visible(True)
ax3.axis["left"].label.set_pad(0)
ax3.axis["bottom"].label.set_pad(20)

plt.show()
