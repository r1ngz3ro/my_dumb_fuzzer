import glob,time,subprocess,random,threading
def fuzz(t_id:int,inp:bytes):
    assert (isinstance(t_id,int))
    assert (isinstance(inp,bytes))
    tmpf=f"tmpinput{t_id}"
    with open(f"tmpinput{t_id}","wb") as fd:
        fd.write(inp)
    sp=subprocess.Popen(["objdump","-d",tmpf],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    ret=sp.wait()
    if ret !=0:
        print(f"exited with code {ret}")
corpus_files=glob.glob("corpus/*")

corpus=set()
for file in corpus_files:
    corpus.add(open(file,"rb").read())


def worker(t_id):
    global corpus ,start ,cases
    cases=0
    corpus=list(corpus)
    start=time.time()
    while True:
        cases+=1
        fuzz(0,random.choice(corpus))
        elapsed=time.time() -start
        speed=cases/elapsed
        print(f"[{elapsed:1.4f}] cases {cases:10} | speed {speed:1.3f} case per second")
for t_id in range(4):
    threading.Thread(target=worker,args=[t_id]).start()
while threading.active_count() > 0:
    time.sleep(0.1)
