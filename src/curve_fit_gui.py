import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, Button
from scipy.optimize import curve_fit

def curve_fit_gui(fun, x, y, *args, **kwargs):
    fitgui = CurveFitGUI(fun, x, y, args, kwargs)
    return fitgui


class CurveFitGUI(object):
    def __init__(self, fun, x, y, picker=5, *args, **kwargs):
        
        self.fun = fun 
        self.x, self.y = x, y

        self.fig, self.ax = plt.subplots()

        self.ax.scatter(x, y, color='black', picker=picker)
        self.point_selector = PointSelector(self.ax, x, y)

        ax_fit_button = self.fig.add_axes([0.5, 0.05, 0.1, 0.075])
        self.fit_button = Button(ax_fit_button, label='fit')
        self.fit_button.on_clicked(self.fit_callback)

        # internals 
        self._fit_line = None

        plt.show()

    def fit_callback(self, event):
        # run the curve_fit function and store the result
        print("fit")
        if self._fit_line is not None and self._fit_line:
            self._fit_line.pop(0).remove()

        if self.point_selector.mask.any():
            self.selected_x = self.x[self.point_selector.mask]
            self.selected_y = self.y[self.point_selector.mask]
            self.params, self.params_cov = curve_fit(self.fun, self.selected_x, self.selected_y)
            self.y_fit = self.fun(self.selected_x, *self.params)
            self._fit_line = self.ax.plot(self.selected_x, self.y_fit, label="fit", zorder=3, color="blue")
        
        self.fig.canvas.draw()

    def inputfun_callback(self, event):
        # allows user to specify the desired function in the gui and parse it
        pass

class PointSelector(object):
    """
    class to define a point selection tool. It allows the user to interactively select points in a matplotlib window.
    - Define a rectangle by dragging the mouse allows to select/unselect all the points in the rectangle
    - Clicking on a point selects/unselects it
    - Clicking the 'select all' button selects or unselect all the point. 

    Non selected points are in black while selected points are colored and have a larger marker.
    """

    def __init__(self, ax, x, y):
        self.ax = ax
        self.canvas = ax.figure.canvas
        self.x, self.y = x, y
        self.mask = np.zeros(x.shape, dtype=bool)

        self._highlight = self.ax.scatter(
            [], [], color='purple', zorder=2, picker=5)

        self.rectangle_selector = RectangleSelector(
            self.ax, self, useblit=True)

        ax_sa_button = self.ax.figure.add_axes([0.7, 0.05, 0.1, 0.075])
        self.select_all_button = Button(ax_sa_button, label='select all')
        self.select_all_button.on_clicked(self.select_all)

        self.canvas.mpl_connect('pick_event', self.onpick)

    def __call__(self, event1, event2):
        print("rectangle selector")
        self.mask ^= self.inside(event1, event2)
        self.update_canvas()

    def update_canvas(self):
        xy = np.column_stack([self.x[self.mask], self.y[self.mask]])
        self._highlight.set_offsets(xy)
        self.canvas.draw()

    def select_all(self, event):
        print("button press: ", self.mask[0])
        if self.mask.all():
            self.mask.fill(False)
        else:
            self.mask.fill(True)

        self.update_canvas()

    def onpick(self, event):
        print("on pick")
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


def main():

if __name__ == "__main__":
    def lorentzian(x, center=0.0, gamma=2.0):
        y = 1/np.pi * 0.5*gamma / ((x - center)**2 + (0.5*gamma)**2)
        return y

    x, y = np.random.random((2, 100))

    # lorentzian + gaussian noise
    np.random.seed(12345)
    x = np.linspace(-2, 3, num=100)
    y_truth = lorentzian(x)
    sig = 0.01
    noise = sig*np.random.normal(size=x.shape)
    y_obs = y_truth + noise

    fit_gui = curve_fit_gui(lorentzian, x, y_obs)

    plt.show()
