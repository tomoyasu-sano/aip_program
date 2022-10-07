import numpy as np
import matplotlib.pyplot as plt
# import data
data_arrays = np.load('/Users/tomoyasu/dev/AIP/data_learning/data_arrays.npy')

# １台１変数可視化（例：最大持ち玉）
check_data = 4
check_table = 1
data = data_arrays[check_table][check_data,:]
#plt.plot(data)
#plt.show()


# 全てのデータ１変数可視化（例：最大持ち玉）
fig = plt.figure()

ax1 = fig.add_subplot(4, 2, 1)
ax2 = fig.add_subplot(4, 2, 2)
ax3 = fig.add_subplot(4, 2, 3)
ax4 = fig.add_subplot(4, 2, 4)
ax5 = fig.add_subplot(4, 2, 5)
ax6 = fig.add_subplot(4, 2, 6)
ax7 = fig.add_subplot(4, 2, 7)
ax8 = fig.add_subplot(4, 2, 8)

ax1.set_ylim(0, 50000)
ax2.set_ylim(0, 50000)
ax3.set_ylim(0, 50000)
ax4.set_ylim(0, 50000)
ax5.set_ylim(0, 50000)
ax6.set_ylim(0, 50000)
ax7.set_ylim(0, 50000)
ax8.set_ylim(0, 50000)

y1 = data_arrays[0][check_data,:]
y2 = data_arrays[1][check_data,:]
y3 = data_arrays[2][check_data,:]
y4 = data_arrays[3][check_data,:]
y5 = data_arrays[4][check_data,:]
y6 = data_arrays[5][check_data,:]
y7 = data_arrays[6][check_data,:]
y8 = data_arrays[7][check_data,:]

c1,c2,c3,c4= "blue","green","red","black"      # 各プロットの色
l1,l2,l3,l4 = "table_1","table_2","table_3","table_4"   # 各ラベル


ax1.plot( y1, color=c1, label=l1)
ax2.plot( y2, color=c2, label=l2)
ax3.plot( y3, color=c3, label=l3)
ax4.plot( y4, color=c4, label=l4)
ax5.plot( y5, color=c1, label=l1)
ax6.plot( y6, color=c2, label=l2)
ax7.plot( y7, color=c3, label=l3)
ax8.plot( y8, color=c4, label=l4)

ax1.legend(loc = 'upper right') 
ax2.legend(loc = 'upper right') 
ax3.legend(loc = 'upper right') 
ax4.legend(loc = 'upper right') 
ax5.legend(loc = 'upper right') 
ax6.legend(loc = 'upper right') 
ax7.legend(loc = 'upper right') 
ax8.legend(loc = 'upper right') 

plt.ylim([0, 50000])

fig.tight_layout()
plt.show()
