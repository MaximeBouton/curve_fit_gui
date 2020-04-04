#!/usr/local/bin/python3

# Test Modules
import sys
import pytest
from os import path

# Import module under test
sys.path.append(path.join(path.dirname(path.abspath(__file__)), "../src"))
from curve_fit_gui import *

def test_instantiation():
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
    assert True



if __name__ == '__main__':
    test_instantiation()
