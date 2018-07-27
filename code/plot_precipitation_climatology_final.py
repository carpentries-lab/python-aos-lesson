import pdb
import argparse
import calendar
import warnings
warnings.filterwarnings('ignore')

import numpy
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
import iris.coord_categorisation
import cmocean
import cmdline_provenance as cmdprov


def read_data(fname, month):
    """Read an input data file"""
    
    cube = iris.load_cube(fname, 'precipitation_flux')
    
    iris.coord_categorisation.add_month(cube, 'time')
    cube = cube.extract(iris.Constraint(month=month))
    
    return cube


def convert_pr_units(cube):
    """Convert kg m-2 s-1 to mm day-1"""
    
    assert cube.units == 'kg m-2 s-1', "Program assumes that input units are kg m-2 s-1"
    
    cube.data = cube.data * 86400
    cube.units = 'mm/day'
    
    return cube


def apply_mask(pr_cube, sftlf_cube, realm):
    """Mask ocean using a sftlf (land surface fraction) file."""
    
    assert pr_cube.shape == sftlf_cube.shape 
    
    if realm == 'land':
        mask = numpy.where(sftlf_cube.data > 50, True, False)
    else:
        mask = numpy.where(sftlf_cube.data < 50, True, False)
    
    pr_cube.data = numpy.ma.asarray(pr_cube.data)
    pr_cube.data.mask = mask
    
    return pr_cube


def plot_data(cube, month, gridlines=False, levels=None):
    """Plot the data."""

    if not levels:
        levels = numpy.arange(0, 10)

    fig = plt.figure(figsize=[12,5])    
    iplt.contourf(cube, cmap=cmocean.cm.haline_r, 
                  levels=levels,
                  extend='max')

    plt.gca().coastlines()
    if gridlines:
        plt.gca().gridlines()
    cbar = plt.colorbar()
    cbar.set_label(str(cube.units))
    
    title = '%s precipitation climatology (%s)' %(cube.attributes['model_id'], month)
    plt.title(title)


def main(inargs):
    """Run the program."""

    cube = read_data(inargs.infile, inargs.month)   
    cube = convert_pr_units(cube)
    clim = cube.collapsed('time', iris.analysis.MEAN)

    if inargs.mask:
        sftlf_file, realm = inargs.mask
        assert realm in ['land', 'ocean']
        sftlf_cube = iris.load_cube(sftlf_file, 'land_area_fraction')
        clim = apply_mask(clim, sftlf_cube, realm)

    plot_data(clim, inargs.month, gridlines=inargs.gridlines,
              levels=inargs.cbar_levels)
    plt.savefig(inargs.outfile)
    
    new_log = cmdprov.new_log(infile_history={inargs.infile: cube.attributes['history']})
    fname, extension = inargs.outfile.split('.')
    cmdprov.write_log(fname+'.txt', new_log)


if __name__ == '__main__':

    description='Plot the precipitation climatology.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("infile", type=str, help="Input file name")
    parser.add_argument("month", type=str, choices=calendar.month_abbr[1:], help="Month to plot")
    parser.add_argument("outfile", type=str, help="Output file name")

    parser.add_argument("--gridlines", action="store_true", default=False,
                        help="Include gridlines on the plot")
    parser.add_argument("--cbar_levels", type=float, nargs='*', default=None,
                        help='list of levels / tick marks to appear on the colourbar')
    parser.add_argument("--mask", type=str, nargs=2, metavar=('SFTLF_FILE', 'REALM'), default=None,
                        help='Apply a land or ocean mask (specify the realm to mask: "land" or "ocean")')

    args = parser.parse_args()            
    main(args)