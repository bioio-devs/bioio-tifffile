#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import time
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pytest
from bioio_base import exceptions, test_utilities
from distributed import Client, LocalCluster

from bioio_tifffile import Reader

from .conftest import LOCAL_RESOURCES_DIR


@pytest.mark.parametrize(
    "filename, "
    "set_scene, "
    "expected_scenes, "
    "expected_shape, "
    "expected_dtype, "
    "expected_dims_order, "
    "expected_channel_names, "
    "expected_physical_pixel_sizes",
    [
        (
            "s_1_t_1_c_1_z_1.ome.tiff",
            "Image:0",
            ("Image:0",),
            (325, 475),
            np.uint16,
            "YX",
            None,
            (None, 1.0833333604166673, 1.0833333604166673),
        ),
        (
            "s_1_t_1_c_1_z_1.tiff",
            "Image:0",
            ("Image:0",),
            (325, 475),
            np.uint16,
            "YX",
            None,
            (None, 1.08333441666775, 1.08333441666775),
        ),
        (
            "s_1_t_1_c_10_z_1.ome.tiff",
            "Image:0",
            ("Image:0",),
            (10, 1736, 1776),
            np.uint16,
            "CYX",
            [f"Channel:0:{i}" for i in range(10)],
            (None, 1, 1),
        ),
        (
            "s_1_t_10_c_3_z_1.tiff",
            "Image:0",
            ("Image:0",),
            (10, 3, 325, 475),
            np.uint16,
            "TCYX",
            ["Channel:0:0", "Channel:0:1", "Channel:0:2"],
            (None, 1.08333441666775, 1.08333441666775),
        ),
        (
            "s_3_t_1_c_3_z_5.ome.tiff",
            "Image:0",
            ("Image:0", "Image:1", "Image:2"),
            (5, 3, 325, 475),
            np.uint16,
            "ZCYX",
            ["Channel:0:0", "Channel:0:1", "Channel:0:2"],
            (None, 1.0833333604166673, 1.0833333604166673),
        ),
        (
            "s_3_t_1_c_3_z_5.ome.tiff",
            "Image:1",
            ("Image:0", "Image:1", "Image:2"),
            (5, 3, 325, 475),
            np.uint16,
            "ZCYX",
            ["Channel:1:0", "Channel:1:1", "Channel:1:2"],
            (None, 1.0833333604166673, 1.0833333604166673),
        ),
        (
            "s_3_t_1_c_3_z_5.ome.tiff",
            "Image:2",
            ("Image:0", "Image:1", "Image:2"),
            (5, 3, 325, 475),
            np.uint16,
            "ZCYX",
            ["Channel:2:0", "Channel:2:1", "Channel:2:2"],
            (None, 1.0833333604166673, 1.0833333604166673),
        ),
        (
            "s_1_t_1_c_1_z_1_RGB.tiff",
            "Image:0",
            ("Image:0",),
            (7548, 7548, 3),
            np.uint16,
            "YXS",  # S stands for samples dimension
            None,
            (None, None, None),
        ),
        (
            # Doesn't affect this test but this is actually an OME-TIFF file
            "s_1_t_1_c_2_z_1_RGB.tiff",
            "Image:0",
            ("Image:0",),
            (2, 32, 32, 3),
            np.uint8,
            "CYXS",  # S stands for samples dimension
            ["Channel:0:0", "Channel:0:1"],
            (None, 1, 1),
        ),
        pytest.param(
            "s_1_t_1_c_1_z_1.ome.tiff",
            "Image:1",
            None,
            None,
            None,
            None,
            None,
            (None, None, None),
            marks=pytest.mark.xfail(raises=IndexError),
        ),
        pytest.param(
            "s_3_t_1_c_3_z_5.ome.tiff",
            "Image:3",
            None,
            None,
            None,
            None,
            None,
            (None, None, None),
            marks=pytest.mark.xfail(raises=IndexError),
        ),
    ],
)
def test_tiff_reader(
    filename: str,
    set_scene: str,
    expected_scenes: Tuple[str, ...],
    expected_shape: Tuple[int, ...],
    expected_dtype: np.dtype,
    expected_dims_order: str,
    expected_channel_names: List[str],
    expected_physical_pixel_sizes: Tuple[
        Optional[float], Optional[float], Optional[float]
    ],
) -> None:
    # Construct full filepath
    uri = LOCAL_RESOURCES_DIR / filename

    # Run checks
    test_utilities.run_image_file_checks(
        ImageContainer=Reader,
        image=uri,
        set_scene=set_scene,
        expected_scenes=expected_scenes,
        expected_current_scene=set_scene,
        expected_shape=expected_shape,
        expected_dtype=expected_dtype,
        expected_dims_order=expected_dims_order,
        expected_channel_names=expected_channel_names,
        expected_physical_pixel_sizes=expected_physical_pixel_sizes,
        expected_metadata_type=str,
    )


def test_tiff_reader_with_non_tiff_file(sample_text_file: pathlib.Path) -> None:
    with pytest.raises(exceptions.UnsupportedFileFormatError):
        Reader(sample_text_file)


@pytest.mark.parametrize(
    "filename, "
    "first_scene_id, "
    "first_scene_shape, "
    "second_scene_id, "
    "second_scene_shape",
    [
        (
            "s_3_t_1_c_3_z_5.ome.tiff",
            "Image:0",
            (5, 3, 325, 475),
            "Image:1",
            (5, 3, 325, 475),
        ),
        (
            "s_3_t_1_c_3_z_5.ome.tiff",
            "Image:1",
            (5, 3, 325, 475),
            "Image:2",
            (5, 3, 325, 475),
        ),
    ],
)
def test_multi_scene_tiff_reader(
    filename: str,
    first_scene_id: str,
    first_scene_shape: Tuple[int, ...],
    second_scene_id: str,
    second_scene_shape: Tuple[int, ...],
) -> None:
    # Construct full filepath
    uri = LOCAL_RESOURCES_DIR / filename

    # Run checks
    test_utilities.run_multi_scene_image_read_checks(
        ImageContainer=Reader,
        image=uri,
        first_scene_id=first_scene_id,
        first_scene_shape=first_scene_shape,
        first_scene_dtype=np.dtype(np.uint16),
        second_scene_id=second_scene_id,
        second_scene_shape=second_scene_shape,
        second_scene_dtype=np.dtype(np.uint16),
    )


@pytest.mark.parametrize(
    "dims_from_meta, guessed_dims, expected",
    [
        ("QZYX", "CZYX", "CZYX"),
        ("ZQYX", "CZYX", "ZCYX"),
        ("ZYXC", "CZYX", "ZYXC"),
        ("TQQYX", "TCZYX", "TCZYX"),
        ("QTQYX", "TCZYX", "CTZYX"),
        # testing that nothing happens when Q isn't present
        ("LTCYX", "DIMOK", "LTCYX"),
    ],
)
def test_merge_dim_guesses(
    dims_from_meta: str, guessed_dims: str, expected: str
) -> None:
    assert Reader._merge_dim_guesses(dims_from_meta, guessed_dims) == expected


def test_micromanager_ome_tiff_binary_file() -> None:
    # Construct full filepath
    uri = (
        LOCAL_RESOURCES_DIR
        / "image_stack_tpzc_50tp_2p_5z_3c_512k_1_MMStack_2-Pos001_000.ome.tif"
    )

    # Even though the file name says it is an OME TIFF, this is
    # a binary TIFF file where the actual metadata for all scenes
    # lives in a different image file.
    # (image_stack_tpzc_50tp_2p_5z_3c_512k_1_MMStack_2-Pos000_000.ome.tif)
    # Because of this, we will read "non-main" micromanager files as just
    # normal TIFFs

    # Run image read checks on the first scene
    # (this files binary data)
    test_utilities.run_image_file_checks(
        ImageContainer=Reader,
        image=uri,
        set_scene="Image:0",
        expected_scenes=("Image:0",),
        expected_current_scene="Image:0",
        expected_shape=(50, 5, 3, 256, 256),
        expected_dtype=np.dtype(np.uint16),
        expected_dims_order="TZCYX",
        expected_channel_names=["Channel:0:0", "Channel:0:1", "Channel:0:2"],
        expected_physical_pixel_sizes=(1.75, 0.0002, 0.0002),
        expected_metadata_type=str,
    )


@pytest.mark.parametrize(
    "filename, set_scene, get_dims, get_specific_dims, expected_shape",
    [
        (
            "s_1_t_1_c_2_z_1_RGB.tiff",
            "Image:0",
            "CYXS",
            {},
            (2, 32, 32, 3),
        ),
    ],
)
@pytest.mark.parametrize("chunk_dims", ["YX", "ZYX"])
@pytest.mark.parametrize("processes", [True, False])
def test_parallel_read(
    filename: str,
    set_scene: str,
    chunk_dims: str,
    processes: bool,
    get_dims: str,
    get_specific_dims: Dict[str, Union[int, slice, range, Tuple[int, ...], List[int]]],
    expected_shape: Tuple[int, ...],
) -> None:
    """
    This test ensures that our produced dask array can be read in parallel.
    """
    # Construct full filepath
    uri = LOCAL_RESOURCES_DIR / filename

    # Init image
    img = Reader(uri, chunk_dims=chunk_dims)
    img.set_scene(set_scene)

    # Init cluster
    cluster = LocalCluster(processes=processes)
    client = Client(cluster)

    # Select data
    out = img.get_image_dask_data(get_dims, **get_specific_dims).compute()
    assert out.shape == expected_shape

    # Shutdown and then safety measure timeout
    cluster.close()
    client.close()
    time.sleep(5)


@pytest.mark.parametrize(
    "filename, "
    "first_scene, "
    "expected_first_chunk_shape, "
    "second_scene, "
    "expected_second_chunk_shape",
    [
        (
            "image_stack_tpzc_50tp_2p_5z_3c_512k_1_MMStack_2-Pos000_000.ome.tif",
            0,
            (50, 5, 256, 256),
            1,
            (50, 5, 256, 256),
        ),
        (
            "image_stack_tpzc_50tp_2p_5z_3c_512k_1_MMStack_2-Pos000_000.ome.tif",
            1,
            (50, 5, 256, 256),
            0,
            (50, 5, 256, 256),
        ),
    ],
)
@pytest.mark.parametrize("processes", [True, False])
def test_parallel_multifile_tiff_read(
    filename: str,
    first_scene: int,
    expected_first_chunk_shape: Tuple[int, ...],
    second_scene: int,
    expected_second_chunk_shape: Tuple[int, ...],
    processes: bool,
) -> None:
    """
    This test ensures that we can serialize and read 'multi-file multi-scene' formats.
    See: https://github.com/AllenCellModeling/aicsimageio/issues/196

    We specifically test with a Distributed cluster to ensure that we serialize and
    read properly from each file.
    """
    # Construct full filepath
    uri = LOCAL_RESOURCES_DIR / filename

    # Init image
    img = Reader(uri)

    # Init cluster
    cluster = LocalCluster(processes=processes)
    client = Client(cluster)

    # Select data
    img.set_scene(first_scene)
    first_out = img.get_image_dask_data("TZYX").compute()
    assert first_out.shape == expected_first_chunk_shape

    # Update scene and select data
    img.set_scene(second_scene)
    second_out = img.get_image_dask_data("TZYX").compute()
    assert second_out.shape == expected_second_chunk_shape

    # Shutdown and then safety measure timeout
    cluster.close()
    client.close()
    time.sleep(5)


@pytest.mark.parametrize(
    "filename, expected_shape",
    [
        ("s_1_t_10_c_3_z_1.tiff", (10, 3, 325, 475)),
    ],
)
def test_no_scene_prop_access(
    filename: str,
    expected_shape: Tuple[int, ...],
) -> None:
    # Construct full filepath
    uri = LOCAL_RESOURCES_DIR / filename

    # Construct image and check no scene call with property access
    img = Reader(uri)
    assert img.shape == expected_shape
