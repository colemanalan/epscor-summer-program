# Programs for the EPSCOR 2021 summer program

This repo includes various tools, code, examples, etc. to be used in the EPSCOR 2021 summer program hosted at U. Delaware.

## Required Software

To run all programs in this repository, you will need many standard python libraries including

 * sklearn
 * pickle
 * numpy

Of these, all but `sklearn` are already included on the IceCube cluster in Madison (AKA the Cobalt machines) To load these, run in your terminal:

``eval  `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.0/setup.sh` ``



## Machine Learning

An example of a random forrest regression to train a network is included in the `examples` directory. To run this, you will need to first download the .obj files. This can be complete by going to `data` and running `./DownloadData.sh`. The files will be directly pulled into the `data` directory.
