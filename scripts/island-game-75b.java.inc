  Bitmap hole(boolean wet){int W=10,H=6;int[] b=new int[W*H];for(int y=0;y<H;y++)for(int x=0;x<W;x++){float u=(x-4.5f)/5f,v=(y-2.5f)/3f,d=u*u+v*v;if(d<=1)b[y*W+x]=d<.55f?(wet?0xFF3E2A1C:0xFF5E4029):(wet?0xFF7A5638:0xFF9A7048);}return fin(b,W,H,false);}
  Bitmap drop(){int W=9,H=11;int[] b=new int[W*H];for(int y=0;y<H;y++)for(int x=0;x<W;x++)if(circ(x,y,4,4,4))b[y*W+x]=0xFFFFFFFF;P(b,W,4,9,0xFFFFFFFF);P(b,W,4,2,0xFF3E8EDB);for(int y=3;y<6;y++)for(int x=3;x<6;x++)P(b,W,x,y,0xFF3E8EDB);return fin(b,W,H,true);}
  Bitmap bag(){int W=14,H=14;int[] b=new int[W*H];for(int y=5;y<13;y++)for(int x=2;x<12;x++)P(b,W,x,y,0xFFE59A59);for(int y=5;y<8;y++)for(int x=2;x<12;x++)P(b,W,x,y,0xFFD07F3E);for(int y=9;y<12;y++)for(int x=4;x<10;x++)P(b,W,x,y,0xFFD07F3E);P(b,W,6,7,0xFFFFE27A);P(b,W,7,7,0xFFFFE27A);int[][] h={{5,2},{6,2},{7,2},{8,2},{4,3},{4,4},{9,3},{9,4}};for(int[] q:h)P(b,W,q[0],q[1],0xFFB36A33);return fin(b,W,H,true);}
  Bitmap toolIcon(int t){int W=12,H=12;int[] b=new int[W*H];
   if(t==1){for(int i=0;i<7;i++)P(b,W,9-i,1+i,0xFFA9744B);P(b,W,9,0,0xFFA9744B);P(b,W,10,0,0xFFA9744B);for(int y=7;y<11;y++)for(int x=2;x<6;x++)P(b,W,x,y,0xFFC9C3CE);}
   else if(t==2){for(int y=1;y<11;y++)for(int x=3;x<9;x++)P(b,W,x,y,y<3?0xFFF29BB5:0xFFFFF1D6);P(b,W,5,5,0xFF4E9944);P(b,W,6,5,0xFF4E9944);P(b,W,5,6,0xFF72BE58);P(b,W,6,6,0xFF72BE58);P(b,W,5,8,0xFF8A5A3A);P(b,W,6,8,0xFF8A5A3A);}
   else{for(int y=5;y<11;y++)for(int x=2;x<9;x++)P(b,W,x,y,x==3?0xFF9CC8EE:0xFF6FA8DC);P(b,W,9,5,0xFF6FA8DC);P(b,W,10,4,0xFF6FA8DC);P(b,W,11,3,0xFF6FA8DC);for(int x=3;x<7;x++)P(b,W,x,3,0xFF6FA8DC);P(b,W,3,4,0xFF6FA8DC);P(b,W,6,4,0xFF6FA8DC);}
   return fin(b,W,H,true);}
  Plot plotAt(int cx,int cy){for(Plot p:plots)if(p.cx==cx&&p.cy==cy)return p;return null;}
  boolean validCell(int cx,int cy){if(cx<0||cy<0||cx>=WW/12||cy>=WH/12)return false;int x=cx*12+6,y=cy*12+6;if(tk(x,y)!=3||tk(cx*12,cy*12)!=3||tk(cx*12+11,cy*12)!=3||tk(cx*12,cy*12+11)!=3||tk(cx*12+11,cy*12+11)!=3)return false;for(float[] o:things){float dx=x-o[0],dy=y-o[1],r=o[3]+7;if(dx*dx+dy*dy<r*r)return false;}return true;}
  long dur(int crop){return fast?20000L:(crop<3?3L:6L)*3600000L;}
  void say(String s){toast=s;toastT=2.2f;}
  void burst(float x,float y,int col,int n){for(int i=0;i<n;i++){Part q=new Part();q.x=x;q.y=y-2;q.vx=((float)Math.random()-.5f)*40;q.vy=-((float)Math.random()*30+10);q.life=.6f;q.col=col;parts.add(q);}}
  void load(){try{JSONObject g=data.optJSONObject("game");if(g==null)return;JSONArray a=g.optJSONArray("plots");if(a!=null)for(int i=0;i<a.length();i++){JSONObject o=a.getJSONObject(i);Plot p=new Plot();p.cx=o.getInt("x");p.cy=o.getInt("y");p.crop=o.optInt("c",-1);p.stage=o.optInt("s",0);p.wet=o.optBoolean("w",false);p.readyAt=o.optLong("t",0);plots.add(p);}JSONArray v=g.optJSONArray("inv");if(v!=null)for(int i=0;i<5;i++)inv[i]=v.optInt(i);water=g.optInt("water",0);tool=g.optInt("tool",0);seed=Math.max(0,Math.min(4,g.optInt("seed",0)));fast=g.optBoolean("fast",false);if(g.has("px")){float x=(float)g.getDouble("px"),y=(float)g.getDouble("py");if(walk(x,y)){px=x;py=y;}}}catch(Exception ignored){}}
  void persist(){try{JSONObject g=new JSONObject();JSONArray a=new JSONArray();for(Plot p:plots){JSONObject o=new JSONObject();o.put("x",p.cx);o.put("y",p.cy);o.put("c",p.crop);o.put("s",p.stage);o.put("w",p.wet);o.put("t",p.readyAt);a.put(o);}g.put("plots",a);JSONArray v=new JSONArray();for(int n:inv)v.put(n);g.put("inv",v);g.put("water",water);g.put("tool",tool);g.put("seed",seed);g.put("fast",fast);g.put("px",px);g.put("py",py);data.put("game",g);save();}catch(Exception ignored){}}
  void leave(){running=false;persist();}
  void queue(int kind,int cx,int cy,float x,float y){pend=kind;pcx=cx;pcy=cy;ptx=x;pty=y;holding=false;holdWalk=false;target(x,y);}
  void tapWorld(float wx,float wy){holdWalk=false;pend=0;
   if(Math.abs(wx-bx)<9&&wy>by-24&&wy<by+3){line=lines[(int)(Math.random()*lines.length)];talk=3.5f;return;}
   int cx=(int)Math.floor(wx/12),cy=(int)Math.floor(wy/12);Plot p=plotAt(cx,cy);float mx=cx*12+6,my=cy*12+6;
   if(p!=null&&p.crop>=0&&p.stage==3){queue(1,cx,cy,mx,my);return;}
   if(tool==3){if(p!=null&&p.crop>=0&&p.stage<3){queue(2,cx,cy,mx,my);return;}int k=tk((int)wx,(int)wy);if(k==4||k<=1){for(int i=0;i<=40;i++){float f=i/40f,x=wx+(px-wx)*f,y=wy+(py-wy)*f;if(walk(x,y)){queue(5,cx,cy,x,y);return;}}}}
   if(tool==1&&p==null&&validCell(cx,cy)){queue(3,cx,cy,mx,my);return;}
   if(tool==2&&p!=null&&p.crop<0){queue(4,cx,cy,mx,my);return;}
   holdWalk=true;holding=true;target(wx,wy);}
  void perform(){Plot p=plotAt(pcx,pcy);float dx=ptx-px,dy=pty-py;if(dx*dx+dy*dy>1){int k=(int)Math.round(Math.atan2(dy,dx)/(Math.PI/4));k=((k%8)+8)%8;dir=MAP[k];}actT=.4f;float ax=ptx,ay=pty;long now=System.currentTimeMillis();
   if(pend==1&&p!=null&&p.crop>=0&&p.stage==3){inv[p.crop]++;say("+1 "+names[p.crop]);burst(ax,ay,0xFFFFE27A,10);p.crop=-1;p.stage=0;p.wet=false;persist();}
   else if(pend==2&&p!=null&&p.crop>=0&&p.stage<3){if(p.wet)say("Already watered");else if(water<=0)say("The can is empty - refill it at the pond");else{water--;p.wet=true;p.readyAt=now+dur(p.crop);burst(ax,ay,0xFF6FB6F0,12);say(water>0?"Watered":"Watered - the can is now empty");persist();}}
   else if(pend==3&&p==null&&validCell(pcx,pcy)){Plot n=new Plot();n.cx=pcx;n.cy=pcy;plots.add(n);burst(ax,ay,0xFF8A6244,10);persist();}
   else if(pend==4&&p!=null&&p.crop<0){p.crop=seed;p.stage=0;p.wet=false;burst(ax,ay,0xFFFFFFFF,6);say(names[seed]+" seed planted");persist();}
   else if(pend==5){water=10;burst(ax,ay,0xFF6FB6F0,10);say("Watering can filled");persist();}}
