# coding: utf-8

# # Palletier
# Palletier is a Python implementation of the solution for the distributer's
# pallet packing problem presented by Erhan Baltacioğlu in his thesis
#   The distributer's three-dimensional pallet-packing problem: a human
#   intelligence-based heuristic approach.
import collections
from itertools import permutations
from copy import copy, deepcopy

from palletier.box import Box
from palletier.packer import Packer
from palletier.pallet import Pallet
from palletier.packedpallet import PackedPallet

Dims = collections.namedtuple('Dims', ['dim1', 'dim2', 'dim3'])


class Solver:
    """The volume optimization solver"""

    def __init__(self, pallets, boxes, allow_rotation):
        """Initializes the solver with the pallets available and the boxes
        to be packed.

        Args:
            pallets ([Pallet]): The list of pallets available to the solver
            boxes ([Box]): The boxes to be packed

        Raises:
            TypeError: If an element in pallets is not a Pallet
            TypeError: If an element in boxes is not a Box
        """

        if all(isinstance(pallet, Pallet) for pallet in pallets):
            self.pallets = pallets
        else:
            raise TypeError('All elements of the pallets list '
                            'must be of type Pallet')

        if all(isinstance(pallet, Pallet) for pallet in pallets):
            self.boxes = boxes
        else:
            raise TypeError('All elements of the boxes list '
                            'must be of type Box')
        self.total_num_boxes = len(self.boxes)
        self.total_boxes_vol = sum(box.vol for box in self.boxes)
        self.packed_pallets = []
        self.allow_rotation = allow_rotation

    def pack(self):
        remaining_boxes = self.boxes
        while len(remaining_boxes) != 0:  # All boxes need to be packed
            single_solutions = []  # A solution for each pallet type
            for pallet in self.pallets:
                packer = Packer(remaining_boxes, pallet,
                                allow_rotation=self.allow_rotation)
                pallet_ori, packed, unpacked, score = packer.iterations()
                single_solutions.append((pallet_ori, packed, unpacked, score))
                pallet.weight = 0  # Reset weight for next iteration
            # Get the best solution by score
            solution = max(single_solutions, key=lambda x: x[3])
            best_pallet, best_packed, best_unpacked, score = solution
            # Make this a test
            # The boxes we sent to pack do not fit into any pallets
            if len(best_unpacked) == len(remaining_boxes):
                for box in best_unpacked:
                    box.orientation = box.dims
                    self.packed_pallets.append(PackedPallet(
                        Pallet(dims=box.dims, name='BOX',
                               orientation=box.dims),
                        [box],
                    ))
                break
            else:
                self.packed_pallets.append(PackedPallet(copy(best_pallet),
                                                        deepcopy(best_packed)))
                remaining_boxes = best_unpacked

    def print_solution(self):
        for packed in self.packed_pallets:
            dims = packed.pallet.orientation
            print(
                f"Packed Pallet #{packed.idx} with utilization of {packed.utilization}")
            print(f"Using Pallet #{packed.pallet.idx} with dims {dims}")
            """
            print(f"With {packed.num_boxes} boxes:")
            for box in packed.boxes:
                print(f"Box #{box.idx} with dims {box.orientation}")
                print(f"  located at {box.pos}")
            """
