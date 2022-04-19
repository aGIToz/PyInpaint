# PyInpaint
A lightwieght inpainting tool for images written in python. Basically the inpainting is achieved using harmonic extension on a non-local graph created using image to be inpainted.

For `p=2` the solution to the above equation yields non-local means.

## Installation
```bash
pip install pyinpaint
```

## Usage
- Command line
```bash
pyinpaint --org_img "path/to/original/image" --mask "path/to/mask"
```

- Python
```python
from pyinpaint import Inpaint
inpaint = Inpaint(org_img, mask)
inpainted_img = inpaint()
```

## Results
- image1
- image2
- image3

## How to create an inpainting mask ?

## Params description and usage
> The following description of the parameters is useful to grain speed ups and to inpaint low spatial frequency texture images.

- ps:
- k_boundary:
- k_search:
- k_patch:
