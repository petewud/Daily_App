  @Override void tick(float dt){super.tick(dt);for(int i=crit.size()-1;i>=0;i--){float[] q=crit.get(i);q[0]+=q[3]*dt;q[1]+=q[4]*dt;q[5]-=dt;q[6]+=dt;if(q[5]<=0)crit.remove(i);}}
  @Override void checkGrowth(){super.checkGrowth();long now=System.currentTimeMillis();boolean ch=false;java.util.Iterator<java.util.Map.Entry<Integer,long[]>> in=saps.entrySet().iterator();
   while(in.hasNext()){java.util.Map.Entry<Integer,long[]> e=in.next();long[] s=e.getValue();if(s[1]!=1||now<s[2])continue;s[0]++;s[1]=0;ch=true;if(s[0]>=3){float[] o=anyThing(e.getKey());if(o!=null){o[2]=0;o[3]=4;ptrees.add(e.getKey());}say("A sapling grew into a tree!");in.remove();}}
   if(ch)persist();}
  @Override void heldProp(Canvas c,float x,float y){float p=act!=0?1-aT/aTot:0;
   if(act==12){float k=7*(float)Math.sin(Math.PI*p);c.drawBitmap(bootBmp,x+FX[dir]*k-2,y-3+FY[dir]*k*.6f-(k>2?2:0),pix);return;}
   if(act==13){float a=(float)(-60+120*Math.sin(Math.PI*p));spr(c,netBmp,x+HND[dir][0],y+HND[dir][1],3,9.5f,a,dir>=5);return;}
   if(act==15)return;
   if(act==4&&aMode==3){float a=10*(float)Math.sin(p*20);spr(c,sapBmp[0],x+HND[dir][0],y+HND[dir][1]+2,7,12,a,dir>=5);return;}
   super.heldProp(c,x,y);}
  @Override int dipFx(){if(act==15||act==12){float p=1-aT/aTot;return p>.15f&&p<.85f?1:0;}return super.dipFx();}
  @Override void drawDyn(Canvas c,int which){if(which==1){for(float[] q:crit){int k=(int)q[2];Bitmap b=bugBmp[k];float x=sn(q[0]),y=sn(q[1]);sh(c,x,y,6);c.save();if(q[3]<0)c.scale(-1,1,x,y);c.drawBitmap(b,x-b.getWidth()/2f,y-b.getHeight(),pix);c.restore();}}super.drawDyn(c,which);}
  @Override void drawThing(Canvas c,float[] o){int t=(int)o[2];float tt=SystemClock.uptimeMillis()/1000f;
   if(t==10){Plot p=plots.get((int)o[4]);int x=p.cx*12,y=p.cy*12-7;c.drawBitmap(plantBmp[p.crop][p.stage],x,y,pix);
    if(p.stage<3&&!p.wet){int top=p.stage==0?14:p.stage==1?9:4;c.drawBitmap(dropPx,x+2.5f,y+top-10+(float)Math.sin(tt*3.2f+p.cx*1.7f)*1.6f,pix);}
    else if(p.stage==3){starP.setAlpha((int)(190+65*Math.sin(tt*6f+p.cy)));c.drawBitmap(starPx,x+8.5f,y-1.5f+(float)Math.sin(tt*3f)*.8f,starP);}
    return;}
   if(t==11){long[] s=saps.get(tkey(o));int st=s==null?0:(int)Math.min(2,s[0]);int x=Math.round(o[0]),y=Math.round(o[1]);sh(c,x,y,8);c.drawBitmap(sapBmp[st],x-7,y-17,pix);
    if(s!=null&&s[1]!=1){int top=st==0?7:st==1?10:17;c.drawBitmap(dropPx,x-3.5f,y-top-10+(float)Math.sin(tt*3.2f+x)*1.6f,pix);}return;}
   if(t==3&&act==15&&tkey(o)==liftKey){float lift=Math.round(6*(float)Math.sin(Math.PI*(1-aT/aTot)));c.save();c.translate(0,-lift);super.drawThing(c,o);c.restore();return;}
   super.drawThing(c,o);}
