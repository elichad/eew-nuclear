import random
import math
import pandas as pd
df = pd.read_excel('Nuclear Materials Datasheet.xlsx')
df = df.set_index('Nuclei')
core_materials = ['U235', 'Fe56']
n = 100 #number of neutrons
time_step = 1 
start_pos = (0,0) #starting position
positions = [] #list of positions
energies = [] #energies of neutrons in respective positions
angles = [] #angles of neutrons in respective positions anti-clockwise
energy = 0.025
properties = [] #list of properties of materials
mass = 1.67e-27 #mass of neutron (kg)
new_xcoordinate = 0
new_ycoordinate = 0
current_shell_var = 0
def generate_random_angle():
    angle = random.uniform(0, 2*math.pi) #in radians
    return angle

def move(mean_free_path, x, y, angle):
    new_xcoordinate = x - mean_free_path * math.sin(angle)
    new_ycoordinate = y + mean_free_path * math.cos(angle)
    return(new_xcoordinate, new_ycoordinate)

def calculate_energy(atomic_mass, new_angle, previous_angle, initial_energy):
    alpha = ((float(atomic_mass -1)/float(atomic_mass + 1))) ** 2
    gamma = new_angle - previous_angle
    delta = ((1+alpha)/2)*((1-alpha)/2)*abs(math.cos(gamma))
    return(initial_energy * (1-delta))
    
    
#angle = generate_random_angle()
#path = find_mean_free_path(705*(10**(-24)), 19.1*(10**(-3)), 23.5*(10**(-2)))
#print(move(path, 0, 0, angle))
def choose_material(df,core_materials,current_shell):  
    material = core_materials[int(current_shell_var)]
    temp_material = df.loc[material]
    fission = temp_material['fission']
    elastic = temp_material['elastic']
    capture = temp_material['capture']
    total = temp_material['total'] 
    density = temp_material['density']
    atomic_mass = temp_material['mass']
    return(fission, elastic, capture, total, density, atomic_mass)
    
def add(shell_radius):
    add_var = 0
    for j in range (len(shell_radius)):
        add_var = add_var + shell_radius[j]
    return add_var

def current_shell(x, y, current_shell_var,number_of_shells,shell_radius):
    displacement = math.sqrt(x*x + y*y)
    if displacement < shell_radius[0]:
        current_shell_var = 0
        return current_shell_var
    elif displacement > shell_radius[len(shell_radius) - 1]:
        return -1
    else:
        for k in range (number_of_shells):
            if displacement > shell_radius[k] and displacement < shell_radius[k+1]:
                current_shell_var = k
                return current_shell_var
    
def select_event(energy, fission, elastic, capture, total): #classifies interaction dependent on energy and prob
    if energy > 1000000:
        return 2 #Elastic
    elif energy < 0.001:
        return 3 #Capture
    else:
        random_number = random.randint(1, total)
        if random_number < fission: 
            return 1
        elif random_number < fission + elastic and random_number > fission: 
            return 2
        else: 
            return 3
        
#print(select_event(0.025, 590, 15, 100, 705))
def find_velocity(energy, mass):
    joules = energy * 1.6e-19
    velocity = math.sqrt(2*joules/mass) #using KE equation
    return velocity
    
#def find_number_of_steps(time_step, mean_free_path, energy, mass):
#    velocity = math.sqrt(2*energy/mass) #using KE equation
#    time_for_one_step = mean_free_path/velocity #using speed = distance x time
#    number_of_steps = time_step/time_for_one_step
#    return(int(number_of_steps))

def find_mean_free_path(microscopic_cross_section, density, atomic_mass):#using moderation equations
    choose_material(df,core_materials,current_shell_var)
    atomic_number_density = (density * 6.023 * (10**23))/atomic_mass
    mean_free_path = 1/(microscopic_cross_section * atomic_number_density)
    return mean_free_path

#print(find_mean_free_path(705*(10**(-24)), 19.1*(10**(-3)), 23.5*(10**(-2))))
#print(find_number_of_steps(1e-9, 1.73, 0.025, mass))
#print(is_outside(5, 5, 5))
    
    
    
      
    
        
        
    

    
