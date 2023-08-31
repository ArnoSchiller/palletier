
# ..\PackingUtils\env\Scripts\activate
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
try:
    import palletier
    PACKER_AVAILABLE = True
except ImportError as e:
    PACKER_AVAILABLE = False


class PalletierPacker():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_params(self) -> dict:
        return {}

    def pack_variant(self):
        pallets = [
            palletier.Pallet(dims=(80, 1, 50), max_weight=0)
        ]

        boxes = []
        # "AMELAND WPC Steckzaun Füllung"
        for _ in range(5):  # 9
            boxes.append(palletier.Box(dims=(27, 1, 40)))
        # "Aluminium Steckzaunpfosten, silber"
        for _ in range(9):  # 9
            boxes.append(palletier.Box(dims=(6, 1, 6)))

        packer = palletier.Solver(pallets=pallets, boxes=boxes)
        packer.pack()

        print(len(packer.packed_pallets))
        visualize(packer)
        packer.print_solution()


def visualize(packer):
    for packed in packer.packed_pallets:
        fig, ax = plt.subplots()
        pal_dims = packed.pallet.orientation

        ax.axes.set_xlim(0, pal_dims[0])
        ax.axes.set_ylim(0, pal_dims[2])
        ax.set_xlabel("Width")
        ax.set_ylabel("Height")
        ax.set_aspect('equal')

        for box in packed.boxes:

            dim = box.orientation
            ax.add_patch(
                Rectangle((box.pos[0], box.pos[2]), dim[0], dim[2],
                          facecolor="r", edgecolor="black", linewidth=2)
            )

        plt.show()

    def _get_rotation_type(self, box):
        if box.orientation == box.dims:
            return 0
        raise NotImplementedError()

    def is_packer_available(self) -> bool:
        return PACKER_AVAILABLE


if __name__ == '__main__':
    PalletierPacker().pack_variant()
