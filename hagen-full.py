# coding=CP1251              /
import sqlite3, sys

if len(sys.argv)<2:
    print('Missed arguments\nUsage: python hagen-full.py "path/to/Полная парадигма. Морфология.txt" path/to/sqlite.db\nDownload source from http://www.speakrus.ru/dict/hagen-morph.rar')
    quit()
file = open(sys.argv[1])
conn = sqlite3.connect(sys.argv[2])
gender={'муж':1, 'жен':2, 'ср':3,'общ':4}
number={'ед':1,'мн':2}
case={'им':1,'род':2,'дат':3,'вин':4,'тв':5,'пр':6,'зват':7,'счет':8,'мест':8,'парт':10}
partofspeech={'сущ':1,'прл':2,'гл':3,'мест':4,'союз':5,'предик':6,'част':7,'межд':8,'предл':9, 'числ':10, 'прч':11, 'дееп':12, 'нар':13,'ввод':14}
tense={'буд':3,'наст':2, 'прош':1}
declension={'1-е':1,'2-е':2,'3-е':3}
transitive={'перех':1,'пер/не':2,'непер':3}
pledge={'страд'}
spirit={'одуш':1,'неод':2}
adverb_type={'вопр':1,'обст':2,'опред':3,'сравн':4}
circumstance_type={'врем':1,'места':2,'напр':3,'причин':4,'цель':5}
definition_type={'степ':1,'кач':2,  'спос':3}
perfect_type={'сов':1,'несов':2,'2вид':3}
impersonal={'безл'}
shortened={'крат'}
immutable={'неизм'}
reflexive={'воз'}
number_type={'кол':1,'поряд':2,'собир':3,'неопр':4}
pronoun_type={'прил':1,'сущ':2,'нар':3}
superlative_degree={'прев'}
imperative_mood={'пов'}
infinitive={'инф'}
cursor = conn.cursor()
cursor.execute("CREATE TABLE raw_morpho(new_group text,main_word text,optional text,word text,flags text,frequency text);")
cursor.execute("CREATE TABLE parsed_morpho(new_group text,main_word text,optional text,word text,part_of_speech text,gender text,number text,plural text,tense text,declension text,transitive text,spirit text,adverb_type text,circumstance_type text,definition_type text,perfect_type text,number_type text, pronoun_type text,infinitive text,pledge text,impersonal text,shortened text,immutable text,reflexive text,superlative text,imperative text);")
flags=set()
new_group=True
for line in file:
    if not line.strip():
        new_group=True
    else:
        if line.startswith(' '):
            main_word=False
            line=line.strip(' ')
        else:
            main_word=True
        if line.startswith('*'):
            optional=True
            line=line.strip('*')
        else:
            optional=False
        ar=line.split('|')
        ff=bytes(ar[1].strip(' ').encode().decode('cp866'),'cp866').decode('utf-8')
        fl=ff.split(' ')
        try:
            part_of_speech=partofspeech[fl[0]]
        except:
            part_of_speech=0
            print('zhopa')
            quit()
        for l in fl[1:]:
            try:
                sgender=gender[l]
            except:
                sgender=0 if not 'sgender' in locals() else sgender
            try:
                snumber=number[l]
            except:
                snumber=0 if not 'snumber' in locals() else snumber
            try:
                splural=case[l]
            except:
                splural=0 if not 'splural' in locals() else splural
            try:
                stense=tense[l]
            except:
                stense=0 if not 'stense' in locals() else stense
            try:
                sdeclension=declension[l]
            except:
                sdeclension=0 if not 'sdeclension' in locals() else sdeclension
            try:
                stransitive=transitive[l]
            except:
                stransitive=0 if not 'stransitive' in locals() else stransitive
            try:
                sspirit=spirit[l]
            except:
                sspirit=0 if not 'sspirit' in locals() else sspirit
            try:
                sadverb_type=adverb_type[l]
            except:
                sadverb_type=0 if not 'sadverb_type' in locals() else sadverb_type
            try:
                scircumstance_type=circumstance_type[l]
            except:
                scircumstance_type=0 if not 'scircumstance_type' in locals() else scircumstance_type
            try:
                sdefinition_type=definition_type[l]
            except:
                sdefinition_type=0 if not 'sdefinition_type' in locals() else sdefinition_type
            try:
                sperfect_type=perfect_type[l]
            except:
                sperfect_type=0 if not 'sperfect_type' in locals() else sperfect_type
            try:
                snumber_type=number_type[l]
            except:
                snumber_type=0 if not 'snumber_type' in locals() else snumber_type
            try:
                spronoun_type=pronoun_type[l]
            except:
                spronoun_type=0 if not 'spronoun_type' in locals() else spronoun_type
            sinfinitive= 1 if l=='инф' else 0 if not 'sinfinitive' in locals() else sinfinitive
            spledge=1 if l=='страд' else 0 if not 'spledge' in locals() else spledge
            simpersonal=1 if l=='безл' else 0 if not 'simpersonal' in locals() else simpersonal
            sshortened=1 if l=='крат' else 0 if not 'sshortened' in locals() else sshortened
            simmutable=1 if l=='неизм' else 0 if not 'simmutable' in locals() else simmutable
            sreflexive=1 if l=='воз' else 0 if not 'sreflexive' in locals() else sreflexive
            ssuperlative=1 if l=='прев' else 0 if not 'ssuperlative' in locals() else ssuperlative
            simperative=1 if l=='пов' else 0 if not 'simperative' in locals() else simperative
        if len(fl)<=1:
            sgender=0
            snumber=0
            splural=0
            stense=0
            sdeclension=0
            stransitive=0
            sspirit=0
            sadverb_type=0
            scircumstance_type=0
            sdefinition_type=0
            sperfect_type=0
            snumber_type=0
            spronoun_type=0
            sinfinitive=0
            spledge=0
            simpersonal=0
            sshortened=0
            simmutable=0
            sreflexive=0
            ssuperlative=0
            simperative=0
        cursor.execute("INSERT INTO raw_morpho(new_group,main_word,optional,word,flags,frequency) values(?,?,?,?,?,?);",(new_group,main_word,optional,bytes(ar[0].strip(' ').encode().decode('cp866'),'cp866').decode('utf-8'),bytes(ar[1].strip(' ').encode().decode('cp866'),'cp866').decode('utf-8'),ar[2].strip()))
        cursor.execute("INSERT INTO parsed_morpho(new_group,main_word,optional,word,part_of_speech,gender,number,plural,tense,declension,transitive,spirit,adverb_type,circumstance_type,definition_type,perfect_type,number_type,pronoun_type,infinitive,pledge,impersonal,shortened,immutable,reflexive,superlative,imperative) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
            ,(new_group,main_word,optional,bytes(ar[0].strip(' ').encode().decode('cp866'),'cp866').decode('utf-8'),part_of_speech,sgender,snumber,splural,stense,sdeclension,stransitive,sspirit,sadverb_type,scircumstance_type,sdefinition_type,sperfect_type,snumber_type,spronoun_type,sinfinitive,spledge,simpersonal,sshortened,simmutable,sreflexive,ssuperlative,simperative))
        del sgender,snumber,splural,stense,sdeclension,stransitive,sspirit,sadverb_type,scircumstance_type,sdefinition_type,sperfect_type,snumber_type,spronoun_type,sinfinitive,spledge,simpersonal,sshortened,simmutable,sreflexive,ssuperlative,simperative
        new_group=False
conn.commit()
conn.close()
