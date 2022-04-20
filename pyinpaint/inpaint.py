"""
Amitoz AZAD 2022-04-18 11:29
"""


# load libs
import numpy as np 
from scipy import spatial
from tqdm import tqdm
import matplotlib.image as mpimg

from pyinpaint.utils import *


class Inpainting:
  """
  Inpaints an image using Dirichlet interpolation.
  Happens to be nlm for p=2 in p laplacian.
  """
  def __init__(self, org_img, mask, ps):
    """
    org_img: path to the original image (rgb or gray)
    mask: path to the mask (binary image, 0,1)
    ps: patch size (used for creating a dynamic non-local graph)
    """
    self.org_img = org_img
    self.mask = mask 
    self.ps = ps

  def __call__(self, k_boundary=4, k_search=1000, k_patch=5):
    """
    k_boundary: used for finding the boundary pixels
    k_search: used for search in the neighborhood of the boundary pixels
    k_patch: used for creating a dynamic non-local graph
    """
    inpainted_img =  self.forward(k_boundary, k_search, k_patch)
    return inpainted_img

  def preprocess(self):
    img = mpimg.imread(self.org_img)
    mask = mpimg.imread(self.mask)
    img = (img - np.min(img))/ (np.max(img) - np.min(img)).astype("float32") + 0.01
    img = (img.T * mask.T).T
    self._shape = img.shape
    position = pmat(self._shape)
    texture = fmat(img)
    self._position = (position - np.min(position) )/ (np.max(position) - np.min(position))
    self._texture = (texture - np.min(texture) )/ (np.max(texture) - np.min(texture))
    self._patches = create_patches(img, (self.ps, self.ps))

  def postprocess(self, fmat):
      return to_img(fmat, self._shape)

  def forward(self, k_boundary, k_search, k_patch):
    self.preprocess()

    kdt = spatial.cKDTree(self._position)
    dA = np.where(self._texture.any(axis=1))[0]
    A = np.where(~self._texture.any(axis=1))[0]

    pbar = tqdm(desc=f"# of pixels to be inpainted are {A.size}", total = A.size, 
            bar_format = '{l_bar}{bar}|{n_fmt}/{total_fmt}')
    while A.size >=1 :
      dmA = np.array([]).astype("int")
      for i in A : 
        _, indices = kdt.query(self._position[i], k_boundary)
        if (~np.isin(indices, A)).any():
          dmA = np.append(dmA,i)
          mask = (~(self._patches[i].flatten() == 0)).astype("int")
          _, indices = kdt.query(self._position[i], k_search)
          part_of_dA = indices[~np.isin(indices,A)]
          new_patches = mask.flatten() * self._patches[part_of_dA]
          kdt_ = spatial.cKDTree(new_patches)
          _, indices= kdt_.query(self._patches[i].flatten(),k_patch)
          ids = part_of_dA[indices]
          self._texture[i] = self._texture[ids].mean(axis=0)
      self._patches = create_patches(to_img(self._texture,(self._shape)),(self.ps,self.ps))
      dA = np.concatenate((dA,dmA), axis=0)
      A = A[~np.isin(A,dmA)]
      #pbar.set_description(desc=f"# of pixels to be inpainted are {A.size}")
      pbar.update(dmA.size)
    pbar.close()
    return self.postprocess(self._texture)


def check_args(cls):
  def correct_args(org_img, mask, ps=7):
    if (isinstance(org_img,str) and isinstance(mask,str) and isinstance(ps,int)):
      return cls(org_img, mask, ps)
    else:
      raise Exception(f"arg[0]:str, arg[1]:str, arg[2]:int")
  return correct_args


Inpaint = check_args(Inpainting)
