# Neural-Networks

## Contents
1. [Compatibility Issues with Python 3](README.md#compatibility-issues-with-python-3)
2. [PySpike Installation](README.md#pyspike-installation)
3. [Useful GitHub links](README.md#useful-github-links)

## Compatibility Issues with Python 3

The code can only run on Python 2 because Brian2 is not supported or working correctly on Python 3 at the moment. Please refer to the steps below on how to modify Jupyter notebook environment to Python 2 using Anaconda if you already have Python 3 installed: 

1. Open up Anaconda command prompt

2. Enter the following code
      ```
      conda create -n ipykernel_py2 python=2 ipykernel
      source activate ipykernel_py2    # On Windows, remove the word 'source'
      python -m ipykernel install --user
      ```
      
3. Install packages required for the project code into this new Python 2 environment
    - With the Anaconda command prompt still open go the folder where **requirements.txt** is saved.
      ```
      cd C:\Users\kdilh\Documents\GitHub\Neural-Networks
      ```
      Then type, 
      
      ```
      pip install -r requirements.txt
      ```

4. Open up the project code on Jupyter Notebook and go to **Kernel --> Change Kernel --> Python 2** before running the code

Resource: [Installing the IPython kernel](https://ipython.readthedocs.io/en/latest/install/kernel_install.html#installing-the-ipython-kernel)

## PySpike Installation

PySpike requires the MSVC (Microsoft Visual C) compiler version 12 and above to install its cython package. Python 2 however only works with compiler version 9. The installation can be done by editing the **setup.py** installation file so that cython is not installed. For more details refer to the following forum: [Installation failure](https://github.com/mariomulansky/PySpike/issues/22) 

Here's one way to install PySpike:

1. If it's not already there, clone/download the PySpike GitHub repository into the Neural-Networks folder: [PySpike GitHub](https://github.com/mariomulansky/PySpike)
2. Edit **setup.py** in the **PySpike** folder so that cython will not be installed:

      <img src ="https://github.com/KokilaP/Neural-Networks/blob/master/images/pyspike.JPG" title="Edited portion of setup.py" height="187" width="371">
      
3. Install PySpike by running the new **setup.py**:
    - If using Anaconda:
       - Open up Anaconda prompt and activate the appropriate environment (as shown in **Compatibility Issues**)
       - cd into the **PySpike** folder where **setup.py** is
       - Type in: 
         ```
         python setup.py build_ext --inplace
         ```
For more installation methods: [PySpike](http://mariomulansky.github.io/PySpike/)

## Useful GitHub links

* Basic reference to use GitHub commandline: [https://git-scm.com/docs](https://git-scm.com/docs)
* Reference to resolve common conflicts with GitHub files: [http://allendowney.github.io/amgit/conflict.html](http://allendowney.github.io/amgit/conflict.html)
