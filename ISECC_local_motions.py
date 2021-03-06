#!/usr/bin/env python3.5
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import argparse
import sys
import os
import time
import math
import numpy as np
from pyquaternion import Quaternion
from datetime import datetime
from isecc import utils
from isecc import starparse

def getStarHeader( my_star, regen_string ):
    header = []
    header_index = int( 0 )
    full_header = []
    
    # Add run info to output star file
    date = str( datetime.now() )
    append_this = ''.join( [ '# SCRIPT_RUN_DATE: ', date ] )
    full_header.append( append_this.strip() )

    append_this = ''.join( [ '# SCRIPT_VERSION: ', sys.argv[0] ] )
    full_header.append( append_this.strip() )

    arguments = ' '.join( sys.argv[1:] )
    append_this = ''.join( [ '# SCRIPT_ARGS: ', arguments ] )
    full_header.append( append_this.strip() )

    with open(my_star, "r") as my_star:
        
        START_PARSE = None    # Needed for relion 3.1 star format

        for line in my_star:

            if START_PARSE == None:
                ### Store full header for final output
                full_header.append( line.strip() )

            if line.strip() == 'data_particles':
                START_PARSE = True

            if START_PARSE:
                if line.startswith('loop_'):
                    full_header.append( '' )
                    full_header.append( line.strip() )
                if line.startswith('_rln'):
                    full_header.append( line.strip() )
                    header_index = int( header_index + 1 )
                    header.append( line[1:].split()[0] )

    if 'rlnImageOriginalName' not in header:
        header.append( 'rlnImageOriginalName' )
        header_index = int( header_index + 1 )
        append_this = ''.join( [ '_rlnImageOriginalName #', str(header_index) ] )
        full_header.append( append_this )


    if 'rlnCustomUID' not in header:
        header.append( 'rlnCustomUID' )
        header_index = int( header_index + 1 )
        append_this = ''.join( [ '_rlnCustomUID #', str(header_index) ] )
        full_header.append( append_this )

    if 'rlnCustomVertexGroup' not in header:
        header.append( 'rlnCustomVertexGroup' )
        header_index = int( header_index + 1 )
        append_this = ''.join( [ '_rlnCustomVertexGroup #', str(header_index) ] )
        full_header.append( append_this )

    if 'rlnCustomOriginXYZAngstWrtParticleCenter' not in header:
        print( "rlnCustomOriginXYZAngstWrtParticleCenter not in header" )

    if 'rlnCustomRelativePose' not in header:
        print( "rlnCustomRelativePose not in header" ) 

    ### Add info for how to regenerate subparticles
    if '--timestamp_run' not in full_header[2] :
        full_header[2] = ' '.join( [ full_header[2], '--timestamp_run', regen_string ] )

    return header, full_header


def getStarData( my_star, header_length ):
    with open(my_star, "r") as my_star:
        stardata = []

        START_PARSE = None      # Needed for relion 3.1 star format

        for line in my_star:

            if line.strip() == 'data_particles':
                START_PARSE = True

            if START_PARSE:

                linesplit = line.split()

                if len( linesplit ) == header_length:
                    if line[0] != '#':      # avoid the stupid comment line
                        stardata.append( linesplit )
    return stardata


def generateSubparticleArray( ndarray_pent, header_pent, ndarray_hex, header_hex ):

    ### Get index for icosahedral (priors) and locally refined X and Y values

    ## Pentavalent
    icos_X_index_pent,  icos_Y_index_pent  =  starparse.getOffsetAngstPriors( header_pent )
    local_X_index_pent, local_Y_index_pent =  starparse.getOffsetAngst( header_pent )

    ## Hexavalent
    icos_X_index_hex,  icos_Y_index_hex  =  starparse.getOffsetAngstPriors( header_hex )
    local_X_index_hex, local_Y_index_hex =  starparse.getOffsetAngst( header_hex )


    ### Get index for the local XYZ relative to particle origin
    relativeXYZ_index_pent = starparse.getOriginXYZAngstWrtParticleCenter( header_pent )
    relativeXYZ_index_hex = starparse.getOriginXYZAngstWrtParticleCenter( header_hex )

    ### Get index for the vertex group assignment
    vertexGroup_index_pent = starparse.getVertexGroup( header_pent )
    vertexGroup_index_hex = starparse.getVertexGroup( header_hex )

    ### Get index for whole particle unique identifier
    micrographname_index_pent, imagename_index_pent, particleID_index_pent = starparse.getMicrographName( header_pent )
    micrographname_index_hex, imagename_index_hex, particleID_index_hex = starparse.getMicrographName( header_hex )


    ### Example vertex specifier from hexavalent:    5f01a.3f01a.2f01a
    ### Example vertex specifier from pentavalent:    5f01

    total_particle_number = np.true_divide( len( ndarray_pent ), 12 )
    total_particle_number2 = np.true_divide( len( ndarray_hex ), 60 )
    total_subparticle_number = int( len( ndarray_pent ) + len( ndarray_hex ) )

    if total_particle_number != total_particle_number2:
        print( 'ERROR: Total particles from pentavalent file does not equal particle number from hexavalent!' )
        print( total_particle_number, '!=', total_particle_number2 )
        sys.exit()


    subparticle_array_dtype = np.dtype( [   ( 'ParticleSpecifier', '|S200' ), 
                        ( 'Subparticle_type', '|S11' ), 
                        ( 'Vertex5f_general', 'i4' ), ( 'Vertex5f_specific', '|S1' ),
                        ( 'Vertex3f_general', 'i4' ), ( 'Vertex3f_specific', '|S1' ),
                        ( 'Vertex2f_general', 'i4' ), ( 'Vertex2f_specific', '|S1' ),
                        ( 'SubparticleOrigin_icos',  '<f4', (2,) ),
                        ( 'SubparticleOrigin_local', '<f4', (2,) ),
                        ( 'SubparticleRelative_XYZ', '<f4', (3,) )  ] )

    subparticle_array = np.zeros( total_subparticle_number, dtype=subparticle_array_dtype )

    ### Read everything into a subparticle array
    print( '\nAdding all pentavalent capsomers into subparticle array.' )
    
    ### Start with the pentavalent
    for index in range(0, len( ndarray_pent ) ):

        # Particle Specifier
        subparticle_array[ index ][ 'ParticleSpecifier' ] = ndarray_pent[ index ][ particleID_index_pent ]
        # Subparticle Type
        subparticle_array[ index ][ 'Subparticle_type' ] = 'pentavalent'
        # X,Y Priors
        subparticle_array[ index ][ 'SubparticleOrigin_icos' ] = ndarray_pent[ index ][ icos_X_index_pent ], ndarray_pent[ index ][ icos_Y_index_pent ]
        # X,Y Locally Refined
        subparticle_array[ index ][ 'SubparticleOrigin_local' ] = ndarray_pent[ index ][ local_X_index_pent ], ndarray_pent[ index ][ local_Y_index_pent ]
        # Relative X,Y,Z with respect to particle center
        subparticle_array[ index ][ 'SubparticleRelative_XYZ' ] = ndarray_pent[ index ][ relativeXYZ_index_pent ].split(',')
        # Vertex Assignment
        vertex_assignment = int( str( ndarray_pent[ index ][ vertexGroup_index_pent ] )[2:4] )  #example: '5f01'
        subparticle_array[ index ][ 'Vertex5f_general' ] = vertex_assignment


    ### Here we want to also find the max and min z values.
    ### Below syntax gets the 3rd column (z) of field 'SubparticleRelative_XYZ'
    max_z = np.amax( subparticle_array[:]['SubparticleRelative_XYZ'][:,2] )
    min_z = np.amin( subparticle_array[:]['SubparticleRelative_XYZ'][:,2] )
    print( '  Note: Relative z range is from', min_z, 'to', max_z )
    

    ### Add in the hexavalents
    print( 'Adding all hexavalent capsomers into subparticle array.' )

    for index in range( 0, len( ndarray_hex ) ):

        # Sort out the two indexes
        hex_index = index
        subpart_index = int( len( ndarray_pent ) + hex_index )

        # Particle Specifier
        subparticle_array[ subpart_index ][ 'ParticleSpecifier' ] = ndarray_hex[ hex_index ][ particleID_index_hex ]
        # Subparticle Type
        subparticle_array[ subpart_index ][ 'Subparticle_type' ] = 'hexavalent'
        # X,Y Priors
        subparticle_array[ subpart_index ][ 'SubparticleOrigin_icos' ] = ndarray_hex[ hex_index ][ icos_X_index_hex ], ndarray_hex[ hex_index ][ icos_Y_index_hex ]
        # X,Y Locally Refined
        subparticle_array[ subpart_index ][ 'SubparticleOrigin_local' ] = ndarray_hex[ hex_index ][ local_X_index_hex ], ndarray_hex[ hex_index ][ local_Y_index_hex ]
        # Relative X,Y,Z with respect to particle center
        subparticle_array[ subpart_index ][ 'SubparticleRelative_XYZ' ] = ndarray_hex[ hex_index ][ relativeXYZ_index_hex ].split(',')

        # Vertex Assignment
        vertex_assignment = str( ndarray_hex[ hex_index ][ vertexGroup_index_hex ] )    # example: '5f01a.3f01a.2f01a'
        subparticle_array[ subpart_index ][ 'Vertex5f_general'  ] = vertex_assignment[2:4]    # character 3-4
        subparticle_array[ subpart_index ][ 'Vertex5f_specific' ] = vertex_assignment[4]    # character 5
        subparticle_array[ subpart_index ][ 'Vertex3f_general'  ] = vertex_assignment[8:10]    # character 9-10
        subparticle_array[ subpart_index ][ 'Vertex3f_specific' ] = vertex_assignment[10]    # character 11
        subparticle_array[ subpart_index ][ 'Vertex2f_general'  ] = vertex_assignment[14:16]    # character 15-16
        subparticle_array[ subpart_index ][ 'Vertex2f_specific' ] = vertex_assignment[16]    # character 17

    return subparticle_array, max_z


def correlateRefinedCapsomers( subparticle_array, max_z, inclusion_threshold ) :

    particle_names = np.array( subparticle_array['ParticleSpecifier'] )

    unique_particles = np.unique( particle_names )

    z_threshold = np.around( (inclusion_threshold * max_z), decimals = 2 )
    central_slice_limit = np.around( 1.05, decimals = 3 )
    central_slice_threshold = np.around( ( central_slice_limit * max_z), decimals = 2 )

    print( '\nNote: Current threshold is', inclusion_threshold, 'of particle radius. Will only consider vertices where:' )
    print( '   pentavalent relative Z >', z_threshold, 'or' )
    print( '   pentavalent relative Z <', (-1*z_threshold), '\n' )

    print( 'Will report deltas in distance between hexavalent and pentavalent capsomer' )
    print( '   ...as compared to icosahedral refinement. Values in Angstroms.' )
    print( '   Note: Z-dimension is flattened for this analysis.\n' )

    print( 'For central plane, will consider deltas in z-range of:' )
    print( '   ',(-1*central_slice_threshold),'< pentavalent relative Z <', central_slice_threshold )
    print( '   This represents a threshold of:', central_slice_limit )
    print( '   Note: Z-dimension is flattened for this analysis.\n' )


    ### iterate through all the unique particles
    for index, item in enumerate(unique_particles, start=0):

        ### Particle specifier for printout
        particle_specifier = str(index).rjust(5, '0')

        # make temporary array with all subparticles from current particle
        condition = subparticle_array['ParticleSpecifier'] == item

        #subparticles = np.extract( condition, subparticle_array )    # Don't need to use np.extract
        subparticles = subparticle_array[condition]

        #### Check distances along central plane (Z~=0)
        assessed_diameter = []
        max_diameter = 0

        for assessed_index, subparticle in enumerate(subparticles, start=0):

            ### Icos coords
            reference_x_icos  = subparticle['SubparticleRelative_XYZ'][0]
            reference_y_icos  = subparticle['SubparticleRelative_XYZ'][1]
            reference_z_icos  = subparticle['SubparticleRelative_XYZ'][2]
            reference_xy_icos = np.array( [ reference_x_icos, reference_y_icos, 0 ] )
            reference_xyz_icos = np.array( [ reference_x_icos, reference_y_icos, reference_z_icos ] )

            ### Local coords
            reference_delta_x = subparticle['SubparticleOrigin_local'][0] - subparticle['SubparticleOrigin_icos'][0]
            reference_delta_y = subparticle['SubparticleOrigin_local'][1] - subparticle['SubparticleOrigin_icos'][1]
            reference_x_local = subparticle['SubparticleRelative_XYZ'][0] + reference_delta_x
            reference_y_local = subparticle['SubparticleRelative_XYZ'][1] + reference_delta_y
            reference_xy_local = np.array( [ reference_x_local, reference_y_local, 0 ] )

            """ This code looks for capsomers within a tolerance of the central plane """
            if (reference_z_icos > (-1*central_slice_threshold)) and (reference_z_icos < central_slice_threshold) and (assessed_index not in assessed_diameter):

                for compare_index, compare in enumerate(subparticles, start=0):

                    ### Icos coords
                    compare_x_icos  = compare['SubparticleRelative_XYZ'][0]
                    compare_y_icos  = compare['SubparticleRelative_XYZ'][1]
                    compare_z_icos  = compare['SubparticleRelative_XYZ'][2]
                    compare_xy_icos = np.array( [ compare_x_icos, compare_y_icos, 0 ] )
                    compare_xyz_icos = np.array( [ compare_x_icos, compare_y_icos, compare_z_icos ] )
                    negate_compare_xyz_icos = -1 * compare_xyz_icos

                    ### Local coords
                    compare_delta_x = compare['SubparticleOrigin_local'][0] - compare['SubparticleOrigin_icos'][0]
                    compare_delta_y = compare['SubparticleOrigin_local'][1] - compare['SubparticleOrigin_icos'][1]
                    compare_x_local = compare['SubparticleRelative_XYZ'][0] + compare_delta_x
                    compare_y_local = compare['SubparticleRelative_XYZ'][1] + compare_delta_y
                    compare_xy_local = np.array( [ compare_x_local, compare_y_local, 0 ] )


                    this_diameter = utils.assess3dDistance( reference_xyz_icos, compare_xyz_icos )
                    if this_diameter > max_diameter:
                        max_diameter = this_diameter
                        ideal_polar_distance = np.around( utils.assess3dDistance( reference_xyz_icos, compare_xyz_icos ), decimals=2 )
                        flattened_ideal_polar_distance = np.around( utils.assess3dDistance( reference_xy_icos, compare_xy_icos ), decimals=2 )
                        flattened_real_polar_distance  = np.around( utils.assess3dDistance( reference_xy_local, compare_xy_local ), decimals=2 )

                print( ideal_polar_distance, flattened_ideal_polar_distance, flattened_real_polar_distance )


    return


def main(args):

    ### Today's date will be used in the subparticle path
    date = str( datetime.now().strftime("%Y%m%d") )
    hour = str( datetime.now().strftime("%H%M") )
    RUN_ID = '_'.join( [ 'assess', date, hour ] )
    regen_string = '_'.join( [ date, hour ] )

    if args.pentavalent.endswith(".star"):
        filename = args.pentavalent
        print( "\nReading locally refined coordinates from:", filename )
        pent_header, fullheader = getStarHeader( filename, regen_string )
        stardata = getStarData( filename, len( pent_header ) )
        pentavalent_ndarray = np.asarray( stardata, order='C' )
    else:
        print( "Please provide a valid star file" )
        sys.exit()


    if args.hexavalent.endswith(".star"):
        filename = args.hexavalent
        print( "Reading locally refined coordinates from:", filename )
        hex_header, fullheader = getStarHeader( filename, regen_string )
        stardata = getStarData( filename, len( hex_header ) )
        hexavalent_ndarray = np.asarray( stardata, order='C' )
    else:
        print( "Please provide a valid star file" )
        sys.exit()

    subparticle_array, max_z = generateSubparticleArray( pentavalent_ndarray, pent_header, hexavalent_ndarray, hex_header  )
    correlateRefinedCapsomers( subparticle_array, max_z, args.threshold )

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pentavalent", required=True, help="Locally refined pentavalent capsomers")
    parser.add_argument("--hexavalent", required=True, help="Locally refined hexavalent capsomers")
    parser.add_argument("--threshold", type=float, default='0.9', help="Threshold for inclusion")
    sys.exit(main(parser.parse_args()))
