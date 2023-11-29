# bioio-tifffile

[![Build Status](https://github.com/bioio-devs/bioio-tifffile/actions/workflows/ci.yml/badge.svg)](https://github.com/bioio-devs/bioio-tifffile/actions)
[![Documentation](https://github.com/bioio-devs/bioio-tifffile/actions/workflows/docs.yml/badge.svg)](https://bioio-devs.github.io/bioio-tifffile)
[![PyPI version](https://badge.fury.io/py/bioio-tifffile.svg)](https://badge.fury.io/py/bioio-tifffile)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.9+](https://img.shields.io/badge/python-3.9,3.10,3.11-blue.svg)](https://www.python.org/downloads/release/python-390/)

A BioIO reader plugin for reading TIFFs using `tifffile`

---


## Documentation

[See the full documentation on our GitHub pages site](https://bioio-devs.github.io/bioio/OVERVIEW.html) - the generic use and installation instructions there will work for this package.

## Installation

**Stable Release:** `pip install bioio-tifffile`<br>
**Development Head:** `pip install git+https://github.com/bioio-devs/bioio-tifffile.git`

## Example Usage (see full documentation for more examples)

Install bioio-tifffile alongside bioio:

`pip install bioio bioio-tifffile`

```python
from bioio import BioImage

# Get a BioImage object
img = BioImage("my_file.tiff")  # selects the first scene found
img.data  # returns 5D TCZYX numpy array
img.xarray_data  # returns 5D TCZYX xarray data array backed by numpy
img.dims  # returns a Dimensions object
img.dims.order  # returns string "TCZYX"
img.dims.X  # returns size of X dimension
img.shape  # returns tuple of dimension sizes in TCZYX order
img.get_image_data("CZYX", T=0)  # returns 4D CZYX numpy array

# Get the id of the current operating scene
img.current_scene

# Get a list valid scene ids
img.scenes

# Change scene using name
img.set_scene("Image:1")
# Or by scene index
img.set_scene(1)

# Use the same operations on a different scene
# ...
```

## Issues
[_Click here to view all open issues in bioio-devs organization at once_](https://github.com/search?q=user%3Abioio-devs+is%3Aissue+is%3Aopen&type=issues&ref=advsearch) or check this repository's issue tab.


## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.
