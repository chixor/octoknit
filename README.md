Octoknit
=======================

![Octoknit Screenshot v1](http://octoknit.chixor.net/img/screenshot.jpg)

Introduction
------------
Use this website to design patterns, share them and send to a Brother 950i knitting machine.


Status
------
This is in active development. Current plans include:

- Improving the user journey from beginner to regular.
- Replace the commandline python script with a full php solution.
- Extend the upload to knitting machine script to support multi-mylar sheet patterns and multi colour.

Demo
----
http://octoknit.chixor.net/

License
-------
Copyright 2014 all rights reserved. In order to retain some measure of control over this codebase's early development I've restricted the license for now. I'll review its license when it's in a more stable state.

Setup
-----
Apache config:
```
<VirtualHost *:80>
    ServerName octoknit.me
    DocumentRoot "/Users/chixor/Sites/octoknit/public"
    SetEnv APPLICATION_ENV "development"
    <Directory /Users/chixor/Sites/octoknit/public>
        Options +Indexes +FollowSymLinks +ExecCGI
        DirectoryIndex index.php
        AllowOverride All
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>
```
