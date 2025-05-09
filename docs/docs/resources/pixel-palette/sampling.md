



# Sampling

## Basic

Higher sampling rates reduces the amount of noise in the images, but at the expense of increased rendering time.

Camera samples are also called AA samples because these samples are used for anti-aliasing. AA samples = number of primary rays cast per pixel.

Get to known some big renderer names: Arnold, V-Ray, Redshift, Blender's Cycles, RenderMan.

V-Ray uses a method called adaptive sampling, where the renderer adjusts the number of samples dynamically based on the content of the scene.

The noise threshold is a parameter used in many rendering engines to control when the renderer should stop refining (sampling) a particular image or pixel area. If the noise level in a specific area is below the set noise threshold, the renderer will stop adding more samples to that area.

Most modern renderers include some form of adaptive sampling techniques. In renderers with adaptive sampling, the noise threshold helps in dynamically adjusting how many samples are needed for different parts of the image.

In Arnold, diffuse, specular, transmission, sss, and volume sampling rates are expressed for each Camera (AA) sample or primary ray. This AA sampling rate can, therefore, be considered as a global multiplier for all the other ones. For example, if AA samples is 3 and diffuse samples is 2, the total amount of diffuse samples per-pixel is 3*3 * 2*2 = 36.

Subsurface Scattering (SSS) is a mechanism of light transport in which light penetrates the surface of a translucent object, is scattered by interacting with the material, and then exits the surface at a different point. When light hits a surface with subsurface scattering properties, part of the light is reflected off the surface (specular reflection), part is absorbed (diffuse), and the rest penetrates into the material (SSS). Once inside the material, the light bounces around, scattering in random directions. After multiple internal scatterings, some of the light rays find their way back to the surface and exit the material at different points from where they entered. The path that light takes inside the material and the distance it travels before re-emerging affect the color and the soft appearance typical of SSS materials.

Modern path tracers often use a technique called "random walk subsurface scattering" to simulate SSS. This process is computationally intensive because it requires simulating many potential paths to achieve a realistic effect.

