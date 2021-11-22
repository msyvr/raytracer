import numpy as np

def discriminant(a, b, c):
    '''
    if the discriminant is < 0, the solution to the quadratic formula is complex -> no intersection -> t = np.inf
    '''
    return (b**2) - (4*a*c)

def normal_to_sphere(point_on_sphere, sphere_center):
    '''
    the normal computed points outward
    '''
    return (np.array(point_on_sphere) - np.array(sphere_center))/np.linalg.norm(point_on_sphere - sphere_center)

def t_sphere(a, b, c):
    '''
    11.17
    the smaller solution to the quadratic formula yields the nearest intersection; if t < 0, the intersection is 'behind' the ray origin (start point), so treated as no intersection: t = np.inf
    '''
    return (-b - (discriminant(a, b, c)**0.5))/(2*a) #if (-b - (discriminant(a, b, c)**0.5))/(2*a) > 0 else np.inf

def intersect_sphere(ray, sphere):
    a = np.dot(ray_direction, ray_direction)
    b = -2*np.dot(sphere_center, ray_direction)
    c = np.dot(sphere_center, sphere_center) - (sphere.radius**2)
    d = discriminant(a, b, c)
    print(d)
    if d >= 0: # negative discriminant implies solution lies in complex plane
        return t_sphere(a, b, c)
    else:
        return np.inf

if __name__ == '__main__':
    r = .2
    sphere_center = np.array([.5, 0, -2.5])
    light = np.array([0, 0, -2])
    hit_point = np.array([.5-r, 0, -2.5])
    ray_direction = light - hit_point
    surf_normal = normal_to_sphere(hit_point, sphere_center)
    k_shift = .001
    ray_start = hit_point + k_shift*surf_normal
    
    c = np.inf
    print(np.linalg.norm(b))
    print(75**0.5)



