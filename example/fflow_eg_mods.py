"""
Some example modules to demo event processing
"""
import numpy as np


class Generator():
    def __init__(self, mean, variance, quantity):
        self.mean = mean
        self.variance = variance
        self.quantity = quantity

    def __call__(self, data):
        data["values"] = np.random.normal(loc=self.mean, scale=self.variance, size=self.quantity)


class Summarize():
    def __init__(self, methods, replace_values=False):
        self.methods = {m: getattr(np, m) for m in methods}
        self.replace_values = replace_values

    def __call__(self, data):
        for name, method in self.methods.items():
            data[name] = method(data["values"])
        if self.replace_values:
            del data["values"]

