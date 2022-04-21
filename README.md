# PyInpaint
A lightwieght image inpainting tool written in python. Simple and effective tool to remove scratches, bruises and small holes in images. Could be easily integrated at the backend for Flask or Django apps related to image restoration.

Inpainting is a process of image restoration, the idea is to fill the damage, deteriorated or missing part of an image to present a complete image. It can also be used to remove unwanted parts in an image. Deep learning based approaches use GANs to inpaint. This requires significant amount of training. The proposed tool quickly inpaints by solving a PDE on graphs. 

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
![image](https://user-images.githubusercontent.com/38216671/164308585-23f48a12-6ae3-4bf5-b6a3-efca66592548.png)
![image](https://user-images.githubusercontent.com/38216671/164310841-6cbc55d3-f6b3-449f-9148-a81d28d6c707.png)


## Video demonstration
This video shows:
- How to create an inpainting mask in Gimp.
- How to inpaint using command line.

## How it works?
Basically the inpainting is achieved using harmonic extension on a non-local graph created using image to be inpainted.
![image](https://user-images.githubusercontent.com/38216671/164374512-39a1ba1e-84cc-4570-ac3c-ca98df15cc61.png)
- `f(u)` is the signal (rgb values) on the node `u`.
- `\Delta_{w,p}` is the weighted graph `p` Laplacian.
- `A` is the area to be inpainted.
- `dA` is the area where signal is given as `g(u)`.

For `p=2` the solution to the above equation yields non-local means.
![image](https://user-images.githubusercontent.com/38216671/164375021-4e7da575-38ff-4bab-aa31-8f4518eb8bfc.png)
- `w(u,v)` is the weight on the edge from node `u` to `v`.
- `N(u)` is the set of neighbors of node `u`.
- `d(u)` is the degree at node `u`.

## Params description
The following description of the parameters is useful to **gain speed-ups** and to **inpaint low spatial frequency** texture images.

| Param | Description |
| --- | --- |
| ps | Patch size, it is used for creating the non-local graph. The default value is 7. To gain speed-up try with 3 or 5. Ideally it should be an odd value. For images with low spatial frequency texture, should be kept high like 11, 13 or 15 ... |
| k_boundary | To determine the nodes at the intersection of `A` and `dA`. The default is 4. To gain speed-up try changing to 8 or 16. |
| K_search | Determines the region for searching the non-local neighbors of a node. The default is 1000. For large size images it should be increased. To gain speed-up try with 300, 400, 500. |
| K_patch | The KNN value for the non-local graph construction. The default is 5. Try 3 for speed-up. Try larger value to increase the resolution. |
