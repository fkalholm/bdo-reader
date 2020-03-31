import numpy as np
# Checks which tag the hex-code corresponds to,
# and returns a string with the name.
lookup_dict = {
    0x00: 'shversion',
    0x01: 'shbuilddate',
    0x02: 'filedate',
    0x03: 'user',
    0x04: 'host',
    0x05: 'format',
    # Beam config, 0xCBXX
    0xCB00: 'jpart0',
    0xCB01: 'apro0',
    0xCB02: 'zpro0',
    0xCB03: 'beamx',
    0xCB04: 'beamy',
    0xCB05: 'beamz',
    0xCB06: 'sigmax',
    0xCB07: 'sigmay',
    0xCB08: 'tmax0',
    0xCB09: 'sigmat0',
    0xCB0A: 'beamtheta',
    0xCB0B: 'beamphi',
    0xCB0C: 'beamdivx',
    0xCB0D: 'beamdivy',
    0xCB0E: 'beamdivk',
    # Confguration, 0xCCXX
    0xCC00: 'dele',
    0xCC01: 'demin',
    0xCC02: 'itypst',
    0xCC03: 'itypms',
    0xCC04: 'oln',
    0xCC05: 'inucre',
    0xCC06: 'iemtrans',
    0xCC07: 'iextspec',
    0xCC08: 'intrfast',
    0xCC09: 'intrslow',
    0xCC0A: 'apzlscl',
    0xCC0B: 'ioffset',
    0xCC0C: 'irifimc',
    0xCC0D: 'irifitrans',
    0xCC0E: 'irifizone',
    0xCC0F: 'ext_nproj',
    0xCC10: 'ext_ptvdose',
    0xCC11: 'ixfirs',
    # CT specific tags, 0xCEXX
    0xCE00: 'ct_ang',
    0xCE01: 'ct_icnt',
    0xCE02: 'ct_len',
    # Estimator specific tags, 0xEEXX
    0xEE00: 'est_geotyp',
    0xEE01: 'est_pages',
    # Detector tags, 0xDDXX
    0xDD00: 'det_geotyp',
    0xDD01: 'det_nbin',
    0xDD02: 'det_part',
    0xDD03: 'det_dtype',
    0xDD04: 'det_partz',
    0xDD05: 'det_parta',
    0xDD06: 'det_dmat',
    0xDD07: 'det_nbine',
    0xDD08: 'det_difftype',
    0xDD09: 'det_zonestart',
    0xDD0A: 'det_dsize',
    0xDD0B: 'det_dsizexyz',
    0xDD0C: 'det_xyz_start',
    0xDD0D: 'det_xyz_stop',
    0xDD0E: 'det_dif_start',
    0xDD0F: 'det_dif_stop',
    0xDD10: 'det_voxvol',
    0xDD11: 'det_thresh',
    0xDDBB: 'det_data',
    # Runtime variables, 0xAAXX
    0xAA00: 'rt_nstat',
    0xAA01: 'rt_time'
}


def token_get(f):
    # Get the tag id, descriptor and length
    dtypes = np.dtype([('t_id', '<u8'),
                       ('p_desc', 'S8'),
                       ('p_length', '<u8')])
    token = np.fromfile(f, dtype=dtypes, count=1)
    try:
        return token[0][0], token[0][1], token[0][2]
    except:
        return None, None, None


def bdo_bin_to_dict(file):

    with open(file, 'rb') as f:
        r_dict = {}
        # adding start items
        r_dict['magic'] = np.fromfile(f, dtype='S6', count=1)[0].decode('ascii')
        r_dict['endian'] = np.fromfile(f, dtype='S2', count=1)[0].decode('ascii')
        r_dict['ver_str'] = np.fromfile(f, dtype='S16', count=1)[0].decode('ascii')

        while True:
            # getting token
            t_id, p_desc, p_len = token_get(f)
            if p_desc is None:
                break

            # getting payload
            payl = np.fromfile(f, dtype=p_desc, count=p_len)

            # if a string, decode the binary
            if p_desc.decode('ascii')[0] == 'S':
                r_dict[lookup_dict[t_id]] = payl[0].decode('ascii')
            else:
                r_dict[lookup_dict[t_id]] = payl
        return r_dict
