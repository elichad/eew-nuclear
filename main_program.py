##Import libraries
import random
import math
from utilities import *
##Define functions

##Main Program
n = 100 #number of neutrons
time_step = 1e-9 #nanosecond

#Create position list
start_pos = 0, 0 #x, y
positions = []
for i  in range(n):
    positions.append(start_pos)

#Create energy list
start_energy = 0.0025 #MeV
energies = []
for i  in range(n):
    energies.append(start_energy)
    
#Material
U235 = {"fission":590, \
            "elastic":15, \
            "capture":100,\
            "density":0.0191,\
            "mass":235e-3,\
            "microscopic_cross_section":705e-24}

path_length = find_mean_free_path(705e-24, 0.0191, 235e-3) #(microscopic_cross_section, density kg/cm^3, mass of material)
print(path_length)
#for neutron in positions:
#    #Movement
#    angle = generate_random_angle()
#    neutron = move(path_length, neutron[0], neutron[1], angle)
#    event = select_event(start_energy, 590, 15, 100, 705)
#    if event == (1):#Fission
#        energies.append(energies[positions.index(neutron)])
#        positions.append(neutron)
#    elif event == (2):#Movement
#        pass
#    else:#Capture
#        positions.remove(neutron)
#        energies.pop(positions.index(neutron))


n_steps = find_number_of_steps(time_step, path_length, start_energy, 1.67e-27) #nanoseconds, cm, eV, mass of a neutron
for i in range(len(positions)):
    for x in range(n_steps):
        angle = generate_random_angle()
        current_pos = move(path_length, positions[i][0], positions[i][1], angle)
        print(current_pos)
        positions[i] = current_pos
        event = select_event(start_energy, 590, 15, 100, 705)
        if event == (1):#Fission
            energies.append(energies[i])
            positions.append(positions[i])
        elif event == (2):#Movement
            pass
        elif event == (3) or isOutside(0.5, current_pos[0], current_pos[1]) == True: #Capture
            positions.pop(i)
            energies.pop(i)
        
    
    
    
    
    