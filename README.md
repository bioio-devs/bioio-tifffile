# bioio-tifffile

[![Build Status](https://github.com/bioio-devs/bioio-tifffile/workflows/CI/badge.svg)](https://github.com/bioio-devs/bioio-tifffile/actions)
[![Documentation](https://github.com/bioio-devs/bioio-tifffile/workflows/Documentation/badge.svg)](https://bioio-devs.github.io/bioio-tifffile)

A BioIO reader plugin for reading TIFFs using Tifffile

---

## Installation

**Stable Release:** `pip install bioio-tifffile`<br>
**Development Head:** `pip install git+https://github.com/bioio-devs/bioio-tifffile.git`

## Quickstart

```python
from bioio_tifffile import Reader 

r = Reader("my-image.tiff")
r.dims
```

## Documentation

For full package documentation please visit [bioio-devs.github.io/bioio-tifffile](https://bioio-devs.github.io/bioio-tifffile).

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

**MIT License**
