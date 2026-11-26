  @Override int bit(int[] s){return s[0]==0?1<<(14+s[1]):s[0]==1?1<<(9+s[1]):s[0]==2?1<<s[1]:1<<(21+s[1]);}
  @Override void slotsBuild(){slots.clear();slots.add(new int[]{0,1,0});slots.add(new int[]{0,3,0});if(haveAxe)slots.add(new int[]{0,4,0});if(haveNet)slots.add(new int[]{0,6,0});if(sapN>0)slots.add(new int[]{0,5,sapN});for(int i=0;i<5;i++)if(seeds[i]>0)slots.add(new int[]{1,i,seeds[i]});for(int i=0;i<9;i++)if(it[i]>0)slots.add(new int[]{2,i,it[i]});for(int i=0;i<10;i++)if(bug[i]>0)slots.add(new int[]{3,i,bug[i]});}
  @Override void cardsBuild(){cardI.clear();for(int i=0;i<5;i++)cardI.add(new int[]{0,i,buyP[i]});cardI.add(new int[]{4,0,30});if(!haveAxe)cardI.add(new int[]{1,4,60});if(!haveNet)cardI.add(new int[]{5,6,40});for(int i=0;i<9;i++)if(it[i]>0)cardI.add(new int[]{2,i,sellP[i]});for(int i=0;i<10;i++)if(bug[i]>0)cardI.add(new int[]{3,i,bugP[i]});}
  String slotName(int[] s){if(s[0]==0)return s[1]==1?"Shovel":s[1]==3?"Watering can":s[1]==4?"Axe":s[1]==5?"Sapling":"Bug net";if(s[0]==1)return iname[s[1]]+" seeds";if(s[0]==2)return iname[s[1]];return bname[s[1]];}
  String cardName(int[] c){if(c[0]==0)return iname[c[1]]+" seeds";if(c[0]==1)return "Axe";if(c[0]==4)return "Sapling";if(c[0]==5)return "Bug net";if(c[0]==2)return iname[c[1]];return bname[c[1]];}
  Bitmap slotBmp(int[] s){return s[0]==0?(s[1]==4?axeBmp:s[1]==5?sapBmp[1]:s[1]==6?netBmp:toolBmp[s[1]]):s[0]==1?packBmp[s[1]]:s[0]==2?itemBmp[s[1]]:bugBmp[s[1]];}
  Bitmap cardBmp(int[] c){return c[0]==0?packBmp[c[1]]:c[0]==1?axeBmp:c[0]==4?sapBmp[1]:c[0]==5?netBmp:c[0]==2?itemBmp[c[1]]:bugBmp[c[1]];}
  void iconFit(Canvas c,Bitmap b,float cx,float cy,float box){float f=Math.min(box/b.getWidth(),box/b.getHeight());f=Math.min(f,dens*3.2f);icon(c,b,cx,cy,b.getWidth()*f,b.getHeight()*f);}
  void sil(Canvas c,Bitmap b,float cx,float cy,float box){float f=Math.min(box/b.getWidth(),box/b.getHeight());f=Math.min(f,dens*3.2f);float w=b.getWidth()*f,h=b.getHeight()*f;dest.set(cx-w/2,cy-h/2,cx+w/2,cy+h/2);c.drawBitmap(b,null,dest,silP);}
  void txt(Canvas c,String s,float cx,float y,float size,float maxW,int col){ink.setTextSize(size);float w=ink.measureText(s);if(w>maxW)ink.setTextSize(size*maxW/w);ink.setColor(col);c.drawText(s,cx,y,ink);}
  @Override void shopPress(int i){if(i>=cardI.size())return;int[] c=cardI.get(i);popType=c[0];popId=c[1];popPrice=c[2];boolean sell=c[0]==2||c[0]==3;
   if(sell)popMax=c[0]==2?it[c[1]]:bug[c[1]];else if(c[0]==1||c[0]==5)popMax=1;else popMax=Math.max(1,coins/popPrice);
   if(popMax<=0)return;popQty=1;pop=sell?1:2;}
  void popConfirm(){int n=popQty;
   if(pop==1){if(popType==2){n=Math.min(n,it[popId]);it[popId]-=n;}else{n=Math.min(n,bug[popId]);bug[popId]-=n;}int total=n*popPrice;coins+=total;say("Sold "+n+" for "+total+" coins");}
   else{int total=n*popPrice;if(coins<total){say("Not enough coins");pop=0;return;}coins-=total;if(popType==0){seeds[popId]+=n;say("Bought "+n+" "+iname[popId]+" seeds");}else if(popType==1){haveAxe=true;say("Bought an axe!");}else if(popType==4){sapN+=n;say("Bought "+n+" sapling"+(n>1?"s":""));}else{haveNet=true;say("Bought a bug net!");}}
   pop=0;chime(softSound);persist();}
  void popPress(int id){if(id==410)popQty=Math.max(1,popQty-1);else if(id==411)popQty=Math.min(popMax,popQty+1);else if(id==412)popQty=popMax;else if(id==413)popConfirm();else pop=0;}
  @Override int hit(float x,float y){
   if(pop!=0){if(pMinus.contains(x,y))return 410;if(pPlus.contains(x,y))return 411;if(pMax.contains(x,y))return 412;if(pOk.contains(x,y))return 413;if(popRect.contains(x,y))return 40;return 414;}
   if(closeRect.contains(x,y))return 1;if(bagRect.contains(x,y))return 2;if(tool!=0&&chipRect.contains(x,y))return 3;
   if(logOpen){if(logX.contains(x,y))return 61;if(panelRect.contains(x,y))return 40;}
   else if(shop){if(shopX.contains(x,y))return 50;for(int i=0;i<cardR.size();i++)if(cardR.get(i).contains(x,y))return 300+i;if(panelRect.contains(x,y))return 40;}
   else if(panel){for(int i=0;i<slotR.size();i++)if(slotR.get(i).contains(x,y))return 100+i;if(logBtn.contains(x,y))return 60;if(fastRect.contains(x,y))return 30;if(panelRect.contains(x,y))return 40;}
   return 0;}
  @Override void press(int id){
   if(id>=410&&id<=414){popPress(id);return;}
   if(id==3){tool=0;persist();return;}
   if(id==60){logOpen=true;panel=false;shop=false;return;}
   if(id==61){logOpen=false;return;}
   if(id==1){close.run();return;}
   if(id==2){boolean was=panel||logOpen;panel=!was;shop=false;logOpen=false;pop=0;if(was)markSeen();return;}
   if(id==50){shop=false;pop=0;return;}
   if(id==30){fast=!fast;persist();say(fast?"Fast growth on (testing)":"Fast growth off");return;}
   if(id>=300&&id<400){shopPress(id-300);return;}
   if(id>=100&&id<200){int i=id-100;if(i<slots.size()){int[] s=slots.get(i);seen|=bit(s);if(s[0]==0){tool=tool==s[1]?0:s[1];}else if(s[0]==1){if(tool==2&&seed==s[1])tool=0;else{tool=2;seed=s[1];}}else if(s[0]==2)say(iname[s[1]]+" - sells for "+sellP[s[1]]+" coins");else say(bname[s[1]]+" - sells for "+bugP[s[1]]+" coins");persist();}}}
