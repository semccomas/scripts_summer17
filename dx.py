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


u = md.Universe('../Marina_USB/electric_fields/confout.gro')
voltage_sensor1 = u.select_atoms('protein and resid 140-159 164-189 199-218 224-241')
voltage_sensor2 = u.select_atoms('protein and resid 519-539 544-574 581-604 608-621')
voltage_sensor3 = u.select_atoms('protein and resid 856-876 883-913 920-943 947-966')
voltage_sensor4 = u.select_atoms('protein and resid 1170-1189 1196-1220 1239-1246 1261-1276')
pore_domain = u.select_atoms('protein and resid 393-426 720-740 1087-1120 1388-1420')


def integrate_for_z(voltage_sensor, neg):
	com1 = voltage_sensor.center_of_mass()[0:2]
	origin = neg[2][0:2]   #this is the coordinates where bin 0 is for x and y only. This is pretty close to 0 but we need to correct for it anyways 
	size = neg[3][0:2]   #this is the size of each bin
	where_grid = (com1 - origin)/ size   #this therefore convers where we are in the coordinates to where we are in the el.pot grid we found above
	where_grid = where_grid.astype(int)   #have to change to int because we use this as indexes in the grid coordinates
	sum_z = []
	grid = neg[0]
	for z in xrange(neg[1][2]):
		sum_z.append(np.sum(grid[(where_grid[0]-5):(where_grid[0]+5),(where_grid[1]-5):(where_grid[1]+5),z])/ 100)
	
	z_location = []
	size_z = neg[3][2]
	origin_z = neg[2][2]
	for line in xrange(len(sum_z)):
		z_location.append(line * size_z + origin_z)	

	return np.asarray(sum_z), z_location



def which_subtract(neg1, pos1, title, ax, scale):

	z_location = integrate_for_z(voltage_sensor1, neg1)[1]

	vd1_neg = integrate_for_z(voltage_sensor1, neg1)[0]
	vd1_pos = integrate_for_z(voltage_sensor1, pos1)[0]
	vd1_diff = vd1_neg - vd1_pos 

	vd2_neg = integrate_for_z(voltage_sensor2, neg1)[0]
	vd2_pos = integrate_for_z(voltage_sensor2, pos1)[0]
	vd2_diff = vd2_neg - vd2_pos 


	vd3_neg = integrate_for_z(voltage_sensor3, neg1)[0]
	vd3_pos = integrate_for_z(voltage_sensor3, pos1)[0]
	vd3_diff = vd3_neg - vd3_pos 


	vd4_neg = integrate_for_z(voltage_sensor4, neg1)[0]
	vd4_pos = integrate_for_z(voltage_sensor4, pos1)[0]
	vd4_diff = vd4_neg - vd4_pos 

	pd_neg = integrate_for_z(pore_domain, neg1)[0]
	pd_pos = integrate_for_z(pore_domain, pos1)[0]
	pd_diff = pd_neg - pd_pos

	if scale == 'y':
		vd1_diff = vd1_diff / 2
		vd2_diff = vd2_diff / 2
		vd3_diff = vd3_diff / 2
		vd4_diff = vd4_diff / 2
		pd_diff = pd_diff / 2

	ax.plot(z_location, vd1_diff, color = 'blue', label = 'Domain 1')
	ax.plot(z_location, vd2_diff, color = 'red', label = 'Domain 2')
	ax.plot(z_location, vd3_diff, color = 'green', label = 'Domain 3')
	ax.plot(z_location, vd4_diff, color = 'yellow', label = 'Domain 4')
	ax.plot(z_location, pd_diff, color = 'orange', label = 'Pore Domain')
	ax.set_title(title)
	#plt.legend()
	

f, (ax1,ax2,ax3) = plt.subplots(3)
which_subtract(neg, pos, 'Neg vs Pos', ax1, 'y')
which_subtract(neg, eq, 'Neg vs Eq', ax2, 'n')
which_subtract(pos, eq, 'Pos vs Eq', ax3, 'n')

plt.tight_layout()
plt.legend()
plt.savefig('../Marina_USB/electric_fields/comparing_electrostat_pot.png')

