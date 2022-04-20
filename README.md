# PyInpaint
A lightwieght inpainting tool for images written in python. Basically the inpainting is achieved using harmonic extension on a non-local graph created using image to be inpainted.
![image](https://user-images.githubusercontent.com/38216671/164158143-b28c96ef-bd3a-4112-862a-c0b99599e385.png)
- `f(u)` is the signal (rgb values) on the node `u`.
- `\Delta_{w,p}` is the weighted graph `p` Laplacian.
- `A` is the area to be inpainted.
- `dA` is the area where signal is given as `g(u)`.

For `p=2` the solution to the above equation yields non-local means.
![image](https://user-images.githubusercontent.com/38216671/164158622-6824240d-2f3d-41eb-b5a5-24d68027411f.png)
- `w(u,v)` is the weight on the edge from node `u` to `v`.
- `N(u)` is the set of neighbors of node `u`.
- `d(u)` is the degree at node `u`.


## Installation
```bash
pip install pyinpaint
```

## Usage
- Command line
```bash
pyinpaint --org_img "path/to/original/image" --mask "path/to/mask"

# pyinpaint --org_img  --mask  --ps --k_boundary --k_search --k_patch
```
The output is an inpainted image at the path of `org_img`.

- Python
```python
from pyinpaint import Inpaint
inpaint = Inpaint(org_img, mask)
inpainted_img = inpaint()

#inpaint = Inpaint(org_img, mask, ps)
#inpainted_img = inpaint(k_boundary, k_search, k_patch)
```
This returns a numpy array `inpainted_img`.

## Results
- image1
- image2
- image3

## How to create an inpainting mask ?

## Params description and usage
The following description of the parameters is useful to **gain speed-ups** and to **inpaint low spatial frequency** texture images.

- ps: Patch size, it is used for creating the non-local graph. The default value is 7. To gain speed-up try with 3 or 5. Ideally it should be an odd value. For images with low spatial frequency texture, should be kept high like 11, 13 or 15 ...
- k_boundary: This is used to determine the nodes at the intersection of `A` and `dA`. The default is 4. To gain speed-up try changing to 8 or 16.  
- k_search: This is used for searching the non-local neighbors of a node. The default is 1000. For large size images it should be increased. To gain speed-up try with 300, 400, 500.
- k_patch: The knn value for the non-local graph construction. The default is 5. Try 3 for speed-up. Try larger value to increase the resolution.
