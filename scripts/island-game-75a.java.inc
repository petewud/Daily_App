
 // A_DAY_TO_KEEP_ISLAND_75
 void openIsland75(){Dialog full=new Dialog(this,android.R.style.Theme_Material_Light_NoActionBar_Fullscreen);IslandGame75 game=new IslandGame75(()->full.dismiss());android.view.Window w=full.getWindow();if(w!=null){w.setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(0xFF3E72C6));w.setDecorFitsSystemWindows(false);w.setStatusBarColor(Color.TRANSPARENT);w.setNavigationBarColor(Color.TRANSPARENT);w.setNavigationBarContrastEnforced(false);w.setStatusBarContrastEnforced(false);WindowManager.LayoutParams lp=w.getAttributes();lp.layoutInDisplayCutoutMode=WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_ALWAYS;w.setAttributes(lp);}full.setContentView(game);full.setOnDismissListener(d->game.leave());full.show();if(w!=null)w.setLayout(-1,-1);}
 class IslandGame75 extends IslandDemo74 {
  class Plot{int cx,cy,crop=-1,stage;boolean wet;long readyAt;}
  class Part{float x,y,vx,vy,life;int col;}
  final java.util.ArrayList<Plot> plots=new java.util.ArrayList<>();final java.util.ArrayList<Part> parts=new java.util.ArrayList<>();
  final int[] inv=new int[5];final String[] names={"Tulip","Daisy","Sunflower","Carrot","Tomato"};
  final Bitmap[][] plantBmp=new Bitmap[5][4];Bitmap holeDry,holeWet,dropBmp,bagBmp;final Bitmap[] toolBmp=new Bitmap[4];
  final RectF bagRect=new RectF(),panelRect=new RectF(),fastRect=new RectF(),dest=new RectF();final RectF[] toolRect=new RectF[4],seedRect=new RectF[5];
  int tool,seed,water,pend,pcx,pcy,downBtn;float ptx,pty,actT,growT,toastT,insT,insB,insL,insR;boolean fast,panel,holdWalk;String toast="";
  IslandGame75(Runnable onClose){super(onClose);for(int i=0;i<4;i++)toolRect[i]=new RectF();for(int i=0;i<5;i++)seedRect[i]=new RectF();makeArt();load();}
  void P(int[] b,int w,int x,int y,int c){if(x>=0&&y>=0&&x<w&&y<b.length/w)b[y*w+x]=c;}
  Bitmap fin(int[] b,int W,int H,boolean outline){if(outline)edge(b,W,H);return Bitmap.createBitmap(b,W,H,Bitmap.Config.ARGB_8888);}
  void makeArt(){for(int c=0;c<5;c++)for(int s=0;s<4;s++)plantBmp[c][s]=plant(c,s);holeDry=hole(false);holeWet=hole(true);dropBmp=drop();bagBmp=bag();for(int i=1;i<4;i++)toolBmp[i]=toolIcon(i);}
  Bitmap plant(int crop,int stage){int W=12,H=16;int[] b=new int[W*H];int g=0xFF4E9944,gl=0xFF72BE58;int[] pet={0xFFF0607E,0xFFFFFFFF,0xFFFFD23C};int pc=crop<3?pet[crop]:0;
   if(stage==0){for(int x=5;x<8;x++){P(b,W,x,14,0xFF8A5A3A);P(b,W,x,15,0xFF6D4429);}}
   else if(stage==1){for(int y=10;y<16;y++)P(b,W,6,y,g);P(b,W,5,10,gl);P(b,W,4,9,gl);P(b,W,7,11,gl);P(b,W,8,10,gl);}
   else if(stage==2){for(int y=6;y<16;y++)P(b,W,6,y,g);P(b,W,5,11,gl);P(b,W,4,10,gl);P(b,W,3,10,gl);P(b,W,7,12,gl);P(b,W,8,11,gl);P(b,W,9,11,gl);if(crop<3){for(int y=4;y<7;y++)for(int x=5;x<8;x++)P(b,W,x,y,pc);}else if(crop==3){for(int x=4;x<9;x++)P(b,W,x,6,gl);P(b,W,3,7,gl);P(b,W,9,7,gl);}else{for(int x=4;x<9;x++)for(int y=7;y<12;y++)P(b,W,x,y,gl);}}
   else if(crop==0){for(int y=7;y<16;y++)P(b,W,6,y,g);P(b,W,4,12,gl);P(b,W,3,11,gl);P(b,W,8,12,gl);P(b,W,9,11,gl);for(int y=2;y<7;y++)for(int x=4;x<9;x++)P(b,W,x,y,pc);P(b,W,4,2,0);P(b,W,6,2,0);P(b,W,8,2,0);P(b,W,5,3,0xFFFF9AAE);}
   else if(crop==1){for(int y=5;y<16;y++)P(b,W,6,y,g);P(b,W,4,12,gl);P(b,W,3,11,gl);P(b,W,8,12,gl);P(b,W,9,11,gl);for(int dy=-3;dy<=3;dy++)for(int dx=-3;dx<=3;dx++)if(Math.abs(dx)+Math.abs(dy)<=3&&dx*dx+dy*dy<=6)P(b,W,6+dx,4+dy,0xFFFFFFFF);P(b,W,6,4,0xFFFFD23C);P(b,W,5,4,0xFFFFD23C);P(b,W,7,4,0xFFFFD23C);P(b,W,6,3,0xFFFFD23C);P(b,W,6,5,0xFFFFD23C);}
   else if(crop==2){for(int y=6;y<16;y++)P(b,W,6,y,g);P(b,W,4,12,gl);P(b,W,3,11,gl);P(b,W,8,12,gl);P(b,W,9,11,gl);for(int dy=-4;dy<=4;dy++)for(int dx=-4;dx<=4;dx++){int d=dx*dx+dy*dy;if(d<=14)P(b,W,6+dx,4+dy,d<=5?0xFF7A4B2A:0xFFFFD23C);}}
   else if(crop==3){P(b,W,3,5,gl);P(b,W,6,5,gl);P(b,W,9,5,gl);P(b,W,4,6,g);P(b,W,6,6,g);P(b,W,8,6,g);for(int y=7;y<10;y++)for(int x=5;x<8;x++)P(b,W,x,y,g);for(int x=4;x<9;x++)P(b,W,x,10,0xFFF08A2C);for(int x=5;x<8;x++){P(b,W,x,11,0xFFF08A2C);P(b,W,x,12,0xFFE07A22);}P(b,W,6,13,0xFFE07A22);}
   else{for(int y=5;y<14;y++)for(int x=2;x<10;x++)P(b,W,x,y,((x+y)&1)==0?gl:g);int[][] f={{3,8},{8,7},{5,11},{7,10},{4,6}};for(int[] q:f){P(b,W,q[0],q[1],0xFFFF8A7A);P(b,W,q[0]+1,q[1],0xFFE0453C);P(b,W,q[0],q[1]+1,0xFFE0453C);P(b,W,q[0]+1,q[1]+1,0xFFC03A33);}}
   return fin(b,W,H,stage>0);}
