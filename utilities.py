import random
import math

n = 100 #number of neutrons
time_step = 1 
start_pos = (0,0) #starting position
positions = [] #list of positions
energies = [] #energies of neutrons in respective positions
material_names = "U235"
radius = 5 #radius of nucleus
energy = 0.025
properties = [] #list of properties of materials
mass = 1.67e-27 #mass of neutron (kg)

def generate_random_angle():
    angle = random.uniform(0, 2*math.pi) #in radians
    return angle

def move(mean_free_path, x, y, angle):
    if angle > math.pi and angle < 3/2 * math.pi: #-ve x, -ve y
        new_xcoordinate = x - mean_free_path*math.sin(angle)
        new_ycoordinate = y - mean_free_path*math.cos(angle)
    elif angle > 3/2 * math.pi: #-ve x, +ve y
        new_xcoordinate = x - mean_free_path*math.sin(angle)
        new_ycoordinate = y + mean_free_path*math.cos(angle)
    elif angle == math.pi: #directly down
        new_xcoordinate = x
        new_ycoordinate = y - mean_free_path
    elif angle == 2*math.pi or angle == 0: #directly up
        new_xcoordinate = x
        new_ycoordinate = y + mean_free_path
    elif angle == 1/2 * math.pi: #directly to the right
        new_xcoordinate = x + mean_free_path
        new_ycoordinate = y
    elif angle == 3/2 * math.pi: #directly to the left
        new_xcoordinate = x - mean_free_path
        new_ycoordinate = y
    elif angle < math.pi and angle > 1/2 * math.pi: #+ve x, -ve y
        new_xcoordinate = x + mean_free_path*math.sin(angle)
        new_ycoordinate = y - mean_free_path*math.cos(angle)
    elif angle < 1/2 * math.pi: #+ve x, +ve y
        new_xcoordinate = x + mean_free_path*math.sin(angle)
        new_ycoordinate = y + mean_free_path*math.cos(angle)
    else:
        return (0, 0)
    return new_xcoordinate, new_ycoordinate
    
#angle = generate_random_angle()
#print(move(1.73, 0, 0, angle))

def is_outside(radius, x, y): #checks neutron has not escpaed
    if math.sqrt(x*x + y*y) > radius:
        return(True)
    else:
        return(False)
    
def select_event(energy, fission, elastic, capture, total): #classifies interaction dependent on energy and prob
    if energy > 2000000:
        return 2
    elif energy < 0.001:
        return 3
    else:
        random_number = random.randint(1, total)
        if random_number < fission:
            return 1
        elif random_number < fission + elastic and random_number > fission:
            return 2
        else:
            return 3
        
#print(select_event(0.025, 590, 15, 100, 705))

def find_number_of_steps(time_step, mean_free_path, energy, mass):
    velocity = math.sqrt(2*energy/mass) #using KE equation
    time_for_one_step = mean_free_path/velocity #using speed = distance x time
    number_of_steps = time_step/time_for_one_step
    return(int(number_of_steps))

def find_mean_free_path(microscopic_cross_section, density, atomic_mass): #using moderation equations
    atomic_number_density = (density * 6.023 * (10**23))/atomic_mass
    mean_free_path = 1/(microscopic_cross_section * atomic_number_density)
    return mean_free_path

print(find_mean_free_path(705*(10**(-24)), 19.1*(10**(-3)), 23.5*(10**(-2))))
#print(find_number_of_steps(1e-9, 1.73, 0.025, mass))
#print(is_outside(5, 5, 5))
    
    
    
      
    
        
        
    

    
