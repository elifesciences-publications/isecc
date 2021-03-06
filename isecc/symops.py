#!/usr/bin/env python3.5

import numpy as np

def getSymOps():

    ### Generate array containing I1 rotations ready for pyQuaternion in format [ a, bi, cj, dk ]
    I1Quaternions = np.array( [ [ 1.000, 0.000, 0.000, 0.000 ],    [ 0.000, 1.000, 0.000, 0.000 ],
                                [ 0.809, -0.500, 0.000, 0.309 ],   [ -0.309, 0.809, 0.000, -0.500 ],
                                [ 0.309, 0.809, 0.000, -0.500 ],   [ 0.809, 0.500, 0.000, -0.309 ],
                                [ -0.500, 0.809, 0.309, 0.000 ],   [ 0.500, 0.809, 0.309, 0.000 ],
                                [ 0.500, 0.809, -0.309, 0.000 ],   [ 0.809, 0.309, -0.500, 0.000 ],
                                [ 0.809, 0.309, 0.500, 0.000 ],    [ 0.809, -0.309, -0.500, 0.000 ],
                                [ 0.809, -0.309, 0.500, 0.000 ],   [ -0.500, 0.809, -0.309, 0.000 ],
                                [ 0.000, 0.809, 0.500, -0.309 ],   [ 0.500, 0.500, 0.500, -0.500 ],
                                [ 0.809, 0.000, 0.309, -0.500 ],   [ 0.809, -0.500, 0.000, -0.309 ],
                                [ 0.809, 0.500, 0.000, 0.309 ],    [ -0.500, 0.500, 0.500, -0.500 ],
                                [ 0.809, 0.000, -0.309, 0.500 ],   [ 0.809, 0.000, 0.309, 0.500 ],
                                [ -0.500, 0.500, -0.500, -0.500 ], [ 0.000, 0.809, -0.500, -0.309 ],
                                [ -0.309, 0.809, 0.000, 0.500 ],   [ 0.809, 0.000, -0.309, -0.500 ],
                                [ 0.500, -0.309, 0.000, 0.809 ],   [ 0.000, -0.500, 0.309, 0.809 ],
                                [ 0.500, 0.500, -0.500, -0.500 ],  [ -0.309, -0.500, 0.809, 0.000 ],
                                [ 0.000, 0.809, -0.500, 0.309 ],   [ 0.309, 0.809, 0.000, 0.500 ],
                                [ -0.500, 0.500, 0.500, 0.500 ],   [ 0.000, 0.809, 0.500, 0.309 ],
                                [ 0.309, 0.500, 0.809, 0.000 ],    [ 0.000, -0.500, -0.309, 0.809 ],
                                [ -0.500, -0.309, 0.000, 0.809 ],  [ -0.500, 0.000, 0.809, 0.309 ],
                                [ -0.309, 0.500, 0.809, 0.000 ],   [ -0.500, 0.000, 0.809, -0.309 ],
                                [ 0.500, 0.500, -0.500, 0.500 ],   [ 0.500, 0.500, 0.500, 0.500 ],
                                [ 0.500, 0.000, 0.809, 0.309 ],    [ 0.309, -0.500, 0.809, 0.000 ],
                                [ 0.500, 0.000, 0.809, -0.309 ],   [ -0.500, 0.500, -0.500, 0.500 ],
                                [ 0.000, 0.309, 0.809, -0.500 ],   [ -0.309, 0.000, -0.500, 0.809 ],
                                [ -0.500, 0.309, 0.000, 0.809 ],   [ 0.309, 0.000, -0.500, 0.809 ],
                                [ 0.500, 0.309, 0.000, 0.809 ],    [ 0.309, 0.000, 0.500, 0.809 ],
                                [ 0.000, -0.309, 0.809, 0.500 ],   [ 0.000, 0.000, 0.000, 1.000 ],
                                [ -0.309, 0.000, 0.500, 0.809 ],   [ 0.000, 0.500, 0.309, 0.809 ],
                                [ 0.000, 0.309, 0.809, 0.500 ],    [ 0.000, -0.309, 0.809, -0.500 ],
                                [ 0.000, 0.500, -0.309, 0.809 ],   [ 0.000, 0.000, 1.000, 0.000 ]     ]    )

    I2Quaternions = np.array( [ [  1.000, 0.000, 0.000, 0.000 ],   [ 0.000, 0.000, 0.000, 1.000 ],          
                                [ 0.809, -0.309, 0.000, -0.500 ],  [ -0.309, 0.500, 0.000, 0.809 ],          
                                [ 0.309, 0.500, 0.000, 0.809 ],    [ 0.809, 0.309, 0.000, 0.500 ],          
                                [ -0.500, 0.000, 0.309, 0.809 ],   [ 0.500, 0.000, 0.309, 0.809 ],          
                                [ 0.500, 0.000, -0.309, 0.809 ],   [ 0.809, 0.000, -0.500, 0.309 ],          
                                [ 0.809, 0.000, 0.500, 0.309 ],    [ 0.809, 0.000, -0.500, -0.309 ],          
                                [ 0.809, 0.000, 0.500, -0.309 ],   [ -0.500, 0.000, -0.309, 0.809 ],          
                                [ 0.000, 0.309, 0.500, 0.809 ],    [ 0.500, 0.500, 0.500, 0.500 ],          
                                [ 0.809, 0.500, 0.309, 0.000 ],    [ 0.809, 0.309, 0.000, -0.500 ],          
                                [ 0.809, -0.309, 0.000, 0.500 ],   [ -0.500, 0.500, 0.500, 0.500 ],          
                                [ 0.809, -0.500, -0.309, 0.000 ],  [ 0.809, -0.500, 0.309, 0.000 ],          
                                [ -0.500, 0.500, -0.500, 0.500 ],  [ 0.000, 0.309, -0.500, 0.809 ],          
                                [ -0.309, -0.500, 0.000, 0.809 ],  [ 0.809, 0.500, -0.309, 0.000 ],          
                                [ -0.500, 0.809, 0.000, 0.309 ],   [ 0.000, 0.809, -0.309, 0.500 ],          
                                [ 0.500, 0.500, -0.500, 0.500 ],   [ -0.309, 0.000, 0.809, -0.500 ],          
                                [ 0.000, -0.309, -0.500, 0.809 ],  [ 0.309, -0.500, 0.000, 0.809 ],          
                                [ 0.500, 0.500, -0.500, -0.500 ],  [ 0.000, -0.309, 0.500, 0.809 ],          
                                [ 0.309, 0.000, 0.809, 0.500 ],    [ 0.000, 0.809, 0.309, 0.500 ],          
                                [ 0.500, 0.809, 0.000, 0.309 ],    [ -0.500, -0.309, 0.809, 0.000 ],          
                                [ -0.309, 0.000, 0.809, 0.500 ],   [ -0.500, 0.309, 0.809, 0.000 ],          
                                [ -0.500, 0.500, 0.500, -0.500 ],  [ -0.500, 0.500, -0.500, -0.500 ],          
                                [ 0.500, -0.309, 0.809, 0.000 ],   [ 0.309, 0.000, 0.809, -0.500 ],          
                                [ 0.500, 0.309, 0.809, 0.000 ],    [ 0.500, 0.500, 0.500, -0.500 ],          
                                [ 0.000, 0.500, 0.809, 0.309 ],    [ 0.309, 0.809, 0.500, 0.000 ],          
                                [ 0.500, 0.809, 0.000, -0.309 ],   [ -0.309, 0.809, 0.500, 0.000 ],          
                                [ -0.500, 0.809, 0.000, -0.309 ],  [ -0.309, 0.809, -0.500, 0.000 ],          
                                [ 0.000, -0.500, 0.809, -0.309 ],  [ 0.000, 1.000, 0.000, 0.000 ],          
                                [ 0.309, 0.809, -0.500, 0.000 ],   [ 0.000, 0.809, -0.309, -0.500 ],          
                                [ 0.000, -0.500, 0.809, 0.309 ],   [ 0.000, 0.500, 0.809, -0.309 ],          
                                [ 0.000, 0.809, 0.309, -0.500 ],   [ 0.000, 0.000, 1.000, 0.000 ]     ]    )

    return I1Quaternions
