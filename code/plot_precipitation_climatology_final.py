import argparse
import xarray
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy
import cmocean


def convert_pr_units(darray):
    """Convert kg m-2 s-1 to mm day-1.
    
    Args:
      darray (xarray.core.dataarray.DataArray): Precipitation data
    
    """
    
    darray.data = darray.data * 86400
    darray.attrs['units'] = 'mm/day'
    
    return darray


def apply_mask(darray, sftlf_file, realm):
    """Mask ocean or land using a sftlf (land surface fraction) file.
    
    Args:
      darray (xarray.core.dataarray.DataArray): Data to mask
      sftlf_file (str): Land surface fraction file
      realm (str): Realm to mask
    
    """
   
    dset = xarray.open_dataset(sftlf_file)
    sftlf_darray = dset['sftlf']
   
    if realm == 'land':
        masked_darray = darray.where(sftlf_darray.data < 50)
    else:
        masked_darray = darray.where(sftlf_darray.data > 50)   
   
    return masked_darray


def plot_climatology(clim_darray, model_name, season, gridlines=False):
    """Plot the precipitation climatology.
    
    Args:
      clim_darray (xarray.core.dataarray.DataArray): Precipitation climatology data
      season (str): Season    
    
    """
        
    fig = plt.figure(figsize=[12,5])
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
    clim_darray.sel(season=season).plot.contourf(ax=ax,
                                                 levels=numpy.arange(0, 15, 1.5),
                                                 extend='max',
                                                 transform=ccrs.PlateCarree(),
                                                 cbar_kwargs={'label': clim_darray.units},
                                                 cmap=cmocean.cm.haline_r)
    ax.coastlines()
    if gridlines:
        plt.gca().gridlines()
    
    title = '%s precipitation climatology (%s)' %(model_name, season)
    plt.title(title)


def main(inargs):
    """Run the program."""

    dset = xarray.open_dataset(inargs.pr_file)
    pr_darray = dset['pr']
    
    clim_darray = pr_darray.groupby('time.season').mean(dim='time')
    clim_darray = convert_pr_units(clim_darray)

    if inargs.mask:
        sftlf_file, realm = inargs.mask
        clim_darray = apply_mask(clim_darray, sftlf_file, realm)

    plot_climatology(clim_darray, dset.attrs['model_id'], inargs.season)
    plt.savefig(inargs.output_file, dpi=200)


if __name__ == '__main__':
    description='Plot the precipitation climatology.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("pr_file", type=str, help="Precipitation data file")
    parser.add_argument("season", type=str, help="Season to plot")
    parser.add_argument("output_file", type=str, help="Output file name")

    parser.add_argument("--mask", type=str, nargs=2,
                        metavar=('SFTLF_FILE', 'REALM'), default=None,
                        help='Realm to mask: "land" or "ocean")')

    args = parser.parse_args()
    
    main(args)
