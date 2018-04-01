# SQLITify

This project is collections of standalone scripts and patches for converting different pieces of data into SQLite database format.
Right now it concentrated on dictionaries that exists in form of ad hoc text files or are purely web-based (this limits ability to query them alot).

### urban-dictionary.py

Being run from command line, creates file urban-dict.db in current directory. Process is safe to interrupt with pressing Ctrl-C or programmaticaly
(this is necessary because it takes very long time to complete) and will continue from point it was stopped previously.

### hagen-full.py

Command line utility, usage python hagen-full.py "path/to/������ ���������. ����������.txt" path/to/sqlite.db
First argument is Russian morphology text file, it could be extracted from [here](http://www.speakrus.ru/dict/hagen-morph.rar) (RAR archive).
Second argument is resulting DB, it will coontain table parsed_morpho with structure

<table>
<tr><td>Column</td><td>Possible values</td></tr>
<tr><td>new_group</td><td>True if first row of grouped words</td></tr>
<tr><td>main_word</td><td>True if this word is default form (like infinitive for verbs, etc.)</td></tr>
<tr><td>optional</td><td>True if this form is optional</td></tr>
<tr><td>word</td><td>Word itself</td></tr>
<tr><td>part_of_speech</td><td>'���':1,'���':2,'��':3,'����':4,'����':5,'������':6,'����':7,'����':8,'�����':9, '����':10, '���':11, '����':12, '���':13,'����':14</td></tr>
<tr><td>gender</td><td>'���':1, '���':2, '��':3,'���':4</td></tr>
<tr><td>number</td><td>'��':1,'��':2</td></tr>
<tr><td>plural</td><td>'��':1,'���':2,'���':3,'���':4,'��':5,'��':6,'����':7,'����':8,'����':8,'����':10</td></tr>
<tr><td>tense</td><td>'���':3,'����':2, '����':1</td></tr>
<tr><td>declension</td><td>'1-�':1,'2-�':2,'3-�':3</td></tr>
<tr><td>transitive</td><td>'�����':1,'���/��':2,'�����':3</td></tr>
<tr><td>spirit</td><td>'����':1,'����':2</td></tr>
<tr><td>adverb_type</td><td>'����':1,'����':2,'�����':3,'�����':4</td></tr>
<tr><td>circumstance_type</td><td>'����':1,'�����':2,'����':3,'������':4,'����':5</td></tr>
<tr><td>definition_type</td><td>'����':1,'���':2,  '����':3</td></tr>
<tr><td>perfect_type</td><td>'���':1,'�����':2,'2���':3</td></tr>
<tr><td>number_type</td><td>'���':1,'�����':2,'�����':3,'�����':4</td></tr>
<tr><td>pronoun_type</td><td>'����':1,'���':2,'���':3</td></tr>
<tr><td>infinitive</td><td>1 if true</td></tr>
<tr><td>pledge</td><td>1 if '�����'</td></tr>
<tr><td>impersonal</td><td>1 if '����'</td></tr>
<tr><td>shortened</td><td>1 if '����'</td></tr>
<tr><td>immutable</td><td>1 if '�����'</td></tr>
<tr><td>reflexive</td><td>1 if '���'</td></tr>
<tr><td>superlative</td><td>1 if '����'</td></tr>
<tr><td>imperative</td><td>1 if '���'</td></tr>
</table>
