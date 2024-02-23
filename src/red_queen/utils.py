"""
This module contains utility functions and classes for the red_queen project.
"""

# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


def compute_metrics(dictionary, metrics):
    circuit = dictionary["circuit"]
    new_dict = {}
    for key, val in dictionary.items():
        if key != "circuit":
            new_dict[key] = val

    for name, metric in metrics.items():
        new_dict[name] = metric(circuit)
    return new_dict
