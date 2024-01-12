# Normalize-H-and-E-images
A method to normalize H and E images for Image Processing and Quantitative Testing, this is referenced from a paper - https://www.cs.unc.edu/~mn/sites/default/files/macenko2009.pdf

Setting up the tool:
1. Cloning the repository: `git clone https://github.com/unikill066/Normalize-H-and-E-images.git`
2. Install all the necessary libraries: `pip install -r requirements.txt` to run the tool in 2 ways; from the terminal/any python IDE or from Jupyter Notebook/Lab(.ipynb)

2.1 Running the tool from terminal: 
  1. Windows: `python h_and_e_nrom_script.py C:\path\to\neuron\images C:\path\to\output\directory`
  2. Linux and MacOS: `python h_and_e_nrom_script.py /path/to/neuron/images /path/to/output/directory`

2.2 Running the tool from Jupyter Notebook/Lab:
  1. Spin a jpyter notebook instance from the conda/miniconda terminal: `jupyter notebook`
  2. Run the code cell(s) to generate the normalized images.

Output:
The output is put in 3 folders in `/path/to/output/directory`:
  1. h - hematoxylin separated images
  2. e - eosin separated images
  3. norm - normalized images

Foot notes on the theory behind this tool:
1. H and E stains are applied to a Neuronal Image, where H-Hematoxylin stains for nucleic acids (*blue-purple*) and eosin stains for proteins (*bright pink*).
2. All color values are converted to their corresponding optical density (OD) values using the formula `OD = -log10(I)`, where I is the RGB color vector, and each component is normalized in the range of `[0, 1]`. This transformation results in a linear combination of OD values. `OD-hat` represents values that pass a pre-defined filter with `beta=0.15`.
3. Color deconvolution is performed to transform color values into quantitative values of interest:
   ```
   OD = V · S
   S = V^(-1) · OD
   ```
   > where V and S are stain vectors and saturation of each stain, respectively
4. The single value decomposition (SVD) is applied to the OD tuples, creating a plane from SVD directions corresponding to the two largest singular values. This plane is then projected and normalized.
5. NMF-based algorithms attempt to factor the OD matrix into V and S using an algorithm that automatically finds the correct stain vectors for the image and performs color deconvolution.
6. The angle at each point is calculated with respect to the SVD direction, and the data is normalized between the 1st and 99th percentiles. A value of 0 corresponds to a white pixel, and 1 corresponds to a black pixel, maintaining stability for low OD values with no stains.
7. Finally, the values are converted back to OD space to reconstruct an image.
