
# ..\PackingUtils\env\Scripts\activate

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
        if not self.is_packer_available():
            raise ImportError(
                "PalletierPacker requires palletier to be installed (pip install -r requirements_palletier.txt)")

        pallets = [palletier.Pallet(
            dims=(10, 4, 3),
            max_weight=0
        )]

        boxes = []
        for idx in range(3):
            boxes.append(palletier.Box(dims=(2, 2, 2)))

        packer = palletier.Solver(
            pallets=pallets, boxes=boxes, allow_rotation=False)
        packer.pack()

        for p in packer.packed_pallets:
            for box in p.boxes:
                print(box, box.pos, box.orientation)

    def _get_rotation_type(self, box):
        if box.orientation == box.dims:
            return 0
        raise NotImplementedError()

    def is_packer_available(self) -> bool:
        return PACKER_AVAILABLE


if __name__ == '__main__':
    PalletierPacker().pack_variant()
