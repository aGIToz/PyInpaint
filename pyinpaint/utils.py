"""
Amitoz AZAD 2022-04-18 11:30
Basic utilities to preprocess and postprocess.
"""


# libs
import numpy as np
import skimage


def fmat(img):
    """
    Converts to a feature matrix (N by c)
    """
    try:
        l, w, c = img.shape
        fmat = np.ones((l*w,c)) 
        for i in range(c): fmat[:,i] = np.reshape(img[:,:,i],(l*w,))
    except ValueError:
        try:
            l, w = img.shape
            fmat = np.ones((l*w,1)) 
            fmat = np.reshape(img,(l*w,1))
        except ValueError:
            print("Image should be at least a 2D array.")
    return fmat



def pmat(shape):
    """
    Returns the position feature matrix.
    """
    x = np.arange(0,shape[1],1)
    y = np.arange(shape[0],0,-1)
    meshx, meshy = np.meshgrid(x,y)
    x = np.reshape(meshx,(shape[0]*shape[1],1)) 
    y = np.reshape(meshy,(shape[0]*shape[1],1)) 
    pmat = np.concatenate((x,y),axis=1) / max(shape[0],shape[1])
    return pmat



def to_img(fmat, shape):
    """
    Converts from fmat to img.
    """
    img = np.zeros(shape)
    try:
        l, w, c = img.shape
        for i in range(c): img[:,:,i] = np.reshape(fmat[0:,i],(l,w))
    except ValueError:
        try:
            l, w = img.shape
            img = np.reshape(fmat,(l,w))
        except ValueError:
            print("Image should be at least a 2D array.")
    return img


# code taken from pygsp https://github.com/epfl-lts2/pygsp
# thanks to Michaël Defferrard 
def create_patches(img, patch_shape=(3,3)):
    try:
        h, w, d = img.shape
    except ValueError:
        try:
            h, w = img.shape
            d = 0
        except ValueError:
            print("Image should be at least a 2D array.")

    try:
        r, c = patch_shape
    except ValueError:
        r = patch_shape[0]
        c = r

    pad_width = [(int((r - 0.5) / 2.), int((r + 0.5) / 2.)),
                 (int((c - 0.5) / 2.), int((c + 0.5) / 2.))]

    if d == 0:
        window_shape = (r, c)
        d = 1  # For the reshape in the return call
    else:
        pad_width += [(0, 0)]
        window_shape = (r, c, d)

    # Pad the image.
    img = np.pad(img, pad_width=pad_width, mode='symmetric')

    # Extract patches as node features.
    # Alternative: sklearn.feature_extraction.image.extract_patches_2d.
    #              sklearn has much less dependencies than skimage.
    try:
        import skimage
    except Exception:
        raise ImportError('Cannot import skimage, which is needed to '
                          'extract patches. Try to install it with '
                          'pip (or conda) install scikit-image.')
    patches = skimage.util.view_as_windows(img, window_shape=window_shape)
    patches = patches.reshape((h * w, r * c * d))
    return patches
