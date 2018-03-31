import urllib.request, re, sqlite3, traceback, html, time

S9='         '
B9='\b\b\b\b\b\b\b\b\b'
def read_page(base_url,param = None):
    url=base_url%urllib.parse.urlencode(param) if param else base_url
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr

def read_list(letter,start,last_page,cursor,conn,percent):
    param={'character':letter}
    base_url="https://www.urbandictionary.com/browse.php?%s"
    reg_word=re.compile(r'<a href="/define.php\?term=([^"]+)">',re.M)
    if last_page==0:
        mystr = read_page(base_url,param)
        l=reg_word.finditer(mystr)
        last=0
        for ll in l:
            last=ll.end(1)
            cursor.execute("INSERT INTO word_url(url,done) values(?,?);",(ll.group(1),0))
        conn.commit()
        reg_last=re.compile(r'<a href="/browse.php\?character=.\&amp;page=(\d+)">Last ',re.M)
        l=reg_last.search(mystr[last:])
        last_page=int(l.group(1))
        start=1
        cursor.execute("INSERT INTO letter(letter,done_page,total_page) values(?,?,?);",(letter,start,last_page))
    for i in range(start+1,last_page+1):
        print(B9+'%8.4f%%'%((percent+(i-1)/float(last_page))/27*100),end='',flush=True)
        param['page']=i
        mystr=read_page(base_url,param)
        l=reg_word.finditer(mystr)
        for ll in l:
            cursor.execute("INSERT INTO word_url(url,done) values(?,?);",(ll.group(1),0))
        cursor.execute("UPDATE letter SET done_page=? WHERE letter=?;",(i,letter))
        conn.commit()

def search_word(xstr,regex,default = ''):
    s=regex.search(xstr)
    return s.group(1) if s else default

def quasy_hyper(mo):
    return '[%s:'%mo.group(1)

def remove_html(s):    
    s=html.unescape(s)
    s=re.subn('<br/>','',s)[0]
    s=re.subn('<a class="autolink" href="/define.php\?term=([^"]+)">',quasy_hyper,s)[0]
    s=re.subn('</a>',']',s)[0]
    return s

def read_word(url,cursor,conn):
    base_url="https://www.urbandictionary.com/define.php?term=%s"%url #dirty hack 'cause we already stored urls encoded, double encoding should not happen!
    mystr=read_page(base_url)
    reg_definition=re.compile(r'<div class="def-panel" ',re.M)
    reg_number=re.compile(r'<div class="row"><div class="small-6 columns"><div class="ribbon">([^<]+)</div></div>',re.M)
    reg_category=re.compile(r'<span class="category[^>]+><a href="/category.php\?category=[^>]+><span [^>]+>([^>]+)</span></a></span>',re.M)
    reg_word=re.compile(r'<a class="word" href="/define.php\?term=[^>]+>([^>]+)</a>',re.M)
    reg_meaning=re.compile(r'<div class="meaning">(.*?)</div>',re.M)
    reg_example=re.compile(r'<div class="example">(.*?)</div>',re.M)
    reg_contributor=re.compile(r'<div class="contributor">by <a href="/author.php\?author=[^"]+">([^<]+?)</a> ([^<]+?)</div>',re.M)
    reg_vote=re.compile(r'<span class="count">(\d+)</span>',re.M)
    reg_tags=re.compile(r'<a href="/tags.php\?tag=[^"]+">#([^>]+)</a>',re.M)
    reg_gif=re.compile(r'<div class="gif"><img [^s]*src="([^"]+)"',re.M)
    l=list(map(lambda l:l.end(0),reg_definition.finditer(mystr)))
    l1=l[:]
    del l1[0]
    l1.append(len(mystr))
    for i in range(0,len(l)):
        number=search_word(mystr[l[i]:l1[i]],reg_number,0)
        if number=='Top definition':
            number='1'
        word=html.unescape(search_word(mystr[l[i]:l1[i]],reg_word))
        category=search_word(mystr[l[i]:l1[i]],reg_category)
        meaning=remove_html(search_word(mystr[l[i]:l1[i]],reg_meaning))
        example=remove_html(search_word(mystr[l[i]:l1[i]],reg_example))
        gif=search_word(mystr[l[i]:l1[i]],reg_gif)
        s=reg_contributor.search(mystr[l[i]:l1[i]])
        if s:
            contributor=s.group(1)
            try:
                contribution_date=time.strftime('%Y%m%d',time.strptime(s.group(2),"%B %d, %Y"))
            except:
                contribution_date='error'
        else:
            contributor=''
            contribution_date=''
        sa=reg_vote.findall(mystr[l[i]:l1[i]])
        if sa:
            up_vote=int(sa[0])
            down_vote=int(sa[1])
        else:
            up_vote=0
            down_vote=0
        tags=reg_tags.findall(mystr[l[i]:l1[i]])
        cursor.execute("INSERT INTO word(word,number,category,meaning,example,contributor,contribution_date,up_vote,down_vote) values(?,?,?,?,?,?,?,?,?);",(word,number,category,meaning,example,contributor,contribution_date,up_vote,down_vote))

def word_percent(done_index,max_index):
    return '%8.4f%%'%(done_index/float(max_index)*100)

letters=set(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','*'])
conn = sqlite3.connect('urban-dict.db')
cursor = conn.cursor()
try:
    print('Checking DB...',end='')
    cursor.execute("select name from sqlite_master where type='table';")
    names=cursor.fetchall()
    t_letter=False
    t_word_url=False
    t_words=False
    for name in names:
        if name[0]=='letter':
            t_letter=True
        elif name[0]=='word_url':
            t_word_url=True
        elif name[0]=='word':
            t_words=True
    print('done')
    print('Get URL list...'+S9,end='',flush=True)
    if not t_letter:
        cursor.execute("create table letter(letter text,done_page text,total_page text);")
    else:
        cursor.execute("select letter from letter where done_page=total_page;")
        letters=letters-set(map(lambda s:s[0],cursor.fetchall()))
        cursor.execute("select letter,done_page,total_page from letter where done_page<>total_page;")
        unfinished=cursor.fetchone()
        percent=27-len(letters)
        if unfinished:
            letters=letters-set(unfinished[0])
            read_list(unfinished[0],int(unfinished[1]),int(unfinished[2]),cursor,conn,percent)
    if not t_word_url:
        cursor.execute("CREATE TABLE word_url(url text,done text);")
    if not t_words:
        cursor.execute("CREATE TABLE word(word text,number text,category text,meaning text,example text,contributor text,contribution_date text,up_vote text,down_vote text);")
    i=0
    for let in letters:
        read_list(let,0,0,cursor,conn,27-len(letters)+i)
        i+=1
    print(B9+'done',flush=True)
    cursor.execute("select MAX(rowid) from word_url where done=1;")
    res=cursor.fetchone()[0]
    last_retrieved=res if res else 0
    start_index=last_retrieved+1
    pack_size=10
    end_index=last_retrieved+pack_size
    cursor.execute("select MAX(rowid) from word_url;")
    final_index=cursor.fetchone()[0]
    print('Get words...'+word_percent(start_index,final_index),end='',flush=True)
    while True:
        cursor.execute("select rowid,url from word_url where rowid between ? and ?;",(start_index,end_index))
        urls=cursor.fetchall()
        for url in urls:
            read_word(url[1],cursor,conn)
        cursor.execute("UPDATE word_url SET done=1 WHERE rowid between ? and ?;",(start_index,end_index))
        conn.commit()
        if urls[-1][0]!=end_index:
            print(B9+'done',flush=True)
            break
        else:
            start_index=end_index+1
            end_index=end_index+pack_size
            print(B9+word_percent(start_index,final_index),end='',flush=True)
except (KeyboardInterrupt, SystemExit):
    conn.rollback()
except:
    conn.rollback()
    traceback.print_exc()
conn.close()
