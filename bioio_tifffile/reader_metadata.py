#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

import bioio_types.reader_metadata

###############################################################################


class ReaderMetadata(bioio_types.reader_metadata.ReaderMetadata):
    @staticmethod
    def get_supported_extensions() -> List[str]:
        return ["tif", "tiff"]

    @staticmethod
    def get_reader() -> bioio_types.reader.Reader:
        from .reader import Reader

        return Reader
