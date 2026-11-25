 // A_DAY_TO_KEEP_NOTES_WIDGET_733
 class NotesScroll733 extends ScrollView {
  NotesThumb733 thumb;
  NotesScroll733(){super(MainActivity.this);}
  @Override protected void onScrollChanged(int l,int t,int oldl,int oldt){super.onScrollChanged(l,t,oldl,oldt);if(thumb!=null)thumb.invalidate();}
  @Override protected void onLayout(boolean changed,int l,int t,int r,int b){super.onLayout(changed,l,t,r,b);if(thumb!=null)thumb.invalidate();}
 }
 class NotesThumb733 extends View {
  final NotesScroll733 scroll;final Paint pen=new Paint(Paint.ANTI_ALIAS_FLAG);
  NotesThumb733(NotesScroll733 value){super(MainActivity.this);scroll=value;scroll.thumb=this;setClickable(false);setFocusable(false);setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_NO);}
  @Override protected void onDraw(Canvas canvas){super.onDraw(canvas);if(!scroll.isVerticalScrollBarEnabled()||scroll.getChildCount()==0||getHeight()<=0)return;int extent=scroll.getHeight()-scroll.getPaddingTop()-scroll.getPaddingBottom(),range=scroll.getChildAt(0).getHeight();if(extent<=0||range<=extent)return;float height=Math.min(getHeight(),Math.max(dp(22),getHeight()*extent/(float)range));float fraction=Math.max(0,Math.min(1,scroll.getScrollY()/(float)(range-extent)));float top=(getHeight()-height)*fraction;pen.setColor(blend(LILAC,INK,.30f));canvas.drawRoundRect(0,top,getWidth(),top+height,dp(3),dp(3),pen);}
 }
