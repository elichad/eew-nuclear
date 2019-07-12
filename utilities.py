import random
import math
import pandas as pd

df = pd.read_excel('Nuclear Materials Datasheet.xlsx')
df = df.set_index('Nuclei')
"""
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
"""
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
def choose_material(df, material):  
    print('material',material)
    properties = df.loc[material]
    """
    shell_properties =[]
    fission=[]
    elastic=[]
    capture=[]
    total=[]
    density=[]
    atomic_mass=[]
    for i in range (number_of_shells):
        
        fission.append(core_materials[i]['fission'])
        elastic.append(core_materials[i]['elastic'])
        capture.append(core_materials[i]['capture'])
        total.append(core_materials[i]['total']) 
        density.append(core_materials[i]['density'])
        atomic_mass.append(core_materials[i]['mass'])
        shell_properties.append(fission,elastic,capture,total,density,atomic_mass)
    """
    return(properties)
    
#choose_material(df,['U235','Fe56'],0,2)
#choose_material(df,['U235','Fe56'],1,2)
    
def add(shell_radius):
    add_var = 0
    for j in range (len(shell_radius)):
        add_var = add_var + shell_radius[j]
    return add_var

def current_shell(x, y, number_of_shells,shell_radius):
    displacement = math.sqrt(x*x + y*y)
    if displacement < shell_radius[0]:
        current_shell_var = 0
        return current_shell_var
    elif displacement > shell_radius[len(shell_radius) - 1]:
        return -1
    else:
        for k in range (number_of_shells):
            if displacement > shell_radius[k] and displacement < shell_radius[k+1]:
                current_shell_var = k+1
                return current_shell_var
    
def select_event(energy, material_properties): #classifies interaction dependent on energy and prob
    if energy > 1000000:
        return 2 #Elastic
    elif energy < 0.001:
        return 3 #Capture
    else:
        random_number = random.randint(1, material_properties["total"]*100)
        if random_number < material_properties["fission"]*100: 
            return 1
        elif random_number < material_properties["fission"]*100 + material_properties["elastic"]*100 and random_number > material_properties["fission"]*100: 
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
    #choose_material(df,core_materials,current_shell_var)
    #density = density*10**-3 #Converts density to kg/cm^3
    #atomic_mass = atomic_mass * 10**-2
    microscopic_cross_section = microscopic_cross_section * 10**-24 #cm^-2
    atomic_number_density = (density * 6.023 * (10**23))/atomic_mass #atoms/cm^2
    mean_free_path = 1/(100 * microscopic_cross_section * atomic_number_density)  #metres
    return mean_free_path

#print(find_mean_free_path(705*(10**(-24)), 19.1*(10**(-3)), 23.5*(10**(-2))))
#print(find_number_of_steps(1e-9, 1.73, 0.025, mass))
#print(is_outside(5, 5, 5))
    
    
    
      
    
        
        
    

    
