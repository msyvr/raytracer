### Python raytracer
- based on [Whitted](https://www.cs.drexel.edu/~david/Classes/Papers/p343-whitted.pdf) (recursive Fresnel-governed reflection/refraction)
- !not! performance optimized

#### Description: ray tracing
- A 3D scene volume is rendered to a 2D display by simulating optical interactions with scene elements (human vision).
- To flatten the 3D scene to 2D, each display pixel is associated with the nearest scene interaction along a line extending from a virtual camera/eye, through the scene pixel, and into the scene volume to the nearest intersection aka 'hit' point.
- All optical interactions contributing to the light at that 'hit' point are integrated to yield the pixel value. Pixel values represent color as [red, green, blue]. 
- The number and arrangement of display plane pixels is:
  - n_vertical_pixels * n_horizontal_pixels

#### Output: image file
- With matplotlib, a .png file is generated with imsave().
- If no matplotlib, can write to .ppm file, [formatted as](http://netpbm.sourceforge.net/doc/ppm.html):
  - P3 (width: int) (height: int) 'r' 'g' 'b' 'r' 'g' 'b'  ... 'r' 'g' 'b' \n
    - for .ppm files, 'r' 'g' 'b'  are each in (usually) range(256) (and maximally limited to range(2^16))

#### Details: Scene elements + optical interactions
- The scene consists of object elements (spheres, planes) and lights. Scene elements have attributes such as color, surface finish, and refractive index.
- NB: light consists of photons, not rays; here, the light effectively 'emitted' from a scene element surface point toward the observer is an approximation, both due to the ray approximation of light and to the homogeneous and approximate optical properties assigned to scene elements.

#### Reference: Model

                    Ambient Light
                    |||||||||||||||||||||||||||||||||||||||
                    |||||||||||||||||||||||||||||||||||||||
                                                        ====
                Display Plane                           ====
                    |\              _____               ====
                    | \            /     \   Scene      ====
                    |  \          /       \     Objects ====
      Observer      |   \        (         )            ====
       \            |    \        \       /     ______  ====
       O) - - - - - |- >  \ - - - *\     /     (      ) ====
       /             \    |          ---        (    )  ====
                      \   |                      (  )   ====
                       \  |                       --    ====
                        \ |                             ====
                         \|                             ====
                                      ***   Scene
                                      ***   Light

#### Use
- License: MIT
- Language: Python (built on python 3.9.7)
- Modules used:
  - time (can be omitted without affecting the output)
  - numpy
  - matplotlib
- This file is executed stand-alone - no other file or framework dependencies aside from the python modules imported.
