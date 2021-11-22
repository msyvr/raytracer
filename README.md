Ray tracer
in python
should be in rust 
but I'm working on python atm
:)

# Scene rendered:
# Pixel values represent color as (red, green, blue) with each in 0..255
# The number and arrangement of pixels is: 
# n_vertical_pixels * n_horizontal_pixels

# The output file format is .ppm, specified as:
# P3 (width: int) (height: int) (r) (g) (b) (r) (g) (b) ... (r) (g) (b)\n
# (nb: there's a newline after the last value and whitespace or newline separates elements)
# r, g, b vals are often 0..255 and are limited to 0..65535

# Convention: horizontal = x axis, vertical = y axis, z axis is normal to the display plane

# To have the pixels ordered as [(r1, c1), (r1, c2), ...], the nested loop for computing pixel values is structured as:
# outer loop --> vertical (y)
# inner loop --> horizontal (x)

Render a scene consisting of light sources + objects/surfaces

Objects, surfaces can have: color, reflectance, index of refraction properties 

Rendering consists of assignment of a color value to each display pixel.

The core concept is that only those 'rays' passing through the display plane to reach the observer contribute to the rendered scene, so those are the only ones which need to be computed. The display plane pixel that the ray passes through is assigned the 'value' of the scene point that that specific pixel-ray intersects.

(NB: light consists of photons, not rays, and the light effectively emitted from the surface toward the observer is generally an approximation, taking into account a limited set of factors in determining the light that's incident at the nearest-surface point - which is used to yield the pixel value.)

                    Indirect Light
                    |||||||||||||||||||||||||||||||||||||||
                    |||||||||||||||||||||||||||||||||||||||
                                                        ====
                Display Plane                           ====
                    |\              _____               ====
                    | \            /     \   Scene      ====
                    |  \          /       \     Objects ====
Observer            |   \        (         )            ====
       \            |    \        \       /     ______  ====
       O) - - - - - |- >  \ - - - *\     /     (      ) ====
       /             \    |          ---        (    )  ====
                      \   |                      (  )   ====
                       \  |                       --    ====
                        \ |                             ====
                         \|                             ====
                                ||||||||||||||||||||||||||
                                ||||||||||||||||||||||||||
                                Indirect light

Notes on the output file format: PPM
from http://netpbm.sourceforge.net/doc/ppm.html:

A PPM file consists of a sequence of one or more PPM images. There are no data, delimiters, or padding before, after, or between images.

Each PPM image consists of the following:

    A "magic number" for identifying the file type. A ppm image's magic number is the two characters "P6".
    Whitespace (blanks, TABs, CRs, LFs).
    A width, formatted as ASCII characters in decimal.
    Whitespace.
    A height, again in ASCII decimal.
    Whitespace.
    The maximum color value (Maxval), again in ASCII decimal. Must be less than 65536 and more than zero.
    A single whitespace character (usually a newline).
    A raster of Height rows, in order from top to bottom. Each row consists of Width pixels, in order from left to right. Each pixel is a triplet of red, green, and blue samples, in that order. Each sample is represented in pure binary by either 1 or 2 bytes. If the Maxval is less than 256, it is 1 byte. Otherwise, it is 2 bytes. The most significant byte is first.

    A row of an image is horizontal. A column is vertical. The pixels in the image are square and contiguous.

    In the raster, the sample values are "nonlinear." They are proportional to the intensity of the ITU-R Recommendation BT.709 red, green, and blue in the pixel, adjusted by the BT.709 gamma transfer function. (That transfer function specifies a gamma number of 2.2 and has a linear section for small intensities). A value of Maxval for all three samples represents CIE D65 white and the most intense color in the color universe of which the image is part (the color universe is all the colors in all images to which this image might be compared). 