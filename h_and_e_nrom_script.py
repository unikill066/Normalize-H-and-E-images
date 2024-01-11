# imports
from natsort import natsorted
import numpy as np, cv2, matplotlib.pyplot as plt, os, typer

# constants
Io = 240  # Transmitted light intensity, Normalizing factor for image intensities
alpha = 1  # As recommend in the paper. tolerance for the pseudo-min and pseudo-max (default: 1)
beta = 0.15  # As recommended in the paper. OD threshold for transparent pixels (default: 0.15)

HERef = np.array([[0.5626, 0.2159],
                  [0.7201, 0.8012],
                  [0.4062, 0.5581]])
maxCRef = np.array([1.9705, 1.0308])


# @click.command()
def remove_h_and_e_stain(directory, image_filepath):
    """
    The method separates the H and E staining from the given *directory* and save h, e and norm, i.e,
     H staining, E staining and Normalized images to the respective directories in *image_filepath*
    :param directory: filepath where the staining images are present
    :param image_filepath: directory where the h, e and norm directories are created and the output is saved to
    the respective directories
    """
    try:
        counter = 0

        if not os.path.exists(directory) or not os.path.exists(image_filepath):
            raise Exception("Filepath: {} does not exist.".format(directory))

        for image_file in natsorted(os.listdir(directory)):
            if str(os.path.join(directory, image_file)).endswith(".png"):
                counter += 1
                print("Processing the image:", os.path.join(directory, image_file))
                img = cv2.imread(directory + os.sep + image_file, 1)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                h, w, c = img.shape
                img = img.reshape((-1, 3))

                OD = -np.log10((img.astype(np.float_) + 1) / Io)  # Use this for opencv imread
                ODhat = OD[~np.any(OD < beta, axis=1)]
                eigvals, eigvecs = np.linalg.eigh(np.cov(ODhat.T))
                That = ODhat.dot(eigvecs[:, 1:3])  # Dot product

                phi = np.arctan2(That[:, 1], That[:, 0])
                minPhi = np.percentile(phi, alpha)
                maxPhi = np.percentile(phi, 100 - alpha)

                vMin = eigvecs[:, 1:3].dot(np.array([(np.cos(minPhi), np.sin(minPhi))]).T)
                vMax = eigvecs[:, 1:3].dot(np.array([(np.cos(maxPhi), np.sin(maxPhi))]).T)

                if vMin[0] > vMax[0]:
                    HE = np.array((vMin[:, 0], vMax[:, 0])).T
                else:
                    HE = np.array((vMax[:, 0], vMin[:, 0])).T

                Y = np.reshape(OD, (-1, 3)).T
                C = np.linalg.lstsq(HE, Y, rcond=None)[0]

                maxC = np.array([np.percentile(C[0, :], 99), np.percentile(C[1, :], 99)])
                tmp = np.divide(maxC, maxCRef)
                C2 = np.divide(C, tmp[:, np.newaxis])

                Inorm = np.multiply(Io, np.exp(-HERef.dot(C2)))
                Inorm[Inorm > 255] = 254
                Inorm = np.reshape(Inorm.T, (h, w, 3)).astype(np.uint8)

                H = np.multiply(Io, np.exp(np.expand_dims(-HERef[:, 0], axis=1).dot(np.expand_dims(C2[0, :], axis=0))))
                H[H > 255] = 254
                H = np.reshape(H.T, (h, w, 3)).astype(np.uint8)

                E = np.multiply(Io, np.exp(np.expand_dims(-HERef[:, 1], axis=1).dot(np.expand_dims(C2[1, :], axis=0))))
                E[E > 255] = 254
                E = np.reshape(E.T, (h, w, 3)).astype(np.uint8)

                if not os.path.exists(image_filepath):
                    os.mkdir(image_filepath)
                if not os.path.exists(os.path.join(image_filepath, 'h')):
                    os.makedirs(image_filepath + os.sep + "h")
                if not os.path.exists(os.path.join(image_filepath, 'e')):
                    os.makedirs(image_filepath + os.sep + "e")
                if not os.path.exists(os.path.join(image_filepath, 'norm')):
                    os.makedirs(image_filepath + os.sep + "norm")

                plt.imsave("{}/norm_{}.png".format(os.path.join(image_filepath, "norm"), counter), Inorm)
                plt.imsave("{}/h_{}.png".format(os.path.join(image_filepath, "h"), counter), H)
                plt.imsave("{}/e_{}.png".format(os.path.join(image_filepath, "e"), counter), E)

    except Exception as error:
        return error

    finally:
        pass


if __name__ == '__main__':
    typer.run(remove_h_and_e_stain)