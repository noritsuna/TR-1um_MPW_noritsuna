# Copyright (c) 2025 Leo Moser <leo.moser@pm.me>
# SPDX-License-Identifier: Apache-2.0
# modified by OpenSUSI jun1okamura <jun1okamura@gmail.com>  

import sys
import pya
import click

@click.command()
@click.argument(
    "input",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option("--top", required=True)
def check_top(input: str, top: str):
    ly = pya.Layout()
    ly.read(input)

    # Ensure exactly one top-level cell exists.
    if len(ly.top_cells()) > 1:
        print(f"[Error] More than one top-level cell in {input}!")
        sys.exit(1)

    # Fail if no top-level cell is found.
    if ly.top_cell() == None:
        print(f"[Error] No top-level cell in {input}!")
        sys.exit(1)

    # Validate the top cell name matches the expected design name.
    if ly.top_cell().name != top:
        print(f"[Error] Top-level cell name '{ly.top_cell().name}' does not match expected name '{top}'!")
        sys.exit(1)

    # Report name match.
    print(f"Design name '{top}' matches as the top-level cell in '{input}'.")

    # OpenSUSI-MPW die size and frame cell names.
    FRAME_CELL_NAMEs = ['OSS_FRAME', 'OSS_FRAME_TEG']
    CHIP_SIZE_WIDTH  = 2500.00
    CHIP_SIZE_HEIGHT = 2500.00

    # Check database unit (dbu).
    if ly.dbu != 0.001:
        print("[Error]: Database unit (dbu) is not 0.001um.")
        sys.exit(1)

    # Check bounding box matches expected die area.
    if ly.top_cell().dbbox().p1 != pya.DPoint(-CHIP_SIZE_WIDTH/2, -CHIP_SIZE_HEIGHT/2) or ly.top_cell().dbbox().p2 != pya.DPoint(CHIP_SIZE_WIDTH/2, CHIP_SIZE_HEIGHT/2) :
        print("[Error]: Layout area is not (%.2f,%.2f)(%.2f,%.2f)." % (-CHIP_SIZE_WIDTH/2, -CHIP_SIZE_HEIGHT/2, CHIP_SIZE_WIDTH/2, CHIP_SIZE_HEIGHT/2) )
        sys.exit(1)

    # Check required frame/TEG cell exists.
    for cl in ly.each_cell():    
        if cl.name in FRAME_CELL_NAMEs:
            print(f"Design name '{input}' fit into OpenSUSI-MPW die area (%.2f,%.2f)(%.2f,%.2f)." % (-CHIP_SIZE_WIDTH/2, -CHIP_SIZE_HEIGHT/2, CHIP_SIZE_WIDTH/2, CHIP_SIZE_HEIGHT/2) )
            sys.exit(0)
    # No frame found.
    print(f"[Error]: There is NO OpenSUSI-MPW recomended frame/TEG in {ly.top_cell().name}.")
    sys.exit(1)

if __name__ == "__main__":
    check_top()
