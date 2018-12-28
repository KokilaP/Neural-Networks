# Neural-Networks

## Compatibility Issues

The code can only run on Python 2 because Brian2 is not supported or working correctly on Python 3 at the moment. Please refer to the steps below on how to modify Jupyter notebook environment to Python 2 using Anaconda: 

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

