  void checkGrowth(){long now=System.currentTimeMillis();boolean ch=false;for(Plot p:plots)if(p.crop>=0&&p.wet&&now>=p.readyAt){p.stage=Math.min(3,p.stage+1);p.wet=false;ch=true;}if(ch)persist();}
  void tick(float dt){if(pend!=0){float dx=ptx-px,dy=pty-py;if(dx*dx+dy*dy<(pend==5?196f:100f)){perform();pend=0;hasT=false;}else if(!hasT)pend=0;}
   for(int i=parts.size()-1;i>=0;i--){Part q=parts.get(i);q.x+=q.vx*dt;q.y+=q.vy*dt;q.vy+=80*dt;q.life-=dt;if(q.life<=0)parts.remove(i);}
   if(toastT>0)toastT-=dt;growT+=dt;if(growT>1){growT=0;checkGrowth();}}
  @Override void step(float dt){if(actT>0){actT-=dt;boolean k=hasT;hasT=false;super.step(dt);hasT=k;}else super.step(dt);tick(dt);}
  @Override void drawThing(Canvas c,float[] o){if(o[2]<10){super.drawThing(c,o);return;}Plot p=plots.get((int)o[4]);int x=p.cx*12,y=p.cy*12-7;c.drawBitmap(plantBmp[p.crop][p.stage],x,y,pix);float tt=(SystemClock.uptimeMillis()%2000)/2000f;if(p.stage<3&&!p.wet){int bob=Math.round((float)Math.sin(tt*6.283f)*1.2f);c.drawBitmap(dropBmp,x+1,y+(p.stage==0?7:p.stage==1?4:0)-9+bob,pix);}if(p.stage==3&&tt<.5f){fill.setColor(0xFFFFFFFF);c.drawRect(x+9,y+1,x+10,y+4,fill);c.drawRect(x+8,y+2,x+11,y+3,fill);}}
  @Override public android.view.WindowInsets onApplyWindowInsets(android.view.WindowInsets in){android.graphics.Insets i=in.getInsets(android.view.WindowInsets.Type.systemBars()|android.view.WindowInsets.Type.displayCutout());insT=i.top;insB=i.bottom;insL=i.left;insR=i.right;invalidate();return in;}
  @Override protected void onAttachedToWindow(){super.onAttachedToWindow();requestApplyInsets();}
  @Override protected void onDetachedFromWindow(){persist();super.onDetachedFromWindow();}
  int hit(float x,float y){if(closeRect.contains(x,y))return 1;if(bagRect.contains(x,y))return 2;if(panel){for(int i=1;i<4;i++)if(toolRect[i].contains(x,y))return 10+i;for(int i=0;i<5;i++)if(seedRect[i].contains(x,y))return 20+i;if(fastRect.contains(x,y))return 30;if(panelRect.contains(x,y))return 40;}return 0;}
  void press(int id){if(id==1)close.run();else if(id==2)panel=!panel;else if(id>=11&&id<=13){int t=id-10;tool=tool==t?0:t;persist();}else if(id>=20&&id<25){seed=id-20;tool=2;persist();}else if(id==30){fast=!fast;persist();say(fast?"Fast growth on (testing)":"Fast growth off");}}
  @Override public boolean onTouchEvent(MotionEvent e){int a=e.getActionMasked();float x=e.getX(),y=e.getY();
   if(a==MotionEvent.ACTION_DOWN){downBtn=hit(x,y);if(downBtn!=0)return true;tapWorld(cx0+x/scale,cy0+y/scale);return true;}
   if(downBtn!=0){if(a==MotionEvent.ACTION_UP){int id=hit(x,y);if(id==downBtn)press(id);downBtn=0;}else if(a==MotionEvent.ACTION_CANCEL)downBtn=0;return true;}
   if(a==MotionEvent.ACTION_MOVE&&holdWalk)target(cx0+x/scale,cy0+y/scale);else if(a==MotionEvent.ACTION_UP||a==MotionEvent.ACTION_CANCEL){holding=false;holdWalk=false;}return true;}
  void icon(Canvas c,Bitmap b,float cx,float cy,float w,float h){dest.set(cx-w/2,cy-h/2,cx+w/2,cy+h/2);c.drawBitmap(b,null,dest,pix);}
  @Override protected void onDraw(Canvas c){long now=SystemClock.uptimeMillis();float dt=Math.min(.05f,(now-last)/1000f);last=now;float t=(now-born)/1000f;int W=getWidth(),H=getHeight();if(W==0)return;step(dt);
   scale=Math.max(3,Math.round(W/140f));float vw=W/(float)scale,vh=H/(float)scale;cx0=sn(Math.max(0,Math.min(WW-vw,px-vw/2)));cy0=sn(Math.max(0,Math.min(WH-vh,py-vh/2)));
   c.drawColor(0xFF3E72C6);c.save();c.scale(scale,scale);c.translate(-cx0,-cy0);c.drawBitmap(world,0,0,pix);
   fill.setColor(0x99FFFFFF);for(float[] f:sparks){float ph=(t*1.1f+f[2])%3f;if(ph<.6f)c.drawRect(f[0],f[1],f[0]+2,f[1]+1,fill);}
   for(Plot p:plots)c.drawBitmap(p.wet?holeWet:holeDry,p.cx*12+1,p.cy*12+4,pix);
   if(hasT){int r=((int)(t*6))%3;int x=Math.round(tx),y=Math.round(ty);fill.setColor(0xDDFFFFFF);c.drawRect(x-2-r,y-2-r,x-1-r,y-1-r,fill);c.drawRect(x+2+r,y-2-r,x+3+r,y-1-r,fill);c.drawRect(x-2-r,y+2+r,x-1-r,y+3+r,fill);c.drawRect(x+2+r,y+2+r,x+3+r,y+3+r,fill);}
   java.util.ArrayList<float[]> lst=new java.util.ArrayList<>(things);for(int i=0;i<plots.size();i++){Plot p=plots.get(i);if(p.crop>=0)lst.add(new float[]{p.cx*12+6,p.cy*12+9,10,0,i});}
   java.util.Collections.sort(lst,(u,k2)->Float.compare(u[1],k2[1]));
   int first=py<=by?0:1;float y1=Math.min(py,by),y2=Math.max(py,by);boolean d1=false,d2=false;
   for(float[] o:lst){if(!d1&&o[1]>y1){drawDyn(c,first);d1=true;}if(!d2&&o[1]>y2){drawDyn(c,1-first);d2=true;}drawThing(c,o);}if(!d1)drawDyn(c,first);if(!d2)drawDyn(c,1-first);
   for(float[] f:flies){float x=sn(f[0]+(float)Math.sin(t*.5f+f[2])*22),y=sn(f[1]+(float)Math.cos(t*.8f+f[2])*14);boolean flap=((((int)(t*9+f[2]*3)))&1)==0;fill.setColor(0xFF3A2A30);c.drawRect(x,y,x+1,y+2,fill);fill.setColor(flyCol[(int)f[3]%5]);if(flap){c.drawRect(x-2,y-1,x,y+1,fill);c.drawRect(x+1,y-1,x+3,y+1,fill);}else{c.drawRect(x-1,y,x,y+1,fill);c.drawRect(x+1,y,x+2,y+1,fill);}}
   for(Part q:parts){fill.setColor(q.col);float x=sn(q.x),y=sn(q.y);c.drawRect(x,y,x+1,y+1,fill);}
   c.restore();int ov=tint();if(ov!=0)c.drawColor(ov);
   float rr2=dens*28,bcx=W-insR-dens*16-rr2,bcy=H-insB-dens*16-rr2;bagRect.set(bcx-rr2,bcy-rr2,bcx+rr2,bcy+rr2);closeRect.set(W-insR-dens*60,insT+dens*12,W-insR-dens*12,insT+dens*60);
   fill.setColor(0xCCFFFFFF);c.drawRoundRect(closeRect,dens*16,dens*16,fill);ink.setColor(0xFF6A5560);ink.setStrokeWidth(dens*3);ink.setStrokeCap(Paint.Cap.ROUND);float mx=closeRect.centerX(),my=closeRect.centerY(),q8=dens*8;c.drawLine(mx-q8,my-q8,mx+q8,my+q8,ink);c.drawLine(mx+q8,my-q8,mx-q8,my+q8,ink);
   ink.setTextAlign(Paint.Align.CENTER);ink.setTextSize(dens*15);
   if(talk>0){float sx=(bx-cx0)*scale,sy=(by-26-cy0)*scale;float tw=ink.measureText(line)+dens*24;float l=Math.max(dens*8,Math.min(W-tw-dens*8,sx-tw/2));fill.setColor(0xF5FFFFFF);c.drawRoundRect(l,sy-dens*40,l+tw,sy-dens*6,dens*14,dens*14,fill);ink.setColor(0xFF6A5560);c.drawText(line,l+tw/2,sy-dens*18,ink);}
   if(toastT>0){float tw=ink.measureText(toast)+dens*28;float top=insT+dens*70;fill.setColor(0xF2FFF7F0);c.drawRoundRect(W/2f-tw/2,top,W/2f+tw/2,top+dens*40,dens*16,dens*16,fill);ink.setColor(0xFF6A5560);c.drawText(toast,W/2f,top+dens*26,ink);}
   if(t<8&&!panel){int al=(int)(255*Math.min(1f,(8-t)/2f));String hint="Tap to walk \u00b7 open the bag for your tools";float tw=ink.measureText(hint)+dens*28;float top=bagRect.top-dens*70;fill.setColor((al*3/5)<<24);c.drawRoundRect(W/2f-tw/2,top,W/2f+tw/2,top+dens*40,dens*16,dens*16,fill);ink.setColor((al<<24)|0xFFFFFF);c.drawText(hint,W/2f,top+dens*26,ink);}
   if(panel){float pl=insL+dens*10,pr=W-insR-dens*10,pb=bagRect.top-dens*10,pt=pb-dens*216;panelRect.set(pl,pt,pr,pb);float bw=(pr-pl-dens*32)/3f,sw=(pr-pl-dens*32)/5f;
    for(int i=1;i<4;i++)toolRect[i].set(pl+dens*8+(i-1)*(bw+dens*8),pt+dens*30,pl+dens*8+(i-1)*(bw+dens*8)+bw,pt+dens*100);
    for(int i=0;i<5;i++)seedRect[i].set(pl+dens*8+i*(sw+dens*4),pt+dens*124,pl+dens*8+i*(sw+dens*4)+sw,pt+dens*184);fastRect.set(pl+dens*8,pt+dens*188,pr-dens*8,pt+dens*210);
    fill.setColor(0xF4FFF7F0);c.drawRoundRect(panelRect,dens*18,dens*18,fill);ink.setTextSize(dens*12);ink.setColor(0xFF8A7080);ink.setTextAlign(Paint.Align.LEFT);c.drawText("Tools",pl+dens*12,pt+dens*21,ink);c.drawText("Seeds (tap to plant) and your harvest",pl+dens*12,pt+dens*116,ink);ink.setTextAlign(Paint.Align.CENTER);ink.setColor(0xFF6A5560);
    for(int i=1;i<4;i++){fill.setColor(tool==i?0xFFFFD9A8:0xFFF3E6DE);c.drawRoundRect(toolRect[i],dens*14,dens*14,fill);icon(c,toolBmp[i],toolRect[i].centerX(),toolRect[i].top+dens*28,dens*34,dens*34);c.drawText(i==1?"Shovel":i==2?"Seeds":"Can "+water+"/10",toolRect[i].centerX(),toolRect[i].bottom-dens*8,ink);}
    for(int i=0;i<5;i++){fill.setColor(tool==2&&seed==i?0xFFFFD9A8:0xFFF3E6DE);c.drawRoundRect(seedRect[i],dens*14,dens*14,fill);icon(c,plantBmp[i][3],seedRect[i].centerX(),seedRect[i].top+dens*26,dens*26,dens*34);c.drawText("x"+inv[i],seedRect[i].centerX(),seedRect[i].bottom-dens*7,ink);}
    fill.setColor(fast?0xFFFFD9A8:0xFFF3E6DE);c.drawRoundRect(fastRect,dens*12,dens*12,fill);c.drawText("Fast growth (testing): "+(fast?"on":"off"),fastRect.centerX(),fastRect.centerY()+dens*4,ink);}
   fill.setColor(panel?0xFFFFD9A8:0xF4FFF7F0);c.drawCircle(bcx,bcy,rr2,fill);icon(c,bagBmp,bcx,bcy,dens*34,dens*34);
   if(tool!=0){float chx=bcx-rr2-dens*32;fill.setColor(0xF4FFF7F0);c.drawCircle(chx,bcy,dens*22,fill);icon(c,toolBmp[tool],chx,bcy,dens*28,dens*28);if(tool==3){ink.setTextSize(dens*11);ink.setColor(0xFF6A5560);c.drawText(""+water,chx,bcy+dens*34,ink);}}
   if(running)postInvalidateOnAnimation();}
 }
