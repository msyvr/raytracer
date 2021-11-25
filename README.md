### Python ray tracer: example image series
Sequential images include optical effects from ambient light only to shadows and indirect lighting.

#### Ambient light only
![](images/example_ambient.png)
#### Diffusely scattered + ambient light
![](images/example_diffuse.png)
#### Shadows + diffusely scattered + ambient light
![](images/example_shadowsdiffuse.png)

### This code
- an exercise, not intended for production use
- !not! performance optimized: ray tracing is computationally expensive and this implementation is slow
  - performance optimization roadmap and status: details on the project page

References: 
- [Computer Graphics from Scratch - Ray Tracing Overview (scratchapixel)](https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-overview)
- [An improved illumination model for shaded display (Whitted)](https://www.cs.drexel.edu/~david/Classes/Papers/p343-whitted.pdf)

#### Ray tracing basics
- This code renders a 3D scene volume to a 2D display using ray tracing
  - each 2D display position (pixel) is mapped* to a point in the 3D volume
  - 'reverse' ray-trace from the hit point, computing optical interactions at intersections, then integrate over these to set the associated pixel's color value
  - consider ambient light, diffuse surface scattering, occlusion/shadows, and indirect light from directional contributions (reflection and refraction, computed recursively)
```
                    Ambient Light
                    |||||||||||||||||||||||||||||||||||||||
                    |||||||||||||||||||||||||||||||||||||||
                                                        ====
                Display Plane                           ====
                    |\              _____               ====
                    | \            /     \   Scene      ====
                    |  \          /       \   Objects   ====
        Camera      |   \        (         )            ====
        |           |    \        \       /     ______  ====
        O)- - - - - |- >  \ - - - *\     /     (      ) ====
        |            \    |          ---        (    )  ====
                      \   |                      (  )   ====
                       \  |                       --    ====
                        \ |                             ====
                         \|                             ====
                                      ***   Scene
                                      ***   Light
```
* 3D -> 2D mapping:
  - parametrize the line ('primary ray') between a virtual camera/eye** and the scene pixel
  - compute the nearest intersection point between the line and scene elements (i.e., find the nearest 'hit')
  - ** the camera and scene are on opposite sides of the display plane

#### Display plane
- The number and arrangement of display plane pixels is:
  - n_vertical_pixels * n_horizontal_pixels
- Pixel values represent color as [red, green, blue]. 

#### Scene elements
- Currently:
  - spheres: position, radius, color
  - planes: point on plane, normal, color
  - lights: position, color
- Elements' optical properties include:
  - Lambertian coefficient: diffuse surface scattering
  - Fresnel coefficients: surface reflectivity, index of refraction

#### Input
Elements are represented by classes; class instances are generated based on geometric, color, and material parameters.

#### Output: image file
- With matplotlib, a .png file is generated via imsave().
- If no matplotlib, can write to .ppm file, [formatted as](http://netpbm.sourceforge.net/doc/ppm.html):
  - P3 (width: int) (height: int) 'r' 'g' 'b' 'r' 'g' 'b'  ... 'r' 'g' 'b' \n
    - for .ppm files, 'r' 'g' 'b'  are each in (usually) range(256) (and maximally limited to range(2^16))

#### Details: Scene elements + optical interactions
- The scene consists of object elements (spheres, planes) and lights. Scene elements have attributes such as color, surface finish, and refractive index.
- NB: light consists of photons, not rays; here, the light effectively 'emitted' from a scene element surface point toward the observer is an approximation, both due to the ray approximation of light and to the homogeneous and approximate optical properties assigned to scene elements.

#### Use

- Modules:
  - numpy
  - matplotlib
  - time (optional)

- Run time:
  - !!NB!! display_scale parameter adjustment will determine execution time:
    - display default is 16:9 * display_scale
    - run time scales with number of pixels, so with display_scale**2 
  - WARNING: ray tracing is computationally expensive and, in its current state, this code is not suitable for real-time frame generation
    - Nvidia has some great tech and resources for real time image generation incorporating ray tracing: [Intro to NVIDIA RTX and DirectX ray tracing tech] (https://developer.nvidia.com/blog/introduction-nvidia-rtx-directx-ray-tracing/)

License: MIT

Language: Python (built on python 3.9.7)
