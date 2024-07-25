import logging
import argparse

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cmocean
import cmdline_provenance as cmdprov


def convert_pr_units(da):
    """Convert kg m-2 s-1 to mm day-1.
    
    Args:
      da (xarray.DataArray): Precipitation data
   
    """
    
    da.data = da.data * 86400
    da.attrs["units"] = "mm/day"
    
    assert da.data.min() >= 0.0, "There is at least one negative precipitation value"
    assert da.data.max() < 2000, "There is a precipitation value/s > 2000 mm/day"
    
    return da


def apply_mask(darray, sftlf_file, realm):
    """Mask ocean or land using a sftlf (land surface fraction) file.
   
    Args:
      da (xarray.DataArray): Data to mask
      sftlf_file (str): Land surface fraction file
      realm (str): Realm to mask
   
    """
  
    ds = xr.open_dataset(sftlf_file)
    if realm.lower() == 'land':
        masked_da = da.where(ds["sftlf"].data < 50)
    elif realm.lower() == 'ocean':
        masked_da = da.where(ds["sftlf"].data > 50)   
    else:
        raise ValueError("""Mask realm is not 'ocean' or 'land'""")

    return masked_da


def create_plot(clim, model, season, gridlines=False, levels=None):
    """Plot the precipitation climatology.
    
    Args:
      clim (xarray.DataArray): Precipitation climatology data
      model (str): Name of the climate model
      season (str): Season
      
    Kwargs:
      gridlines (bool): Select whether to plot gridlines
      levels (list): Tick marks on the colorbar    
    
    """

    if not levels:
        levels = np.arange(0, 13.5, 1.5)
        
    fig = plt.figure(figsize=[12,5])
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
    clim.sel(season=season).plot.contourf(
        ax=ax,
        levels=levels,
        extend="max",
        transform=ccrs.PlateCarree(),
        cbar_kwargs={"label": clim.units},
        cmap=cmocean.cm.haline_r
    )
    ax.coastlines()
    if gridlines:
        plt.gca().gridlines()
    
    title = f"{model} precipitation climatology ({season})"
    plt.title(title)


def get_log_and_key(pr_file, history_attr, plot_type):
    """Get key and command line log for image metadata.
   
    Different image formats allow different metadata keys.
   
    Args:
      pr_file (str): Input precipitation file
      history_attr (str): History attribute from pr_file
      plot_type (str): File format for output image
   
    """
    
    valid_keys = {"png": "History",
                  "pdf": "Title",
                  "svg": "Title",
                  "eps": "Creator",
                  "ps" : "Creator",
    }    

    assert plot_type in valid_keys.keys(), f"Image format not one of: {*[*valid_keys],}"
    log_key = valid_keys[plot_type]
    new_log = cmdprov.new_log(infile_logs={pr_file: history_attr})
    
    return log_key, new_log
   

def main(inargs):
    """Run the program."""

    log_lev = logging.INFO if inargs.verbose else logging.WARNING
    logging.basicConfig(level=log_lev, filename=inargs.logfile)

    ds = xr.open_dataset(inargs.pr_file)
    
    clim = ds["pr"].groupby("time.season").mean("time", keep_attrs=True)

    try:
        input_units = clim.attrs["units"]
    except KeyError:
        raise KeyError("Precipitation variable in {inargs.pr_file} must have a units attribute")

    if input_units == "kg m-2 s-1":
        clim = convert_pr_units(clim)
        logging.info("Units converted from kg m-2 s-1 to mm/day")
    elif input_units == "mm/day":
        pass
    else:
        raise ValueError("""Input units are not 'kg m-2 s-1' or 'mm/day'""")

    if inargs.mask:
        sftlf_file, realm = inargs.mask
        clim = apply_mask(clim, sftlf_file, realm)

    create_plot(
        clim,
        ds.attrs["source_id"],
        inargs.season,
        gridlines=inargs.gridlines,
        levels=inargs.cbar_levels,
    )
                
    log_key, new_log = get_log_and_key(
        inargs.pr_file,
        ds.attrs["history"],
        inargs.output_file.split('.')[-1],
    )
    plt.savefig(
        inargs.output_file,
        metadata={log_key: new_log},
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )


if __name__ == "__main__":
    description = "Plot the precipitation climatology for a given season."
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("pr_file", type=str, help="Precipitation data file")
    parser.add_argument("season", type=str, help="Season to plot")
    parser.add_argument("output_file", type=str, help="Output file name")

    parser.add_argument(
        "--gridlines",
        action="store_true",
        default=False,
        help="Include gridlines on the plot",
    )
    parser.add_argument(
        "--cbar_levels",
        type=float,
        nargs="*",
        default=None,
        help="list of levels / tick marks to appear on the colorbar",
    )
    parser.add_argument(
        "--mask",
        type=str,
        nargs=2,
        metavar=("SFTLF_FILE", "REALM"),
        default=None,
        help="""Provide sftlf file and realm to mask ('land' or 'ocean')""",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Change the minimum logging reporting level from WARNING (default) to DEBUG",
    )
    parser.add_argument(
        "--logfile",
        type=str,
        default=None,
        help="Name of log file (by default logging information is printed to the screen)",
    )

    args = parser.parse_args()
    main(args)