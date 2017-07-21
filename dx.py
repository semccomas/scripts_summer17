#page 42 notes has info on this and math reasoning etc

from gridData import Grid
import numpy as np 
import MDAnalysis as md 
import matplotlib.pyplot as plt 

def opendx(x,y):
# x - working folder, y - dx file
    g = Grid(x+y)
    return g.grid, np.asarray(g.grid.shape), g.origin, g.delta    #g.delta is size of bin, this will show us size of grid which we are going to need for calculations below 


d = '/Users/sarahmccomas/Desktop/Summer17/Marina_USB/electric_fields/'
neg = opendx(d, 'elec.pot_neg.dx')
pos = opendx(d, 'elec.pot_pos.dx')
eq = opendx(d, 'elec.pot_equilib.dx')

#will generate the grid, number of bind, the origin of the grid, and the size of the bins

#subtract one grid from the other grid

n_p = neg[0] - pos[0] 
#print n_p
print np.sum(n_p)
print
print np.sum(n_p, axis = 1) 


u = md.Universe('confout.gro')
voltage_sensor1 = u.select_atoms('protein and resid 140-159 164-189 199-218 224-241')
voltage_sensor2 = u.select_atoms('protein and resid 519-539 544-574 581-604 608-621')
voltage_sensor3 = u.select_atoms('protein and resid 856-876 883-913 920-943 947-966')
voltage_sensor4 = u.select_atoms('protein and resid 1170-1189 1196-1220 1239-1246 1261-1276')



def integrate_for_z(voltage_sensor, neg):
	com1 = voltage_sensor.center_of_mass()[0:2]
	origin = neg[2][0:2]   #this is the coordinates where bin 0 is for x and y only. This is pretty close to 0 but we need to correct for it anyways 
	size = neg[3][0:2]   #this is the size of each bin
	where_grid = (com1 - origin)/ size   #this therefore convers where we are in the coordinates to where we are in the el.pot grid we found above
	where_grid = where_grid.astype(int)   #have to change to int because we use this as indexes in the grid coordinates
	sum_z = []
	grid = neg[0]
	for z in xrange(neg[1][2]):
		sum_z.append(np.sum(grid[(where_grid[0]-10):(where_grid[0]+10),(where_grid[1]-10):(where_grid[1]+10),z])/ 400)
	return np.asarray(sum_z)



def which_subtract(neg1, pos1, title, ax):

	vd1_neg = integrate_for_z(voltage_sensor1, neg1)
	vd1_pos = integrate_for_z(voltage_sensor1, pos1)
	vd1_diff = vd1_neg - vd1_pos 

	vd2_neg = integrate_for_z(voltage_sensor2, neg1)
	vd2_pos = integrate_for_z(voltage_sensor2, pos1)
	vd2_diff = vd2_neg - vd2_pos 


	vd3_neg = integrate_for_z(voltage_sensor3, neg1)
	vd3_pos = integrate_for_z(voltage_sensor3, pos1)
	vd3_diff = vd3_neg - vd3_pos 


	vd4_neg = integrate_for_z(voltage_sensor4, neg1)
	vd4_pos = integrate_for_z(voltage_sensor4, pos1)
	vd4_diff = vd4_neg - vd4_pos 

	ax.plot(vd1_diff, color = 'blue', label = 'Domain 1')
	ax.plot(vd2_diff, color = 'red', label = 'Domain 2')
	ax.plot(vd3_diff, color = 'green', label = 'Domain 3')
	ax.plot(vd4_diff, color = 'yellow', label = 'Domain 4')
	ax.set_title(title)
	#plt.legend()
	

f, (ax1,ax2,ax3) = plt.subplots(3)
which_subtract(neg, pos, 'Neg vs Pos', ax1)
which_subtract(neg, eq, 'Neg vs Eq', ax2)
which_subtract(pos, eq, 'Pos vs Eq', ax3)

plt.tight_layout()
plt.legend()
plt.show()

