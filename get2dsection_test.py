#!/usr/bin/env python3.5

import mrcfile
import numpy as np
from isecc import *
import scipy.ndimage
from scipy.spatial.transform import Rotation as R
from pyem import *
from pyfftw.builders import irfft2
from numpy.fft import fftshift

###
my_file = mrcfile.open('../MRC/icos_scaled.mrc')
my_ndimage = np.copy(my_file.data)
del my_file

def calculateProjection( my_ndimage, my_rotation ):
    my_rotation = iseccFFT_v2.pyquat2scipy(my_rotation)
    my_rotmatrix = R.from_quat(my_rotation)

    """ Get random rotation for testing """
    my_rotmatrix = R.random()
    my_rotmatrix = my_rotmatrix.as_matrix()

    #my_ndimage = iseccFFT_v2.swapAxes_ndimage( my_ndimage )
    #my_2dsection = iseccFFT_v2.get2dsection( my_ndimage, my_rotation )

    f3d = vop.vol_ft(my_ndimage, pfac=2 )
    f2d = vop.interpolate_slice_numba(f3d, my_rotmatrix, pfac=2)

    ift = irfft2(f2d.copy(),
                planner_effort="FFTW_ESTIMATE",
                auto_align_input=True,
                auto_contiguous=True)
    proj = fftshift(ift(f2d.copy(), np.zeros(ift.output_shape, dtype=ift.output_dtype)))

    #iseccFFT_v2.plot2dimage( np.fft.ifftn(f2d).astype(np.float) )
    #iseccFFT_v2.plot2dimage( proj )

    return proj

my_symops = symops.getSymOps()

for symop in my_symops:
    print( symop )
    proj = calculateProjection( my_ndimage, symop )
    iseccFFT_v2.plot2dimage( proj )
