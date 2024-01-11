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
1. H and E stains on an Neuronal Image, H-Hematoxylin stains for neucleic acids (blue-pueple) and eosin stains for proteins (bright pink).
2. All the color values are converted to their corresponding optical density (OD) values; OD = -log10(I), where I is the RGB color vector and each component is normalized in range of [0, 1].
   This transformation created a linear combination of OD values.
   OD-hat, values that pass a pre-defined filter of beta=0.15
4. Color deconvolution to transform color values into quantitative values of interest:
   OD = V . S
   S = V (-1) . OD
     where V and S are stain vectors and saturation of each of the stains respectively
5. NMF based algos attempt to factor the OD matrix into V and S with the algoritum that automatically finds the correct stain vectors for the image and then performs the color deconvolution.
6. The data is put between 1 and 99th percentile, in which, value 0 corresponds to a white pixel and 1 to a black pixel. This is to maintain stability on the low OD value with no stains.
