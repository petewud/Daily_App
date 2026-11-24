#!/usr/bin/env python3
"""6.3 preferences, contrast, schedule symbols, viewer controls and two widgets."""
from pathlib import Path
import re,xml.etree.ElementTree as ET
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text(encoding='utf-8')
if '// A_DAY_TO_KEEP_ROUND_62' not in s:raise SystemExit('Prepare the working version 6.2 source first.')
MARK='// A_DAY_TO_KEEP_PREFERENCES_63'
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

def replace(signature,new):
 global s
 a,b=bounds(s,signature);s=s[:a]+new+s[b:]
def edit(signature,fn):
 global s
 a,b=bounds(s,signature);s=s[:a]+fn(s[a:b])+s[b:]
if MARK not in s:
 helpers=r"""
 // A_DAY_TO_KEEP_PREFERENCES_63
 boolean restoringThemeSession=false,externalPicker=false,skipThemeStart=false;
 void wirePress(View button){button.setOnTouchListener((view,event)->{boolean enabled=data!=null&&data.optBoolean("buttonPress",true)&&android.animation.ValueAnimator.areAnimatorsEnabled();int action=event.getActionMasked();if(!enabled){view.animate().cancel();view.setScaleX(1);view.setScaleY(1);return false;}if(action==MotionEvent.ACTION_DOWN){view.animate().cancel();view.animate().scaleX(.955f).scaleY(.955f).setDuration(75).start();}else if(action==MotionEvent.ACTION_UP||action==MotionEvent.ACTION_CANCEL||(action==MotionEvent.ACTION_MOVE&&(event.getX()<0||event.getY()<0||event.getX()>view.getWidth()||event.getY()>view.getHeight()))){view.animate().cancel();view.animate().scaleX(1).scaleY(1).setDuration(110).start();}return false;});}
 void wireNativeButtons(View view){if(view instanceof Button)wirePress(view);if(view instanceof ViewGroup){ViewGroup group=(ViewGroup)view;for(int i=0;i<group.getChildCount();i++)wireNativeButtons(group.getChildAt(i));}}
 boolean applyThemePolicy(boolean opening){if(data==null)return false;String mode=data.optString("themeMode","manual"),today=LocalDate.now().toString();boolean choose=(mode.equals("daily")&&!today.equals(data.optString("themeDay")))||(mode.equals("eachUse")&&opening);if(!choose)return false;int current=Math.max(0,Math.min(themes.length-1,data.optInt("theme",0)));int selected=current;if(themes.length>1){selected=new Random().nextInt(themes.length-1);if(selected>=current)selected++;}try{data.put("theme",selected);data.put("themeDay",today);save();return selected!=current;}catch(Exception error){android.util.Log.w("ADayToKeep","Could not change theme",error);return false;}}
 @Override protected void onStart(){super.onStart();if(data==null||startupFault)return;if(restoringThemeSession){restoringThemeSession=false;return;}if(externalPicker||skipThemeStart){skipThemeStart=false;return;}if(applyThemePolicy(true)){try{applyTheme();render();}catch(RuntimeException error){startupProblem(error);}}}
 @Override public void startActivityForResult(Intent intent,int requestCode){externalPicker=true;super.startActivityForResult(intent,requestCode);}
 int scheduleColor(String status){if(status.equals("work"))return blend(0xFFBED5F1,LILAC,.055f);if(status.equals("off"))return blend(0xFFF1C5B1,PINK,.045f);if(status.equals("holiday"))return blend(0xFFF6E7A9,MINT,.035f);return WHITE;}
 boolean drawScheduleSymbol(Canvas canvas,String kind,int width,int height){if(!kind.equals("work")&&!kind.equals("off")&&!kind.equals("holiday"))return false;int save=canvas.save();canvas.scale(width/40f,height/40f);Paint p=new Paint(3);int outline=0xFF6E6577;
  if(kind.equals("work")){p.setColor(0xFF779BC6);canvas.drawRoundRect(7,9,33,36,4,4,p);p.setColor(0xFFBFD5EE);canvas.drawRoundRect(10,17,30,35,2,2,p);p.setColor(Color.WHITE);canvas.drawRoundRect(15,4,25,15,3,3,p);p.setColor(0xFFD48F9B);canvas.drawRect(18.5f,6,21.5f,13,p);canvas.drawRect(16.5f,8,23.5f,11,p);p.setColor(Color.WHITE);for(int y=20;y<=26;y+=6)for(int x=13;x<=25;x+=6)canvas.drawRoundRect(x,y,x+3,y+3,1,1,p);p.setColor(0xFF617EA3);canvas.drawRoundRect(17,29,23,36,1,1,p);}
  else if(kind.equals("off")){p.setColor(0xFFBF8E7D);canvas.drawRoundRect(7,10,33,26,6,6,p);p.setColor(0xFFECC4B4);canvas.drawRoundRect(10,13,30,26,4,4,p);p.setColor(0xFFBF8E7D);canvas.drawRoundRect(3,20,37,33,4,4,p);p.setColor(0xFFF4D7C7);canvas.drawRoundRect(9,22,31,29,3,3,p);p.setColor(outline);canvas.drawRoundRect(8,32,12,36,1,1,p);canvas.drawRoundRect(28,32,32,36,1,1,p);p.setStrokeWidth(1.5f);canvas.drawLine(20,23,20,28,p);}
  else {p.setColor(0xFFD3A94F);p.setStrokeWidth(2.6f);p.setStrokeCap(Paint.Cap.ROUND);for(int i=0;i<8;i++){double angle=i*Math.PI/4;canvas.drawLine(20+(float)Math.cos(angle)*13,20+(float)Math.sin(angle)*13,20+(float)Math.cos(angle)*17,20+(float)Math.sin(angle)*17,p);}p.setColor(0xFFF4CF79);canvas.drawCircle(20,20,10,p);p.setColor(0xFF967545);canvas.drawCircle(17,19,1.1f,p);canvas.drawCircle(23,19,1.1f,p);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(1.4f);canvas.drawArc(17,20,23,25,0,180,false,p);}
  canvas.restoreToCount(save);return true;}
 class ActionGlyph extends View {String kind;Paint p=new Paint(3);ActionGlyph(String k){super(MainActivity.this);kind=k;}protected void onDraw(Canvas c){c.save();c.scale(getWidth()/40f,getHeight()/40f);p.setColor(INK);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2.8f);p.setStrokeCap(Paint.Cap.ROUND);if(kind.equals("close")){c.drawLine(11,11,29,29,p);c.drawLine(29,11,11,29,p);}else{c.drawRoundRect(11,13,29,33,3,3,p);c.drawLine(8,10,32,10,p);c.drawRoundRect(16,6,24,10,2,2,p);c.drawLine(17,18,17,28,p);c.drawLine(23,18,23,28,p);}c.restore();}}
 View glyphButton(String description,String icon,int color,Runnable action){FrameLayout button=new FrameLayout(this);button.setBackground(shape(color));button.setContentDescription(description);button.setMinimumHeight(dp(52));button.setMinimumWidth(dp(52));ActionGlyph glyph=new ActionGlyph(icon);FrameLayout.LayoutParams gp=new FrameLayout.LayoutParams(dp(31),dp(31),Gravity.CENTER);button.addView(glyph,gp);button.setOnClickListener(v->{chime(softSound);action.run();});wirePress(button);return button;}
 View themeDropdown(){LinearLayout row=row();row.setPadding(dp(10),dp(9),dp(12),dp(9));row.setBackground(shape(WHITE));row.addView(new Mascot(theme.character,PINK),new LinearLayout.LayoutParams(dp(51),dp(53)));LinearLayout words=col();words.setPadding(dp(10),0,dp(6),0);words.addView(text("Current theme",12));words.addView(label(theme.name,20));row.addView(words,new LinearLayout.LayoutParams(0,-2,1));TextView arrow=label("⌄",25);row.addView(arrow);row.setContentDescription("Choose theme");row.setOnClickListener(v->showThemeMenu(row));wirePress(row);return row;}
 void showThemeMenu(View anchor){ScrollView scroll=new ScrollView(this);scroll.setPadding(dp(7),dp(7),dp(7),dp(7));scroll.setClipToPadding(true);LinearLayout choices=col();scroll.addView(choices);int width=Math.max(dp(240),anchor.getWidth());int height=Math.min(dp(430),(int)(getResources().getDisplayMetrics().heightPixels*.58f));PopupWindow popup=new PopupWindow(scroll,width,height,true);popup.setBackgroundDrawable(shape(CREAM));popup.setElevation(dp(7));popup.setOutsideTouchable(true);View selectedRow=null;
  for(int i=0;i<themes.length;i++){final int index=i;ThemeSpec t=themes[i];LinearLayout preview=row();preview.setPadding(dp(9),dp(8),dp(9),dp(8));GradientDrawable border=shape(Color.TRANSPARENT);border.setStroke(dp(i==themeIndex?3:1),i==themeIndex?t.ink:blend(t.cream,t.ink,.15f));preview.setBackground(new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{new Pattern(t,i),border}));preview.addView(new Mascot(t.character,t.pink),new LinearLayout.LayoutParams(dp(48),dp(52)));LinearLayout copy=col();copy.setPadding(dp(9),0,0,0);TextView name=label(t.name+(i==themeIndex?" · Selected":""),18);name.setTextColor(t.ink);try{name.setTypeface(Typeface.createFromAsset(getAssets(),"fonts/"+t.heading+".ttf"));}catch(Exception ignored){}copy.addView(name);TextView description=text(t.description,11);description.setTextColor(t.ink);copy.addView(description);preview.addView(copy,new LinearLayout.LayoutParams(0,-2,1));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(dp(2),dp(3),dp(2),dp(4));choices.addView(preview,lp);preview.setContentDescription("Theme option: "+t.name+(i==themeIndex?", selected":""));wirePress(preview);preview.setOnClickListener(v->{try{data.put("theme",index);data.put("themeMode","manual");data.put("themeDay",LocalDate.now().toString());save();applyTheme();popup.dismiss();chime(readySound);home();}catch(Exception ignored){}});if(i==themeIndex)selectedRow=preview;}
  popup.showAsDropDown(anchor,0,dp(4));View selected=selectedRow;if(selected!=null)scroll.post(()->scroll.scrollTo(0,Math.max(0,selected.getTop()-dp(5))));}
 """
 anchor=' JSONObject data;'
 if anchor not in s:raise RuntimeError('Activity data anchor missing')
 s=s.replace(anchor,helpers+'\n'+anchor,1)
 edit('View button(String title,',lambda t:t.replace('return r;}','wirePress(r);return r;}') if 'return r;}' in t else t.replace('return r;','wirePress(r);return r;'))
 # Native dialog actions are wired only after their final styling/reparenting.
 edit('void showCute(AlertDialog d){',lambda t:t[:-1]+'if(d.getWindow()!=null)wireNativeButtons(d.getWindow().getDecorView());}')
 edit('View calendarArrow(',lambda t:t.replace('return arrow;','wirePress(arrow);return arrow;'))
 def calendar_changes(t):
  t=t.replace('int[] colors={LILAC,MINT,PINK,WHITE};','int[] colors={scheduleColor("work"),scheduleColor("off"),scheduleColor("holiday"),WHITE};')
  t=t.replace('bg=status.equals("work")?LILAC:status.equals("off")?MINT:status.equals("holiday")?PINK:WHITE;','bg=scheduleColor(status);')
  t=t.replace('choices[i]=tile;','wirePress(tile);choices[i]=tile;')
  t=t.replace('cell.setContentDescription(date.format(pretty)','wirePress(cell);cell.setContentDescription(date.format(pretty)')
  t=t.replace('Pink dots mark days with journal entries.','Dots mark days with journal entries.')
  t=t.replace('Pink dots mark days with entries.','Dots mark days with entries.')
  return t
 edit('void calendar(',calendar_changes)
 edit('void journal(){',lambda t:t.replace('selected.format(pretty)+"  ›"','selected.format(pretty)'))
 edit('void home(){',lambda t:t.replace('shape(d.equals(today)?PINK:WHITE)','shape(scheduleColor(schedule.optString(d.toString(),"unset")))'))
 edit('class Icon extends View {',lambda t:t.replace('protected void onDraw(Canvas canvas){','protected void onDraw(Canvas canvas){if(drawScheduleSymbol(canvas,kind,getWidth(),getHeight()))return;',1))
 replace('class EraserIcon extends View {',r"""class EraserIcon extends View {Paint p=new Paint(3);EraserIcon(){super(MainActivity.this);setContentDescription("Clear day");}protected void onDraw(Canvas c){c.save();c.scale(getWidth()/40f,getHeight()/40f);c.rotate(-35,20,20);p.setStyle(Paint.Style.FILL);p.setColor(0xFFD5A2B8);c.drawRoundRect(8,7,31,32,4,4,p);p.setColor(0xFFD8D0E6);c.drawRoundRect(8,22,31,32,3,3,p);p.setStyle(Paint.Style.STROKE);p.setColor(0xFF796C88);p.setStrokeWidth(1.7f);c.drawRoundRect(8,7,31,32,4,4,p);c.drawLine(8,22,31,22,p);c.restore();}}""")
 # Preserve daily checkbox resets while applying an optional theme policy at a date boundary.
 start=s.find('final Runnable midnight=')
 if start<0:raise RuntimeError('Date-check runnable missing')
 a,b=bounds(s,'final Runnable midnight=')
 end=b
 while end<len(s) and s[end].isspace():end+=1
 if s[end]!=';':raise RuntimeError('Date-check runnable ending missing')
 s=s[:a]+r"""final Runnable midnight=new Runnable(){public void run(){if(data==null)return;String previous=data.optString("lastDay","");String today=LocalDate.now().toString();boolean changed=applyThemePolicy(false);resetDaily();if(changed){applyTheme();render();}else if(screen.equals("home")&&!today.equals(previous))home();handler.postDelayed(this,30000);}};"""+s[end+1:]
 edit('public void onCreate(Bundle b)',lambda t:t.replace('super.onCreate(b);','super.onCreate(b);restoringThemeSession=b!=null;if(b!=null)externalPicker=b.getBoolean("externalPicker",false);',1))
 edit('protected void onSaveInstanceState(Bundle b)',lambda t:t.replace('super.onSaveInstanceState(b);','super.onSaveInstanceState(b);b.putBoolean("externalPicker",externalPicker);',1))
 edit('protected void onActivityResult(',lambda t:re.sub(r'(super\.onActivityResult\([^;]+;)',r'\1externalPicker=false;skipThemeStart=true;',t,count=1))
 # Larger art and full-range spacing remain coupled so no icon collisions are introduced.
 edit('ArrayList<MotionSticker> packedStickers(',lambda t:t.replace('(panel?18:23)','(panel?21:26)').replace('item.size*.95f+dp(17)','item.size*.95f+dp(23)'))
 edit('void drawScattered(',lambda t:t.replace('36000','32000').replace('*dp(7)','*dp(9)').replace('*dp(9);angle','*dp(12);angle').replace(')*14;',')*18;').replace(')*.12f;',')*.15f;'))
 replace('float phase(){','float phase(){return motionEnabled()?(float)((SystemClock.uptimeMillis()%32000L)*(Math.PI*2.0/32000.0)):0;}')
 edit('class Mascot extends AnimatedArt {',lambda t:t.replace('Math.sin(phase())*5','Math.sin(phase())*6').replace('Math.sin(phase()*2)*.045f','Math.sin(phase()*2)*.055f').replace('Math.sin(phase()*2)*4.5f','Math.sin(phase()*2)*5.5f'))

 replace('void settings(){',r"""void settings(){screen="settings";editor=null;base("Settings",true);ScheduleViewport boundary=new ScheduleViewport();ScrollView scroll=new ScrollView(this);scroll.setClipChildren(true);scroll.setClipToPadding(true);scroll.setPadding(dp(4),dp(8),dp(4),dp(12));scroll.setOverScrollMode(View.OVER_SCROLL_NEVER);LinearLayout content=col();scroll.addView(content,new ScrollView.LayoutParams(-1,-2));boundary.addView(scroll,new FrameLayout.LayoutParams(-1,-1));LinearLayout.LayoutParams viewport=new LinearLayout.LayoutParams(-1,0,1);viewport.setMargins(0,dp(6),0,0);root.addView(boundary,viewport);
 content.addView(label("Choose your little world",24));content.addView(text("Your character, colours, pattern & lettering",13));space(content,10);content.addView(themeDropdown(),new LinearLayout.LayoutParams(-1,-2));space(content,7);content.addView(text("Choosing a theme from the menu switches to Manual.",12));space(content,9);
 LinearLayout policy=section(WHITE);policy.addView(label("Theme selection",21));RadioGroup modes=new RadioGroup(this);modes.setOrientation(RadioGroup.VERTICAL);String selected=data.optString("themeMode","manual");String[] labels={"Manual","Randomise Daily","Randomise Each Use"},keys={"manual","daily","eachUse"};for(int i=0;i<3;i++){RadioButton option=new RadioButton(this);option.setId(View.generateViewId());option.setText(labels[i]);option.setTag(keys[i]);option.setTextColor(INK);option.setTypeface(bodyFont);option.setTextSize(16);option.setPadding(dp(3),dp(7),dp(3),dp(7));option.setButtonTintList(android.content.res.ColorStateList.valueOf(blend(LILAC,INK,.4f)));modes.addView(option,new RadioGroup.LayoutParams(-1,-2));option.setChecked(selected.equals(keys[i]));wirePress(option);}modes.setOnCheckedChangeListener((group,id)->{View checked=group.findViewById(id);if(checked==null)return;String mode=(String)checked.getTag();if(mode.equals(data.optString("themeMode","manual")))return;try{data.put("themeMode",mode);if(mode.equals("daily"))data.remove("themeDay");boolean changed=applyThemePolicy(true);save();if(changed)applyTheme();settings();}catch(Exception ignored){}});policy.addView(modes);policy.addView(text("Daily changes on the first opening of a new day, or while the app stays open at midnight. Each Use changes when you return from the background, not between app pages or after choosing an attachment.",12));content.addView(policy);space(content,15);
 LinearLayout options=section(WHITE);options.addView(label("Little preferences",22));Switch motion=new Switch(this);motion.setText("Gentle illustrations");motion.setTextColor(INK);motion.setTypeface(bodyFont);motion.setPadding(dp(3),dp(10),dp(3),dp(10));motion.setChecked(data.optBoolean("animations",true));motion.setOnCheckedChangeListener((v,on)->{try{data.put("animations",on);save();settings();}catch(Exception ignored){}});wirePress(motion);options.addView(motion);
 Switch press=new Switch(this);press.setText("Button press animation");press.setTextColor(INK);press.setTypeface(bodyFont);press.setPadding(dp(3),dp(10),dp(3),dp(10));press.setChecked(data.optBoolean("buttonPress",true));press.setOnCheckedChangeListener((v,on)->{try{data.put("buttonPress",on);save();}catch(Exception ignored){}});wirePress(press);options.addView(press);options.addView(text("Buttons shrink slightly under your finger. Also respects Android's animation setting.",12));
 Switch soundsToggle=new Switch(this);soundsToggle.setText("Soft app sounds");soundsToggle.setTextColor(INK);soundsToggle.setTypeface(bodyFont);soundsToggle.setPadding(dp(3),dp(10),dp(3),dp(10));soundsToggle.setChecked(data.optBoolean("sounds",true));soundsToggle.setOnCheckedChangeListener((v,on)->{try{data.put("sounds",on);save();if(on)chime(checkSound);}catch(Exception ignored){}});wirePress(soundsToggle);options.addView(soundsToggle);
 Switch reset=new Switch(this);reset.setText("Automatically reset completed tasks");reset.setTextColor(INK);reset.setTypeface(bodyFont);reset.setPadding(dp(3),dp(10),dp(3),dp(10));reset.setChecked(data.optBoolean("resetDaily",true));reset.setOnCheckedChangeListener((v,on)->{try{data.put("resetDaily",on);save();if(on)resetDaily();}catch(Exception ignored){}});wirePress(reset);options.addView(reset);options.addView(text("Tasks appear on scheduled dates, counting from creation: 1 = daily, 2 = every other day. This switch clears ticks at the next scheduled appearance. Off keeps ticks until you clear them. Off-day tasks are hidden, not deleted.",13));content.addView(options);space(content,16);
 LinearLayout backup=section(LILAC);backup.addView(label("Keep your memories safe",23));space(backup,9);backup.addView(button("Backup all data","export",WHITE,()->{pending="backup";Intent intent=new Intent(Intent.ACTION_CREATE_DOCUMENT);intent.setType("application/zip");intent.addCategory(Intent.CATEGORY_OPENABLE);intent.putExtra(Intent.EXTRA_TITLE,"A-Day-To-Keep-Backup-"+LocalDate.now()+".zip");startActivityForResult(intent,103);}),new LinearLayout.LayoutParams(-1,-2));space(backup,12);backup.addView(button("Restore a backup","book",WHITE,()->{Intent intent=new Intent(Intent.ACTION_OPEN_DOCUMENT);intent.setType("*/*");intent.addCategory(Intent.CATEGORY_OPENABLE);startActivityForResult(intent,104);}),new LinearLayout.LayoutParams(-1,-2));space(backup,12);backup.addView(text("Includes your schedule, journal, photo/PDF page images, tasks and preferences. Restore replaces current app data. Exports are not encrypted. Save a backup before uninstalling.\n\nKeep patient-identifiable information out of the journal.\n\nA Day To Keep · Version 6.3",13));content.addView(backup);space(content,16);
 }""")
 replace('void viewer(LocalDate d,String file){',r"""void viewer(LocalDate d,String file){Dialog full=new Dialog(this,android.R.style.Theme_Material_Light_NoActionBar_Fullscreen);LinearLayout container=col();container.setBackgroundColor(0xFF342F3D);LinearLayout bar=row();bar.setPadding(dp(10),dp(12),dp(10),dp(12));bar.addView(new View(this),new LinearLayout.LayoutParams(0,1,1));View remove=glyphButton("Delete attachment","trash",PINK,()->ask("Remove this attachment?","This removes the image or PDF page from this CPD entry, not the original file on your phone.",()->{JSONObject e=entry(d,false);if(e!=null){JSONArray images=e.optJSONArray("images");for(int i=images.length()-1;i>=0;i--)if(images.optString(i).equals(file))images.remove(i);save();new File(photos(),file).delete();}full.dismiss();journal();},null));LinearLayout.LayoutParams deleteLp=new LinearLayout.LayoutParams(dp(52),dp(52));deleteLp.setMargins(0,0,dp(9),0);bar.addView(remove,deleteLp);View close=glyphButton("Close attachment","close",LILAC,()->full.dismiss());bar.addView(close,new LinearLayout.LayoutParams(dp(52),dp(52)));container.addView(bar);TextView hint=text("Pinch to zoom · Drag to pan · Double-tap to reset",12);hint.setTextColor(Color.WHITE);hint.setGravity(Gravity.CENTER);container.addView(hint);Zoom zoom=new Zoom();container.addView(zoom,new LinearLayout.LayoutParams(-1,0,1));worker.execute(()->{Bitmap image=decode(new File(photos(),file),3000);runOnUiThread(()->zoom.setImageBitmap(image));});full.setContentView(container);full.show();}
 """)
 edit('protected void onResume()',lambda t:t.replace('super.onResume();','super.onResume();skipThemeStart=false;',1))
 s=s.replace('Version 6.2','Version 6.3')
 edit('void home(){',lambda t:t.replace('card.setContentDescription(', 'wirePress(card);card.setContentDescription('))
 edit('void journal(){',lambda t:t.replace('thumb.setOnClickListener(', 'wirePress(thumb);thumb.setOnClickListener('))
 p.write_text(s,encoding='utf-8')

# Renderers/resources are refreshed even when the source ZIP is already upgraded.
widget_source='package uk.co.littledays;\nimport android.app.PendingIntent;\nimport android.appwidget.*;\nimport android.content.*;\nimport android.graphics.*;\nimport android.os.Bundle;\nimport android.util.AtomicFile;\nimport android.widget.RemoteViews;\nimport org.json.*;\nimport java.io.*;\nimport java.time.LocalDate;\nimport java.time.temporal.ChronoUnit;\n\npublic class KeepWidget extends AppWidgetProvider {\n @Override public void onUpdate(Context context,AppWidgetManager manager,int[] ids){for(int id:ids)update(context,manager,id);}\n @Override public void onAppWidgetOptionsChanged(Context context,AppWidgetManager manager,int id,Bundle options){update(context,manager,id);}\n @Override public void onReceive(Context context,Intent intent){super.onReceive(context,intent);String action=intent.getAction();if(Intent.ACTION_DATE_CHANGED.equals(action)||Intent.ACTION_TIME_CHANGED.equals(action)||Intent.ACTION_TIMEZONE_CHANGED.equals(action))updateAll(context);}\n public static void updateAll(Context context){try{AppWidgetManager manager=AppWidgetManager.getInstance(context);for(Class<?> provider:new Class<?>[]{KeepWidget.class,KeepCountWidget.class}){int[] ids=manager.getAppWidgetIds(new ComponentName(context,provider));for(int id:ids)update(context,manager,id);}}catch(RuntimeException e){android.util.Log.w("ADayToKeep","Widget update deferred",e);}}\n static JSONObject read(Context context,String name){try(InputStream in=new AtomicFile(new File(context.getFilesDir(),name)).openRead()){ByteArrayOutputStream bytes=new ByteArrayOutputStream();byte[] buffer=new byte[8192];int count;while((count=in.read(buffer))!=-1)bytes.write(buffer,0,count);return new JSONObject(bytes.toString("UTF-8"));}catch(Exception e){return new JSONObject();}}\n static int mix(int a,int b,float amount){return Color.rgb(Math.round(Color.red(a)*(1-amount)+Color.red(b)*amount),Math.round(Color.green(a)*(1-amount)+Color.green(b)*amount),Math.round(Color.blue(a)*(1-amount)+Color.blue(b)*amount));}\n static int completedColor(int oldUncompleted){float[] hsv=new float[3];Color.colorToHSV(oldUncompleted,hsv);hsv[1]=Math.max(.42f,Math.min(.76f,hsv[1]*2.4f+.16f));hsv[2]=Math.max(.70f,Math.min(.88f,hsv[2]*.88f));return Color.HSVToColor(hsv);}\n static int uncompletedColor(int oldCompleted){float[] hsv=new float[3];Color.colorToHSV(oldCompleted,hsv);hsv[1]*=.22f;return mix(Color.HSVToColor(hsv),Color.WHITE,.64f);}\n static double channel(int value){double v=value/255.0;return v<=.04045?v/12.92:Math.pow((v+.055)/1.055,2.4);}\n static double luminance(int color){return .2126*channel(Color.red(color))+.7152*channel(Color.green(color))+.0722*channel(Color.blue(color));}\n static double ringContrast(int a,int b){double x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}\n static int ensureRingContrast(int color,int track){float[] hsv=new float[3];Color.colorToHSV(color,hsv);while(ringContrast(color,track)<3.0&&hsv[2]>.30f){hsv[2]=Math.max(.30f,hsv[2]-.025f);color=Color.HSVToColor(hsv);}return color;}\n static void update(Context context,AppWidgetManager manager,int id){try{\n  AppWidgetProviderInfo info=manager.getAppWidgetInfo(id);boolean withCount=info!=null&&info.provider.getClassName().endsWith("KeepCountWidget");JSONObject data=read(context,"data.json"),skin=read(context,"widget-skin.json");JSONArray tasks=data.optJSONArray("tasks");LocalDate today=LocalDate.now();int total=0,completed=0;boolean auto=data.optBoolean("resetDaily",true);\n  if(tasks!=null)for(int i=0;i<tasks.length();i++){JSONObject task=tasks.optJSONObject(i);if(task==null)continue;boolean due=true;try{LocalDate anchor=LocalDate.parse(task.optString("createdOn",today.toString()));long days=ChronoUnit.DAYS.between(anchor,today);due=days>=0&&days%Math.max(1,task.optInt("repeat",1))==0;}catch(Exception ignored){}if(!due)continue;total++;boolean done=task.optBoolean("done");if(auto&&!today.toString().equals(task.optString("completedOn")))done=false;if(done)completed++;}\n  int ink=skin.optInt("ink",0xFF75576C),pink=skin.optInt("pink",0xFFF7DCE4),mint=skin.optInt("mint",0xFFDDEDDC),cream=skin.optInt("cream",0xFFFFF5F0);int previousCompleted=mix(mint,ink,1f/3f);int uncompletedPaint=uncompletedColor(previousCompleted),completedPaint=ensureRingContrast(completedColor(pink),uncompletedPaint);\n  Bitmap card=Bitmap.createBitmap(256,256,Bitmap.Config.ARGB_8888);Canvas c=new Canvas(card);Paint paint=new Paint(Paint.ANTI_ALIAS_FLAG|Paint.FILTER_BITMAP_FLAG);float center=128,radius=116;paint.setColor(cream);c.drawCircle(center,center,104,paint);paint.setStyle(Paint.Style.STROKE);paint.setStrokeWidth(13);paint.setStrokeCap(Paint.Cap.ROUND);paint.setColor(uncompletedPaint);c.drawCircle(center,center,radius,paint);if(total>0&&completed>0){paint.setColor(completedPaint);c.drawArc(new RectF(12,12,244,244),-90,360f*completed/total,false,paint);}\n  paint.setColor(Color.BLACK);paint.setStrokeWidth(2.3f);c.drawCircle(center,center,123.4f,paint);paint.setStyle(Paint.Style.FILL);\n  int clipped=c.save();Path circle=new Path();circle.addCircle(center,center,102,Path.Direction.CW);c.clipPath(circle);Bitmap character=BitmapFactory.decodeFile(new File(context.getFilesDir(),"widget-character.png").toString());RectF characterBounds=withCount?new RectF(40,30,216,206):new RectF(32,26,224,218);if(character!=null){c.drawBitmap(character,null,characterBounds,paint);character.recycle();}else{android.graphics.drawable.Drawable preview=context.getDrawable(R.drawable.launcher_foreground);if(preview!=null){preview.setBounds((int)characterBounds.left,(int)characterBounds.top,(int)characterBounds.right,(int)characterBounds.bottom);preview.draw(c);}}c.restoreToCount(clipped);\n  if(withCount){Typeface font=Typeface.create("sans-serif-rounded",Typeface.BOLD);try{font=Typeface.createFromAsset(context.getAssets(),"fonts/"+skin.optString("font","Mali")+".ttf");}catch(RuntimeException ignored){}paint.setTypeface(font);paint.setTextSize(29);paint.setTextAlign(Paint.Align.CENTER);paint.setColor(ink);c.drawText(completed+"/"+total,128,216,paint);}\n  String status=total==0?"No tasks scheduled today":completed+" of "+total+" tasks complete today";RemoteViews views=new RemoteViews(context.getPackageName(),R.layout.keep_widget);views.setImageViewBitmap(R.id.widget_card,card);views.setContentDescription(R.id.widget_card,"A Day To Keep. "+status+". Tap to open your checklist.");Intent open=new Intent(context,MainActivity.class).putExtra("fromWidget",true).addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP|Intent.FLAG_ACTIVITY_SINGLE_TOP);PendingIntent tap=PendingIntent.getActivity(context,701,open,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);views.setOnClickPendingIntent(R.id.widget_card,tap);manager.updateAppWidget(id,views);\n }catch(Exception|OutOfMemoryError e){android.util.Log.w("ADayToKeep","Could not render checklist widget",e);}}\n}\n'
Path('app/src/main/java/uk/co/littledays/KeepWidget.java').write_text(widget_source,encoding='utf-8')
Path('app/src/main/java/uk/co/littledays/KeepCountWidget.java').write_text('package uk.co.littledays; public class KeepCountWidget extends KeepWidget {}\n',encoding='utf-8')
def resource(relative,text):
 target=Path('app/src/main/res')/relative
 target.parent.mkdir(parents=True,exist_ok=True)
 ET.fromstring(text)
 target.write_text(text,encoding='utf-8')
resource('xml/keep_widget_info.xml','<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android" android:minWidth="40dp" android:minHeight="40dp" android:minResizeWidth="40dp" android:minResizeHeight="40dp" android:targetCellWidth="1" android:targetCellHeight="1" android:initialLayout="@layout/keep_widget" android:previewLayout="@layout/keep_widget" android:previewImage="@drawable/widget_round_preview" android:updatePeriodMillis="1800000" android:resizeMode="horizontal|vertical" android:widgetCategory="home_screen" android:description="@string/widget_description"/>')
resource('xml/keep_widget_count_info.xml','<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android" android:minWidth="40dp" android:minHeight="40dp" android:minResizeWidth="40dp" android:minResizeHeight="40dp" android:targetCellWidth="1" android:targetCellHeight="1" android:initialLayout="@layout/keep_widget" android:previewLayout="@layout/keep_widget" android:previewImage="@drawable/widget_round_preview" android:updatePeriodMillis="1800000" android:resizeMode="horizontal|vertical" android:widgetCategory="home_screen" android:description="@string/widget_count_description"/>')
resource('values/widget_strings.xml','<resources><string name="widget_description">Your theme character and high-contrast circular checklist progress.</string><string name="widget_count_description">Your theme character, circular progress and completed/total checklist count.</string><string name="widget_count_label">A Day To Keep · Ring + Count</string></resources>')
receiver='<receiver android:name=".KeepCountWidget" android:label="@string/widget_count_label" android:exported="false"><intent-filter><action android:name="android.appwidget.action.APPWIDGET_UPDATE"/><action android:name="android.intent.action.DATE_CHANGED"/><action android:name="android.intent.action.TIME_SET"/><action android:name="android.intent.action.TIMEZONE_CHANGED"/></intent-filter><meta-data android:name="android.appwidget.provider" android:resource="@xml/keep_widget_count_info"/></receiver>'

manifest=Path('app/src/main/AndroidManifest.xml');text=manifest.read_text()
if 'android:name=".KeepCountWidget"' not in text:text=text.replace('</application>',receiver+'\n</application>')
text=re.sub(r'(<receiver\b[^>]*android:name="\.KeepWidget"[^>]*android:label=")[^"]+',r'\1A Day To Keep · Ring',text,count=1)
ET.fromstring(text);manifest.write_text(text,encoding='utf-8')
preview=Path('app/src/main/res/drawable/widget_round_preview.xml')
if preview.is_file():
 text=preview.read_text().replace('#F0CCDA','#E2E5E2').replace('#95B6A0','#CB789B')
 if 'android:strokeColor="#000000"' not in text:
  outline='<path android:fillColor="#00000000" android:strokeColor="#000000" android:strokeWidth="1" android:pathData="M54,3.4a50.6,50.6 0,1 0,0.1,0Z"/>'
  text=text.replace('</vector>',outline+'</vector>')
 preview.write_text(text,encoding='utf-8')
gradle=Path('app/build.gradle');g=gradle.read_text();g=re.sub(r'versionCode\s+\d+','versionCode 9',g);g=re.sub(r'versionName\s+[\'\"][^\'\"]+[\'\"]','versionName "6.3"',g);gradle.write_text(g)

# Preserve the existing startup/navigation/keyboard assertions and adapt theme selection
# to its new dropdown, rather than removing that navigation check.
smoke=Path('tools/smoke_test.py')
test=smoke.read_text(encoding='utf-8')
if '# THEME_DROPDOWN_TEST_63' not in test:
 old="tap(tree,'Strawberry Bunny');time.sleep(3);tree=hierarchy('theme-to-home');"
 new="# THEME_DROPDOWN_TEST_63\n tap(tree,'Choose theme');time.sleep(2);tree=hierarchy('theme-menu');verify(tree,'Strawberry Bunny');tap(tree,'Strawberry Bunny');time.sleep(3);tree=hierarchy('theme-to-home');"
 if old not in test:raise RuntimeError('Expected theme smoke-test step missing')
 test=test.replace(old,new,1)
 anchor="if 'KeepWidget' not in info:raise RuntimeError('Widget receiver missing from installed package')"
 if anchor not in test:raise RuntimeError('Widget registration assertion missing')
 test=test.replace(anchor,anchor+"\n if 'KeepCountWidget' not in info:raise RuntimeError('Count widget receiver missing from installed package')",1)
 import ast
 ast.parse(test)
 smoke.write_text(test,encoding='utf-8')
Path('VERSION-6.3-NOTES.txt').write_text("""A Day To Keep 6.3
Two 1x1 widgets: Ring and Ring + Count. Both have a thin black outer circle. Completed
progress uses a more saturated/deeper version of the previous uncompleted hue; the track
uses a light, desaturated version of the previous completed hue. Count adds n/total below
the character. Both use current theme data and update together. No scheduled tasks = 0/0.

Settings content is bounded below the fixed Home/title header. Current theme is shown
on a themed dropdown; selected option has a dark outline and Selected label. Choosing a
theme switches to Manual and returns Home. Three exclusive modes: Manual, Randomise Daily,
Randomise Each Use. Random choices avoid immediately repeating the current theme. Daily
changes at the next app opening on a new day, or within the existing 30-second date check
if app stays open. Each Use changes on returning from the background, not page navigation,
rotation, or returning from Android document/photo pickers. OS lifecycle/device behaviour
still requires testing. Widgets follow the last applied app theme; background widget
updates alone do not select a new random theme before the app opens.

Journal date chevron removed. Calendar footer no longer specifies a dot colour. Viewer
has a top-right X with a separate trash icon to its left and a 9dp gap. Delete confirmation,
zoom, pan, PDFs-as-images, backups, recurrence and keyboard repair remain intact.

Work = hospital in a cool blue; Day Off = sofa in warm peach; Holiday = sun in soft yellow.
Colours are only lightly tinted by the theme, maintaining hue separation; icons distinguish
states without relying on colour alone. Eraser has a tinted lower half and dark outline.
Art is 3dp larger; translations 9/12dp, rotation 18 degrees, scale 15%, period 32 seconds.
Collision reservations were expanded with the new size/motion. Crowded areas show fewer
objects instead of touching ones. Existing illustration/system animation settings respected.
Button press scaling is on by default with its own settings toggle. Native Android file
picker/save-location UI is outside the app and is not restyled or animated by this change.

Package/signing unchanged, versionCode 9, versionName 6.3. New preferences are included in
existing JSON backups automatically. Save an app-data backup before updating in place.
Generated with static checks; CI must compile and test. Widget placement, visual contrast,
press effects and randomisation lifecycle cases still need real-phone verification.
""",encoding='utf-8')
print('Version 6.3 preferences, contrast, symbols, button feedback and both widgets prepared.')
