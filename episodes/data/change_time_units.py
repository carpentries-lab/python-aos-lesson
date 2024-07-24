import argparse
import pdb

import iris
import cf_units
import cmdline_provenance as cmdprov


def main(inargs):
    """Run the program."""

    cube = iris.load_cube(inargs.infile, inargs.variable)

    time_axis = cube.coord('time')
    new_units = cf_units.Unit(inargs.new_time_units, calendar=time_axis.units.calendar)  
    time_axis.convert_units(new_units)

    new_log = cmdprov.new_log(infile_history={inargs.infile: cube.attributes['history']})
    cube.attributes['history'] = new_log
    
    if inargs.infile == inargs.outfile:
        cube.data # to realise lazy data to allow file overwrite
    iris.save(cube, inargs.outfile)


if __name__ == '__main__':

    extra_info ="""example: $ python change_time_units.py pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc
                precipitation_flux "days since 2001-01-01 00:00:00" test.nc"""
                
    description='Change the units of the time axis'
    parser = argparse.ArgumentParser(description=description, epilog=extra_info)
    
    parser.add_argument("infile", type=str, help="Input file name")
    parser.add_argument("variable", type=str, help="Variable to select from file")
    parser.add_argument("new_time_units", type=str, help="New time axis units")
    parser.add_argument("outfile", type=str, help="Output file name")

    args = parser.parse_args()            
    main(args)