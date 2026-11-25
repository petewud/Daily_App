
 // A_DAY_TO_KEEP_ISLAND_74
 void openIsland74(){Dialog full=new Dialog(this,android.R.style.Theme_Material_Light_NoActionBar_Fullscreen);IslandDemo74 game=new IslandDemo74(()->full.dismiss());full.setContentView(game);full.setOnDismissListener(d->game.running=false);full.show();}
 void installGameTap74(){final View hc=homeCharacter;if(hc==null||data==null||!data.optBoolean("gameMode",false))return;hc.setContentDescription("Visit the island");final float[] at=new float[2];final long[] t0={0};hc.setOnTouchListener((v,e)->{int a=e.getActionMasked();if(a==MotionEvent.ACTION_DOWN){at[0]=e.getRawX();at[1]=e.getRawY();t0[0]=e.getEventTime();return true;}if(a==MotionEvent.ACTION_UP){if(Math.abs(e.getRawX()-at[0])<dp(16)&&Math.abs(e.getRawY()-at[1])<dp(16)&&e.getEventTime()-t0[0]<700){chime(softSound);openIsland74();}return true;}return a==MotionEvent.ACTION_MOVE||a==MotionEvent.ACTION_CANCEL;});}
 class IslandDemo74 extends View {
  final Runnable close;final int WW=320,WH=440;final byte[] terr=new byte[WW*WH];Bitmap world,tree,fruit,bush,rock,bunnyA,bunnyB;final Bitmap[][] hero=new Bitmap[8][5];
  final Paint pix=new Paint(),ink=new Paint(Paint.ANTI_ALIAS_FLAG),fill=new Paint();final float dens=getResources().getDisplayMetrics().density;final RectF closeRect=new RectF();
  final java.util.ArrayList<float[]> things=new java.util.ArrayList<>(),sparks=new java.util.ArrayList<>(),flies=new java.util.ArrayList<>();final int[] flyCol={0xFFF29BB5,0xFFFFE27A,0xFFB79CE8,0xFFFFFFFF,0xFFF4A261};final int[] MAP={2,1,0,7,6,5,4,3};
  float px,py,tx,ty,anim,bx,by,btx,bty,bAnim,bwait=1,talk,hx,hy;boolean hasT,holding,moving,bMoving,closing,running=true;int dir,scale=6,cx0,cy0;long last,born;String line="";
  final String[] lines={"What a lovely day!","I'm thinking of planting carrots.","Have you seen any butterflies?","The pond looks so peaceful.","Fancy a walk later?","I heard the fish are biting."};
  final int SKIN=0xFFF3C9A5,HAIR=0xFF4B3228,HAIRL=0xFF664639,SHIRT=0xFFFFF1D6,DENIM=0xFF5B84BE,DENIML=0xFF7BA2D6,DENIMD=0xFF4668A0,BOOT=0xFF7A5238,BOOTD=0xFF5E3F2B,BTN=0xFFE9B949,BLUSH=0xFFF08C8C,EYE=0xFF3A2A30;
  IslandDemo74(Runnable onClose){super(MainActivity.this);close=onClose;pix.setFilterBitmap(false);pix.setAntiAlias(false);fill.setAntiAlias(false);ink.setTypeface(bodyFont);build();born=last=SystemClock.uptimeMillis();}
  int hs(int x,int y,int s){int v=x*374761393+y*668265263+s*1274126177;v=(v^(v>>>13))*1274126177;return v^(v>>>16);}
  int hm(int x,int y,int s,int m){return (hs(x,y,s)&0x7fffffff)%m;}
  float rr(int x,int y,int s){return (hs(x,y,s)&0xffff)/65535f;}
  float vn(float x,float y,int s){int x0=(int)Math.floor(x),y0=(int)Math.floor(y);float fx=x-x0,fy=y-y0;fx=fx*fx*(3-2*fx);fy=fy*fy*(3-2*fy);float a=rr(x0,y0,s),b=rr(x0+1,y0,s),c=rr(x0,y0+1,s),d=rr(x0+1,y0+1,s);return a+(b-a)*fx+(c-a)*fy+(a-b-c+d)*fx*fy;}
  int tk(int x,int y){return x<0||y<0||x>=WW||y>=WH?0:terr[y*WW+x];}
  int dk(int c){return 0xFF000000|((int)(((c>>16)&255)*.55f)<<16)|((int)(((c>>8)&255)*.55f)<<8)|(int)((c&255)*.55f);}
  boolean circ(int x,int y,int cx,int cy,int r){return (x-cx)*(x-cx)+(y-cy)*(y-cy)<=r*r;}
  void put(int[] a,int x,int y,int c){if(x>=0&&y>=0&&x<WW&&y<WH&&terr[y*WW+x]==3)a[y*WW+x]=c;}
  boolean near(int x,int y,int r){for(float[] o:things){float dx=o[0]-x,dy=o[1]-y;if(dx*dx+dy*dy<r*r)return true;}return false;}
  void build(){float cx=WW/2f,cy=WH/2f,pcx=cx+WW*.12f,pcy=cy-WH*.07f;
   for(int y=0;y<WH;y++)for(int x=0;x<WW;x++){float nx=(x-cx)/(WW*.43f),ny=(y-cy)/(WH*.43f);float d=(float)Math.sqrt(nx*nx+ny*ny)+(vn(x/24f,y/24f,1)-.5f)*.30f+(vn(x/8f,y/8f,2)-.5f)*.07f;byte k=(byte)(d<.76f?3:d<.86f?2:d<.96f?1:0);float pdx=(x-pcx)/38f,pdy=(y-pcy)/24f;float pd=pdx*pdx+pdy*pdy+(vn(x/6f,y/6f,5)-.5f)*.25f;if(k==3&&pd<1)k=4;terr[y*WW+x]=k;}
   int[] px0=new int[WW*WH];
   for(int y=0;y<WH;y++)for(int x=0;x<WW;x++){int k=terr[y*WW+x],c;boolean beach=tk(x-1,y)==2||tk(x+1,y)==2||tk(x,y-1)==2||tk(x,y+1)==2;
    if(k==0){c=((x+y)&1)==0?0xFF3E72C6:0xFF4378CC;if(vn(x/5f,y/3f,7)>.72f)c=0xFF4F86D6;}
    else if(k==1){c=beach?0xFFEAF6FF:(((x+y)&1)==0?0xFF62A8E6:0xFF69AEEA);}
    else if(k==2){c=hm(x,y,3,7)==0?0xFFE2CC86:0xFFF0DEA2;}
    else if(k==4){c=vn(x/4f,y/3f,8)>.7f?0xFF7CC8F4:0xFF4DA5E8;}
    else{float v=vn(x/6f,y/6f,4);c=v>.64f?0xFF8CD26F:v<.32f?0xFF6DB65A:0xFF7CC464;if(hm(x,y,6,53)==0)c=0xFF5CA24B;if(beach)c=0xFF68AE55;if(tk(x-1,y)==4||tk(x+1,y)==4||tk(x,y-1)==4||tk(x,y+1)==4)c=0xFFC8B07C;}
    px0[y*WW+x]=c;}
   java.util.Random rnd=new java.util.Random(7);int[] pet={0xFFF29BB5,0xFFFFE27A,0xFFFFFFFF,0xFFB79CE8};
   for(int n=0;n<40;n++){int x=10+rnd.nextInt(WW-20),y=10+rnd.nextInt(WH-20);if(tk(x,y)!=3||tk(x-6,y)!=3||tk(x+6,y)!=3||tk(x,y-6)!=3||tk(x,y+6)!=3)continue;int col=pet[rnd.nextInt(4)];for(int i=0;i<4+rnd.nextInt(4);i++){int fx=x+rnd.nextInt(15)-7,fy=y+rnd.nextInt(15)-7;put(px0,fx,fy,col);put(px0,fx-1,fy,col);put(px0,fx+1,fy,col);put(px0,fx,fy-1,col);put(px0,fx,fy+1,col);put(px0,fx,fy,0xFFFFD35A);}}
   for(int n=0;n<6;n++){int x=(int)pcx-24+rnd.nextInt(48),y=(int)pcy-12+rnd.nextInt(24);if(tk(x,y)==4&&tk(x+3,y)==4&&tk(x,y+2)==4){for(int j=0;j<2;j++)for(int i=0;i<4;i++)px0[(y+j)*WW+x+i]=0xFF3F9B52;px0[y*WW+x+1]=0xFF6CC47A;}}
   world=Bitmap.createBitmap(px0,WW,WH,Bitmap.Config.ARGB_8888);
   px=cx;py=cy+30;hx=cx-45;hy=cy+8;bx=hx;by=hy;btx=bx;bty=by;
   for(int n=0;n<500&&things.size()<36;n++){int x=22+rnd.nextInt(WW-44),y=40+rnd.nextInt(WH-60);if(tk(x,y)!=3||tk(x-12,y)!=3||tk(x+12,y)!=3||tk(x,y+3)!=3||near(x,y,22))continue;float sx=x-px,sy=y-py;if(sx*sx+sy*sy<1200||(x-hx)*(x-hx)+(y-hy)*(y-hy)<900)continue;things.add(new float[]{x,y,rnd.nextInt(4)==0?1:0,4});}
   for(int n=0;n<300&&things.size()<56;n++){int x=14+rnd.nextInt(WW-28),y=14+rnd.nextInt(WH-28);int k=tk(x,y);if((k!=3&&k!=2)||tk(x-6,y)!=k||tk(x+6,y)!=k||near(x,y,13))continue;float sx=x-px,sy=y-py;if(sx*sx+sy*sy<500||(x-hx)*(x-hx)+(y-hy)*(y-hy)<400)continue;things.add(new float[]{x,y,n%3==0?3:2,5});}
   java.util.Collections.sort(things,(a,b)->Float.compare(a[1],b[1]));
   for(int n=0;n<260;n++){int x=rnd.nextInt(WW),y=rnd.nextInt(WH);if(tk(x,y)<=1)sparks.add(new float[]{x,y,rnd.nextFloat()*3});}
   for(int n=0;n<5;n++)flies.add(new float[]{WW/2f-70+rnd.nextInt(140),WH/2f-90+rnd.nextInt(180),rnd.nextFloat()*6,n});
   tree=makeTree(false);fruit=makeTree(true);bush=makeBush();rock=makeRock();bunnyA=makeBunny(false);bunnyB=makeBunny(true);}
  void edge(int[] b,int W,int H){int[] o=b.clone();for(int y=0;y<H;y++)for(int x=0;x<W;x++){if((b[y*W+x]>>>24)==0)continue;boolean e=x==0||y==0||x==W-1||y==H-1||(b[y*W+x-1]>>>24)==0||(b[y*W+x+1]>>>24)==0||(b[(y-1)*W+x]>>>24)==0||(b[(y+1)*W+x]>>>24)==0;if(e)o[y*W+x]=dk(b[y*W+x]);}System.arraycopy(o,0,b,0,b.length);}
  Bitmap makeTree(boolean fr){int W=30,H=38;int[] b=new int[W*H];for(int y=24;y<37;y++)for(int x=13;x<18;x++)b[y*W+x]=x>=16?0xFF6D4429:0xFF8A5A3A;for(int x=11;x<20;x++)b[36*W+x]=0xFF6D4429;
   for(int y=0;y<28;y++)for(int x=0;x<W;x++){if(circ(x,y,15,13,12)||circ(x,y,7,19,8)||circ(x,y,23,19,8)){float l=(x-15)*.6f+(y-13)*.8f;int c=l<-7?0xFF92D870:l<3?0xFF6DBA55:0xFF4E9944;if(hm(x,y,9,9)==0)c=0xFF55A24B;b[y*W+x]=c;}}
   if(fr){int[][] f={{9,14},{20,11},{15,20},{23,19},{7,20}};for(int[] p:f){b[p[1]*W+p[0]]=0xFFFF8A7A;b[p[1]*W+p[0]+1]=0xFFE0453C;b[(p[1]+1)*W+p[0]]=0xFFE0453C;b[(p[1]+1)*W+p[0]+1]=0xFFC03A33;}}
   edge(b,W,H);return Bitmap.createBitmap(b,W,H,Bitmap.Config.ARGB_8888);}
  Bitmap makeBush(){int W=16,H=11;int[] b=new int[W*H];for(int y=0;y<H;y++)for(int x=0;x<W;x++)if(circ(x,y,5,6,5)||circ(x,y,11,6,5)||circ(x,y,8,4,4)){float l=(x-8)*.6f+(y-5)*.8f;b[y*W+x]=l<-3?0xFF8FD46E:l<2?0xFF6BB854:0xFF4D9A45;}b[5*W+6]=0xFFF29BB5;b[7*W+11]=0xFFF29BB5;b[4*W+9]=0xFFFFE27A;edge(b,W,H);return Bitmap.createBitmap(b,W,H,Bitmap.Config.ARGB_8888);}
  Bitmap makeRock(){int W=14,H=9;int[] b=new int[W*H];for(int y=0;y<H;y++)for(int x=0;x<W;x++){float u=(x-6.5f)/6.5f,v=(y-5)/4f;if(u*u+v*v<=1){float l=u*.5f+v*.8f;b[y*W+x]=l<-.4f?0xFFCBC5D0:l<.3f?0xFFAAA4B4:0xFF8A8499;}}edge(b,W,H);return Bitmap.createBitmap(b,W,H,Bitmap.Config.ARGB_8888);}
  Bitmap makeBunny(boolean lift){int W=18,H=24;int[] b=new int[W*H];int fur=0xFFFFF4EA,pink=0xFFF6B7C6;for(int y=0;y<H;y++)for(int x=0;x<W;x++){if(circ(x,y,9,10,6)||circ(x,y,9,17,5)||(x>=4&&x<=6&&y<=7)||(x>=11&&x<=13&&y<=7)){float l=(x-9)*.5f+(y-12)*.5f;b[y*W+x]=l>3?0xFFEAD9CC:fur;}}
   for(int y=1;y<6;y++){b[y*W+5]=pink;b[y*W+12]=pink;}for(int y=15;y<21;y++)for(int x=6;x<12;x++)b[y*W+x]=0xFFF4A6BC;b[9*W+6]=EYE;b[10*W+6]=EYE;b[9*W+11]=EYE;b[10*W+11]=EYE;b[11*W+8]=BLUSH;b[11*W+9]=BLUSH;
   for(int x=5;x<8;x++){b[(lift?20:21)*W+x]=0xFFEAD9CC;b[(lift?21:22)*W+x]=0xFFEAD9CC;}for(int x=10;x<13;x++){b[21*W+x]=0xFFEAD9CC;b[22*W+x]=0xFFEAD9CC;}edge(b,W,H);return Bitmap.createBitmap(b,W,H,Bitmap.Config.ARGB_8888);}
  void R(int[] b,int x,int y,int w,int hh,int c){for(int j=y+1;j<y+1+hh;j++)for(int i=x+1;i<x+1+w;i++)if(i>=0&&j>=0&&i<22&&j<30)b[j*22+i]=c;}
  Bitmap hero(int d,int fr){if(hero[d][fr]!=null)return hero[d][fr];int base=d>4?8-d:d;int W=22,H=30;int[] b=new int[W*H];int aL=fr==1?1:fr==3?-1:0,aR=-aL,lL=fr==1?-1:0,lR=fr==3?-1:0;
   if(base==2){int o=fr==1?-2:fr==3?2:0;R(b,8-o,24,3,2,DENIMD);R(b,7-o,26,5,2,BOOTD);R(b,8+o,24,3,2,DENIM);R(b,8+o,26,5,2,BOOT);R(b,7,13,7,8,SHIRT);R(b,7,18,7,7,DENIM);R(b,11,14,3,5,DENIM);R(b,9,13,1,6,DENIMD);R(b,12,16,1,1,BTN);R(b,9,14+aL,3,6,SHIRT);R(b,10,20+aL,2,1,SKIN);R(b,9,5,7,8,SKIN);R(b,4,2,7,13,HAIR);R(b,5,2,10,4,HAIR);R(b,11,5,5,2,HAIR);R(b,6,3,4,1,HAIRL);R(b,13,9,1,2,EYE);R(b,12,11,2,1,BLUSH);R(b,16,9,1,2,SKIN);}
   else{R(b,5,13,10,8,SHIRT);R(b,3,14+aL,2,6,SHIRT);R(b,15,14+aR,2,6,SHIRT);R(b,3,20+aL,2,1,SKIN);R(b,15,20+aR,2,1,SKIN);R(b,5,18,10,7,DENIM);R(b,5,24,4,2,DENIM);R(b,11,24,4,2,DENIM);R(b,5,26+lL,4,2,BOOT);R(b,11,26+lR,4,2,BOOT);
    if(base<=1){int f=base==1?1:0;R(b,7,14,6,5,DENIM);R(b,6,13,1,5,DENIMD);R(b,13,13,1,5,DENIMD);R(b,6,16,1,1,BTN);R(b,13,16,1,1,BTN);R(b,8,20,4,2,DENIML);R(b,5,5,10,8,SKIN);R(b,4,2,12,4,HAIR);R(b,4,5,2,10,HAIR);R(b,14,5,2,10,HAIR);R(b,5,5,10,2,HAIR);R(b,6,3,4,1,HAIRL);R(b,7+f,9,1,2,EYE);R(b,12+f,9,1,2,EYE);R(b,6+f,11,2,1,BLUSH);R(b,12+f,11,2,1,BLUSH);}
    else{int s=base==3?1:0;for(int i=0;i<6;i++){R(b,6+i,13+i,1,1,DENIMD);R(b,13-i,13+i,1,1,DENIMD);}R(b,8,21,4,2,DENIML);R(b,4+s,2,12,12,HAIR);R(b,5+s,13,10,2,HAIR);R(b,6+s,4,4,1,HAIRL);if(base==3)R(b,16,8,1,3,SKIN);}}
   edge(b,W,H);if(d>4){int[] m=new int[b.length];for(int y=0;y<H;y++)for(int x=0;x<W;x++)m[y*W+W-1-x]=b[y*W+x];b=m;}return hero[d][fr]=Bitmap.createBitmap(b,W,H,Bitmap.Config.ARGB_8888);}
  boolean walk(float x,float y){int k=tk((int)x,(int)y);if(k!=2&&k!=3)return false;for(float[] o:things){float dx=x-o[0],dy=y-o[1];if(dx*dx+dy*dy<o[3]*o[3])return false;}return true;}
  void pickBunny(){for(int i=0;i<12;i++){float x=hx+(float)Math.random()*90-45,y=hy+(float)Math.random()*70-35;if(walk(x,y)){btx=x;bty=y;return;}}btx=bx;bty=by;}
  void step(float dt){float dx=tx-px,dy=ty-py,dist=(float)Math.hypot(dx,dy);moving=false;
   if(hasT&&dist>1.5f){float s=Math.min(dist,42*dt),ux=dx/dist,uy=dy/dist,nx=px+ux*s,ny=py+uy*s;boolean ok=true;if(walk(nx,ny)){px=nx;py=ny;}else if(Math.abs(ux)>.2f&&walk(nx,py))px=nx;else if(Math.abs(uy)>.2f&&walk(px,ny))py=ny;else ok=false;moving=ok;if(ok){int k=(int)Math.round(Math.atan2(dy,dx)/(Math.PI/4));k=((k%8)+8)%8;dir=MAP[k];anim+=dt;}else if(!holding)hasT=false;}else if(hasT&&!holding)hasT=false;
   if(talk>0){talk-=dt;bMoving=false;}else if(bwait>0){bwait-=dt;bMoving=false;}else{float ex=btx-bx,ey=bty-by,ed=(float)Math.hypot(ex,ey);if(ed<1.5f){bwait=1.5f+(float)Math.random()*3;pickBunny();bMoving=false;}else{float s=Math.min(ed,16*dt),nx=bx+ex/ed*s,ny=by+ey/ed*s;float qx=nx-px,qy=ny-py;if(walk(nx,ny)&&qx*qx+qy*qy>64){bx=nx;by=ny;bMoving=true;bAnim+=dt;}else{bwait=.6f;pickBunny();bMoving=false;}}}}
  void sh(Canvas c,int x,int y,int w){fill.setColor(0x33203040);c.drawRect(x-w/2+2,y-2,x+w/2-2,y-1,fill);c.drawRect(x-w/2,y-1,x+w/2,y+1,fill);c.drawRect(x-w/2+2,y+1,x+w/2-2,y+2,fill);}
  void drawDyn(Canvas c,int which){if(which==0){int fr=moving?1+(((int)(anim*8))&3):0;int bob=(fr==2||fr==4)?-1:0;int x=Math.round(px),y=Math.round(py);sh(c,x,y,10);c.drawBitmap(hero(dir,fr),x-11,y-29+bob,pix);}else{boolean up=bMoving&&((((int)(bAnim*6))&1)==1);int x=Math.round(bx),y=Math.round(by);sh(c,x,y,10);c.drawBitmap(up?bunnyB:bunnyA,x-9,y-23+(up?-1:0),pix);}}
  void drawThing(Canvas c,float[] o){int x=Math.round(o[0]),y=Math.round(o[1]);int t=(int)o[2];if(t<=1){sh(c,x,y,18);c.drawBitmap(t==1?fruit:tree,x-15,y-36,pix);}else if(t==2){sh(c,x,y,12);c.drawBitmap(bush,x-8,y-10,pix);}else{sh(c,x,y,12);c.drawBitmap(rock,x-7,y-8,pix);}}
  int tint(){java.time.LocalTime n=java.time.LocalTime.now();float t=n.getHour()+n.getMinute()/60f;if(t<5||t>=21)return 0x44000000|0x1B2A5E;if(t<7)return (((int)(68*(7-t)/2))<<24)|0x1B2A5E;if(t<17)return 0;if(t<19)return (((int)(30*(t-17)/2))<<24)|0xFF8A3D;return (((int)(30+38*(t-19)/2))<<24)|0x1B2A5E;}
  void target(float x,float y){tx=Math.max(2,Math.min(WW-2,x));ty=Math.max(2,Math.min(WH-2,y));hasT=true;}
  @Override public boolean onTouchEvent(MotionEvent e){int a=e.getActionMasked();float x=e.getX(),y=e.getY();float wx=cx0+x/scale,wy=cy0+y/scale;
   if(a==MotionEvent.ACTION_DOWN){closing=closeRect.contains(x,y);if(closing)return true;if(Math.abs(wx-bx)<9&&wy>by-24&&wy<by+3){line=lines[(int)(Math.random()*lines.length)];talk=3.5f;return true;}holding=true;target(wx,wy);}
   else if(a==MotionEvent.ACTION_MOVE&&holding)target(wx,wy);
   else if(a==MotionEvent.ACTION_UP||a==MotionEvent.ACTION_CANCEL){if(closing&&a==MotionEvent.ACTION_UP&&closeRect.contains(x,y))close.run();closing=false;holding=false;}return true;}
  @Override protected void onDetachedFromWindow(){running=false;super.onDetachedFromWindow();}
  @Override protected void onDraw(Canvas c){long now=SystemClock.uptimeMillis();float dt=Math.min(.05f,(now-last)/1000f);last=now;float t=(now-born)/1000f;int W=getWidth(),H=getHeight();if(W==0)return;step(dt);
   scale=Math.max(3,Math.round(W/140f));float vw=W/(float)scale,vh=H/(float)scale;cx0=Math.round(Math.max(0,Math.min(WW-vw,px-vw/2)));cy0=Math.round(Math.max(0,Math.min(WH-vh,py-vh/2)));
   c.drawColor(0xFF3E72C6);c.save();c.scale(scale,scale);c.translate(-cx0,-cy0);c.drawBitmap(world,0,0,pix);
   fill.setColor(0x99FFFFFF);for(float[] f:sparks){float ph=(t*1.1f+f[2])%3f;if(ph<.6f)c.drawRect(f[0],f[1],f[0]+2,f[1]+1,fill);}
   if(hasT){int r=((int)(t*6))%3;int x=Math.round(tx),y=Math.round(ty);fill.setColor(0xDDFFFFFF);c.drawRect(x-2-r,y-2-r,x-1-r,y-1-r,fill);c.drawRect(x+2+r,y-2-r,x+3+r,y-1-r,fill);c.drawRect(x-2-r,y+2+r,x-1-r,y+3+r,fill);c.drawRect(x+2+r,y+2+r,x+3+r,y+3+r,fill);}
   int first=py<=by?0:1;float y1=Math.min(py,by),y2=Math.max(py,by);boolean d1=false,d2=false;
   for(float[] o:things){if(!d1&&o[1]>y1){drawDyn(c,first);d1=true;}if(!d2&&o[1]>y2){drawDyn(c,1-first);d2=true;}drawThing(c,o);}if(!d1)drawDyn(c,first);if(!d2)drawDyn(c,1-first);
   for(float[] f:flies){int x=Math.round(f[0]+(float)Math.sin(t*.5f+f[2])*22),y=Math.round(f[1]+(float)Math.cos(t*.8f+f[2])*14);boolean flap=((((int)(t*9+f[2]*3)))&1)==0;fill.setColor(0xFF3A2A30);c.drawRect(x,y,x+1,y+2,fill);fill.setColor(flyCol[(int)f[3]%5]);if(flap){c.drawRect(x-2,y-1,x,y+1,fill);c.drawRect(x+1,y-1,x+3,y+1,fill);}else{c.drawRect(x-1,y,x,y+1,fill);c.drawRect(x+1,y,x+2,y+1,fill);}}
   c.restore();int ov=tint();if(ov!=0)c.drawColor(ov);
   closeRect.set(W-dens*60,dens*34,W-dens*12,dens*82);fill.setColor(0xCCFFFFFF);c.drawRoundRect(closeRect,dens*16,dens*16,fill);ink.setColor(0xFF6A5560);ink.setStrokeWidth(dens*3);ink.setStrokeCap(Paint.Cap.ROUND);float mx=closeRect.centerX(),my=closeRect.centerY(),q=dens*8;c.drawLine(mx-q,my-q,mx+q,my+q,ink);c.drawLine(mx+q,my-q,mx-q,my+q,ink);
   ink.setTextAlign(Paint.Align.CENTER);ink.setTextSize(dens*15);
   if(talk>0){float sx=(bx-cx0)*scale,sy=(by-26-cy0)*scale;float tw=ink.measureText(line)+dens*24;float l=Math.max(dens*8,Math.min(W-tw-dens*8,sx-tw/2));fill.setColor(0xF5FFFFFF);c.drawRoundRect(l,sy-dens*40,l+tw,sy-dens*6,dens*14,dens*14,fill);ink.setColor(0xFF6A5560);c.drawText(line,l+tw/2,sy-dens*18,ink);}
   if(t<7){int al=(int)(255*Math.min(1f,(7-t)/2f));String hint="Tap to walk \u00b7 hold to keep walking \u00b7 tap the bunny";float tw=ink.measureText(hint)+dens*28;fill.setColor((al*3/5)<<24);c.drawRoundRect(W/2f-tw/2,H-dens*96,W/2f+tw/2,H-dens*56,dens*16,dens*16,fill);ink.setColor((al<<24)|0xFFFFFF);c.drawText(hint,W/2f,H-dens*70,ink);}
   if(running)postInvalidateOnAnimation();}
 }
