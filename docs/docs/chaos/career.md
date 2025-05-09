---
title: Lorem ipsum dolor sit amet
status: new
---

# TBD

## ascascasc

When you select 32-bit color your computer uses 24 bits for the actual colors (many computers call this "true color") plus another 8 bits for the alpha channel (transparency). This produces 16,777,216 possible colors (256^3, ignore the alpha channel) or 4,294,967,296 colors (256^4, include the alpha channel), and has been the standard for a long time, for almost all applications this is more colors than the human eye can discern (the human eye can only detect about 10 million colors).

There are systems which offer even more colors, such as 48-bit color (or 64-bit color if including the alpha channel, which is often called "deep color"). This is largely limited to professional graphics design software in the VFX industry though.

https://en.wikipedia.org/wiki/Color_depth
https://en.wikipedia.org/wiki/Gamut

OpenCL/CUDA vs Compute Shaders:

Although APIs such as OpenCL and CUDA are already available for general purpose computation on the GPU, they are completely separate from OpenGL. Compute shaders are integrated directly within OpenGL,
and therefore are more suitable for general computing tasks that are more closely related to graphics rendering. OpenCL/CUDA are similar but intended to be much more generic, they are used for GPGPU computation in fields other than computer graphics as well, and they also target other hardware like some powerful Intel CPUs on workstations.

Why using premultiplied alpha is the standard?

Premultiplied alpha is closed under composition, non-premultiplied alpha is not! Note that it only matters when we have interpolation and filtering, but has nothing to do with blending or compositing images. For detailed explanations see [Alpha compositing](https://en.wikipedia.org/wiki/Alpha_compositing#Straight_versus_premultiplied) and CMU 15-462/662 Lecture 08 P31.




