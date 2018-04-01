# SQLITify

This project is collections of standalone scripts and patches for converting different pieces of data into SQLite database format.
Right now it concentrated on dictionaries that exists in form of ad hoc text files or are purely web-based (this limits ability to query them alot).

### urban-dictionary.py

Being run from command line, creates file urban-dict.db in current directory. Process is safe to interrupt with pressing Ctrl-C or programmaticaly
(this is necessary because it takes very long time to complete) and will continue from point it was stopped previously.

### hagen-full.py

Command line utility, usage python hagen-full.py "path/to/Ïîëíàÿ ïàðàäèãìà. Ìîðôîëîãèÿ.txt" path/to/sqlite.db
First argument is Russian morphology text file, it could be extracted from [here](http://www.speakrus.ru/dict/hagen-morph.rar) (RAR archive).
Second argument is resulting DB, it will coontain table parsed_morpho with structure

<table>
<tr><td>Column</td><td>Possible values</td></tr>
<tr><td>new_group</td><td>True if first row of grouped words</td></tr>
<tr><td>main_word</td><td>True if this word is default form (like infinitive for verbs, etc.)</td></tr>
<tr><td>optional</td><td>True if this form is optional</td></tr>
<tr><td>word</td><td>Word itself</td></tr>
<tr><td>part_of_speech</td><td>'сущ':1,'прл':2,'гл':3,'мест':4,'союз':5,'предик':6,'част':7,'межд':8,'предл':9, 'числ':10, 'прч':11, 'дееп':12, 'нар':13,'ввод':14</td></tr>
<tr><td>gender</td><td>'муж':1, 'жен':2, 'ср':3,'общ':4</td></tr>
<tr><td>number</td><td>'ед':1,'мн':2</td></tr>
<tr><td>plural</td><td>'им':1,'род':2,'дат':3,'вин':4,'тв':5,'пр':6,'зват':7,'счет':8,'мест':8,'парт':10</td></tr>
<tr><td>tense</td><td>'буд':3,'наст':2, 'прош':1</td></tr>
<tr><td>declension</td><td>'1-е':1,'2-е':2,'3-е':3</td></tr>
<tr><td>transitive</td><td>'перех':1,'пер/не':2,'непер':3</td></tr>
<tr><td>spirit</td><td>'одуш':1,'неод':2</td></tr>
<tr><td>adverb_type</td><td>'вопр':1,'обст':2,'опред':3,'сравн':4</td></tr>
<tr><td>circumstance_type</td><td>'врем':1,'места':2,'напр':3,'причин':4,'цель':5</td></tr>
<tr><td>definition_type</td><td>'степ':1,'кач':2,  'спос':3</td></tr>
<tr><td>perfect_type</td><td>'сов':1,'несов':2,'2вид':3</td></tr>
<tr><td>number_type</td><td>'кол':1,'поряд':2,'собир':3,'неопр':4</td></tr>
<tr><td>pronoun_type</td><td>'прил':1,'сущ':2,'нар':3</td></tr>
<tr><td>infinitive</td><td>1 if true</td></tr>
<tr><td>pledge</td><td>1 if 'страд'</td></tr>
<tr><td>impersonal</td><td>1 if 'безл'</td></tr>
<tr><td>shortened</td><td>1 if 'крат'</td></tr>
<tr><td>immutable</td><td>1 if 'неизм'</td></tr>
<tr><td>reflexive</td><td>1 if 'воз'</td></tr>
<tr><td>superlative</td><td>1 if 'прев'</td></tr>
<tr><td>imperative</td><td>1 if 'пов'</td></tr>
</table>

