# Hostayni Platform

Hostayni is a contact space for entrepreneurs interested in socializing their projects, sharing and learning about entrepreneurship news, participating in innovation and sustainability events, and empowering their knowledge and entrepreneurial skills, thus contributing to the construction of sustainable global cities.

# How to install

<dl>
  <dt>Creating virtual environment to project</dt>
  <br>
   <dd>This step assumes that you have already installed and configured te following package/tools:</dd> 
   
   [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/ "Virtualenvwrapper")
   
   [PostgreSQL database manager](https://www.postgresql.org/download/ "Virtualenvwrapper")
   
* Create the virtual environment.

`mkvirtualenv --python=<path-of-python-in your-system> hostayni`

* Enter to virtual environment.

`workon hostayni`

You get something like this:

`(hostayni) 
bgarcial@elpug ‹ master ●● › : ~/workspace/hostayni_platform/blog
[1] % `


<dt>Cloning the repository</dt>
 <dd>This step assumes that you have already git setup and works in your workstation</dd>
 
 
 
`git clone git@github.com:bgarcial/hostayni_platform.git`
  

  <dt>Installing dependencies/requirements project</dt>
  <dd>When you have cloned/downlaoded the repository, is necessary install project packages.</dd>
  
  * Find yourself in the project's root directory 
  
  
`(hostayni) hostayni_platform/`
  
  * And type the following command to install packages:
  
  `(hostayni) hostayni_platform/blog
[1] %  pip install -r requirements.txt`

It is necessary to wait for the packages to install, which support the Hostayni project



