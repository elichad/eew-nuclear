##Import libraries
import random
import math
from utilities import *
import matplotlib.pyplot as plt
import numpy as np
shell_radius =[]
#Import database

df = pd.read_excel('Nuclear Materials Datasheet.xlsx')
df = df.set_index('Nuclei')
print("How many shells do you want to simulate (including core)?")
number_of_shells = input()
number_of_shells = int(number_of_shells)
for m in range (number_of_shells):
    print("what material would you like layer", m, "to be made of?")    
    core_materials.append(input())
for n in range (number_of_shells):
    print("what would you like the radius of shell", n, "to be? (from centre of core)")
    temporary = input()
    temporary = float(temporary)
    shell_radius.append(temporary)
print("How many neutrons do you want to simulate?")
n = input()
n = int(n)
current_shell_var = 0

n = 10 #initial number of neutrons

time_step = 1e-10 #seconds
avogadro = 6.02e26 #Avogadro's Number
neutron_mass = 1.67e-27 #kg

#Create lists for modelling neutrons
start_energy = 0.025 #eV
energies = []
angles = [] #rad
start_pos = 0, 0 #x, y in m
positions = []
for i in range(n): #Adds starting values to the arrays
    positions.append(start_pos)
    energies.append(start_energy)
    angles.append(0)

#Get properties for materials
fission, capture, elastic, total, density, atomic_mass = choose_material(df,core_materials,current_shell_var) #Imports values for chosen material
total = total * 10**-24 #cm^2
path_length = find_mean_free_path(total, density, atomic_mass)
n_time_steps = 100
reactivities = []

#Loops for each time step
for j in range(n_time_steps):
    indices_to_remove = []
    for i in range(10): #Simulation of neutron source - adds in 10 neutrons every time step
        positions.append(start_pos)
        energies.append(start_energy)
        angles.append(0)
    before = len(positions) #Number of neutrons at the beginning of the time step
    for i in range(len(positions)): #Sets all times to start of time_step
        time = 0 
        count = 0
        while time < time_step: #Moves neutron until the time exceeds the time_step
            velocity = find_velocity(energies[i], neutron_mass)
            time_taken = path_length/(velocity*100) #Time taken for one move
            time += time_taken #Cumulative time of all moves for this neutron
            angle = generate_random_angle()
            current_pos = move(path_length, positions[i][0], positions[i][1], angle) #Calculates new position
            positions[i] = current_pos #Replace old position in the array with the new position
            event = select_event(energies[i], fission, elastic, capture, total) #Determines interaction type
            if event == (3) or current_shell(current_pos[0], current_pos[1], current_shell_var,number_of_shells,shell_radius)==-1: #Checks if neutron should be considered 
                indices_to_remove.append(i) #Adds the position of this neutron to the removal array
                break
            elif event == (2):#Movement
                energies[i] = calculate_energy(atomic_mass/avogadro, angle, angles[i], energies[i]) #Set new energy
                angles[i] = angle
            elif event == 1: #Fission
                energies.append(2e6) #Set energy of new neutron to 2 MeV
                energies[i] = 2e6 #Set energy of current neutron to 2 MeV
                positions.append(positions[i]) #Moves new neutron to current neutron
                angles.append(angle) 
                
    reverse_indices_to_remove = indices_to_remove[::-1] #Reverses removal array so indices are unaffected by item removal
    for i in reverse_indices_to_remove: #Removes all neutron properties from lists
        energies.pop(i)
        angles.pop(i)
        positions.pop(i)
            
    after = len(positions) #Neutrons after time step has finished
    reactivity = after/before
    reactivities.append(reactivity)

plt.plot(range(n_time_steps), reactivities)
plt.ylabel("Reactivities")
plt.xlabel("Number of time steps")
plt.show()
