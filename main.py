from time import time 
# ^^computationally intensive code so benchmarking execution time (alternative module with more granular insights: cProfile)
import math
import numpy as np
import matplotlib.pyplot as plt


#################### coordinates 

# DISPLAY PLANE: transform from display pixels:
# i = 0 : ncolumns-1, j = 0 : nrows-1
# to NDC = normalized 'device' coords:
# x = -1 : 1, y = -nrows/ncolumns : nrows/ncolumns

def xd_from_i(i, ncolumns):
    '''
    scale pixel indices along display width to xd in [-1, 1]
    --> set scene elements (positions and sizes) relative to this scaled 'x' so the FOV will contain the same scene even as the display size changes
    '''
    return (i - (ncolumns/2) + (1/2)) * (2/ncolumns)

def yd_from_j(j, nrows, ncolumns):
    '''
    scale by same factor as xd (since pixels are square, even if display isn't), so end up with yd in [-nrows/ncolumns, nrows/ncolumns] (nb: not in [-1, 1])
    '''
    return ((nrows/2) - j - (1/2)) * (2/ncolumns)

def convert_f_to_zd(ncolumns):
    '''
    convert the camera focal distance to the display plane z-coordinate per display x scaling
    '''
    return -f * 2/ncolumns

##################### camera helper functions

# field of view

def fov_degrees(focal_distance, frame_dimension):
    return (180/(2*pi))*2*atan((frame_dimension/2)/focal_distance)

# focal depth
# bokah


#################### camera generator

class Camera():
    def __init__(self, center = [0, 0, 0], azimuth = 0):
        '''
        generate instances of Camera: defined by its 'sensor' position (center) + any view tilt (rotational angles)
        '''
        self.center = np.array(center)
        self.azimuth = azimuth


#################### ray generator

class Ray():
    def __init__(self, start_point, direction):
        '''
        generate instances of Ray: defined by a starting position and direction (the direction doesn't need to be unit length)
        '''
        self.start_point = np.array(start_point)
        self.direction = np.array(direction)


#################### scene element generators

class Sphere():
    def __init__(self, center, radius, color, k_diffuse = 1, k_refl = 0.5, k_refr = 0.5, n = 1.5):
        '''
        generate instances of Sphere: defined by constant radius (surface - center distance)
        '''
        self.center = np.array(center)
        self.radius = radius
        self.color = np.array(color)
        self.diffuse = k_diffuse
        self.refl = k_refl
        self.refr = k_refr
        self.index = n

    def __str__(self):
        return 'Sphere object: center = ' + str(self.center) + ', radius = ' + str(self.radius)

class Plane():
    def __init__(self, point_on, normal, color, k_diffuse = 1, k_refl = 0.5, k_refr = 0.5, n = 1):
        '''
        generate instances of Plane: defined by a normal that's perpendicular to any on-plane vector, which can be established by any two points on the plane
            *texture applied separately in relation to the scene location
        '''
        self.point_on = np.array(point_on)
        self.normal = np.array(normal)
        self.color = np.array(color)
        self.diffuse = k_diffuse
        self.refl = k_refl
        self.refr = k_refr
        self.index = n

    def __str__(self):
        return 'Plane object: point on plane = ' + str(self.point_on) + ', normal = ' + str(self.normal)


#################### light generator

class Light():
    def __init__(self, center, color):
        '''
        generate instance of Light: parameters similar to other scene objects, but a Light *emits* light, so its color is active, not reactive (eg, its the end point in recursive reflection/refraction)
        '''
        self.center = np.array(center)
        self.color = np.array(color)

    def __str__(self):
        return 'Light object: position = ' + str(self.center) + ', color = ' + str(self.color)


# vector helper functions

# dot product, or if numpy: use np.dot(va, vb)
def dotvecs(vec_a, vec_b):
    dotvecs = 0
    for i in vec_a:
        for j in vec_b:
            dotvecs += i*j
    return docvecs


# unit-length vector - needs numpy module but could adapt to use dotvecs()
def vec_unit(vec):
    return np.array(vec)/np.linalg.norm(vec)


# surface normals: plane.normal attribute established by Plane.__init__

def surface_normal(hit_point, hit_element):
    if isinstance(hit_element, Plane):
        return hit_element.normal
    if isinstance(hit_element, Sphere):
        return normal_to_sphere(hit_point, hit_element.center)

def normal_to_sphere(point_on_sphere, sphere_center):
    '''
    the normal computed points outward
    '''
    return (np.array(point_on_sphere) - np.array(sphere_center))/np.linalg.norm(point_on_sphere - sphere_center)


#################### ray - scene element intersections

# ray-point intersection

def intersect_point(ray, point):
    '''
    returns t for point = ray.start + (t * ray.direction)
    '''
    t = []
    #print(len(point), point[0], ray.start_point[0])
    for i in range(len(point)):
        t.append((point[i] - ray.start_point[i])/ray.direction[i])
        if i > 0:
            if t[i] != t[i-1]:
                return np.inf
    return t[0]


# ray-sphere intersection

def discriminant(a, b, c):
    '''
    if the discriminant is < 0, the solution to the quadratic formula is complex -> no intersection -> t = np.inf
    '''
    return (b**2) - (4*a*c)

def t_sphere(a, b, c):
    '''
    solution to the quadratic formula:
    nb: the nearest intersection is the lower 't' value
    nb: if t < 0, the intersection is 'behind' the ray start point: treat as no intersection: t = np.inf
    '''
    return (-b - (discriminant(a, b, c)**0.5))/(2*a) if (-b - (discriminant(a, b, c)**0.5))/(2*a) > 0 else np.inf

def intersect_sphere(ray, sphere):
    '''
    return ray parameter t for nearest intersection with a sphere
    '''
    a = np.dot(ray.direction, ray.direction)
    ray_start_to_sphere_center = sphere.center - ray.start_point
    b = -2*np.dot(ray_start_to_sphere_center, ray.direction)
    c = np.dot(ray_start_to_sphere_center, ray_start_to_sphere_center) - (sphere.radius**2)
    d = discriminant(a, b, c)
    if d >= 0: # negative discriminant implies solution lies in complex plane
        return t_sphere(a, b, c)
    else:
        return np.inf


# ray-plane intersection

def intersect_plane(ray, plane):
    '''
    return ray parameter t for nearest intersection with a plane
    '''
    ray_dot_normal = np.dot(ray.direction, plane.normal)
    if abs(ray_dot_normal) > .0001: # if smaller, ray is nearly parallel to plane
        t_new = np.dot(plane.point_on - ray.start_point, plane.normal)/ray_dot_normal
        if t_new < 0: # intersection 'before' ray origin -> no in-scene intersection -> np.inf
            return np.inf
        return t_new
    else:
        return np.inf # treat ray as || to plane -> no visible intersection in scene


# ray-scene: nearest intersections

def find_nearest(ray, scene, hit_element = 0):
    '''
    cast ray and return the ray parameter t and Cartesian location of the nearest intersection plus the intersected object
    '''
    t = np.inf
    for element in scene:
        if isinstance(element, Light):
            t_new = intersect_point(ray, element.center)
        elif isinstance(element, Sphere):
            t_new = intersect_sphere(ray, element)
        elif isinstance(element, Plane):
            t_new = intersect_plane(ray, element)
        if t_new < t: # => iteratively reassign t to the most recent lowest t_new
            t = t_new
            hit_element = element
    return t, ray.start_point + (t * np.array(ray.direction)), hit_element


#################### color/shading

def shift_ray_start(start_point, normal, delta = 0):
    '''
    ray origin shifted slightly away from surface: the 'delta' fudge factor compensates for computational inaccuracy that may inadvertently locate the hit_point slightly off to the wrong* side of the hit_object surface; this matters for subsequent computation of next intersection for rays starting at hit_point
    * wrong is determined relative to the surface normal
    '''
    if not delta:
        delta = .0001
    return start_point + delta*normal

# ambient light: constant scaling factor k_ambient

def ambient_contrib(hit_element):
    return k_ambient * hit_element.diffuse * hit_element.color

# diffusely scattered light contributions from non-occluded lights

def diffuse_contrib(hit_point, hit_element):
    '''
    compute the additive color contribution from each light source as diffusely scattered at each intersection (hit) point with a direct line of sight to the light
    '''
    diffuse_color = np.array([0.0, 0.0, 0.0])
    k_shift = .0001
    hit_surf_normal = surface_normal(hit_point, hit_element)
    ray_start = shift_ray_start(hit_point, hit_surf_normal, k_shift)
    for light in lights:
        dir_to_light = light.center - ray_start
        ray_to_light = Ray(ray_start, dir_to_light)
        t_to_light = 1
        new_t, new_hit_point, new_hit_element = find_nearest(ray_to_light, scene)
        if new_t >= t_to_light: #not occluded
            diffuse_color += (((light.color) + hit_element.color)/2) * lambertian_factor(dir_to_light, hit_surf_normal) * hit_element.diffuse
    return diffuse_color

def lambertian_factor(dir_to_light, surface_normal):
    unit_dir_to_light = vec_unit(dir_to_light)
    unit_surface_normal = vec_unit(surface_normal)
    return np.dot(unit_dir_to_light, unit_surface_normal) if np.dot(unit_dir_to_light, unit_surface_normal) >= 0 else 0


# fresnel governed contributions from reflected and refracted rays traced back from the primary ray to a light source or to background (no object or light intersected) or to a total internal reflection point or to a maximum number of recursions (depth)

def fresnel_contrib(t, start_point, direction, start_element, depth = 2):
    '''
    recursively trace rays' reflections and refractions, compounding the rays' fresnel-governed contributions to the the primary ray; depth limits the number of recursions - an alternative would be to halt recursion once the compounded contribution is less than a given minimum
    nb: as for diffuse contributions, incident ray color (intensity) should be scaled by cos angle of incidence to surface normal - NOT YET ADDED
    '''
    if type(hit_element) == int or t == np.inf: # or TIR
        return np.array([0.0, 0.0, 0.0])
    elif start_element in lights or depth == 0:
        return start_element.color # ideally, this would be scaled inversely with distance
    else:
        depth -= 1
        surf_normal = surface_normal(start_point, start_element)
        start_point_shifted = shift_ray_start(start_point, surf_normal)
        refl_next_direction = 2*np.dot(direction, surf_normal)*surf_normal # angle incidence = angle reflection
        refr_next_direction = direction # NOT ACCURATE! NEEDS TO REFLECT SNELL'S LAW
        refl_ray = Ray(start_point_shifted, refl_next_direction) 
        refr_ray = Ray(start_point_shifted, refr_next_direction)
        t_refl, refl_next_hit_point, refl_next_hit_element = find_nearest(refl_ray, scene + lights)
        t_refr, refr_next_hit_point, refr_next_hit_element = find_nearest(refr_ray, scene + lights)
        if t_refr: # surf_normal > 0: FIX THIS - check the direction of the surface normal
            n_from = 1 # from 'outside' to 'inside' so this is air
            n_to = start_element.index
        else:
            n_from = start_element.index
            n_to = 1 # air
        k_refl = 0.5 # FUDGE FACTOR - need to compute Fresnel reflection coefficient
        k_refr = 0.5 # ^^^DITTO
        return start_element.color * ((start_element.refl*fresnel_contrib(t_refl, refl_next_hit_point, refl_next_direction, refl_next_hit_element, depth)) + (start_element.refr*fresnel_contrib(t_refr, refr_next_hit_point, refr_next_direction, refr_next_hit_element, depth)))
        

# indirect but directional (Fresnel-governed)
# compute the surface normal at the hit point
# apply Fresnel ratios to 
# indirect: recursively cast ray from previous intersection, find nearest intersection until base cases:
    # 1) count recursions: if recursive depth exceeds some number, assign 'emitter' the color of the object illuminated ambiently (**if not in shadow - compare to stored map of shadow coords computed in a prior step**);
    # 2) if emitter/light source, recursively 'fill in' values for color based on that emitter/light source
# the recursion will then compute the traced ray color value back to the original hit point; the result will be an additive contribution to the pixel value


#################### main

if __name__ == "__main__":
    start = time()
    # TO ADD: read in scene parameters from file

    # Display plane
    display_scale = 5
    display_width = 16 * display_scale
    display_height = 9 * display_scale
    fov_scale = 1 # fov inversely proportional to fov_scale
    f = (display_width/2) / fov_scale
    zd = convert_f_to_zd(display_width)

    # Camera
    c = Camera([0, 0, 0])

    # Scene: generate spheres, planes, light sources
    # units (!): display coords are scaled to x in [-1, 1] with aspect ratio maintained (y scaled by nrows/ncolumns); to maintain FOV, z scales with display width (this choice assumes display width >= display height so will have a greater impact on potential edge distortions)
    
    small_radius = 0.2
    large_radius = 15
    spheres = [Sphere([j*fov_scale/10, abs(j/2)/10, -1-(abs(j)/10)], small_radius, [.4, 0, .4], 1, .5, .5, 1.5) for j in range(-30, 35, 5)]
    spheres.append(Sphere([0, -large_radius-(1*small_radius), -2.5], large_radius, [.2, .35, .3], 1, 1, 0, 1))
    planes = [Plane([0, -1.5*small_radius, 0], [0, 1, 0], [.1, .35, .6], 1, .5, .5, 1.3)]
    lights = [Light([-.25, small_radius/4, -.5], [1, 1, 1]), Light([1.5, 2 + small_radius, -2], [.8, .8, .8])]
    k_ambient = 0.5
    background_color = np.array([0.1, 0.1, 0.1])
    scene = spheres + planes

    # set up array to store pixel colors: row_index, col_index, [r, g, b]
    img = np.zeros((display_height, display_width, 3))
    colors = ''

    # core logic
    for j in range(display_height):
        yd = yd_from_j(j, display_height, display_width)
        for i in range(display_width):
            xd = xd_from_i(i, display_width)
            pixel_ray = Ray(c.center, [xd, yd, zd])
            t, hit_point, hit_element = find_nearest(pixel_ray, scene + lights)
            if hit_element != 0:# hit_element = 0 means no intersection found
                c_ambient = ambient_contrib(hit_element)
                #c_diffuse = diffuse_contrib(hit_point, hit_element)
                #c_fresnel = fresnel_contrib(t, hit_point, pixel_ray.direction, hit_element, 5)
                color_xy = c_ambient # + c_diffuse + c_fresnel
            else:
                color_xy = background_color
            img[j, i, :] = color_xy
            colors = colors + ' ' + str(color_xy)
    image_filename = 'raytray_image.png'
    plt.imsave(image_filename, img)
    end = time()
    print(f'Image saved as {image_filename}\nDisplay: {display_width} x {display_height}\nTime to compute: {end - start} s')
