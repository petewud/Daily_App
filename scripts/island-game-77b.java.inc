  float[] nearSpot(float x,float y){float[][] c={{0,9},{9,0},{-9,0},{0,-9}};for(float[] d:c)if(walk(x+d[0],y+d[1]))return new float[]{x+d[0],y+d[1]};return null;}
  float[] aroundSpot(float[] o){float[][] c={{0,9},{-9,7},{9,7},{0,13},{-12,0},{12,0}};for(float[] d:c)if(walk(o[0]+d[0],o[1]+d[1]))return new float[]{o[0]+d[0],o[1]+d[1]};return null;}
  float[] walkTo(float x,float y){for(int i=0;i<=60;i++){float u=i/60f,x2=x+(px-x)*u,y2=y+(py-y)*u;if(walk(x2,y2))return new float[]{x2,y2};}return null;}
  float[] critHit(float wx,float wy){for(float[] q:crit)if(Math.abs(wx-q[0])<9&&Math.abs(wy-q[1]+2)<8)return q;return null;}
  float[] flyAt(float wx,float wy){float t=(SystemClock.uptimeMillis()-born)/1000f;for(float[] f:flies){float x=f[0]+(float)Math.sin(t*.5f+f[2])*22,y=f[1]+(float)Math.cos(t*.8f+f[2])*14;if(Math.abs(wx-x)<12&&Math.abs(wy-y)<12)return new float[]{x,y};}return null;}
  float[] rockHit(float wx,float wy){for(int i=things.size()-1;i>=0;i--){float[] o=things.get(i);if((int)o[2]==3&&Math.abs(wx-o[0])<9&&wy>o[1]-11&&wy<o[1]+3)return o;}return null;}
  float[] sapHit(float wx,float wy){for(int i=things.size()-1;i>=0;i--){float[] o=things.get(i);if((int)o[2]==11&&Math.abs(wx-o[0])<8&&wy>o[1]-18&&wy<o[1]+3)return o;}return null;}
  @Override void tapWorld(float wx,float wy){if(act!=0||pop!=0)return;aMode=0;holdWalk=false;pend=0;shop=false;logOpen=false;
   if(Math.abs(wx-bx)<9&&wy>by-24&&wy<by+3){talkBunny();return;}
   int cx=(int)Math.floor(wx/12),cy=(int)Math.floor(wy/12);Plot p=plotAt(cx,cy);float mx=cx*12+6,my=cy*12+6;
   if(p!=null&&p.crop>=0&&p.stage==3){queue2(1,cx,cy,mx,my,mx,my);return;}
   for(int i=0;i<spots.size();i++){float[] s=spots.get(i);if(s[3]==0&&Math.abs(wx-s[0])<8&&Math.abs(wy-s[1]+3)<9){aSpot=i;queue2(8,cx,cy,s[0],s[1]+3,s[0],s[1]);return;}}
   if(Math.abs(wx-stall[0])<17&&wy>stall[1]-30&&wy<stall[1]+3){queue2(10,cx,cy,stall[0],stall[1]+13,stall[0],stall[1]);return;}
   float[] cr=critHit(wx,wy),bf=cr==null?flyAt(wx,wy):null;
   if(tool==6&&(cr!=null||bf!=null)){float[] g=cr!=null?cr:bf;float[] sp=walkTo(g[0],g[1]);if(sp!=null){queue2(13,cx,cy,sp[0],sp[1],g[0],g[1]);return;}}
   else if(cr!=null){say(haveNet?"Equip your net from the bag":"A bug net from the stall would help");return;}
   float[] rk=rockHit(wx,wy);if(rk!=null){float[] sp=aroundSpot(rk);if(sp!=null){liftKey=tkey(rk);queue2(15,cx,cy,sp[0],sp[1],rk[0],rk[1]);return;}}
   float[] sk=sapHit(wx,wy);if(sk!=null){if(tool==3){float[] sp=nearSpot(sk[0],sk[1]);if(sp!=null){aMode=1;aTree=tkey(sk);queue2(2,cx,cy,sp[0],sp[1],sk[0],sk[1]-4);return;}}else{say("Water it with the can to help it grow");return;}}
   float[] tr=treeHit(wx,wy);
   if(tr!=null){int t=(int)tr[2];float[] sp=treeSpot(tr);if(t==5){if(tool==1&&sp!=null){aMode=2;aTree=tkey(tr);queue2(3,cx,cy,sp[0],sp[1],tr[0],tr[1]);}else say("Dig the stump up with the shovel");return;}
    int kind=tool==4?6:t==1?7:0;if(sp!=null&&kind!=0){aTree=tkey(tr);queue2(kind,cx,cy,sp[0],sp[1],tr[0],tr[1]-10);return;}}
   if(tool==3){if(p!=null&&p.crop>=0&&p.stage<3){queue2(2,cx,cy,mx,my,mx,my);return;}float[] w=pondSpot(wx,wy);if(w!=null){queue2(5,cx,cy,w[0],w[1],w[2],w[3]);return;}if(tk((int)wx,(int)wy)<=1){say("That's sea water - fill up at the pond");return;}}
   if(tool==1){if(p!=null&&p.crop>=0){if(digArm==cx*1000+cy&&digT>0){digArm=-1;queue2(9,cx,cy,mx,my,mx,my);}else{digArm=cx*1000+cy;digT=3;say("Tap again to dig this plant up");}return;}if(p==null&&validCell(cx,cy)){queue2(3,cx,cy,mx,my,mx,my);return;}}
   if(tool==2&&p!=null&&p.crop<0&&seeds[seed]>0){queue2(4,cx,cy,mx,my,mx,my);return;}
   if(tool==5&&sapN>0&&p==null&&validCell(cx,cy)){float[] sp=nearSpot(mx,my);if(sp!=null){aMode=3;queue2(4,cx,cy,sp[0],sp[1],mx,my);return;}}
   if(p!=null&&p.crop<0){float[] sp=nearSpot(mx,my);if(sp!=null){queue2(12,cx,cy,sp[0],sp[1],mx,my);return;}}
   holdWalk=true;holding=true;target(wx,wy);}
  @Override void begin(int k){if(k<=10){super.begin(k);return;}faceTo(ax,ay);act=k;aTot=aT=DUR2[k-11];hitAt=HIT2[k-11];actHit=false;lastStrike=0;pourT=0;}
  @Override void apply(){long now=System.currentTimeMillis();
   if(act==3&&aMode==2){float[] o=treeByKey(aTree);if(o!=null&&(int)o[2]==5){things.remove(o);ts.remove(aTree);if(ptrees.contains(aTree))ptrees.remove(Integer.valueOf(aTree));else cleared.add(aTree);it[5]++;say("+1 Wood - the stump is gone");burst(ax,ay,0xFF8A6244,14);chime(softSound);mark76();}return;}
   if(act==2&&aMode==1){long[] s=saps.get(aTree);if(s!=null){if(s[1]==1)say("Already watered");else if(water<=0)say("The can is empty - fill it at the pond");else{water--;s[1]=1;s[2]=now+dur(3);say(water>0?"Watered":"Watered - the can is now empty");mark76();}}return;}
   if(act==4&&aMode==3){int key=Math.round(ax)*1000+Math.round(ay);if(sapN<=0)return;if(anyThing(key)!=null){say("No room here");return;}things.add(new float[]{ax,ay,11,3});sortThings();saps.put(key,new long[]{0,0,0});sapN--;if(sapN<=0&&tool==5)tool=0;say("Sapling planted");burst(ax,ay,0xFF8A6244,8);mark76();return;}
   if(act==12){Plot p=plotAt(pcx,pcy);if(p!=null&&p.crop<0){plots.remove(p);burst(ax,ay,0xFF8A6244,14);burst(ax,ay,0xFF6DB65A,6);mark76();}return;}
   if(act==13){netApply();return;}
   if(act==15){rockApply();return;}
   super.apply();}
  void netApply(){float t=(SystemClock.uptimeMillis()-born)/1000f;int bi=-1;float bd=26*26;
   for(int i=0;i<flies.size();i++){float[] f=flies.get(i);float x=f[0]+(float)Math.sin(t*.5f+f[2])*22,y=f[1]+(float)Math.cos(t*.8f+f[2])*14;float dx=x-px,dy=y-py;if(dx*dx+dy*dy<bd){bd=dx*dx+dy*dy;bi=i;}}
   int ci=-1;float cd=22*22;for(int i=0;i<crit.size();i++){float[] q=crit.get(i);float dx=q[0]-px,dy=q[1]-py;if(dx*dx+dy*dy<cd){cd=dx*dx+dy*dy;ci=i;}}
   int k=-1;if(ci>=0){k=(int)crit.get(ci)[2];crit.remove(ci);}else if(bi>=0&&Math.random()<.85){k=(int)flies.get(bi)[3]%5;}
   if(k<0){say(bi>=0||ci>=0?"It got away!":"Missed - nothing in reach");return;}
   bug[k]++;boolean nw=((bugSeen>>k)&1)==0;bugSeen|=1<<k;say((nw?"New! ":"")+"Caught a "+bname[k]);burst(ax,ay,0xFFFFFFFF,10);chime(softSound);mark76();}
  void rockApply(){long now=System.currentTimeMillis();Long cd=rockCd.get(liftKey);if(cd!=null&&now<cd){say("Just dirt and pebbles");return;}rockCd.put(liftKey,now+(fast?10000L:1800000L));
   if(Math.random()<.5){int r=(int)(Math.random()*100);int k=r<30?5:r<50?6:r<75?7:r<90?8:9;float[] sp={5,4,9,1.5f,3};float a=(float)(Math.random()*6.283);float s=sp[k-5];crit.add(new float[]{ax,ay+3,k,(float)Math.cos(a)*s,(float)Math.sin(a)*s,14f,0});say("A "+bname[k].toLowerCase()+" crawled out!");}
   else say("Just dirt and pebbles");}
