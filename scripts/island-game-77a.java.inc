
 // A_DAY_TO_KEEP_ISLAND_77
 void openIsland77(){Dialog full=new Dialog(this,android.R.style.Theme_Material_Light_NoActionBar_Fullscreen);IslandGame77 game=new IslandGame77(()->full.dismiss());android.view.Window w=full.getWindow();if(w!=null){w.setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(0xFF3E72C6));w.setDecorFitsSystemWindows(false);w.setStatusBarColor(Color.TRANSPARENT);w.setNavigationBarColor(Color.TRANSPARENT);w.setNavigationBarContrastEnforced(false);w.setStatusBarContrastEnforced(false);WindowManager.LayoutParams lp=w.getAttributes();lp.layoutInDisplayCutoutMode=WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_ALWAYS;w.setAttributes(lp);}full.setContentView(game);full.setOnDismissListener(d->game.leave());full.show();if(w!=null)w.setLayout(-1,-1);}
 class IslandGame77 extends IslandGame76 {
  final int[] bug=new int[10],bugP={25,25,35,35,50,20,30,10,40,15};
  final String[] bname={"Rose Butterfly","Sunny Butterfly","Lilac Butterfly","Snowy Butterfly","Amber Butterfly","Ladybird","Stag Beetle","Ant","Snail","Pill Bug"};
  final Bitmap[] bugBmp=new Bitmap[10],sapBmp=new Bitmap[3];Bitmap dropPx,starPx,netBmp,bootBmp;
  final Paint silP=new Paint(),starP=new Paint();
  final java.util.ArrayList<float[]> crit=new java.util.ArrayList<>();
  final java.util.HashMap<Integer,Long> rockCd=new java.util.HashMap<>();
  final java.util.HashMap<Integer,long[]> saps=new java.util.HashMap<>();
  final java.util.ArrayList<Integer> ptrees=new java.util.ArrayList<>(),cleared=new java.util.ArrayList<>();
  final RectF chipRect=new RectF(),logBtn=new RectF(),logX=new RectF(),popRect=new RectF(),pMinus=new RectF(),pPlus=new RectF(),pMax=new RectF(),pOk=new RectF();
  final float[] FX={0,1,1,1,0,-1,-1,-1},FY={1,1,0,-1,-1,-1,0,1},DUR2={1f,.9f,.9f,1f,1.1f,.8f},HIT2={.5f,.5f,.55f,.5f,.5f,.5f};
  boolean haveNet,logOpen;int bugSeen,sapN,aMode,liftKey,pop,popType,popId,popQty,popMax,popPrice;
  IslandGame77(Runnable onClose){super(onClose);silP.setColorFilter(new android.graphics.PorterDuffColorFilter(0xFF4A4A5E,android.graphics.PorterDuff.Mode.SRC_IN));art77();load77();}
  void art77(){axeBmp=axeArt2();dropPx=dropArt();starPx=starArt();netBmp=netArt();bootBmp=bootArt();int[] fc={0xFFF29BB5,0xFFFFE27A,0xFFB79CE8,0xFFFFFFFF,0xFFF4A261};for(int i=0;i<5;i++)bugBmp[i]=bflyArt(fc[i]);bugBmp[5]=ladyArt();bugBmp[6]=beetleArt();bugBmp[7]=antArt();bugBmp[8]=snailArt();bugBmp[9]=pillArt();for(int i=0;i<3;i++)sapBmp[i]=sapArt(i);}
  Bitmap axeArt2(){int W=12,H=12;int[] b=new int[W*H];for(int i=0;i<8;i++)P(b,W,2+i,10-i,0xFFA9744B);int[][] hd={{8,1},{9,1},{10,1},{8,2},{9,2},{10,2},{11,2},{9,3},{10,3},{11,3},{11,4},{10,4}};for(int[] q:hd)P(b,W,q[0],q[1],q[0]>=11?0xFFE6E3EA:q[0]==8?0xFF8F8A99:0xFFB9B3C1);return fin(b,W,H,true);}
  Bitmap dropArt(){int W=7,H=8;int[] b=new int[W*H];int[][] rows={{3,3},{3,3},{2,4},{2,4},{1,5},{1,5},{1,5},{2,4}};for(int y=0;y<H;y++)for(int x=rows[y][0];x<=rows[y][1];x++)b[y*W+x]=0xFF4AA3EE;P(b,W,2,5,0xFFD6EEFF);P(b,W,2,6,0xFFD6EEFF);P(b,W,3,4,0xFF7CC4F8);return fin(b,W,H,true);}
  Bitmap starArt(){int W=7,H=7;int[] b=new int[W*H];for(int i=0;i<7;i++){int d=Math.abs(i-3);int c=d>=3?0xFFFFC94A:d==0?0xFFFFFFFF:0xFFFFF2B8;P(b,W,3,i,c);P(b,W,i,3,c);}P(b,W,2,2,0xFFFFF2B8);P(b,W,4,2,0xFFFFF2B8);P(b,W,2,4,0xFFFFF2B8);P(b,W,4,4,0xFFFFF2B8);return Bitmap.createBitmap(b,W,H,Bitmap.Config.ARGB_8888);}
  Bitmap netArt(){int W=12,H=12;int[] b=new int[W*H];for(int i=0;i<6;i++)P(b,W,2+i,10-i,0xFFA9744B);for(int y=0;y<7;y++)for(int x=5;x<12;x++){float dx=x-8.5f,dy=y-3f,d=(float)Math.sqrt(dx*dx+dy*dy);if(d<=3.4f)P(b,W,x,y,d>=2.4f?0xFFE6E3EA:0x80FFFFFF);}return fin(b,W,H,true);}
  Bitmap bootArt(){int W=4,H=3;int[] b=new int[W*H];for(int i=0;i<W*H;i++)b[i]=0xFF7A5238;return fin(b,W,H,true);}
  Bitmap bflyArt(int col){int W=9,H=7;int[] b=new int[W*H];for(int y=0;y<H;y++)for(int x=0;x<W;x++)if(circ(x,y,2,3,2)||circ(x,y,6,3,2))b[y*W+x]=col;for(int y=1;y<6;y++)b[y*W+4]=0xFF3A2A30;P(b,W,3,0,0xFF3A2A30);P(b,W,5,0,0xFF3A2A30);return fin(b,W,H,true);}
  Bitmap ladyArt(){int W=7,H=6;int[] b=new int[W*H];for(int y=1;y<6;y++)for(int x=0;x<7;x++)if(circ(x,y,3,3,3))b[y*W+x]=0xFFE0453C;P(b,W,2,0,0xFF3A2A30);P(b,W,3,0,0xFF3A2A30);P(b,W,4,0,0xFF3A2A30);for(int y=1;y<6;y++)P(b,W,3,y,0xFF3A2A30);P(b,W,1,3,0xFF3A2A30);P(b,W,5,3,0xFF3A2A30);P(b,W,2,4,0xFF3A2A30);return fin(b,W,H,true);}
  Bitmap beetleArt(){int W=9,H=8;int[] b=new int[W*H];for(int y=2;y<8;y++)for(int x=1;x<8;x++){float u=(x-4)/3.5f,v=(y-5)/3f;if(u*u+v*v<=1)b[y*W+x]=y<4?0xFF6FC2B8:0xFF3E8C8A;}for(int y=0;y<3;y++){P(b,W,2,y,0xFF5B3A29);P(b,W,6,y,0xFF5B3A29);}P(b,W,3,2,0xFF5B3A29);P(b,W,5,2,0xFF5B3A29);return fin(b,W,H,true);}
  Bitmap antArt(){int W=9,H=5;int[] b=new int[W*H];int c=0xFF4A3A3A;int[][] q={{1,2},{2,2},{4,2},{5,2},{7,2},{4,1},{4,3},{2,1},{2,3},{6,1},{6,3},{0,1}};for(int[] p:q)P(b,W,p[0],p[1],c);return fin(b,W,H,true);}
  Bitmap snailArt(){int W=10,H=9;int[] b=new int[W*H];for(int y=0;y<H;y++)for(int x=0;x<W;x++)if(circ(x,y,6,3,3))b[y*W+x]=circ(x,y,6,3,1)?0xFFA66B3A:0xFFD9A766;for(int x=0;x<10;x++)P(b,W,x,7,0xFFE8D9B8);for(int x=0;x<4;x++)P(b,W,x,6,0xFFE8D9B8);P(b,W,1,5,0xFFE8D9B8);P(b,W,1,4,0xFFE8D9B8);P(b,W,0,3,0xFF4A3A3A);P(b,W,2,3,0xFF4A3A3A);return fin(b,W,H,true);}
  Bitmap pillArt(){int W=9,H=6;int[] b=new int[W*H];for(int y=1;y<6;y++)for(int x=0;x<9;x++){float u=(x-4)/4.3f,v=(y-3)/2.4f;if(u*u+v*v<=1)b[y*W+x]=(x%3==0)?0xFF7C7A8C:0xFF9B99AC;}P(b,W,0,3,0xFF5A586A);return fin(b,W,H,true);}
  Bitmap sapArt(int st){int W=14,H=18;int[] b=new int[W*H];int g=0xFF4E9944,gl=0xFF72BE58,br=0xFF8A5A3A;
   if(st==0){for(int y=14;y<18;y++)for(int x=4;x<10;x++)if(circ(x,y,7,17,3))P(b,W,x,y,0xFF8A6244);P(b,W,7,13,g);P(b,W,7,12,g);P(b,W,6,12,gl);P(b,W,8,11,gl);P(b,W,6,11,gl);}
   else if(st==1){for(int y=8;y<18;y++)P(b,W,7,y,br);P(b,W,6,9,gl);P(b,W,5,8,gl);P(b,W,8,10,gl);P(b,W,9,9,gl);P(b,W,6,12,gl);P(b,W,8,13,gl);P(b,W,7,7,gl);P(b,W,6,7,g);P(b,W,8,7,g);}
   else{for(int y=9;y<18;y++){P(b,W,6,y,br);P(b,W,7,y,0xFF6D4429);}for(int y=0;y<12;y++)for(int x=0;x<W;x++)if(circ(x,y,7,6,5)){float l=(x-7)*.6f+(y-6)*.8f;P(b,W,x,y,l<-2?0xFF92D870:l<2?0xFF6DBA55:0xFF4E9944);}}
   return fin(b,W,H,true);}
  float[] anyThing(int k){for(float[] o:things){int t=(int)o[2];if((t<=1||t==5||t==11)&&tkey(o)==k)return o;}return null;}
  void sortThings(){java.util.Collections.sort(things,(u,v)->Float.compare(u[1],v[1]));}
  void load77(){JSONObject g=data.optJSONObject("game");
   if(g!=null){try{haveNet=g.optBoolean("net",false);sapN=g.optInt("sapN",0);bugSeen=g.optInt("bugSeen",0);JSONArray b=g.optJSONArray("bug");if(b!=null)for(int i=0;i<10;i++)bug[i]=b.optInt(i);JSONArray cl=g.optJSONArray("cleared");if(cl!=null)for(int i=0;i<cl.length();i++)cleared.add(cl.getInt(i));JSONArray pt=g.optJSONArray("ptrees");if(pt!=null)for(int i=0;i<pt.length();i++)ptrees.add(pt.getInt(i));JSONArray sp=g.optJSONArray("saps");if(sp!=null)for(int i=0;i<sp.length();i++){JSONArray r=sp.getJSONArray(i);saps.put(r.getInt(0),new long[]{r.getLong(1),r.getLong(2),r.getLong(3)});}}catch(Exception ignored){}}
   for(int k:cleared){float[] o=anyThing(k);if(o!=null)things.remove(o);}
   for(int k:ptrees)if(anyThing(k)==null)things.add(new float[]{k/1000,k%1000,0,4});
   for(java.util.Map.Entry<Integer,long[]> e:saps.entrySet())if(anyThing(e.getKey())==null)things.add(new float[]{e.getKey()/1000,e.getKey()%1000,11,3});
   sortThings();
   for(java.util.Map.Entry<Integer,long[]> e:ts.entrySet()){float[] o=treeByKey(e.getKey());if(o!=null){if(e.getValue()[0]==1){o[2]=5;o[3]=2;}else o[2]=0;}}
   if(tool==5&&sapN<=0)tool=0;if(tool==6&&!haveNet)tool=0;}
  @Override void persist(){persist76();try{JSONObject g=data.optJSONObject("game");if(g==null)return;g.put("net",haveNet);g.put("sapN",sapN);g.put("bugSeen",bugSeen);JSONArray b=new JSONArray();for(int n:bug)b.put(n);g.put("bug",b);JSONArray sp=new JSONArray();for(java.util.Map.Entry<Integer,long[]> e:saps.entrySet()){JSONArray r=new JSONArray();r.put(e.getKey().intValue());r.put(e.getValue()[0]);r.put(e.getValue()[1]);r.put(e.getValue()[2]);sp.put(r);}g.put("saps",sp);JSONArray pt=new JSONArray();for(int k:ptrees)pt.put(k);g.put("ptrees",pt);JSONArray cl=new JSONArray();for(int k:cleared)cl.put(k);g.put("cleared",cl);save();}catch(Exception ignored){}}
