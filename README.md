# Programs for the EPSCOR 2021 summer program

This repo includes various tools, code, examples, etc. to be used in the EPSCOR 2021 summer program hosted at U. Delaware.

## Setup and Required Software

To run all programs in this repository, you will need many standard python libraries including

 * sklearn
 * pickle
 * numpy

Of these, all but `sklearn` are already included on the IceCube cluster in Madison (AKA the Cobalt machines) To load these, run in your terminal:

``eval  `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.0/setup.sh` ``


### Data Sets for the Examples
To run the examples, you will need to first download the .obj files. This can be complete by going to `data` and running `./DownloadData.sh`. The files will be directly pulled into the `data` directory.

---

## Machine Learning

Examples of how to train machine learning networks. Note that you will need to have the example data sets downloaded (see above)

 * `examples/rfr_example.py` trains a random forrest regression using one of the Monte-Carlo data sets in the `data` directory

---

## IceTray

There are examples on how to run an IceTray tray and modules. You must have already loaded up an icecube environment to run these scripts.

 * `examples/icetray/SimpleFilter.py` is an example on how to write a filter to select only the frames which pass some set of pre-dermined values. This shows how to run the filters on both the P and Q-Frames
 * `examples/icetray/CustomModule.py` is an example of writing a module in python which has the ability to run on both the Q and P frames. This style is more useful than the filters when you need to keep track of values between frames, such as calculating the distribution of arrival directions for many events.

The examples run on IceCube-standard files and thus, it would be best to test these directly on the Madison cluster. Otherwise, you may need to download the simulation files by hand.
