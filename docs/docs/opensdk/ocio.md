
# OpenColorIO

- [Source Code](https://github.com/AcademySoftwareFoundation/OpenColorIO)
- [Documentation](https://opencolorio.readthedocs.io/en/latest/)
- [Configuration for ACES](https://opencolorio.readthedocs.io/projects/config-aces/en/latest/)


## Color Science Basics

- Color is the visual byproduct of the spectrum of light as it is either transmitted through a transparent medium, or absorbed and reflected off a surface.
- Complementary colors (aka opposite colors) are pairs of colors which, when combined or mixed, cancel each other out by producing a grayscale color like white or black. When placed next to each other, they create the strongest contrast for those two colors. Complementary color pairs include red–cyan, green–magenta and blue–yellow, or any pairs that sit opposite to each other on the [color wheel](https://www.canva.com/colors/color-wheel/).
- In the HSV color model, hue is measured in degrees from 0~360, saturation and value are expressed in 0-100% percents. Complementary colors must have a 180 degrees difference in hues.
- Lift, Gamma and Gain is a set of controls designed for primary color correction. They allow colorists to manipulate shadows (Lift), midtones (Gamma), and highlights (Gain) to achieve the desired look for an image. Offset is another control used to adjust the overall brightness and color balance across the entire image. More granular control on specific parts of the image can be achieved by using mattes or masks.
- Luminance measures the amount of light that is emitted, passed through or reflected from a surface from a solid angle, in candela per square meter (cd/m²), also known as nits. Illuminance measures the total amount of light falling onto and spreading over a given surface area, in lux (lx) or lumens per square meter (lm/m²). Luminance and illuminance are photometric quantities, they are the equivalents of radiometric quantities radiance and irradiance.

---

<div class="annotate" markdown>
- A typical human eye will respond to wavelengths from ~ 380 to 750 nanometers.(1)This visible band sits between the infrared (with longer wavelengths) and the ultraviolet (with shorter wavelengths), collectively known as optical radiation.
- The human eye can detect a luminance from 10<small>^−6^</small> to 10<small>^8^</small> nits(2), or 14 stops, but can only adapt to about 2-3 orders of magnitude at a time via the iris. This means that, at any given time, the eye can only sense a contrast ratio of 1,000. Larger ranges take time and require neural adaptation. The eye takes ~20–30 minutes to fully adapt from bright sunlight to complete darkness and becomes 10<small>^4^</small> to 10<small>^6^</small> times more sensitive than at full daylight. It takes ~5 minutes to adapt from darkness to bright sunlight.
- Humans have three types of cones (<span class="icon-blue">S</span>, <span class="icon-green">M</span> and <span class="icon-red">L</span>), each sensitive to different wavelengths of light (blue, green and red).
- The [Weber–Fechner law](https://en.wikipedia.org/wiki/Weber%E2%80%93Fechner_law) states that human perception is logarithmic, the perceived intensity is proportional to the logarithm of the stimulus intensity, so we perceive things by the relative change (e.g. in brightness), not the actual change.(3)
- [Metamers](https://en.wikipedia.org/wiki/Metamerism_(color)) are colors with different spectral power distributions (SPDs) but have the same visual appearance. This is possible because different SPDs can map into the same tristimulus values and hence look identical. However, when the lighting conditions change, the two colors may no longer match since different SPDs reflect different wavelengths of light. This phenomenon is known as [metamerism](https://en.wikipedia.org/wiki/Metamerism_(color)).
</div>

1. [Spectral Colors](https://en.wikipedia.org/wiki/Visible_spectrum#Spectral_colors)
2. [Luminances grouped by order of magnitude](https://en.wikipedia.org/wiki/Orders_of_magnitude_(illuminance)#Luminance)
3.  - The human eye can perceive a range of light intensities on a logarithmic scale. This allows us to see objects and details in both dark shade and bright sunlit areas.
    - The human ear has a logarithmic response to sound levels. We can hear very soft noises and tolerate very loud ones.
    - The perceived reduction of the length of a fixed period as we age suggests a logarithmic scale to time.

## Color Space

The [CIE 1931 color space](https://en.wikipedia.org/wiki/CIE_1931_color_space) is the standardized reference color space used to describe all other color spaces. The 2D horseshoe shape is the "CIE 1931 color space chromaticity diagram", with luminance (the third dimension) factored out. Note that the CIE XYZ primaries are not physically realizable.

- The outer curved boundary of the diagram is called the spectral locus. It represents the chromaticity of monochromatic light (pure colors) with wavelengths from 380~700 nm. Each point on the locus corresponds to a specific wavelength of light.
- The color temperature curve, aka the black body curve/locus, is a downward curve in the middle that represents the trajectory of a blackbody's color as its temperature increases. Each point on the curve corresponds to a color temperature.
- The interior of the diagram can be divided into 20 color zones, each with an average dominant wavelength.
- Within this diagram, it's natural and intuitive to encode colors in HSV, where hue (H) corresponds to the dominant wavelength, saturation (S) = distance from white point, and value (V) = height out of plane.

???+ info "Color Spaces"

    This table lists some of the most common color spaces, ordered from smaller to larger in terms of gamut size.\
    Note that ProPhoto RGB covers nearly all perceivable colors, but ACES has even wider gamuts.\
    ProPhoto RGB is more focused on photography and print, while ACES is tailored for film and television production.

    Color Space  | Description                                         | White Point
    -------------|-----------------------------------------------------|-------------
    sRGB         | Standard for web and many consumer devices          | D65
    Rec.709      | Standard for HDTV                                   | D65
    Adobe RGB    | Developed for professional photography and print    | D65
    DCI-P3       | Used in digital cinema and high-end displays        | D63
    Rec.2020     | Standard for UHDTV and HDR content                  | D65
    ProPhoto RGB | Used in high-end photography and imaging            | D50
    ACES         | Used in VFX for HDR and wide gamut                  | ACES White

    Rec.709/sRGB
    DCI-P3 specifications are designed for viewing in a fully darkened theater environment.
    Rec.2100

Gamut is the range of colors (hues and saturations) that can be represented within a particular color space. When people refer to gamut in the CIE 1931 chromaticity diagram, it is a triangle subset of this diagram. Note that color gamut does not have to be a triangle. Monitor's gamut is triangular only because additive colors (light) follow [Grassman's laws](https://en.wikipedia.org/wiki/Grassmann%27s_laws_(color_science)) where color matching is linear.

Gamut is often defined by three primary colors (red, green and blue) which are called color primaries, they are used to create all other colors within the same color space. Each primary is a specific point `(x,y)` on the CIE 1931 chromaticity diagram. These coordinates determine the exact hue and saturation of each primary color. Since different color spaces define different primaries, the same RGB triplet is not the same color. For instance, `rgb(255,0,0)` in color space A and in color space B are different colors. If B is a larger color space, it will give us a redder red, which is "out-of-gamut" in color space A. The process of converting colors from one color space to anothre is called gamut mapping.

Note that RGB is not the only set of color primaries, there are other sets of primaries. These refer to the concept of color (encoding) models. For example, there's also the CMY, YUV, LAB and HSL color models. The CIE 1931 reference color space itself uses the XYZ color model, where the three primaries X, Y, Z are hypothetical but good for mathematical color representation.

The white point is a reference point in a color space that defines what is considered "white" under specific lighting conditions. It sits on the black body curve and is associated with a color temperature (e.g. 3200K), measured in Kelvin (K), which describes the hue of the white light.

???+ info "White Point"

    White Point  | Color Temperature | Usage and Scenario
    -------------|-------------------|-----------------------------------------------------------------------
    D65          | ~6500K            | Represents average daylight
    D63          | ~6300K            | Used in digital cinema and high-end displays.
    D50          | ~5000K            | Common in printing and graphic arts, represents warmer daylight
    D55          | ~5500K            | Used in photography and film for slightly warmer daylight conditions
    D75          | ~7500K            | Represents cooler, bluer daylight, less commonly used
    Illuminant A | ~2856K            | Represents typical incandescent lighting
    ACES White   | N/A               | Unique to ACES, designed for wide range of lighting in film production

Gamma refers to the exponent in a power-law relationship that describes how the brightness of a pixel is encoded in a digital image. Standard gamma values are 2.2 and 2.4. The gamma curve is a transfer function used to correct for the nonlinear response of display devices and the human eye. However, it is not the only transfer function, there are linear, logarithmic and other transfer functions. For example, PQ (Perceptual Quantizer) and HLG (Hybrid Log-Gamma) are both transfer functions specifically designed for HDR content and displays.

!!! note

    Transfer function is not an inherent part of a color space, it is a separate concept that deals with encoding and decoding color values.\
    A color space often provides a transfer function for convenience, but it is not a defining characteristic. For instance, linear-sRGB color space uses the sRGB color gamut, but doesn't have a transfer function since color values are in scene-linear.

At the bare minimum, these are the things to bake into your brain:

<div class="annotate" markdown>
- Color space = Gamut + White point, and it  (although not a defining characteristic)
- Color management often involves 3 color spaces
    - source (capture) color space
    - intermediate (working) color space (1)
    - destination (delivery) color space
- from source color space &rarr; intermediate color space, we need the input transform (IDT).
- from intermediate color space &rarr; delivery color space, we need the output transform (ODT).
</div>
1. ACES is often used as the intermediate color space since it encompasses a very wide color gamut.


Further readings:

- [A Beginner's Guide to (CIE) Colorimetry](https://medium.com/hipster-color-science/a-beginners-guide-to-colorimetry-401f1830b65a)

## Scene-referred vs Display-referred

Color spaces can be categorized by the **image state** they are associated with.

=== "Scene-referred"

    Color spaces defined in relation to input devices (e.g. scenes captured by a camera or created by a renderer) are __scene-referred__. It means that the pixel values correspond to the actual physical luminance and color values of the scene. The data is linear and directly proportional to the light intensity in the real world. In other words, if you double the light intensity in the scene, the pixel value also doubles. This linear property is often referred to as **scene-linear**.

    Lighting, shading and rendering are typically done in scene-referred color spaces. This scene-linear property not only makes it easier to work with physically based calculations, but is also crucial for accurate image operations such as compositing, blending and certain types of color correction and anti-aliasing. Since scene-linear data does not have any nonlinear correction applied, it is not directly suitable for human perception or display.

    !!! warning

        Not all scene-referred data is necessarily scene-linear. Scene-referred data could be encoded in a non-linear fashion (e.g. log) for specific purposes (e.g. debugging and diagnostics).

=== "Display-referred"

    Color spaces defined in relation to output devices (e.g. monitors, television or projectors) are __display-referred__. It means that the pixel values are encoded for display on a physical device. The data is optimized for human perception by taking into account the display's limitations and characteristics. This is sometimes also referred to as **output-referred**.

    !!! warning

        Modifying an image in the display-referred color space limits the result to looking appropriate only on a specific display. The image can look very different on another display with different characteristics.

## Tone Mapping


In practice, tone mapping is the combination of these two since the HDR content's dynamic range will (almost) never match the display's color space. It does some color enhancement in the context of the display's capabilities, and then convert the working color space to the delivery color space (so that your working red can map to another red on the monitor).

today's goal of tone mapping:
- To reduce excessive dynamic range
- To customize the look (colour grading)
- To simulate human vision
- To adapt displayed images to a display and viewing conditions
- To make rendered images look more realistic

While the legacy tone map only intends to preserve limited details and contrast so that it doesn't look washed out on the SDR display, a photographic tone map aims to enhance details and contrast to take full advantage of the display's capabilities. There is a collection of techniques that determine the scene brightness in the previous frame and slowly adapt the exposure parameter. They mimick how the human eye adapts to different lighting conditions, such that the scene gets brighter in dark areas (using a higher exposure) and darker in bright areas (using a lower exposure). Advanced techniques even leverage the power of machine learning to produce better cinematic HDR content. Think of it as a way to enhance visual fidelity, rather than just a color convertion step using a single mathematical function.

dynamic tone mapping happens inside the view transform?

even the best displays come nowhere close to the range of luminances in the real world, there still needs to be a tone mapping step to compress and convert from scene referred to output referred on HDR displays.

In the future, when consumer monitors become more capable, the same films will look better as they require less tone-mapping and the original intent can be more accurately rendered.

## Transfer Function

- OETF (opto-electronic transfer function) converts scene-linear luminance values to non-linear electrical signals. It involves a quantization process that restricts the signal to a certain bit depth. This ensures that the image data can be efficiently stored and transmitted through the HDMI or DP cable.
- EOTF (electro-optical transfer function) converts non-linear electrical signals to visible light emitted by the display. It describes how digital signal values are converted into visible light by the display device. EOTF is typically implemented on the display side so we have no direct control over it a user or content creator.
- OETF and EOTF are both non-linear functions, but they are independent. EOTF is not a simple inversion of OETF.
- OETF is about capturing and encoding, EOTF is about decoding and displaying.
- OOTF (opto-optical transfer function) describes the overall transformation, OOTF = OETF + EOTF.
- OOTF ensures that the final displayed image maintains the intended appearance on the target display.

!!! question "Electrical Signals"

    In the context of display technology, electrical signals are often normalized to the range [0,1] to represent the intensity of light emitted by a display, but the interpretation of these values can vary depending on the type of display. For example, a signal value of 0.5 might correspond to 50~150 nits on SDR displays but 300~500 nits on HDR displays.

!!! note

    A tone mapper is a function that simply maps a range of values to another range of values, but a transfer function is also concerned with physically changing the state of the data from optical to electrical and vice versa (although it is not done by the transfer function itself), so they are totally different things!

    - Tone mapping is generally used to apply a "look", such as the popular filmic S-curve. It adds some contrast in the shadows and a nice roll-off that gradually brings luminance level to 100%. Think of it as a post-processing step just like applying a filter over an image. The post-processing effects should be computed in linear space so it must be done before the transfer function or color space conversion.
    - A transfer function changes the form of the data, hence the name "transfer". It is not a post-processing step used to apply a custom look. While a transfer function also redistributes a range of values to another, it's for a different purpose. When we send our image to the display or save it to a file on disk, OETF remaps the values in order to use the storage more efficiently, that is, with a limited amount of bits, we want to use more bits for the darker areas and less on the brighter areas. When a monitor sends electrical signals to the actual pixels on the screen, EOTF remaps the values to take advantage of the display's capabilities.
    - Tone mapping operates on 16 or 32-bit floats to maintain precision during the process, it does not change the data format so the output is still floating-point. Transfer functions often involve a change in data format, it needs to convert floating-point values to 10 or 12-bit integer values when encoding image data for storage or transmission. This is necessary to reduce data size and match the capabilities of the storage medium or transmission channel.
    - Transfer functions are always applied as part of the standard process. Since EOTF is built into the display's design and operation, OETF must be applied when sending images to the display. In contrast, tone mapping is just an optional tool used to adapt the content to a creative look. You don't have to apply a tone mapper, only if you want to.

### Transfer Function in SDR Workflows

Traditionally, EOTF used for CRT displays was a standard 2.2 gamma curve. This is because the non-linear relationship between the applied voltage and electron output in a CRT picture tube follows such a standard gamma curve. To compensate for that non-linear response of CRTs, image data is gamma encoded (OETF applies an inverse gamma curve) before getting sent to the display. The combined OOTF results in a linear correspondence between the original luminance and the displayed light intensity. In summary, both OETF and EOTF are standard gamma curves, a world of simplicity!

### Transfer Function in HDR Workflows

With modern HDR, 4K and 8K displays, the idea is kind of similar, but it's a very complex topic filled with nuances.

Today, [Rec.2100](https://en.wikipedia.org/wiki/Rec._2100) recommends two standard HDR transfer functions, [PQ (Perceptual Quantization)](https://www.color.org/hdr/04-Timo_Kunkel.pdf) and [HLG (Hybrid-Log-Gamma)](https://en.wikipedia.org/wiki/Hybrid_log%E2%80%93gamma).

=== "HLG (Hybrid-Log-Gamma)"

    - HLG is designed for broadcast, streaming or scenarios where SDR compatibility is desired, so it is not our focus.
    - The HLG transfer function is primarily an OETF. It is used to encode the light captured by cameras into a digital signal. The HLG curve was designed to be backward compatible with SDR displays. The lower half of the signal values use a gamma curve, and the upper half is logarithmic. HLG is also a standard HDR video format that uses the HLG transfer function, Rec.2020 color primaries and a 10-bit bit depth.
    - HLG is a relative scene-referred signal, meaning that HLG-enabled displays automatically adjust light levels based on the content and their display capabilities. HLG does not require metadata to be transmitted with the video stream, as the same signal can be used for both SDR and HDR displays. For PQ, we need to manage metadata.


=== "PQ (Perceptual Quantization)"

    - PQ is designed for high-quality HDR displays where you have control over the viewing environment, which is well-suited for our needs.
    - The PQ transfer function (standardized by SMPTE ST 2084) is primarily an EOTF. It aims for perceptually uniform quantization based on Barten's model to better align with human perception. A PQ-encoded signal can represent luminance levels from 0.0001 nits to 10,000 nits. The PQ curve is not backward compatible with the BT.1886 EOTF (i.e. the standard SDR gamma curve), so PQ-encoded content requires HDR-capable displays to be viewed correctly.
    - PQ is an absolute display-referred signal, meaning that it is designed to map directly to the display's capabilities. This requires display devices to implement tone mapping to adapt the light levels. Display devices use metadata to interpret and display PQ-encoded content correctly. This metadata can be either static or dynamic, which includes information like the mastering display's color primaries and the content's min/max/avg luminance levels (e.g. MaxFALL and MaxCLL).

<div class="annotate" markdown>
Let's focus on HDR workflows using PQ. Here the focus is on converting scene-referred linear values (e.g. in ACES color space) to a display-referred format that the PQ EOTF can interpret. This involves encoding the content for HDR display using the PQ curve. This process is akin to an OETF, but it is not an OETF in the traditional sense as PQ is display-referred.(1)
</div>

1. The PQ curve is designed to be perceptually uniform, meaning it directly maps digital values to absolute luminance levels in a way that aligns with human perception. In this context, the traditional concept of OEFT as used in SDR workflows does not directly apply. In other words, we do not have or need an OEFT.

1. Check your display's HDR standards (e.g. HDR10, Dolby Vision) to see if it supports PQ.
2. Adjust settings in the display's menu and use calibration software to ensure it is operating in the correct HDR mode that supports PQ.
3. Encode the content (rendered output) for HDR display using the PQ curve, make sure to manage metadata.

!!! question "Do I need tone mapping?"

    In the HDR workflow with PQ, both content-side and display-side tone mapping might be applied, which is called **Dual tone mapping**.

    - Content-Side Tone Mapping is optional and used for creative control or specific target display adaptation.
    - Display-Side Tone Mapping is automatically done by the display which adapts PQ-encoded content to its capabilities and limitations.
    - So when do I need content-side tone mapping? or not?








## HDR Users Guide

VESA's [DisplayHDR](https://displayhdr.org/) specifications are open standards that help consumers identify a monitor's HDR capabilities. Common tiers include 400/600/1000 and 1400, where the number indicates the peak brightness in nits. Certified displays have wider color gamuts, 10+ bit depth, higher luminance levels and contrast ratios. You can check the [performance criteria details here](https://displayhdr.org/performance-criteria/). Other HDR standards also exist (e.g. HDR10, Dolby Vision) catering to various applications. Note that these standards can vary wildly in terms of peak brightness, color space and contrast ratios so the HDR experience differs significantly from one display to another.

!!! note

    A typical SDR display is capable of emitting luminance between 50 and 300 nits. While HDR displays can emit 400 &rarr; 2000 nits, the HDR standards allow for a maximum luminance of 10,000 nits.

    There is no standardized way to measure the contrast ratio, but it's often defined as the ratio of the max/min luminance that the display can produce. It is usually written as C:1 (e.g. 3000:1), but can also be expressed in stops by taking its base-2 logarithm where each stop doubles the amount of light. For example, a contrast ratio of 2 stops = 4 times as much light at the brightest pixel than at the darkest pixel. Dynamic range can also be measured this way, either as a ratio or in # of stops.

We need several pieces working together to ensure HDR content is properly rendered and displayed.

=== "Hardware"

    - The display itself must support one or more HDR standards, and color calibration must be done properly.
    - The connection between the graphics card and the display must support HDR. This means using HDMI 2.0+ or DisplayPort 1.4+ cables, which are capable of transmitting data (e.g. 12-bit color) for HDR content.
    - The graphics card and drivers must support HDR processing and output (e.g. output 12-bit color)

=== "Software"

    - The operating system must support HDR and provide settings to enable it.
    - The application, in our case the renderer, must be capable of rendering content in HDR. It needs to handle a wider range of brightness and color values during the rendering process.

!!! danger "Fake HDR"

    If the software does not natively render content in HDR but instead outputs on a HDR display by adjusting the brightness and contrast of the final rendered SDR image to fit a higher dynamic range, it is called ^^fake HDR^^ or ^^pseudo-HDR^^ that can lead to a degraded visual experience. This is because the process of stretching the dynamic range can distort colors. The conversion process can also introduce visual artifacts such as banding, where smooth gradients appear as distinct bands of color.

!!! tip

    To enable HDR on desktop for games:

    - Check your monitor's HDR standards and specs, learn the capabilities of your display.
    - Physically tune your display settings, if there's a review on [rtings](https://www.rtings.com/) that could be helpful.
    - At the OS level, enable HDR in the display settings and run the HDR calibration. This will tell the OS what your display's capabilities are. Note that the ^^Auto HDR^^ option on Windows must be disabled.
    - Open the NVIDIA Control Panel and select "Use NVIDIA color settings" under "Change Resolution", adjust the Output Color Format to use RGB and the Output Color Depth to use 10-bit or 12-bit. Depending on your hardware you may only have certain options available.
    - Make sure your game supports HDR and has it enabled, then enable ^^RTX HDR^^ in the NVIDIA app and click ^^Optimize^^. This often yields much better visual results compared to tweaking graphics settings yourself.
    - For games that don't support HDR, the ^^RTX HDR^^ option will convert SDR content to HDR using your GPU driver, but of course this is a compromise.

## HDR Developers Guide

HDR Formats include: HDR10, HDR10+, Dolby Vision, PQ10 and HLG.


### ????

HDR at the OS level? OS does the tone mapping? or use OCIO? could it be applying twice if both are used ?
While OS support for HDR is important for displaying HDR content directly on HDR-capable monitors, it is not a hard requirement, you can still create, process, and prepare HDR content within your software, even if the OS itself doesn't fully support HDR output.

I'm not sure if glimpse or glimpseRealtime has tone mapping. I think to ensure that the dynamic range of the rendered content fits within the capabilities of our HDR display, we are just manually adjusting the scene setup (light sources, exposure settings, and material properties) to avoid extreme brightness or darkness?

What is fractional scaling? there is no support for HDR, Fractional Scaling, Wide color gamut in Linux.

[Color checker](https://en.wikipedia.org/wiki/ColorChecker)



## Color Management

Ask GPT: what is a complete color management system

Historically, we only have SDR content and SDR monitors, where sRGB is the standard color space. In that context, tone mapping refers to the process of converting HDR values to LDR values, and gamma correction is used to encode/decode luminance values between linear and sRGB color space. A "linear" workflow typically looks like this:

- When reading textures and images, always assume the data is in sRGB and decode it to linear space.
- During lighting, shading and rendering, everything should work with linear values only.
- After rendering, apply tone mapping to compress the dynamic range to the limited [0,1] range.
- Finally, encode the data back to sRGB color space to better match human perception on the display.

In today's world of HDR, this simplistic "de-gamma and re-gamma" workflow no longer applies. A complete color management system (CMS) is needed to manage color accurately throughout the pipeline, from capture to display, across devices and media.

Here's an overview of what a complete color management system should include.

=== "ascasc"

=== "ascasc"


=== "ascasc"


=== "ascasc"


=== "ascasc"


=== "ascasc"

A complete color management system should enable a linear workflow by properly converting colors for input, rendering, display and output, and we need a proper view transform that prepares color values from the rendering space for display, not just a gamma curve. The view transform should also involve a tone map with a photographic response.

need to be in the same frame of reference

Floating Point Render Target is enabled
If you will be rendering images for further processing like compositing and grading, make sure that File Output Image format on the Common tab of the Render Settings window is set to a format that supports high-dynamic-range values, such as OpenEXR.

Ideally, no color space conversions should be required during the execution of the render, as all input assets such as textures, plate re-projections, and skydomes, can be linearized beforehand.  Image viewing of scene-linear data is typically handled by converting to the color space being delivered to digital intermediate (commonly a log color space), and then applying the view transform suitable for the specified display. For convenience, these transforms are typically baked into a single 3D-LUT, though care must be taken to assure the LUT has suitable fidelity over an ppropriate HDR domain. As mentioned earlier, you must use a viewing transform when viewing HDR scene-linear data.

Rendering and shading occurs in a scene-linear floating point space, typically named “ln”. Half-float (16-bit) images are labeled lnh, full float images (32-bit) are labeled lnf. All image inputs should be converted to ln prior to render-time. Typically, this is done when textures are published. Renderer outputs are always floating-point. Color outputs are typically stored as lnh (16-bit half float). Data outputs (normals, depth data, etc) are stored as ncf (“not color” data, 32-bit full float).

https://acescentral.com/user-guides/

user interfaces are generally authored in the output referred sRGB space. This means that some care needs to be taken in compositing them into the HDR scene. (You don’t want to have your user squinting at a 1000 nit white dialog, so white sRGB content clearly doesn’t mean maximum brightness).

A good solution that we’ve worked with for getting from scene referred to output referred is the Academy Color Encoding System (ACES).　A central part of ACES is that it applies a filmic sigmoid curve in an extremely wide color space. The result is that the overly bright colors naturally desaturate to white.　The sigmoidal curve is actually similar to how the eyes work. ACES color space is a high-dynamic range, scene-linear space, with middle gray pegged to 0.18, and a very wide color gamut.




### Color Configuration

A color configuration (typically a YAML file) contains all the information that OCIO needs.

- It includes definitions for various color spaces available in a project, such as linear, sRGB, ACES and others, along with their associated transforms.
- It outlines the mathematical transformations required to convert images from one color space to another.
- It assigns roles to specific color spaces, which are used by applications to understand how to handle different types of color data (e.g. the "scene_linear" role for linear scene-referred data).
- It defines how images should be displayed on different devices, including any necessary view transforms to ensure consistent appearance.

??? example "Example Color Configuration"

    This `config.ocio` is an overly simplified color config file. In practice, this file can have 5k+ lines, it is often accompanied by a variety of other files, such as color space presets (`.csp` files), LUTs (`.spi1d`, `.spi3d`, `.cube` files) and ICC color profiles (`.icc` files).


[OpenColorIO Configuration for ACES](https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES) provides a set of configuration files that enable OCIO to work seamlessly with the ACES color management framework. You can generate OCIO configurations for ACES using this package, or simply download the [built-in configurations](https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES/releases). The configuration includes a variety of color transformations that are necessary for working with ACES, such as converting between different color spaces, applying look modifications, and managing display outputs. While it provides a standardized framework, the configuration can be customized to meet the specific needs of a production.

OpenImageIO depends on OpenColorIO, but it only allows applying color conversions to images. We would still need OCIO for pixels directly in framebuffers.








