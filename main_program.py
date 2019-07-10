##Import libraries
import random
import math
from utilities import *
import matplotlib.pyplot as plt
import numpy as np
##Define functions

##Main Program
n = 100 #number of neutrons
time_step = 1e-10 #second

#Create position list
start_pos = 0, 0 #x, y
positions = []
for i  in range(n):
    positions.append(start_pos)


#Create energy list
start_energy = 0.025 #eV
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

path_length = find_mean_free_path(U235["microscopic_cross_section"], U235["density"], U235["mass"])#(microscopic_cross_section, density kg/cm^3, mass of material)
print(path_length)
before = len(positions)
n_time_steps = 4
reactivities = []

#n_steps = find_number_of_steps(time_step, path_length, start_energy, 1.67e-27) #nanoseconds, cm, eV, mass of a neutron
for j in range(n_time_steps):
    for i in range(len(positions)):
        time = 0 
        count = 0
        while time < time_step: 
            count += 1
            velocity = find_velocity(energies[i], 1.67e-27)
            time_taken = path_length/(velocity*100)
            time += time_taken
            angle = generate_random_angle()
            current_pos = move(path_length, positions[i][0], positions[i][1], angle)
            positions[i] = current_pos
            event = select_event(energies[i], 590, 15, 100, 705)
            if event == (1):#Fission
                energies.append(2e6)
                energies[i] = 2e6
                positions.append(positions[i])
            elif event == (2):#Movement
                energies[i] = 2/(3*235) * energies[i]
            elif event == (3) or isOutside(0.5, current_pos[0], current_pos[1]): #Capture
                positions.pop(i)
                energies.pop(i)
                break
    print(count)
            
    after = len(positions)
    reactivity = after/before
    reactivities.append(reactivity)

print(reactivities)
plt.plot([1, 2, 3, 4], reactivities)
plt.xticks(np.arange(1, 5, 1)) 
plt.ylabel("Reactivities")
plt.xlabel("Number of time steps")
plt.show()

        
    
    
    
    
    