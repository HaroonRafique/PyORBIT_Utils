from pylab import *


def set_mystyle():
    params = {
        'figure.subplot.left': 0.15,
        'figure.subplot.right': 0.95,
        'figure.subplot.bottom': 0.15,
        'figure.subplot.top': 0.9,
        'figure.subplot.wspace': 0.2,
        'figure.subplot.hspace': 0.2,
        'axes.labelsize': 'large',
        'axes.linewidth': 2,
        'legend.fancybox': True,
        'legend.fontsize': 'large',
        'xtick.labelsize': 'large',
        'ytick.labelsize': 'large',
        'xtick.major.pad': 18,
        'ytick.major.pad': 18,
        'text.fontsize': 'large'
    }
    rcParams.update(params)


# # Format axes
# majorFormatter = FormatStrFormatter('%3.2e')
# sctfcFormatter = ScalarFormatter(useOffset=False, useMathText=True)
# sctfcFormatter.set_scientific(True)

# gcf().subplots_adjust(left=None, bottom=None, right=0.80, top=None, wspace=None, hspace=None)
