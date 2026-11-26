  final float[][] HND={{8,-12},{9,-13},{9,-14},{8,-16},{8,-15},{-8,-16},{-9,-14},{-9,-13}};
  float[] handPos(){return new float[]{sn(px)+HND[dir][0],sn(py)+HND[dir][1]};}
  void strikeFx(){if(act==6){shakeKey=aTree;shakeT=.25f;burst(ax,ay,0xFFB98A57,6);burst(ax,ay-6,0xFF72BE58,4);}else if(act==7){shakeKey=aTree;shakeT=.3f;burst(ax,ay-6,0xFF72BE58,5);}else burst(ax,ay,0xFF8A6244,6);performHapticFeedback(android.view.HapticFeedbackConstants.CLOCK_TICK);}
  void spr(Canvas c,Bitmap b,float x,float y,float gx,float gy,float ang,boolean fl){c.save();c.translate(x,y);if(fl)c.scale(-1,1);c.rotate(ang);c.drawBitmap(b,-gx,-gy,pix);c.restore();}
  void heldProp(Canvas c,float x,float y){if(act==0)return;float p=1-aT/aTot;boolean fl=dir>=5;float hx2=x+HND[dir][0],hy2=y+HND[dir][1];double tw=2*Math.PI;
   if(act==1){if(p>.35f){float lift=Math.min(1f,(p-.35f)*3f);Bitmap b=itemBmp[aItem];c.drawBitmap(b,x-b.getWidth()/2f,y-46-lift*4,pix);}}
   else if(act==8){if(p>.4f){Bitmap b=itemBmp[aItem];c.drawBitmap(b,x-b.getWidth()/2f,y-40,pix);}}
   else if(act==2){float a=38*Math.min(1f,(float)Math.sin(Math.PI*p)*1.6f);spr(c,toolBmp[3],hx2,hy2,5,8,a,fl);}
   else if(act==5){float a=-8*(float)Math.sin(p*14);spr(c,toolBmp[3],hx2,hy2+3*(float)Math.sin(Math.PI*p),5,8,a,fl);}
   else if(act==4){float a=18*(float)Math.sin(p*30);spr(c,packBmp[seed],hx2,hy2,6,7,a,fl);}
   else if(act==3||act==9){float a=(float)(-110-55*Math.cos(tw*2*p));spr(c,toolBmp[1],hx2,hy2,9.5f,1.5f,a,fl);}
   else if(act==6){float a=(float)(17-57*Math.cos(tw*3*p));spr(c,axeBmp,hx2,hy2,3f,9.5f,a,fl);}}
  int dipFx(){int n=act==6?3:(act==3||act==9)?2:0;if(n==0)return 0;float ph=((1-aT/aTot)*n)%1f;return ph>.4f&&ph<.7f?1:0;}
  @Override void drawDyn(Canvas c,int which){if(which!=0){super.drawDyn(c,which);return;}int fr=moving?1+(((int)(anim*8))&3):0;int bob=(fr==2||fr==4)?-1:0;float x=sn(px),y=sn(py);bob+=dipFx();sh(c,x,y,10);c.drawBitmap(hero(dir,fr),x-11,y-29+bob,pix);heldProp(c,x,y+bob);}
  @Override void drawThing(Canvas c,float[] o){int t=(int)o[2];int x=Math.round(o[0]),y=Math.round(o[1]);
   if(t==10){Plot p=plots.get((int)o[4]);c.drawBitmap(plantBmp[p.crop][p.stage],p.cx*12,p.cy*12-7,pix);return;}
   if(t==6){sh(c,x,y,26);c.drawBitmap(stallBmp,x-17,y-27,pix);return;}
   if(t==5){sh(c,x,y,12);c.drawBitmap(stumpBmp,x-15,y-36,pix);return;}
   if(t<=1&&shakeT>0&&tkey(o)==shakeKey){c.save();c.translate(Math.round((float)Math.sin(shakeT*60)*1.5f),0);super.drawThing(c,o);c.restore();return;}
   super.drawThing(c,o);}
  void talkBunny(){long today=todayNum();if(rDay!=today){rDay=today;rItem=(int)(Math.random()*9);rDone=false;}
   if(gDay!=today){gDay=today;int k=(int)(Math.random()*5);seeds[k]+=2;line="Clover: Lovely to see you! Take these.";talk=4;say("+2 "+iname[k]+" seeds");chime(softSound);mark76();return;}
   if(!rDone){if(it[rItem]>0){it[rItem]--;rDone=true;int rw=sellP[rItem]*2;coins+=rw;line="Clover: Just what I needed, thank you!";talk=4;say("+"+rw+" coins");chime(softSound);mark76();return;}line="Clover: Could you spare a "+iname[rItem].toLowerCase()+"?";talk=4;return;}
   line="Clover: "+chat[(int)(Math.random()*chat.length)];talk=3.5f;}
  void dropFx(Canvas c,float x,float y,float r){android.graphics.Path d=dropPath;d.reset();d.moveTo(x,y-r*1.9f);d.cubicTo(x+r*.3f,y-r*1.2f,x+r,y-r*.5f,x+r,y+r*.35f);d.cubicTo(x+r,y+r*1.1f,x+r*.5f,y+r*1.5f,x,y+r*1.5f);d.cubicTo(x-r*.5f,y+r*1.5f,x-r,y+r*1.1f,x-r,y+r*.35f);d.cubicTo(x-r,y-r*.5f,x-r*.3f,y-r*1.2f,x,y-r*1.9f);d.close();
   vp.setStyle(Paint.Style.STROKE);vp.setStrokeWidth(dens*3);vp.setColor(0xFFFFFFFF);c.drawPath(d,vp);vp.setStyle(Paint.Style.FILL);vp.setColor(0xFF4AA3EE);c.drawPath(d,vp);vp.setColor(0xCCFFFFFF);c.drawOval(x-r*.55f,y-r*.1f,x-r*.15f,y+r*.6f,vp);}
  void starFx(Canvas c,float x,float y,float r,int fillC,int edgeC){android.graphics.Path d=dropPath;d.reset();d.moveTo(x,y-r);d.quadTo(x,y,x+r,y);d.quadTo(x,y,x,y+r);d.quadTo(x,y,x-r,y);d.quadTo(x,y,x,y-r);d.close();vp.setStyle(Paint.Style.FILL);vp.setColor(fillC);c.drawPath(d,vp);vp.setStyle(Paint.Style.STROKE);vp.setStrokeWidth(dens*1.2f);vp.setColor(edgeC);c.drawPath(d,vp);}
  int bit(int[] s){return s[0]==0?1<<(14+s[1]):s[0]==1?1<<(9+s[1]):1<<s[1];}
  void slotsBuild(){slots.clear();slots.add(new int[]{0,1,0});slots.add(new int[]{0,3,0});if(haveAxe)slots.add(new int[]{0,4,0});for(int i=0;i<5;i++)if(seeds[i]>0)slots.add(new int[]{1,i,seeds[i]});for(int i=0;i<9;i++)if(it[i]>0)slots.add(new int[]{2,i,it[i]});}
  void cardsBuild(){cardI.clear();for(int i=0;i<5;i++)cardI.add(new int[]{0,i,buyP[i]});if(!haveAxe)cardI.add(new int[]{1,4,60});for(int i=0;i<9;i++)if(it[i]>0)cardI.add(new int[]{2,i,sellP[i]});}
  void markSeen(){for(int[] s:slots)seen|=bit(s);persist();}
  void shopPress(int i){if(i>=cardI.size())return;int[] c=cardI.get(i);
   if(c[0]==0){if(coins<c[2]){say("Not enough coins");return;}coins-=c[2];seeds[c[1]]++;say("Bought "+iname[c[1]]+" seeds");}
   else if(c[0]==1){if(coins<c[2]){say("Not enough coins");return;}coins-=c[2];haveAxe=true;say("Bought an axe!");}
   else{if(it[c[1]]<=0)return;it[c[1]]--;coins+=c[2];say("Sold "+iname[c[1]]+" +"+c[2]);}
   chime(softSound);persist();}
  @Override int hit(float x,float y){if(closeRect.contains(x,y))return 1;if(bagRect.contains(x,y))return 2;
   if(shop){if(shopX.contains(x,y))return 50;for(int i=0;i<cardR.size();i++)if(cardR.get(i).contains(x,y))return 300+i;if(panelRect.contains(x,y))return 40;}
   else if(panel){for(int i=0;i<slotR.size();i++)if(slotR.get(i).contains(x,y))return 100+i;if(fastRect.contains(x,y))return 30;if(panelRect.contains(x,y))return 40;}
   return 0;}
  @Override void press(int id){if(id==1){close.run();return;}
   if(id==2){boolean was=panel;panel=!panel;shop=false;if(was)markSeen();return;}
   if(id==50){shop=false;return;}
   if(id==30){fast=!fast;persist();say(fast?"Fast growth on (testing)":"Fast growth off");return;}
   if(id>=300&&id<400){shopPress(id-300);return;}
   if(id>=100&&id<200){int i=id-100;if(i<slots.size()){int[] s=slots.get(i);seen|=bit(s);if(s[0]==0){tool=tool==s[1]?0:s[1];}else if(s[0]==1){if(tool==2&&seed==s[1])tool=0;else{tool=2;seed=s[1];}}else say(iname[s[1]]+" - sells for "+sellP[s[1]]+" coins");persist();}}}
