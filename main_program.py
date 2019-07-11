##Import libraries
import random
import math
from utilities import *
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel('Nuclear Materials Datasheet.xlsx')
df = df.set_index('Nuclei')

number_of_shells = 2
core_materials = ['U235', 'Fe56']
shell_radius = [5, 15]
current_shell_var = 0
##Define functions
#print(df)

##Main Program
n = 10 #initial number of neutrons
time_step = 1e-10 #seconds
avogadro = 6.02e26 #Avogadro's Number
neutron_mass = 1.67e-27 #kg

#Create lists
start_energy = 0.025 #eV
energies = [] #eV
angles = [] #rad
start_pos = 0, 0 #x, y in m
positions = [] # m
for i  in range(n):
    positions.append(start_pos)
    energies.append(start_energy)
    angles.append(0)


fission, capture, elastic, total, density, atomic_mass = choose_material(df,core_materials,current_shell_var)
print(fission)
print(capture)
print(elastic)
print(total)  
print(density)

#Material
microscopic_cross_section = total * 10**-24
path_length = find_mean_free_path(microscopic_cross_section, density, atomic_mass)#(microscopic_cross_section, density kg/cm^3, mass of material)
print(path_length)
n_time_steps = 10
reactivities = []

#n_steps = find_number_of_steps(time_step, path_length, start_energy, 1.67e-27) #nanoseconds, cm, eV, mass of a neutron
for j in range(n_time_steps):
    not_reverse_indices_to_remove = []
    for i in range(10):
        positions.append(start_pos)
        energies.append(start_energy)
        angles.append(0)
    before = len(positions)
    for i in range(len(positions)):
        time = 0 
        count = 0
        while time < time_step: 
            count += 1
            velocity = find_velocity(energies[i], neutron_mass)
            time_taken = path_length/(velocity*100)
            time += time_taken
            angle = generate_random_angle()
            current_pos = move(path_length, positions[i][0], positions[i][1], angle)
            positions[i] = current_pos
            event = select_event(energies[i], 590, 15, 100, 705)
            if event == (3) or current_shell(current_pos[0], current_pos[1], current_shell_var,number_of_shells,shell_radius)==-1:
                not_reverse_indices_to_remove.append(i)
                break
            elif event == (2):#Movement
                energies[i] = calculate_energy(atomic_mass/avogadro, angle, angles[i], energies[i])
                angles[i] = angle
            elif event == 1: #Capture
                energies.append(2e6)
                energies[i] = 2e6
                positions.append(positions[i])
                angles.append(angle)
                
    indices_to_remove = not_reverse_indices_to_remove[::-1]
    for i in indices_to_remove:
        energies.pop(i)
        angles.pop(i)
        positions.pop(i)
            
    after = len(positions)
    reactivity = after/before
    reactivities.append(reactivity)

print("reactivities - ", reactivities)
plt.plot(range(n_time_steps), reactivities)
#plt.xticks(np.arange(1, 5, 1)) 
plt.ylabel("Reactivities")
plt.xlabel("Number of time steps")
plt.show()
