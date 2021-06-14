# Programs for the EPSCOR 2021 summer program

This repo includes various tools, code, examples, etc. to be used in the EPSCOR 2021 summer program hosted at U. Delaware.

## Setup and Required Software

To run the examples, you will need to first download the .obj files. This can be complete by going to `data` and running `./DownloadData.sh`. The files will be directly pulled into the `data` directory.

You will need to load the CVMFS and IceTray frameworks. For more, see: `examples/cluster/README.md`.

---

## Using Bash and the Madison Cluster

There are some short tutorials on how to use bash and login to the cluster. For more information, see the README in `./examples/cluster`.

---

## Machine Learning

Examples of how to train machine learning networks. Note that you will need to have the example data sets downloaded (see above)

 * `examples/rfr_example.py` trains a random forrest regression using one of the Monte-Carlo data sets in the `data` directory

---

## IceTray

There are several examples on how to run an IceTray tray and modules. You must have already loaded up an icecube environment to run these scripts.

 * `examples/icetray/Lesson1_SimpleFilter.py` is an example on how to write a filter to select only the frames which pass some set of pre-dermined values. This shows how to run the filters on both the P and Q-Frames
 * `examples/icetray/Lesson2_CustomModule.py` is an example of writing a module in python which has the ability to run on both the Q and P frames. This style is more useful than the filters when you need to keep track of values between frames, such as calculating the distribution of arrival directions for many events.
 * `examples/icetray/Lesson3_PlottingModule.py` This builds on the previous example. Often, you might want to extract various pieces of information from the frame and make a plot of the values. This script is an example of how to store various values from many frames and to make a plot of what the module saw.
 * `examples/icetray/Lesson4_UsingGCDFiles.py` Information about the detector layout is not stored directly in the Q/P frames. Instead, this information is stored in the Geometry frame. In this example, we extract this IceTop hits (charge/time) as well as where those hits are and make a plot.

The examples run on IceCube-standard files and thus, it would be best to test these directly on the Madison cluster. Otherwise, you may need to download the simulation files by hand.
