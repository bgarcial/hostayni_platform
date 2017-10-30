# Hostayni Platform





# Todo

- [ ] Users Schema
- [ ] Contents Data Schema

- [View Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet "Markdown Cheatsheet")
- [View Markdown Navigator](https://plugins.jetbrains.com/plugin/7896-markdown-navigator "Markdown Navigator - JetBrains Plugin")
- 
# Credits



======

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
  
  
  `(hostayni) 
bgarcial@elpug ‹ master ●● › : ~/workspace/hostayni_platform/
[1] % `
  
  * And type the following command to install packages:
  
  `(hostayni) 
bgarcial@elpug ‹ master ●● › : ~/workspace/hostayni_platform/blog
[1] %  pip install -r requirements.txt`

It is necessary to wait for the packages to install, which support the Hostayni project

======
------

# Enter to virtual environment and frontend branch

<dt>Activating virtuelenvwrapper</dt>
  
 In your CLI enter:
 
 `workon hostayni`
 
 
 *  Enter to the projects root directory
  
  
`(hostayni) 
bgarcial@elpug ‹ master ●● › : ~/workspace/hostayni_platform/
[1] % `
  
  
* Enter to branch to work

`git checkout frontend`
    
`Switched to branch 'frontend'`

`(hostayni) 
bgarcial@elpug ‹ frontend ●● › : ~/workspace/hostayni_platform
[0] %`


<dt>git lifecycle basics</dt>

* Check status files project

`git status`

* Add files to commit repository

`git add <filename-modified>

* Preparing files to push repository

`git commit -m 'I am commiting files to the Hostayni project'`

* Push files to the github repository

`git push origin frontend`

</dl>



