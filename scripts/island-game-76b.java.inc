  int digArm=-1;float digT;
  void load76(){JSONObject g=data.optJSONObject("game");
   if(g==null||!g.has("seeds")){seeds[0]=4;seeds[1]=4;coins=100;for(int i=0;i<5;i++)it[i]=inv[i];seen=(1<<15)|(1<<17)|(1<<9)|(1<<10)|31;}
   else{try{JSONArray a=g.optJSONArray("seeds"),b=g.optJSONArray("it");for(int i=0;i<5;i++)seeds[i]=a==null?0:a.optInt(i);for(int i=0;i<9;i++)it[i]=b==null?0:b.optInt(i);coins=g.optInt("coins",0);haveAxe=g.optBoolean("axe",false);seen=g.optInt("seen",0);JSONArray t=g.optJSONArray("trees");if(t!=null)for(int i=0;i<t.length();i++){JSONArray r=t.getJSONArray(i);ts.put(r.getInt(0),new long[]{r.getLong(1),r.getLong(2),r.getLong(3)});}}catch(Exception ignored){}}
   if(g!=null){fDay=g.optLong("fday",-1);fMask=g.optInt("fmask",0);rDay=g.optLong("rday",-1);rItem=g.optInt("ritem",0);rDone=g.optBoolean("rdone",false);gDay=g.optLong("gday",-1);}
   for(java.util.Map.Entry<Integer,long[]> e:ts.entrySet()){float[] o=treeByKey(e.getKey());if(o!=null){if(e.getValue()[0]==1){o[2]=5;o[3]=2;}else o[2]=0;}}
   for(int i=plots.size()-1;i>=0;i--){Plot p=plots.get(i);float dx=p.cx*12+6-stall[0],dy=p.cy*12+6-stall[1];if(dx*dx+dy*dy<400)plots.remove(i);}
   if(!walk(px,py)){px=stall[0];py=stall[1]+16;}
   if(fDay!=todayNum()){fDay=todayNum();fMask=0;}
   spawnSpots();if(tool==4&&!haveAxe)tool=0;fixSeed();}
  void spawnSpots(){spots.clear();java.util.Random r=new java.util.Random(fDay*31+5);int made=0;for(int n=0;n<900&&made<8;n++){int x=14+r.nextInt(WW-28),y=14+r.nextInt(WH-28);int k=tk(x,y);boolean shellSpot=made<4;if(shellSpot?(k!=2||tk(x-3,y)!=2||tk(x+3,y)!=2):(k!=3||tk(x-4,y)!=3||tk(x+4,y)!=3||near(x,y,12)))continue;float dx=x-stall[0],dy=y-stall[1];if(dx*dx+dy*dy<400)continue;spots.add(new float[]{x,y,shellSpot?7:8,(fMask>>made)&1});made++;}}
  @Override void persist(){persist76();}
  void persist76(){try{JSONObject g=new JSONObject();JSONArray a=new JSONArray();for(Plot p:plots){JSONObject o=new JSONObject();o.put("x",p.cx);o.put("y",p.cy);o.put("c",p.crop);o.put("s",p.stage);o.put("w",p.wet);o.put("t",p.readyAt);a.put(o);}g.put("plots",a);
   JSONArray v=new JSONArray();for(int n:it)v.put(n);g.put("it",v);JSONArray sd=new JSONArray();for(int n:seeds)sd.put(n);g.put("seeds",sd);JSONArray iv=new JSONArray();for(int i=0;i<5;i++)iv.put(it[i]);g.put("inv",iv);
   g.put("water",water);g.put("tool",tool);g.put("seed",seed);g.put("fast",fast);g.put("px",px);g.put("py",py);g.put("coins",coins);g.put("axe",haveAxe);g.put("seen",seen);
   JSONArray tr=new JSONArray();for(java.util.Map.Entry<Integer,long[]> e:ts.entrySet()){JSONArray r=new JSONArray();r.put(e.getKey().intValue());r.put(e.getValue()[0]);r.put(e.getValue()[1]);r.put(e.getValue()[2]);tr.put(r);}g.put("trees",tr);
   g.put("fday",fDay);g.put("fmask",fMask);g.put("rday",rDay);g.put("ritem",rItem);g.put("rdone",rDone);g.put("gday",gDay);data.put("game",g);save();}catch(Exception ignored){}}
  void mark76(){persist();performHapticFeedback(android.view.HapticFeedbackConstants.CONTEXT_CLICK);}
  void queue2(int k,int cx,int cy,float x,float y,float tx2,float ty2){queue(k,cx,cy,x,y);ax=tx2;ay=ty2;}
  float[] treeHit(float wx,float wy){for(int i=things.size()-1;i>=0;i--){float[] o=things.get(i);int t=(int)o[2];if((t<=1||t==5)&&Math.abs(wx-o[0])<13&&wy>o[1]-34&&wy<o[1]+3)return o;}return null;}
  float[] treeSpot(float[] o){float[][] c={{0,8},{-9,7},{9,7},{0,12},{-13,3},{13,3}};for(float[] d:c)if(walk(o[0]+d[0],o[1]+d[1]))return new float[]{o[0]+d[0],o[1]+d[1]};return null;}
  float[] pondSpot(float wx,float wy){float qx=-1,qy=-1;boolean f=false;for(int dy=-7;dy<=7&&!f;dy+=2)for(int dx=-7;dx<=7;dx+=2)if(tk((int)(wx+dx),(int)(wy+dy))==4){qx=wx+dx;qy=wy+dy;f=true;break;}if(!f)return null;for(int i=0;i<=60;i++){float u=i/60f,x=qx+(px-qx)*u,y=qy+(py-qy)*u;if(walk(x,y))return new float[]{x,y,qx,qy};}return null;}
  @Override void tapWorld(float wx,float wy){if(act!=0)return;holdWalk=false;pend=0;shop=false;
   if(Math.abs(wx-bx)<9&&wy>by-24&&wy<by+3){talkBunny();return;}
   int cx=(int)Math.floor(wx/12),cy=(int)Math.floor(wy/12);Plot p=plotAt(cx,cy);float mx=cx*12+6,my=cy*12+6;
   if(p!=null&&p.crop>=0&&p.stage==3){queue2(1,cx,cy,mx,my,mx,my);return;}
   for(int i=0;i<spots.size();i++){float[] s=spots.get(i);if(s[3]==0&&Math.abs(wx-s[0])<8&&Math.abs(wy-s[1]+3)<9){aSpot=i;queue2(8,cx,cy,s[0],s[1]+3,s[0],s[1]);return;}}
   if(Math.abs(wx-stall[0])<17&&wy>stall[1]-30&&wy<stall[1]+3){queue2(10,cx,cy,stall[0],stall[1]+13,stall[0],stall[1]);return;}
   float[] tr=treeHit(wx,wy);
   if(tr!=null){if((int)tr[2]==5){say("It will grow back soon");return;}float[] sp=treeSpot(tr);int kind=tool==4?6:(int)tr[2]==1?7:0;if(sp!=null&&kind!=0){aTree=tkey(tr);queue2(kind,cx,cy,sp[0],sp[1],tr[0],tr[1]-10);return;}}
   if(tool==3){if(p!=null&&p.crop>=0&&p.stage<3){queue2(2,cx,cy,mx,my,mx,my);return;}float[] w=pondSpot(wx,wy);if(w!=null){queue2(5,cx,cy,w[0],w[1],w[2],w[3]);return;}if(tk((int)wx,(int)wy)<=1){say("That's sea water - fill up at the pond");return;}}
   if(tool==1){if(p!=null&&p.crop>=0){if(digArm==cx*1000+cy&&digT>0){digArm=-1;queue2(9,cx,cy,mx,my,mx,my);}else{digArm=cx*1000+cy;digT=3;say("Tap again to dig this plant up");}return;}if(p!=null){queue2(9,cx,cy,mx,my,mx,my);return;}if(validCell(cx,cy)){queue2(3,cx,cy,mx,my,mx,my);return;}}
   if(tool==2&&p!=null&&p.crop<0&&seeds[seed]>0){queue2(4,cx,cy,mx,my,mx,my);return;}
   holdWalk=true;holding=true;target(wx,wy);}
  final float[] DUR={0,.8f,1.2f,1.1f,.9f,1.0f,1.6f,1.0f,.8f,1.1f,0},HIT={0,.5f,.55f,.6f,.5f,.5f,.92f,.5f,.5f,.55f,0};
  void faceTo(float x,float y){float dx=x-px,dy=y-py;if(dx*dx+dy*dy>1){int k=(int)Math.round(Math.atan2(dy,dx)/(Math.PI/4));k=((k%8)+8)%8;dir=MAP[k];}}
  void begin(int k){faceTo(ax,ay);if(k==10){shop=true;panel=false;return;}Plot p=plotAt(pcx,pcy);aItem=k==1&&p!=null&&p.crop>=0?p.crop:k==8?(int)spots.get(aSpot)[2]:0;act=k;aTot=aT=DUR[k];hitAt=HIT[k];actHit=false;lastStrike=0;pourT=0;}
  void apply(){Plot p=plotAt(pcx,pcy);long now=System.currentTimeMillis();
   if(act==1){if(p!=null&&p.crop>=0&&p.stage==3){int c=p.crop;it[c]++;String s="+1 "+iname[c];if(Math.random()<.6){seeds[c]++;s+=" and a seed";}say(s);burst(ax,ay,0xFFFFE27A,12);p.crop=-1;p.stage=0;p.wet=false;chime(softSound);mark76();}}
   else if(act==2){if(p!=null&&p.crop>=0&&p.stage<3){if(p.wet)say("Already watered");else if(water<=0)say("The can is empty - fill it at the pond");else{water--;p.wet=true;p.readyAt=now+dur(p.crop);say(water>0?"Watered":"Watered - the can is now empty");mark76();}}}
   else if(act==3){if(p==null&&validCell(pcx,pcy)){Plot n=new Plot();n.cx=pcx;n.cy=pcy;plots.add(n);burst(ax,ay,0xFF8A6244,12);mark76();}}
   else if(act==4){if(p!=null&&p.crop<0&&seeds[seed]>0){seeds[seed]--;p.crop=seed;p.stage=0;p.wet=false;say(iname[seed]+" planted");fixSeed();mark76();}}
   else if(act==5){water=10;say("Watering can filled");burst(ax,ay,0xFF6FB6F0,10);mark76();}
   else if(act==6){float[] o=treeByKey(aTree);if(o!=null){int t0=(int)o[2];ts.put(aTree,new long[]{1,now+(fast?25000L:6L*3600000L),t0});o[2]=5;o[3]=2;int w=3+(int)(Math.random()*2);it[5]+=w;String s="+"+w+" Wood";if(t0==1){int a=1+(int)(Math.random()*2);it[6]+=a;s+=", +"+a+" Apple";}say(s);burst(o[0],o[1]-4,0xFFB98A57,14);chime(softSound);mark76();}}
   else if(act==7){float[] o=treeByKey(aTree);if(o!=null&&(int)o[2]==1){ts.put(aTree,new long[]{2,now+(fast?25000L:12L*3600000L),1});o[2]=0;int a=2+(int)(Math.random()*2);it[6]+=a;say("+"+a+" Apple");burst(o[0],o[1]-10,0xFFE0453C,12);mark76();}}
   else if(act==8){float[] s=spots.get(aSpot);if(s[3]==0){s[3]=1;fMask|=1<<aSpot;int k=(int)s[2];it[k]++;say("+1 "+iname[k]);burst(s[0],s[1],0xFFFFFFFF,8);mark76();}}
   else if(act==9){if(p!=null){if(p.crop>=0){seeds[p.crop]++;say("Dug up - seed returned");}else say("Hole filled in");plots.remove(p);burst(ax,ay,0xFF8A6244,10);mark76();}}}
  @Override void step(float dt){if(act!=0){hasT=false;holding=false;super.step(dt);}else super.step(dt);}
  @Override void tick(float dt){
   if(pend!=0){float dx=ptx-px,dy=pty-py,lim=(pend==5||pend>=6)?36f:144f;if(dx*dx+dy*dy<lim){int k=pend;pend=0;hasT=false;begin(k);}else if(!hasT)pend=0;}
   if(act!=0){aT-=dt;float p=1-aT/aTot;int n=act==6?3:(act==3||act==9||act==7)?2:0;
    if(n>0){int idx=(int)Math.floor(p*n);if(p*n-idx>=.5f&&idx>=lastStrike){lastStrike=idx+1;strikeFx();}}
    if(act==2&&p>.2f&&p<.8f){pourT-=dt;if(pourT<=0){pourT=.05f;float[] h=handPos();Part q=new Part();q.x=h[0]+(dir>=5?-4:4);q.y=h[1]-2;q.vx=(ax-q.x)/.45f;q.vy=((ay-q.y)-8.1f)/.45f;q.life=.45f;q.col=0xFF6FB6F0;parts.add(q);}}
    if(!actHit&&p>=hitAt){actHit=true;apply();}
    if(aT<=0)act=0;}
   for(int i=parts.size()-1;i>=0;i--){Part q=parts.get(i);q.x+=q.vx*dt;q.y+=q.vy*dt;q.vy+=80*dt;q.life-=dt;if(q.life<=0)parts.remove(i);}
   if(toastT>0)toastT-=dt;if(shakeT>0)shakeT-=dt;if(digT>0)digT-=dt;growT+=dt;if(growT>1){growT=0;checkGrowth();}}
  @Override void checkGrowth(){super.checkGrowth();long now=System.currentTimeMillis();boolean ch=false;java.util.Iterator<java.util.Map.Entry<Integer,long[]>> in=ts.entrySet().iterator();while(in.hasNext()){java.util.Map.Entry<Integer,long[]> e=in.next();if(now<e.getValue()[1])continue;float[] o=treeByKey(e.getKey());if(o!=null){float dx=px-o[0],dy=py-o[1];if(dx*dx+dy*dy<64)continue;o[2]=e.getValue()[2];o[3]=4;}in.remove();ch=true;}if(ch)persist();}
