import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, Button, TextBox
from scipy.optimize import curve_fit

def curve_fit_gui(fun, x, y, *args, **kwargs):
    """graphical and interactive curve fitting function 
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
    
    Args:
        fun (function): the function used for fitting (see )
        x (numpy array): the x coordinate of the data to fit
        y (numpy array): the y coordinate of the data to fit 
        *args : any extra arguments that can be passed to scipy.optimize.curve_fit
        *kwargs : any keyword arguments that can be passed to scipy.optimize.curve_fit
    """
    fitgui = CurveFitGUI(fun, x, y, *args, **kwargs)
    return fitgui

class CurveFitGUI(object):
    def __init__(self, fun, x, y, picker=5, **kwargs):
        
        self.fun = fun 
        self.x, self.y = x, y
        self.kwargs = kwargs

        # create figure and plot raw data
        self.fig = plt.figure(num='fit gui')
        self.ax = self.fig.add_axes([0.1, 0.2, 0.8, 0.79])
        self.ax.scatter(x, y, color='black', alpha=0.5, picker=picker)

        # point selection widgets
        self.point_selector = PointSelector(self.ax, x, y)

        # fit button
        ax_fit_button = self.fig.add_axes([0.7, 0.01, 0.05, 0.05])
        self.fit_button = Button(ax_fit_button, label='fit')
        self.fit_button.on_clicked(self.fit_callback)

        #XXX weird bug the p0 entry becomes unresponsive
        # function entry box 
        # self.funbox_ax = self.fig.add_axes([0.15, 0.07, 0.5, 0.05])
        # self.funbox = TextBox(self.funbox_ax, 'Function:')
        # self.funbox.on_submit(self.inputfun_callback)

        # # initial guess
        # self.p0_ax = self.fig.add_axes([0.15, 0.01, 0.5, 0.05])
        # self.p0 = TextBox(self.p0_ax, 'P0:')
        # self.p0.on_submit(self.inputp0_callback)

        # internals 
        self._fit_line = None

    def fit_callback(self, event):
        # run the curve_fit function and store the result
        print("fit")
        if self._fit_line is not None and self._fit_line:
            self._fit_line.pop(0).remove()

        if self.point_selector.mask.any():
            self.selected_x = self.x[self.point_selector.mask]
            self.selected_y = self.y[self.point_selector.mask]
            self.params, self.params_cov = curve_fit(self.fun, self.selected_x, self.selected_y, **self.kwargs)
            self.y_fit = self.fun(self.selected_x, *self.params)
            self._fit_line = self.ax.plot(self.selected_x, self.y_fit, label="fit", zorder=3, color="blue")
        
        self.fig.canvas.draw()

    def inputfun_callback(self, text):
        print("inputfun callback")
        if text:
            def inputfun(x, *p):
                res = eval(text)
                return res
            
            self.fun = inputfun

    def inputp0_callback(self, text):
        print("p0 callback")
        if text:
            self.p0 = eval(text)

        return

class PointSelector(object):
    """A class for setting interactive point selection in a matplotlib scatter plot.

    Heavily inspired from https://stackoverflow.com/questions/31919765/choosing-a-box-of-data-points-from-a-plot

    Features:
    - Define a rectangle by dragging the mouse allows to select/unselect all the points in the rectangle
    - Clicking on a point selects/unselects it
    - Clicking the 'select all' button selects or unselect all the point. 

    Non selected points are in black while selected points are colored.
    """

    def __init__(self, ax, x, y):
        self.ax = ax
        self.canvas = ax.figure.canvas
        self.x, self.y = x, y
        self.mask = np.zeros(x.shape, dtype=bool)

        self._highlight = self.ax.scatter(
            [], [], color='purple', zorder=2, picker=5, alpha=0.5)

        self.rectangle_selector = RectangleSelector(
            self.ax, self, useblit=True)

        ax_sa_button = self.ax.figure.add_axes([0.8, 0.01, 0.1, 0.05])
        self.select_all_button = Button(ax_sa_button, label='select all')
        self.select_all_button.on_clicked(self.select_all)

        self.canvas.mpl_connect('pick_event', self.onpick)

    def __call__(self, event1, event2):
        # print("rectangle selector")
        self.mask ^= self.inside(event1, event2)
        self.update_canvas()

    def update_canvas(self):
        xy = np.column_stack([self.x[self.mask], self.y[self.mask]])
        self._highlight.set_offsets(xy)
        self.canvas.draw()

    def select_all(self, event):
        if self.mask.all():
            # print("unselect everything")
            self.mask.fill(False)
        else:
            # print("select everything")
            self.mask.fill(True)

        self.update_canvas()

    def onpick(self, event):
        # print("on pick")
        # toggle point selection
        if event.artist != self._highlight:
            self.mask[event.ind[0]] = not self.mask[event.ind[0]]

        self.update_canvas()

    def inside(self, event1, event2):
        """Returns a boolean mask of the points inside the rectangle defined by
        event1 and event2."""
        # Note: Could use points_inside_poly, as well
        x0, x1 = sorted([event1.xdata, event2.xdata])
        y0, y1 = sorted([event1.ydata, event2.ydata])
        mask = ((self.x > x0) & (self.x < x1) &
                (self.y > y0) & (self.y < y1))
        return mask


if __name__ == "__main__":
    def lorentzian(x, center=0.0, gamma=2.0):
        y = 1/np.pi * 0.5*gamma / ((x - center)**2 + (0.5*gamma)**2)
        return y

    # lorentzian + gaussian noise
    np.random.seed(12345)
    x = np.linspace(-2, 3, num=100)
    y_truth = lorentzian(x)
    sig = 0.01
    noise = sig*np.random.normal(size=x.shape)
    y_obs = y_truth + noise

    fit_gui = curve_fit_gui(lorentzian, x, y_obs)

    plt.show()
