#!/usr/bin/env python3
"""6.2: bounded schedule viewport, collision-safe stronger motion and circular widget."""
from pathlib import Path
import re,xml.etree.ElementTree as ET
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text(encoding='utf-8')
if '// A_DAY_TO_KEEP_WRITING_FIX_61' not in s:raise SystemExit('Run the working version 6 and fix_writing.py before update_round.py.')
MARK='// A_DAY_TO_KEEP_ROUND_62'
def bounds(text,signature):
 a=text.find(signature)
 if a<0:raise RuntimeError('Source section missing: '+signature)
 start=text.find('{',a);i=start+1;depth=1;state='code'
 while i<len(text) and depth:
  c=text[i];pair=text[i:i+2]
  if state=='line':
   if c=='\n':state='code'
  elif state=='comment':
   if pair=='*/':state='code';i+=1
  elif state in ('"',"'"):
   if c=='\\':i+=1
   elif c==state:state='code'
  else:
   if pair=='//':state='line';i+=1
   elif pair=='/*':state='comment';i+=1
   elif c in ('"',"'"):state=c
   elif c=='{':depth+=1
   elif c=='}':depth-=1
  i+=1
 if depth:raise RuntimeError('Unbalanced Java section: '+signature)
 return a,i

def replace(signature,replacement):
 global s
 a,b=bounds(s,signature);s=s[:a]+replacement+s[b:]
def edit(signature,fn):
 global s
 a,b=bounds(s,signature);s=s[:a]+fn(s[a:b])+s[b:]
if MARK not in s:
 # This previously rebuilt every day card every 30 seconds, even on the same date.
 old=re.search(r'final Runnable midnight\s*=\s*new Runnable\(\)\s*\{',s)
 if not old:raise RuntimeError('Daily refresh runnable missing')
 a,b=bounds(s,old.group(0))
 end=b
 while end<len(s) and s[end].isspace():end+=1
 if end>=len(s) or s[end]!=';':raise RuntimeError('Daily refresh runnable terminator missing')
 s=s[:a]+r"""final Runnable midnight=new Runnable(){public void run(){if(data==null)return;String previous=data.optString("lastDay","");String today=LocalDate.now().toString();resetDaily();if(screen.equals("home")&&!today.equals(previous))home();handler.postDelayed(this,30000);}};"""+s[end+1:]
 def home_change(t):
  expected='work.addView(strip,new LinearLayout.LayoutParams(-1,dp(87)));'
  if expected not in t:raise RuntimeError('Expected schedule strip insertion missing')
  t=t.replace(expected,'ScheduleViewport scheduleViewport=new ScheduleViewport();scheduleViewport.addView(strip,new FrameLayout.LayoutParams(-1,-1));work.addView(scheduleViewport,new LinearLayout.LayoutParams(-1,dp(87)));',1)
  t=t.replace('strip.setClipChildren(true);','strip.setClipChildren(true);strip.setHorizontalFadingEdgeEnabled(false);',1)
  return t
 edit('void home(){',home_change)
 insert=r"""
 // A_DAY_TO_KEEP_ROUND_62
 class ScheduleViewport extends FrameLayout {
  ScheduleViewport(){super(MainActivity.this);setClipChildren(true);setClipToPadding(true);setPadding(0,0,0,0);setLayerType(View.LAYER_TYPE_NONE,null);}
  @Override protected void dispatchDraw(Canvas canvas){int save=canvas.save();canvas.clipRect(0,0,getWidth(),getHeight());super.dispatchDraw(canvas);canvas.restoreToCount(save);}
 }
 static class MotionSticker {float cx,cy,size,radius,offset,tilt;String name;}
 final LinkedHashMap<String,ArrayList<MotionSticker>> scatterCache=new LinkedHashMap<String,ArrayList<MotionSticker>>(32,.75f,true){@Override protected boolean removeEldestEntry(Map.Entry<String,ArrayList<MotionSticker>> entry){return size()>32;}};
 ArrayList<MotionSticker> packedStickers(Rect b,int index,int seed,boolean panel){String key=b.width()+":"+b.height()+":"+index+":"+seed+":"+panel;ArrayList<MotionSticker> cached=scatterCache.get(key);if(cached!=null)return cached;ArrayList<MotionSticker> placed=new ArrayList<>();Random random=new Random(seed);String[] names=motifs(index);float area=b.width()/(float)dp(90)*b.height()/dp(90);int target=Math.max(3,Math.min(panel?26:60,(int)(area*(panel?1.35f:1.0f))));int tries=0;
  while(placed.size()<target&&tries++<2400){MotionSticker item=new MotionSticker();item.size=dp((panel?18:23)+random.nextInt(panel?12:13));
   // Reserve the circumscribed painted area at maximum scale, plus the COMPLETE
   // translation envelope and a visible gap. Thus future frames cannot collide.
   item.radius=item.size*.95f+dp(17);float edge=item.radius+dp(2);if(b.width()<=edge*2||b.height()<=edge*2)continue;item.cx=edge+random.nextFloat()*(b.width()-edge*2);item.cy=edge+random.nextFloat()*(b.height()-edge*2);boolean clear=true;for(MotionSticker other:placed){float dx=item.cx-other.cx,dy=item.cy-other.cy,minimum=item.radius+other.radius+dp(4);if(dx*dx+dy*dy<minimum*minimum){clear=false;break;}}if(!clear)continue;item.offset=random.nextFloat()*(float)Math.PI*2;item.tilt=random.nextFloat()*36-18;item.name=names[random.nextInt(names.length)];placed.add(item);
  }scatterCache.put(key,placed);return placed;
 }
 """
 anchor=' JSONObject data;'
 if anchor not in s:raise RuntimeError('Activity field anchor missing')
 s=s.replace(anchor,insert+'\n'+anchor,1)
 replace('void drawScattered(Canvas c,Rect b,int index,int seed,boolean panel,boolean animate){',r"""void drawScattered(Canvas c,Rect b,int index,int seed,boolean panel,boolean animate){if(b.width()<=0||b.height()<=0)return;ArrayList<MotionSticker> items=packedStickers(b,index,seed,panel);StickerPainter painter=new StickerPainter();float phase=animate?(float)((SystemClock.uptimeMillis()%36000L)*(Math.PI*2/36000.0)):0;for(MotionSticker item:items){float cx=b.left+item.cx,cy=b.top+item.cy,angle=item.tilt,scale=1;if(animate){cx+=(float)Math.sin(phase*2+item.offset)*dp(7);cy+=(float)Math.cos(phase*3+item.offset)*dp(9);angle+=(float)Math.sin(phase+item.offset)*14;scale=1+(float)Math.sin(phase*2+item.offset)*.12f;}int save=c.save();c.rotate(angle,cx,cy);c.scale(scale,scale,cx,cy);painter.draw(c,item.name,cx-item.size/2,cy-item.size/2,item.size,panel?84:90);c.restoreToCount(save);}}""")
 replace('float phase(){','float phase(){return motionEnabled()?(float)((SystemClock.uptimeMillis()%36000L)*(Math.PI*2.0/36000.0)):0;}')
 # Keep the same mascot artwork, but omit its disk/badge when rendering the compact widget.
 def mascot_change(t):
  expected='String animal;int accent;Paint p=new Paint(3);'
  if expected not in t:raise RuntimeError('Mascot field declaration missing')
  t=t.replace(expected,'String animal;int accent;boolean faceOnly=false;Paint p=new Paint(3);',1)
  t=t.replace('fill(accent);c.drawCircle(50,51,43,p);','fill(accent);if(!faceOnly)c.drawCircle(50,51,43,p);',1)
  badge='new StickerPainter().draw(c,motifs(characterIndex(animal))[0],70,71,25,255);'
  if badge not in t:raise RuntimeError('Mascot badge drawing missing')
  t=t.replace(badge,'if(!faceOnly)'+badge,1)
  t=t.replace('Math.sin(phase())*3','Math.sin(phase())*5').replace('Math.sin(phase()*2)*.025f','Math.sin(phase()*2)*.045f').replace('Math.sin(phase()*2)*2.8f','Math.sin(phase()*2)*4.5f')
  return t
 edit('class Mascot extends AnimatedArt {',mascot_change)
 edit('void refreshWidgetSnapshot(){',lambda t:t.replace('Mascot mascot=new Mascot(t.character,t.pink);','Mascot mascot=new Mascot(t.character,t.pink);mascot.faceOnly=true;',1))
 s=s.replace('Version 6.1','Version 6.2').replace('Version 6.0','Version 6.2')
 p.write_text(s,encoding='utf-8')
# The rest of this script regenerates the small widget resources, safely on repeat runs.

widget_update='static void update(Context context,AppWidgetManager manager,int id){try{\n JSONObject data=read(context,"data.json"),skin=read(context,"widget-skin.json");JSONArray tasks=data.optJSONArray("tasks");LocalDate today=LocalDate.now();int total=0,completed=0;boolean auto=data.optBoolean("resetDaily",true);\n if(tasks!=null)for(int i=0;i<tasks.length();i++){JSONObject task=tasks.optJSONObject(i);if(task==null)continue;boolean due=true;try{LocalDate anchor=LocalDate.parse(task.optString("createdOn",today.toString()));long days=ChronoUnit.DAYS.between(anchor,today);due=days>=0&&days%Math.max(1,task.optInt("repeat",1))==0;}catch(Exception ignored){}if(!due)continue;total++;boolean done=task.optBoolean("done");if(auto&&!today.toString().equals(task.optString("completedOn")))done=false;if(done)completed++;}\n int ink=skin.optInt("ink",0xFF75576C),pink=skin.optInt("pink",0xFFF7DCE4),mint=skin.optInt("mint",0xFFDDEDDC),cream=skin.optInt("cream",0xFFFFF5F0);\n final int size=256;Bitmap card=Bitmap.createBitmap(size,size,Bitmap.Config.ARGB_8888);Canvas c=new Canvas(card);Paint p=new Paint(Paint.ANTI_ALIAS_FLAG|Paint.FILTER_BITMAP_FLAG);float center=128,radius=116;\n p.setColor(cream);c.drawCircle(center,center,104,p);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(13);p.setStrokeCap(Paint.Cap.ROUND);p.setColor(pink);c.drawCircle(center,center,radius,p);\n int progress=Color.rgb((Color.red(mint)*2+Color.red(ink))/3,(Color.green(mint)*2+Color.green(ink))/3,(Color.blue(mint)*2+Color.blue(ink))/3);\n if(total>0&&completed>0){p.setColor(progress);c.drawArc(new RectF(center-radius,center-radius,center+radius,center+radius),-90,360f*completed/total,false,p);}p.setStyle(Paint.Style.FILL);\n int clipped=c.save();Path circle=new Path();circle.addCircle(center,center,102,Path.Direction.CW);c.clipPath(circle);Bitmap character=BitmapFactory.decodeFile(new File(context.getFilesDir(),"widget-character.png").toString());if(character!=null){c.drawBitmap(character,null,new RectF(32,26,224,218),p);character.recycle();}else{android.graphics.drawable.Drawable preview=context.getDrawable(R.drawable.launcher_foreground);if(preview!=null){preview.setBounds(26,26,230,230);preview.draw(c);}}c.restoreToCount(clipped);\n String status=total==0?"No tasks scheduled today":completed+" of "+total+" tasks complete today";RemoteViews views=new RemoteViews(context.getPackageName(),R.layout.keep_widget);views.setImageViewBitmap(R.id.widget_card,card);views.setContentDescription(R.id.widget_card,"A Day To Keep. "+status+". Tap to open your checklist.");Intent open=new Intent(context,MainActivity.class).putExtra("fromWidget",true).addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP|Intent.FLAG_ACTIVITY_SINGLE_TOP);PendingIntent tap=PendingIntent.getActivity(context,701,open,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);views.setOnClickPendingIntent(R.id.widget_card,tap);manager.updateAppWidget(id,views);\n }catch(Exception|OutOfMemoryError e){android.util.Log.w("ADayToKeep","Could not render round checklist widget",e);}}\n'
widget=Path('app/src/main/java/uk/co/littledays/KeepWidget.java')
text=widget.read_text(encoding='utf-8')
a,b=bounds(text,'static void update(Context context,AppWidgetManager manager,int id){')
widget.write_text(text[:a]+widget_update.rstrip()+text[b:],encoding='utf-8')
def resource(relative,text):
 target=Path('app/src/main/res')/relative
 target.parent.mkdir(parents=True,exist_ok=True)
 ET.fromstring(text)
 target.write_text(text,encoding='utf-8')
resource('layout/keep_widget.xml','<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android" android:layout_width="match_parent" android:layout_height="match_parent" android:padding="0dp"><ImageView android:id="@+id/widget_card" android:layout_width="match_parent" android:layout_height="match_parent" android:scaleType="fitCenter" android:adjustViewBounds="false" android:contentDescription="A Day To Keep circular checklist progress" android:src="@drawable/widget_round_preview"/></FrameLayout>')
resource('xml/keep_widget_info.xml','<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android" android:minWidth="40dp" android:minHeight="40dp" android:minResizeWidth="40dp" android:minResizeHeight="40dp" android:targetCellWidth="1" android:targetCellHeight="1" android:initialLayout="@layout/keep_widget" android:previewLayout="@layout/keep_widget" android:previewImage="@drawable/widget_round_preview" android:updatePeriodMillis="1800000" android:resizeMode="horizontal|vertical" android:widgetCategory="home_screen" android:description="@string/widget_description"/>')
resource('drawable/widget_round_preview.xml','<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108"><path android:fillColor="#FFF5F0" android:pathData="M54,11a43,43 0,1 0,0.1,0Z"/><path android:fillColor="#00000000" android:strokeColor="#F0CCDA" android:strokeWidth="6" android:pathData="M54,5a49,49 0,1 0,0.1,0Z"/><path android:fillColor="#00000000" android:strokeColor="#95B6A0" android:strokeLineCap="round" android:strokeWidth="6" android:pathData="M54,5A49,49 0,0 1,103,54"/><path android:fillColor="#FFFDFA" android:strokeColor="#927E98" android:strokeWidth="1.5" android:pathData="M33,49C24,22 38,17 44,42C50,39 58,39 64,42C70,17 84,22 75,49C94,80 14,80 33,49Z"/><path android:fillColor="#927E98" android:pathData="M42,55a2,2 0,1 0,0.1,0M64,55a2,2 0,1 0,0.1,0M51,60L57,60L54,64Z"/><path android:fillColor="#EDA8B6" android:pathData="M32,62a5,3 0,1 0,10,0a5,3 0,1 0,-10,0M66,62a5,3 0,1 0,10,0a5,3 0,1 0,-10,0"/></vector>')
resource('values/widget_strings.xml','<resources><string name="widget_description">Your theme character with a circular progress ring for today’s checklist.</string></resources>')

gradle=Path('app/build.gradle');g=gradle.read_text();g=re.sub(r'versionCode\s+\d+','versionCode 8',g);g=re.sub(r'versionName\s+[\'\"][^\'\"]+[\'\"]','versionName "6.2"',g);gradle.write_text(g)
Path('VERSION-6.2-NOTES.txt').write_text("""A Day To Keep 6.2
Schedule: explicit bounded viewport aligned to the title control; 30-second day checks
no longer recreate the home screen when the date is unchanged. Midnight/date changes
still reset and redraw due tasks. Normal user navigation can still rebuild Home.
Artwork: seeded, cached rejection-sampled positions with non-overlapping reserved disks.
The reserved disks cover maximum scale, arbitrary rotation, complete translation range
and a visible gap, not just starting positions. Tight spaces contain fewer illustrations.
Movement raised from 4/5dp to 7/9dp, rotation from 9 to 14 degrees, breathing to 12 percent,
and loop period shortened to 36 seconds. All motion remains seamless and optional.
Widget: 1x1 target cell, theme character without disk/badge and a circular checklist-progress
ring; no visible title/count text. Content description retains accessibility information.
fitCenter preserves the circle on rectangular cell allocations. Android/launcher controls
actual cell dimensions. Remove the older wide widget and add the widget again for 1x1.
Open the updated app once so the new mascot snapshot is generated. Widget does not animate.
Previous writing-mode repair, schedule, recurrence, backups and PDF attachment features
remain in place. Signing/application ID preserved. Save an app-data backup before updating.
Generated with static checks, not an Android compile; CI and device testing still needed.
""",encoding='utf-8')
print('Version 6.2 schedule clipping, collision-safe animation and 1x1 radial widget prepared.')
