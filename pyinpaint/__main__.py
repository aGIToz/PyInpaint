"""
Amitoz AZAD 2022-04-19 06:59
"""

import os
import argparse

import matplotlib.pyplot as plt

from pyinpaint import Inpaint


def modify(path):
    file_name = os.path.splitext(path)[0]
    file_extension = os.path.splitext(path)[1]
    path = file_name +"_inpainted" + file_extension
    return path


def main():
    """
    Calls the inpaint module, and saves the inpainted image.
    """
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--org_img", type=str, help="The path to the original image.")
    argparser.add_argument("--mask", type=str, help="The path to the original image.")
    argparser.add_argument("--ps", type=int, default=7, help="Patch size.")
    argparser.add_argument("--k_boundary", type=int, default=4, help="To determine the boundary pixels. Ideally should be 4 or 8.")
    argparser.add_argument("--k_search", type=int, default=1000, help="Determines the search range, normally 500 or 1000")
    argparser.add_argument("--k_patch", type=int, default=5, help="knn value for the non-local graph, ideal values are 3,5,7")

    args = argparser.parse_args()

    inpaint = Inpaint(args.org_img, args.mask, args.ps)
    inpainted_img = inpaint(args.k_boundary, args.k_search, args.k_patch)

    path_to_output = modify(args.org_img) 
    plt.imsave(path_to_output, inpainted_img)


if __name__ == "__main__":
    main()
