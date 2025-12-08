#!/usr/bin/env python3
import numpy as np
from gnuradio import digital

# ---------------------------------------------------------
# 1. Gray-coded QPSK (4-QAM) symbol map
# ---------------------------------------------------------
# Gray code mapping:
#   00 → +1 + j
#   01 → -1 + j
#   11 → -1 - j
#   10 → +1 - j
sym_map = np.array([
    1+1j,    # 00
   -1+1j,    # 01
   -1-1j,    # 11
    1-1j     # 10
]) / np.sqrt(2)

# integer mapping (same order)
pre_diff = [0, 1, 3, 2]

# ---------------------------------------------------------
# 2. Build QPSK constellation (non-differential)
#    Matches your GR version exactly
# ---------------------------------------------------------
constellation = digital.constellation_rect(
    sym_map,      # sequence[complex]
    pre_diff,     # sequence[int]
    4,            # rotational symmetry
    1,            # real_sectors
    1,            # imag_sectors
    1.0,          # width_real_sectors
    1.0           # width_imag_sectors
).base()

constellation.set_npwr(1.0)   # normalize

# ---------------------------------------------------------
# 3. Parameters
# ---------------------------------------------------------
access_code = "11100001010110101110100010010011"
bits_per_symbol = constellation.bits_per_symbol()  # should be 2

# ---------------------------------------------------------
# 4. Convert access code bits → symbols
# ---------------------------------------------------------
# Break bits into groups of bps
bits = np.array(list(access_code), dtype=int)
bit_groups = np.reshape(bits, (-1, bits_per_symbol))

# Convert each 2-bit group to integer: (b0<<1 | b1)
indexes = (bit_groups[:,0] << 1) | bit_groups[:,1]

# ---------------------------------------------------------
# 5. Modulate those symbol indexes using the SAME constellation
# ---------------------------------------------------------
preamble_syms = constellation.points()[indexes]

# ---------------------------------------------------------
# 6. Save preamble symbols for GRC Vector Source
# ---------------------------------------------------------
np.save("preamble_symbols.npy", preamble_syms.astype(np.complex64))
print("Saved preamble_symbols.npy")
