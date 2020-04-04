# Curve Fitting GUI

[![Build Status](https://travis-ci.org/MaximeBouton/curve_fit_gui.svg?branch=master)](https://travis-ci.org/MaximeBouton/curve_fit_gui)
[![Coverage Status](https://coveralls.io/repos/github/MaximeBouton/curve_fit_gui/badge.svg?branch=master)](https://coveralls.io/github/MaximeBouton/curve_fit_gui?branch=master)

This project provides a graphical interface for the scipy [curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) function. 
It is relying on [matplotlib](https://matplotlib.org/) for the GUI.


## Usage 

```python 
import numpy as np
import curve_fit_gui

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

```

![demo](fitgui_demo.gif)
