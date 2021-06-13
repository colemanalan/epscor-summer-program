# Using Bash and the Madison Cluster

## Logging into the Cluster
To access the Madison cluster (also known as the Cobalts and/or NPX), you will need an LDAP account. To get one, do the following:

1. You can request one by writing an email to help@icecube.wisc.edu and include your local PI in cc. 
2. Test it by logging into your IceCube email account at https://webmail.wipac.wisc.edu using your LDAP login.
3. While you are at it, create an IceCube Slack account by going to https://icecube-spno.slack.com/ and making an account __using your IceCube email address__.
4. Connect to the IceCube cluster by running this in your terminal: `ssh YourLdapNameHere@pub.icecube.wisc.edu` and then enter your password.
5. The step above will only connect you to the _login_ node. To start doing work (and to be able to access all IC files), next run `ssh cobalt`. This will put you on one of the Cobalt nodes which are used for, short, interactive work.


## Using Bash
Bash is one of the most common languages to use when you are interacting with a terminal.
The Madison cluster, by default uses bash.

### Useful Bash Commands
Here are a few useful bash commands to get you started:

* `cd <directory>` - moves to the specified directory. Using `..` for the `<directory>` will move you up one dir, using `~` will bring you to your home directory.
* `ls` - Lists the contents of your current directory. You can also give `ls` another directory which you are not currently at and it will list the contents of that one instead.
* `scp <file> <output>` - Makes a copy of `<file>` and moves it to the specified location. If output is a directory, will make the same-named file in that directory. If it is a file name, will copy and rename it to that.
* `mv <original> <final>` - Moves `<original>` to a new location `<final>`. Note: if you want to rename something, in bash, you move it instead.
* `less <file>` - Enters a terminal-based GUI where you can read the contents of an ASCII file. Close GUI with `q`.
* `nano <file>` - Enters a terminal-based GUI where you can edit the contents of an ASCII file. Close GUI with `Ctrl+x`.
* `cat <file(s)>` - Prints the contents of a file to the terminal.
* `head <file(s)>` - Prints the first few lines of a file to the terminal
* `tail <file(s)>` - Prints the last few lines of a file to the terminal
* `ssh <name>@<cluster>` - Connects you to a cluster (see above for the Madison settings)
* `pwd` - Prints the location of the directory you are in
* `man <program>` - Will print out the manual for (almost) every bash program
* `exit` - Will end your bash session (and will close your ssh session or terminal window)
* `Ctrl+c` or `Command+c` - Will kill any currently running, interactive, program
* `source <Bash Script>` - Runs a bash script
* `which <program>` - Prints the location of a program to the terminal

## Location of Things on the Cluster
When you first login to the Madison cluster, you will be in your _home_ directory `/home/yourname`. You can check this by running `pwd`.

### Your Data Directory
Your home directory is the only directory which is backed up. However, it is not very big, mainly, you will be working in your _data_ directory. This is located at `/data/user/yourname`. You can go there by running `cd /data/user/yourname`.

__Recommendation:__ Since you will typically be going to your _data_ directory, you can create a shortcut to it in your home directory. Go to your home directory by running `cd ~` (note that `~` is the bash shortcut to your home directory). 
Next make a link to your _data_ directory using `ln -s /data/user/yourname work`. 
This will make a _symbolic_ (thus the `-s`) link to your _data_ dir and call the shortcut `work` (you can choose a different name, if you prefer).

Your data directory has a maximum limit of 2TB. This is a lot, but if you ever hit that limit, you will have problems! You can check to see how you are doing compared to your limit by running `lfs quota -hg $(whoami) /data/user/$(whoami)`.

### IceTop Simulations
The icetop simulations are very computationally expensive to run.
So typically, you will not simulate them yourself and will instead just use the ones which we all share.
You can find them in:

`/data/ana/CosmicRay/IceTop_level3/sim/IC86.2012/`

The sub directories are the four elemental primaries that we simulate:

* proton - 12360
* iron - 12362
* helium - 12630
* oxygen - 12631

###Scintillator and Radio Simulations
For logistical reasons, the scintillator and radio simulations live in a different location.
You can find the raw CORSIKA files here:

`/data/sim/IceCubeUpgrade/CosmicRay/Radio/coreas/data`

in which there are various types of libraries for discrete or continuous distributions of showers.
The showers are sorted by primary, energy, and zenith bins.

Alternatively, you can instead use the processed I3 files, located here:

`/data/sim/IceCubeUpgrade/CosmicRay/Radio/coreas/i3-files`

The subdirectories match those of the CORSIKA simulations above.

##Setting up your Environment and Standard Software
It will be important to set up your bash _environment_ so that you can more easily run scripts and so that you do not have to install so many programs yourself. 

### CVMFS
Eventually, you will almost certainly be running some python scripts, so you can load up (almost) everything you need by running ``eval  `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh` ``. (You can also just try to use the most recent one by checking for the latest version using `ls /cvmfs/icecube.opensciencegrid.org/py3*` and using the highest number.)

Once you do this, you can check to make sure it worked by running `which python`. It should print out something like `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/RHEL_7_x86_64/bin/python` instead of the default `/usr/bin/python`.

Not only does this make a version of python (and various python libraries) available to you, but it also includes things like C++ compilers and C++ libraries available as well. This suite of programs extends to what is useful/required to run IceTray, so there is no guarantee that _everything_ that you need will be there.

### IceTray
You may also need to load up some variables if you intend to use the IceTray analysis framework. Likely, you will have installed your own installation of IceTray somewhere. Go to your _build_ directory and run `./env-shell.sh`. It should print a little logo and tell which which version of python it found. For more, see the IceTray example scripts.
