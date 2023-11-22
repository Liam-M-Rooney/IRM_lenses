# A computational method to reconstruct the topology of convex lens specimens and calculate their radius of curvature.
3D reconstruction and analysis of lens specimens using Interference Reflection Microscopy image data.

IRM image data should be exported as a .PNG file. Images should be cropped and median filtered (σ = 2) to remove any high-frequency noise in the image, and appropirately contrast adjusted.

The _Calibration_ script is first used to verify the correct feature detection parameters for IRM data. The position of the zeroth order minimum was noted as the centre of the lens and the radius was noted as half the width of the image. The position of the intensity maxima along a given radius is calculated using the _find_peaks_ function, iteratively optimising the detection thresholds for peak height, distance, and prominence to ensure that each maxima was detected. A line intensity profile noting the position of each interference maxima was generated along radius (r). The axial position of each interference order was calculated using Equation 1 and plotted to show the curvature along a given radius; where z = fringe spacing, N = order, lambda = wavelength of incident light, and n = refractive index of the imaging medium.

z=N(lambda⁄(2n))					Eq. 1

The surface curvature of each lens was reconstructed using the _3D Reconstruction_ script with the optimised setting for each lens applied from the Calibration script. The 3D convex surface was reconstructed by assigning an axial position, as above, to each interference order detected along each radius (360 radii measured per image). The radius of curvature (R) value for each radius was calculated using Equation 2.

R=(r^2+〖z_N〗^2)⁄(2∙z_N )					Eq. 2

The measured radius of curvature for each lens (R2) is calculated using the _Radius Analysis_ script. The R-value for each radius was compiled into a histogram that compared the experimental measurements to the theoretical R2 (i.e., the manufacturer quoted value). The maximum peak position from each histogram determined the R2 value for each lens.

The variable parameters are listed below for each script.

_**Calibration**_:

Update directory to location of prepared .PNG file and add to code directory.

L36 - Title of .PNG file.

L44 - [x , y] centre coordinates determined in FIJI.

L52 - radius (r), should be less than half the width of the .PNG image in pixels.

L60 - angle, in radians, can be varied to verify parameters at different radii.

L102/103 - detection threshold for interference orders, should be altered to verify that all orders are detected around various radii by changing with angle (L66).

L115 - wavelength in meters, should be updated according to image acquisition settings.


_**3D Reconstruction**_:

L34, 44, 52, 59 - should be copied from optimised _Calibration_ script.

L76 - determines the number of interference orders that are reconstructed. This should be set high to begin with (i.e., greater than the number of orders along the radius) and then reduced according to the prompt following the first run of the script. 'np.linspace(0, max-1, max)' where 'max' is the total number of orders along a given measurement radius.

L145 - scaling factor for reconstruction (meters/pixels), should be obtained from .PNG parameters in FIJI.

L152/153 - detection thresholds determined from _Calibration_ script.

L170 - 'k' = colour, where 'k' = black, 'red' = red, 'green' green etc.

L186 - the theoretical curvature (m), should be updated according to the commercial lens manufacturer specifications.

L197 - name of output file for analysing radius of curvature.

L200-233 - theoretical curvature code; update parameters from manufacturer for comparison of experimental and theoretical curvatures.

L207 - 'R' = the theoretical curvature (m), should be updated according to the commercial lens manufacturer specifications.

L208 - ‘z1’ = the height of the theoretical lens, can be adjusted to match with the reconstructed lens.


_**Radial Analysis**_:

L27 - update to match analysis file name/L196 from _3D Reconstruction_ script.

L32 - Update to theoretical radius of curvature (m).
