# SQLITify

This project is collections of standalone scripts and patches for converting different pieces of data into SQLite database format.
Right now it concentrated on dictionaries that exists in form of ad hoc text files or are purely web-based (this limits ability to query them alot).

### urban-dictionary.py

Being run from command line, creates file urban-dict.db in current directory. Process is safe to interrupt with pressing Ctrl-C or programmaticaly
(this is necessary because it takes very long time to complete) and will continue from point it was stopped previously.