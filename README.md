# PQPBA
This repository contains the implementation code of the paper titled "Post-Qunatum Secure Password Based Authentication". The implementation is done in python3.
Our protocol contains three stages. They are:
1. User registration phase
2. Authentication phase
3. Key rotation phase

ML socket library is required to execute our code. This can be installed as follows:
       
        pip install mlsocket --user


Along with above mentioned phases, We also include a benchmarking directory for the performance reference. Following are the commands for 
executing the benchmarking directory.

    python3 <name_of_the_file.py>
**name_of_the_file** can be either *test_registration* or *test_authentication* or *test_keyrotation*

Following are the commands to execute all the phases:
1. Open the teriminal in the required directory.
2. run the following command:

        python3 website.py
4. Open another terminal in the same directory and run the following:

        python3 secure_server.py   


