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
for i in range(n): #Adds starting values to the arrays
    positions.append(start_pos)
    energies.append(start_energy)
    angles.append(0)


fission, capture, elastic, total, density, atomic_mass = choose_material(df,core_materials,current_shell_var) #Imports values for chosen material
print(fission)
print(capture)
print(elastic)
print(total)  
print(density)

#Material
microscopic_cross_section = total * 10**-24 #cm^2
path_length = find_mean_free_path(microscopic_cross_section, density, atomic_mass)#(microscopic_cross_section, density kg/cm^3, mass of material)
print(path_length)
n_time_steps = 100
reactivities = []

#n_steps = find_number_of_steps(time_step, path_length, start_energy, 1.67e-27) #nanoseconds, cm, eV, mass of a neutron
for j in range(n_time_steps):
    indices_to_remove = []
    for i in range(10): #Simulation of neutron source - adds in 10 neutrons every time step
        positions.append(start_pos)
        energies.append(start_energy)
        angles.append(0)
    before = len(positions) #Number of neutrons which the time step starts with
    for i in range(len(positions)):
        time = 0 
        count = 0
        while time < time_step: #Carries on moving the neutron until the total time it's moved for is equal/greater than time step
            velocity = find_velocity(energies[i], neutron_mass)
            time_taken = path_length/(velocity*100) #Time taken for one move
            time += time_taken #Cumulative time of all moves for this neutron
            angle = generate_random_angle()
            current_pos = move(path_length, positions[i][0], positions[i][1], angle) #Calculate new position after move
            positions[i] = current_pos #Replace old position in the array with the new position
            event = select_event(energies[i], fission, elastic, capture, total) #Determine what interaction to use
            if event == (3) or current_shell(current_pos[0], current_pos[1], current_shell_var,number_of_shells,shell_radius)==-1: #Checks if neutron has been captured or has left the radius 
                indices_to_remove.append(i) #Adds the position of this neutron to the removal array
                break
            elif event == (2):#Movement
                energies[i] = calculate_energy(atomic_mass/avogadro, angle, angles[i], energies[i]) #Set new energy
                angles[i] = angle
            elif event == 1: #Fission
                energies.append(2e6) #Set speed of new neutron to 2 MeV
                energies[i] = 2e6 #Set speed of current neutron to 2 MeV
                positions.append(positions[i]) #Set the position of the new neutron to the position of the current neutron
                angles.append(angle) 
                
    reverse_indices_to_remove = indices_to_remove[::-1] #Reverses the removal array so that elements are removed from the back to the front so no errors with elements shifting
    for i in reverse_indices_to_remove: #Removes all the neutron properties based on the indices in the removal array
        energies.pop(i)
        angles.pop(i)
        positions.pop(i)
            
    after = len(positions) #Neutrons after time step has finished
    reactivity = after/before
    reactivities.append(reactivity)

#print("reactivities - ", reactivities)
plt.plot(range(n_time_steps), reactivities)
#plt.xticks(np.arange(1, n_time_steps, 1)) #Forces x-axis to be only int values
plt.ylabel("Reactivities")
plt.xlabel("Number of time steps")
plt.show()
