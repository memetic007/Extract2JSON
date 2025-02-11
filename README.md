# WELL New App Tools

This is a set of tools intended to be used as utility programs for developing new front ends for The WELL. Such as for mobile and desktop OSes.  

These three tools can be used to eliminate the need to deal with communications, parsing, and basic data structuring.

They are intended at this point to be used on your desktop with python.

In the future I may migrate the latter two programs to run on The WELL, but for now I reccomend using them on your desktop.  


## remoteexec.py

Command line interface to execute commands on The WELL.  It is meant to be run from your desktop.  Allowing for development in your favorite IDE or enviornment.

example: python remoteexec.py --username username --password yourpassword -- "extract -s -1 news,pol,welltech"

remoteexec.py returns the results of the command as stdout

Note the additional "--" after username and password with a space before and after that is before the command.  An artifact of the command line parser I'm using

prerequisites:  paramiko   [pip install paramiko] ssh2, sftp, and remote command library.

It is fast enough for prototyping but because it is stateless, it logs into The WELL each time it is invoked.  On my roadmap is to create a standalone desktop proxy server 
that maintains the connection to The WELL reducing the latency on each invocation.  remoteexec.py would connect to the proxy server rather than The WELL directly.

## extract2json.py

Takes the output of remoteeexec.py and if it is extract content from conferences it parses it into a fairly simple JSON format corresponding to a list of python dictionaries, one dictiorary per line.  

example: python remoteexec.py --username username --password yourpassword -- "extract -s -1 news,pol,welltech" | python extract2json.py

The contents of each dictionary for each line include:
            "type": dictType,
            "handle": current_handle,
            "topic": dictTopic,
            "title": dictTitle,
            "username": dictUsername,
            "pseud": dictPseud,
            "datetime": dictTimeDate,
            "text": dictText,

The three "types" are "topicheader" "postheader" and "posttext"

Each line of a post is a seperate JSON dictionary.  Quite verbose. Good thing text is essentially free to move around these days!

Not all "types" of extract output lines use all the fields, though they are present in the dictionary.  Those fields not used have value "" for the moment.  

There is a test mode for standalone testing:  python extract2json.py -test

In test mode, rather than reading from stdin, a sample of output from remoteexec.py is read in from textstring.txt which is included in the repository.  

## python makeobjects2json.py 

takes the JSON output of extract2json.py and converts it into JSON representing nested Topic and Post Python objects.  The Post object contains a field, "text", that is a list of strings that holds the post text.

The JSON output is easily converitable back to the Python and Dart structures and pretty confident most object oriented languages will be able to use it.

example: python remoteexec.py --username username --password yourpassword -- "extract -s -1 news,pol,welltech" | python extract2json.py | python makeobjects.py 

There is a test mode for standalone testing:  python makeobjects.py -test

In test mode rather than reading from stdin, a sample of output from extract2json.py is read in from linejson.txt which is included in the repository.  

The default behavior is to return a JSON list that can be converted into a list of topics which contains Posts.

There is an addiitonal behavior that can be used by passing the -conf flag.  When used, the output will be a JSON list that can be converted into a list of Conferences which contains Topics which contains Posts.  Exeample: python makeobjects2json.py -conf

See the Conf, Topic, and Post classes in the classes.py file for the data structures.



