import struct


ROI_TYPES = {
    1: 'rect',
    3: 'line',
    5: 'polyline',
    7: 'freehand',
    9: 'angle',
    10: 'point'
}


def extract_coords(raw_file_bytes, n_coords, left, top):
    fmt_coords = ">" + "h" * n_coords
    l_coords = struct.calcsize(fmt_coords)
    x_raw = struct.unpack(fmt_coords, raw_file_bytes[64:64+l_coords])
    y_raw = struct.unpack(fmt_coords, raw_file_bytes[64+l_coords:64+2*l_coords])

    x = [x + left for x in x_raw]
    y = [y + top for y in y_raw]

    return list(zip(x, y))


def roi_from_fpath(roi_fpath):
    with open(roi_fpath, 'rb') as fh:
        raw_file_bytes = fh.read()

    type_code, top, left, bottom, right = struct.unpack(">Bxhhhh", raw_file_bytes[6:16])
    x1, y1, x2, y2 = struct.unpack(">ffff", raw_file_bytes[18:34])
    n_coordinates, = struct.unpack(">h", raw_file_bytes[16:18])

    coords = extract_coords(raw_file_bytes, n_coordinates, left, top)

    roi = {
        'type': ROI_TYPES[type_code],
        'coords': coords
    }

    if roi['type'] == 'line':
        roi['x1'] = x1
        roi['y1'] = y1
        roi['x2'] = x2
        roi['y2'] = y2

    return roi
