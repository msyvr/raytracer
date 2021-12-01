sphere_small_radius = 0.2
sphere_small_color = [.4, 0, .4] # muted purple
sphere_range_min

large_radius = 20
    spheres = [Sphere([j*fov_scale/10, abs(j/2)/10, -1-(abs(j)/10)], small_radius, [.4, 0, .4], .75) for j in range(-30, 35, 5)]
    spheres.append(Sphere([0, -large_radius+(.5*small_radius), -4.5], large_radius, [.2, .35, .3], 0.4))
    planes = [Plane([0, -small_radius, 0], [0, 1, 0], [.1, .35, .6], .4)]
    lights = [Light([-.25, small_radius/4, -.5], [1, 1, 1]), Light([1.5, 2 + small_radius, -2], [.8, .8, .8])]
    k_ambient = 0.1
    background_color = np.array([0.1, 0.1, 0.1])
    scene = spheres + planes