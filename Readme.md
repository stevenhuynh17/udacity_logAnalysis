—————————————

INTRODUCTION:

—————————————

PROJECT: Logs Analysis Project

DESCRIPTION: Collects and sorts the information specified for the project

AUTHORS: Steven Huynh


———————————————————————

OPERATING INSTRUCTIONS:

———————————————————————

Setting up your VM environment:
1) Install VirtualBox version 5.1 (Oct 2017) for most stable use: https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
2) Install Vagrant: https://www.vagrantup.com/downloads.html
3) Download the VM configuration into a folder you plan to hold the project: https://github.com/udacity/fullstack-nanodegree-vm
4) Navigate to the vagrant folder from the repository through the terminal
5) Type 'vagrant up'. If it doesn't work , do 'vagrant init' then try again.
6) Type 'vagrant ssh'. Setup complete.

Running the program:
1) In your VM, make sure the file newsdata.sql is there and then type 'psql -d news -f newsdata.sql'. The sql file can be found through the following link: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
2) Connect to the database with 'psql -d news'
3) Open up another terminal window, navigate to the same folder and run 'python queries.py'


—————————

CONTENTS:

—————————
- queries.py
- output.txt
- readme.txt
- newsdata.sql (Must download)
