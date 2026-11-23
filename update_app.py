#!/usr/bin/env python3
from pathlib import Path
import re, math, wave, struct, urllib.request, time
root=Path('.')
p=root/'app/src/main/java/uk/co/littledays/MainActivity.java'
s=p.read_text(encoding='utf-8')
MARK='// A_DAY_TO_KEEP_V2'
def block(start,end,new):
 global s
 a=s.find(start)
 if a<0: raise RuntimeError('Expected source section missing: '+start)
 b=s.find(end,a+len(start))
 if b<0: raise RuntimeError('Expected end section missing: '+end)
 s=s[:a]+new+'\n '+s[b:]
def one(old,new):
 global s
 if old not in s: raise RuntimeError('Expected original code missing: '+old[:100])
 s=s.replace(old,new,1)
if MARK not in s:
 s=s.replace('java.nio.file.Files.readString(new File(staging,"data.json").toPath())','new String(java.nio.file.Files.readAllBytes(new File(staging,"data.json").toPath()), java.nio.charset.StandardCharsets.UTF_8)')
 if 'try(android.graphics.pdf.PdfDocument pdf=new android.graphics.pdf.PdfDocument()){' in s:
  one('try(android.graphics.pdf.PdfDocument pdf=new android.graphics.pdf.PdfDocument()){','android.graphics.pdf.PdfDocument pdf=new android.graphics.pdf.PdfDocument();try{')
  one('w.finish();pdf.writeTo(out);}}','w.finish();pdf.writeTo(out);}finally{pdf.close();}}')
 s=s.replace('final int INK=','int INK=',1)
 helpers=r"""
 // A_DAY_TO_KEEP_V2
 static class ThemeSpec {
  String name,description,character,heading,body; int ink,pink,lilac,mint,cream,white;
  ThemeSpec(String n,String d,String c,String h,String b,int i,int p,int l,int m,int cr,int w){name=n;description=d;character=c;heading=h;body=b;ink=i;pink=p;lilac=l;mint=m;cream=cr;white=w;}
 }
 final ThemeSpec[] themes={
  new ThemeSpec("Strawberry Bunny","Blush gingham · sweet little strawberries","bunny","Chewy","Mali",0xFF75576C,0xFFF7DCE4,0xFFEBDFF2,0xFFDDEDDC,0xFFFFF5F0,0xFFFFFCFA),
  new ThemeSpec("Cloud Kitten","Sky-blue clouds · a dreamy kitten","cat","PatrickHand","Mali",0xFF526785,0xFFDDEAF8,0xFFE5E1F5,0xFFDDF2EF,0xFFF3F9FF,0xFFFCFDFF),
  new ThemeSpec("Honey Bear","Peach polka dots · a honey-loving bear","bear","Chewy","PatrickHand",0xFF7A604B,0xFFF7DFC9,0xFFF4E7C0,0xFFE6EACF,0xFFFFF9E9,0xFFFFFDFA),
  new ThemeSpec("Clover Pond","Mint ripples · a friendly little frog","frog","Mali","PatrickHand",0xFF4F7164,0xFFD9EAD9,0xFFDCECEB,0xFFEAF0CF,0xFFF3FAEF,0xFFFCFFFA),
  new ThemeSpec("Moonlight Mochi","Lavender stars · a sleepy mochi","mochi","PatrickHand","Mali",0xFF635B81,0xFFE9DDF1,0xFFDDDFF2,0xFFE2EBF0,0xFFF4F1FA,0xFFFDFBFF)
 };
 int themeIndex=0; ThemeSpec theme; Typeface headingFont,bodyFont;
 android.media.SoundPool sounds; int checkSound,softSound,readySound; HashSet<Integer> loadedSounds=new HashSet<>();
 void applyTheme(){themeIndex=Math.max(0,Math.min(themes.length-1,data.optInt("theme",0)));theme=themes[themeIndex];INK=theme.ink;PINK=theme.pink;LILAC=theme.lilac;MINT=theme.mint;CREAM=theme.cream;WHITE=theme.white;try{headingFont=Typeface.createFromAsset(getAssets(),"fonts/"+theme.heading+".ttf");bodyFont=Typeface.createFromAsset(getAssets(),"fonts/"+theme.body+".ttf");}catch(Exception e){headingFont=Typeface.create("sans-serif-rounded",Typeface.BOLD);bodyFont=Typeface.create("sans-serif",Typeface.NORMAL);}getWindow().setStatusBarColor(CREAM);getWindow().setNavigationBarColor(CREAM);}
 void initSounds(){sounds=new android.media.SoundPool.Builder().setMaxStreams(3).setAudioAttributes(new android.media.AudioAttributes.Builder().setUsage(android.media.AudioAttributes.USAGE_ASSISTANCE_SONIFICATION).setContentType(android.media.AudioAttributes.CONTENT_TYPE_SONIFICATION).build()).build();sounds.setOnLoadCompleteListener((pool,id,status)->{if(status==0)loadedSounds.add(id);});checkSound=sounds.load(this,uk.co.littledays.R.raw.check,1);softSound=sounds.load(this,uk.co.littledays.R.raw.soft,1);readySound=sounds.load(this,uk.co.littledays.R.raw.ready,1);}
 void chime(int id){if(sounds==null||!data.optBoolean("sounds",true)||!loadedSounds.contains(id))return;android.media.AudioManager audio=(android.media.AudioManager)getSystemService(AUDIO_SERVICE);if(audio.getRingerMode()!=android.media.AudioManager.RINGER_MODE_NORMAL)return;sounds.play(id,.18f,.18f,1,0,1);}
 void migrateTasks(){boolean changed=false;for(int i=0;i<tasks.length();i++){JSONObject t=tasks.optJSONObject(i);if(t==null)continue;try{if(!t.has("repeat")){t.put("repeat",1);changed=true;}if(t.optBoolean("done")&&!t.has("completedOn")){t.put("completedOn",data.optString("lastDay",LocalDate.now().toString()));changed=true;}}catch(Exception ignored){}}if(changed)save();}
 LinearLayout section(int color){LinearLayout box=col();box.setPadding(dp(11),dp(11),dp(11),dp(11));box.setBackground(shape(color));box.setElevation(dp(2));return box;}
 void styleTree(View v){if(v instanceof TextView){TextView t=(TextView)v;t.setTextColor(INK);t.setTypeface(v instanceof Button?headingFont:bodyFont);if(v instanceof EditText){t.setBackground(shape(WHITE));t.setPadding(dp(15),dp(12),dp(15),dp(12));t.setHintTextColor((INK&0x00FFFFFF)|0x88000000);}}if(v instanceof ViewGroup){ViewGroup g=(ViewGroup)v;for(int i=0;i<g.getChildCount();i++)styleTree(g.getChildAt(i));}}
 class Mascot extends View {
  String animal; int accent; Paint p=new Paint(3);
  Mascot(String a,int c){super(MainActivity.this);animal=a;accent=c;setContentDescription(a+" character");}
  void fill(int c){p.setColor(c);p.setStyle(Paint.Style.FILL);}
  protected void onDraw(Canvas c){c.save();c.scale(getWidth()/100f,getHeight()/100f);fill(accent);c.drawCircle(50,53,45,p);fill(animal.equals("bear")?0xFFD9AB7C:animal.equals("frog")?0xFFA7CCA3:0xFFFFFCF5);
   if(animal.equals("bunny")){c.drawOval(24,4,41,57,p);c.drawOval(59,4,76,57,p);}
   if(animal.equals("bear")){c.drawCircle(26,30,15,p);c.drawCircle(74,30,15,p);}
   if(animal.equals("frog")){c.drawCircle(28,31,16,p);c.drawCircle(72,31,16,p);}
   if(animal.equals("cat")){Path ears=new Path();ears.moveTo(18,46);ears.lineTo(20,10);ears.lineTo(43,34);ears.lineTo(58,34);ears.lineTo(80,10);ears.lineTo(82,46);ears.close();c.drawPath(ears,p);}
   c.drawOval(14,29,86,86,p);fill(0xFF745C6B);c.drawCircle(36,54,3,p);c.drawCircle(64,54,3,p);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2.5f);c.drawArc(43,57,57,68,0,180,false,p);fill(0xFFEAA5B5);c.drawOval(22,62,36,69,p);c.drawOval(65,62,79,69,p);
   if(animal.equals("mochi")){fill(0xFFD6C5EB);c.drawCircle(75,21,10,p);fill(accent);c.drawCircle(80,17,9,p);}
   if(animal.equals("bunny")){fill(0xFFEBA1B1);c.drawOval(28,10,36,34,p);c.drawOval(64,10,72,34,p);}
   c.restore();}
 }
 """
 one(' JSONObject data;',helpers+'\n JSONObject data;')
 one('super.onCreate(b);load();resetDaily();','super.onCreate(b);load();applyTheme();initSounds();migrateTasks();resetDaily();')
 one('handler.removeCallbacks(midnight);worker.shutdown();','handler.removeCallbacks(midnight);worker.shutdown();if(sounds!=null)sounds.release();')
 block('void resetDaily(){','int dp(',r"""void resetDaily(){String today=LocalDate.now().toString();boolean changed=false;if(data.optBoolean("resetDaily",true)){for(int i=0;i<tasks.length();i++){JSONObject t=tasks.optJSONObject(i);if(t==null||!t.optBoolean("done"))continue;try{LocalDate completed=LocalDate.parse(t.optString("completedOn",data.optString("lastDay",today)));int interval=Math.max(1,t.optInt("repeat",1));if(!LocalDate.now().isBefore(completed.plusDays(interval))){t.put("done",false);t.remove("completedOn");changed=true;}}catch(Exception ignored){}}}if(!today.equals(data.optString("lastDay"))){try{data.put("lastDay",today);}catch(Exception ignored){}changed=true;}if(changed)save();}
 """)
 one('t.setTextColor(INK);t.setFontFeatureSettings("kern");','t.setTextColor(INK);t.setTypeface(bodyFont);t.setFontFeatureSettings("kern");')
 one('t.setTypeface(Typeface.create("sans-serif-rounded",Typeface.BOLD));','t.setTypeface(headingFont);t.setShadowLayer(dp(1),0,dp(1),0x55FFFFFF);')
 one('r.setOnClickListener(v->action.run());','r.setOnClickListener(v->{chime(softSound);action.run();});')
 one('h.setPadding(dp(10),0,0,0);','h.setPadding(dp(10),0,0,0);h.setTextSize(back?22:26);h.setMaxLines(2);')
 block('void home(){','String ordinal(',r"""void home(){screen="home";editor=null;resetDaily();base("A Day To Keep",false);
 LinearLayout banner=row();banner.addView(new Mascot(theme.character,PINK),new LinearLayout.LayoutParams(dp(58),dp(60)));LinearLayout words=col();words.setPadding(dp(9),0,0,0);words.addView(label("Make a little room for you",18));words.addView(text("Little plans. Lovely memories.",13));banner.addView(words,new LinearLayout.LayoutParams(0,-2,1));root.addView(banner);space(root,10);
 LinearLayout work=section(LILAC);work.addView(button("Work Schedule","calendar",WHITE,()->calendar("work",LocalDate.now(),null)));space(work,8);
 HorizontalScrollView strip=new HorizontalScrollView(this);strip.setHorizontalScrollBarEnabled(false);strip.setClipToPadding(false);LinearLayout days=row();LocalDate today=LocalDate.now();int width=Math.max(dp(48),(getResources().getDisplayMetrics().widthPixels-dp(54))/6);final View[] todayCard={null};
 for(int n=-30;n<=365;n++){LocalDate d=today.plusDays(n);LinearLayout card=col();card.setGravity(Gravity.CENTER);card.setPadding(dp(1),dp(7),dp(1),dp(7));GradientDrawable background=shape(d.equals(today)?PINK:WHITE);if(d.equals(today))background.setStroke(dp(2),INK);card.setBackground(background);TextView dow=label(d.format(DateTimeFormatter.ofPattern("EEE",Locale.UK)),13);dow.setGravity(Gravity.CENTER);card.addView(dow);Icon icon=new Icon(schedule.optString(d.toString(),"unset"));card.addView(icon,new LinearLayout.LayoutParams(dp(28),dp(30)));TextView date=text(d.format(DateTimeFormatter.ofPattern("MMM",Locale.UK))+" "+ordinal(d.getDayOfMonth()),11);date.setGravity(Gravity.CENTER);card.addView(date);LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(width-dp(4),dp(87));cp.setMargins(dp(2),0,dp(2),0);days.addView(card,cp);if(d.equals(today))todayCard[0]=card;card.setContentDescription(d.format(pretty)+", "+schedule.optString(d.toString(),"not set"));card.setOnClickListener(v->calendar("work",d,null));}
 strip.addView(days);work.addView(strip);root.addView(work);strip.post(()->{if(todayCard[0]!=null)strip.scrollTo(Math.max(0,todayCard[0].getLeft()-dp(2)),0);});space(root,12);
 LinearLayout cpd=section(PINK);cpd.addView(button("CPD · Your daily journal","book",WHITE,()->{selected=LocalDate.now();journal();}));TextView caption=text("A place for today's thoughts & discoveries",12);caption.setPadding(dp(9),dp(5),0,0);cpd.addView(caption);root.addView(cpd);space(root,12);
 LinearLayout daily=section(MINT);LinearLayout title=row();title.addView(label("Daily Stuff",23),new LinearLayout.LayoutParams(0,dp(46),1));title.addView(button("Add","plus",WHITE,()->addTask()));daily.addView(title);daily.addView(text("Hold & drag to reorder · Swipe right to remove",11));space(daily,5);ScrollView scroll=new ScrollView(this);LinearLayout list=col();scroll.addView(list);daily.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));root.addView(daily,new LinearLayout.LayoutParams(-1,0,1));buildTasks(list);
 }
 """)
 block('void addTask(){','int taskIndex(',r"""void addTask(){LinearLayout form=col();form.setPadding(dp(20),dp(6),dp(20),dp(12));EditText name=new EditText(this);name.setSingleLine(true);name.setHint("A little thing to do…");form.addView(label("Your task",16));space(form,5);form.addView(name);space(form,12);form.addView(label("Repeat every",16));LinearLayout repeatRow=row();EditText repeat=new EditText(this);repeat.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);repeat.setText("1");repeat.setSelectAllOnFocus(true);repeatRow.addView(repeat,new LinearLayout.LayoutParams(dp(90),-2));TextView suffix=text("  day(s)",16);repeatRow.addView(suffix);form.addView(repeatRow);space(form,8);form.addView(text("Completed tasks reset after this many days.\nAll tasks stay visible in your list.",12));AlertDialog d=new AlertDialog.Builder(this).setTitle("A little task to keep").setView(form).setNegativeButton("Cancel",null).setPositiveButton("Add task",null).create();showCute(d);d.getButton(-1).setOnClickListener(v->{String value=name.getText().toString().trim();if(value.isEmpty()){name.setError("Give your task a name");return;}int interval;try{interval=Integer.parseInt(repeat.getText().toString().trim());if(interval<1||interval>3650)throw new NumberFormatException();}catch(Exception ex){repeat.setError("Enter 1 to 3650 days");return;}try{JSONObject o=new JSONObject();o.put("id",UUID.randomUUID().toString());o.put("text",value);o.put("done",false);o.put("repeat",interval);tasks.put(o);save();chime(readySound);d.dismiss();home();}catch(Exception ex){toast("Could not add task");}});}
 """)
 one('TextView t=text(task.optString("text"),16);',r'TextView t=text(task.optString("text")+"\n"+(task.optInt("repeat",1)==1?"Every day":"Every "+task.optInt("repeat",1)+" days"),16);')
 one('task.put("done",!task.optBoolean("done"));save();home();','boolean checked=!task.optBoolean("done");task.put("done",checked);if(checked)task.put("completedOn",LocalDate.now().toString());else task.remove("completedOn");save();chime(checked?checkSound:softSound);home();')
 one('note.setTextSize(17);','note.setTextSize(18);note.setTypeface(bodyFont);')
 block('void showCute(AlertDialog d){','void ask(',r"""void showCute(AlertDialog d){d.show();Window window=d.getWindow();if(window!=null){GradientDrawable bg=shape(CREAM);bg.setCornerRadius(dp(28));window.setBackgroundDrawable(bg);window.setDimAmount(.32f);}View content=d.findViewById(android.R.id.content);if(content!=null){styleTree(content);if(content instanceof ViewGroup){ViewGroup parent=(ViewGroup)content;parent.setPadding(dp(4),dp(5),dp(4),dp(5));}}int titleId=getResources().getIdentifier("alertTitle","id","android");TextView title=d.findViewById(titleId);if(title!=null){title.setTypeface(headingFont);title.setTextColor(INK);title.setTextSize(24);title.setShadowLayer(1,0,1,0x88FFFFFF);}for(int which:new int[]{DialogInterface.BUTTON_POSITIVE,DialogInterface.BUTTON_NEGATIVE,DialogInterface.BUTTON_NEUTRAL}){Button b=d.getButton(which);if(b!=null){b.setTextColor(INK);b.setTypeface(headingFont);b.setAllCaps(false);b.setTextSize(17);b.setBackground(shape(which==DialogInterface.BUTTON_POSITIVE?PINK:MINT));b.setPadding(dp(18),dp(6),dp(18),dp(6));if(b.getLayoutParams() instanceof ViewGroup.MarginLayoutParams){ViewGroup.MarginLayoutParams lp=(ViewGroup.MarginLayoutParams)b.getLayoutParams();lp.setMargins(dp(4),dp(5),dp(4),dp(7));b.setLayoutParams(lp);}}}}
 """)
 block('void settings(){','@Override protected void onActivityResult(',r"""void settings(){screen="settings";editor=null;base("Settings",true);ScrollView sc=new ScrollView(this);LinearLayout p=col();sc.addView(p);root.addView(sc,new LinearLayout.LayoutParams(-1,0,1));p.addView(label("Choose your little world",24));p.addView(text("A new character, palette, pattern & lettering",13));space(p,10);
 for(int i=0;i<themes.length;i++){final int index=i;ThemeSpec t=themes[i];LinearLayout preview=row();preview.setPadding(dp(12),dp(9),dp(12),dp(9));preview.setBackground(new Pattern(t,index));preview.addView(new Mascot(t.character,t.pink),new LinearLayout.LayoutParams(dp(59),dp(62)));LinearLayout words=col();words.setPadding(dp(10),0,0,0);TextView title=label(t.name+(index==themeIndex?" · Selected":""),20);title.setTextColor(t.ink);try{title.setTypeface(Typeface.createFromAsset(getAssets(),"fonts/"+t.heading+".ttf"));}catch(Exception ignored){}words.addView(title);TextView desc=text(t.description,12);desc.setTextColor(t.ink);words.addView(desc);LinearLayout swatches=row();for(int color:new int[]{t.pink,t.lilac,t.mint}){View swatch=new View(this);swatch.setBackground(shape(color));LinearLayout.LayoutParams sp=new LinearLayout.LayoutParams(dp(29),dp(10));sp.setMargins(0,dp(6),dp(4),0);swatches.addView(swatch,sp);}words.addView(swatches);preview.addView(words,new LinearLayout.LayoutParams(0,-2,1));p.addView(preview,new LinearLayout.LayoutParams(-1,-2));space(p,9);preview.setOnClickListener(v->{try{data.put("theme",index);save();applyTheme();chime(readySound);settings();}catch(Exception ignored){}});}
 space(p,8);LinearLayout options=section(WHITE);options.addView(label("Little preferences",22));Switch sound=new Switch(this);sound.setText("Soft app sounds");sound.setTextColor(INK);sound.setTypeface(bodyFont);sound.setChecked(data.optBoolean("sounds",true));sound.setPadding(dp(3),dp(12),dp(3),dp(12));sound.setOnCheckedChangeListener((v,on)->{try{data.put("sounds",on);save();if(on)chime(checkSound);}catch(Exception ignored){}});options.addView(sound);options.addView(text("Quiet chimes for tasks and buttons.\nRespects your phone's silent/vibrate setting.",12));space(options,9);Switch reset=new Switch(this);reset.setText("Automatically reset completed tasks");reset.setTextColor(INK);reset.setTypeface(bodyFont);reset.setChecked(data.optBoolean("resetDaily",true));reset.setPadding(dp(3),dp(12),dp(3),dp(12));reset.setOnCheckedChangeListener((v,on)->{try{data.put("resetDaily",on);save();if(on)resetDaily();}catch(Exception ignored){}});options.addView(reset);options.addView(text("Each task resets using its own repeat interval, counted from the day you check it. Every day = 1; every two days = 2. With this off, ticks stay until you clear them. Tasks are never hidden or removed. When the app is closed, resets happen on the next open.",13));p.addView(options);space(p,17);
 LinearLayout backups=section(LILAC);backups.addView(label("Keep your memories safe",23));space(backups,9);backups.addView(button("Backup all data","export",WHITE,()->{pending="backup";Intent i=new Intent(Intent.ACTION_CREATE_DOCUMENT);i.setType("application/zip");i.addCategory(Intent.CATEGORY_OPENABLE);i.putExtra(Intent.EXTRA_TITLE,"A-Day-To-Keep-Backup-"+LocalDate.now()+".zip");startActivityForResult(i,103);}));space(backups,9);backups.addView(button("Restore a backup","book",WHITE,()->{Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.setType("*/*");i.addCategory(Intent.CATEGORY_OPENABLE);startActivityForResult(i,104);}));space(backups,9);backups.addView(text("Includes your journal, photo copies, schedule, tasks, repeat intervals, theme and sound setting. Restore replaces existing data. Backups and PDFs are not encrypted. Save backups before uninstalling.\n\nKeep patient-identifiable details and clinical photographs out of your journal.\n\nA Day To Keep · Version 2.0",13));p.addView(backups);space(p,18);
 }
 """)
 one('deleteTree(old);deleteTree(staging);resetDaily();settings();','deleteTree(old);deleteTree(staging);applyTheme();migrateTasks();resetDaily();settings();')
 s=s.replace('Little Days','A Day To Keep').replace('Little-Days','A-Day-To-Keep')
 for old,new in [('color(0xFFAE96C7);','color(blend(LILAC,INK,.25f));'),('color(0xFF91BCA3);','color(blend(MINT,INK,.24f));'),('color(0xFFE4A0B4);','color(blend(PINK,INK,.20f));'),('color(0xFFB69ACA);','color(blend(LILAC,INK,.25f));'),('color(0xFFCB92A7);','color(blend(PINK,INK,.25f));'),('color(0xFF78A78D);','color(blend(MINT,INK,.30f));'),('color(0xFF8DB59F);','color(blend(MINT,INK,.30f));'),('color(0xFFC58FA9);','color(blend(PINK,INK,.30f));')]:s=s.replace(old,new)
 block('class Gingham extends','class Icon extends',r"""int blend(int a,int b,float f){return Color.rgb((int)(Color.red(a)*(1-f)+Color.red(b)*f),(int)(Color.green(a)*(1-f)+Color.green(b)*f),(int)(Color.blue(a)*(1-f)+Color.blue(b)*f));}
 class Gingham extends Pattern {Gingham(){super(theme,themeIndex);}}
 class Pattern extends android.graphics.drawable.Drawable {
  ThemeSpec palette;int kind;Paint p=new Paint(3);Pattern(ThemeSpec t,int k){palette=t;kind=k;}
  public void draw(Canvas c){if(palette==null){c.drawColor(0xFFFFF7F3);return;}c.drawColor(palette.cream);int width=getBounds().width(),height=getBounds().height();p.setColor(blend(palette.cream,palette.pink,.48f));int step=dp(kind==0?23:42);
   if(kind==0){for(int x=0;x<width;x+=step*2)c.drawRect(x,0,x+step,height,p);for(int y=0;y<height;y+=step*2)c.drawRect(0,y,width,y+step,p);p.setColor(blend(palette.cream,palette.pink,.8f));for(int y=dp(55);y<height;y+=dp(126))for(int x=dp(27);x<width;x+=dp(105)){c.drawOval(x,y,x+dp(9),y+dp(12),p);}}
   else if(kind==1){for(int y=dp(20);y<height;y+=step*2)for(int x=dp(12)+(y/step%2)*step;x<width;x+=step*2){c.drawCircle(x,y,dp(7),p);c.drawCircle(x+dp(9),y-dp(3),dp(9),p);c.drawCircle(x+dp(18),y,dp(7),p);}}
   else if(kind==2){for(int y=dp(14);y<height;y+=step)for(int x=dp(14)+(y/step%2)*step/2;x<width;x+=step)c.drawCircle(x,y,dp(3),p);}
   else if(kind==3){p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(dp(1));for(int y=dp(20);y<height;y+=step*2)for(int x=dp(20);x<width;x+=step*2){c.drawOval(x-dp(13),y-dp(5),x+dp(13),y+dp(5),p);c.drawOval(x-dp(20),y-dp(9),x+dp(20),y+dp(9),p);}p.setStyle(Paint.Style.FILL);}
   else{p.setStrokeWidth(dp(1));for(int y=dp(20);y<height;y+=step)for(int x=dp(18)+(y/step%2)*step/2;x<width;x+=step){c.drawLine(x-dp(3),y,x+dp(3),y,p);c.drawLine(x,y-dp(3),x,y+dp(3),p);c.drawCircle(x+dp(18),y+dp(15),dp(1),p);}}
  }
  public void setAlpha(int a){}public void setColorFilter(ColorFilter f){}public int getOpacity(){return PixelFormat.OPAQUE;}
 }
 """)
 s=s.replace('toast(req==102?"PDF saved":"Backup saved");','runOnUiThread(()->chime(readySound));toast(req==102?"PDF saved":"Backup saved");')
 p.write_text(s,encoding='utf-8')
gradle=root/'app/build.gradle'
g=gradle.read_text();g=re.sub(r'versionCode\s+\d+', 'versionCode 2',g);g=re.sub(r'versionName\s+[\'\"][^\'\"]+[\'\"]','versionName "2.0"',g);gradle.write_text(g)
manifest=root/'app/src/main/AndroidManifest.xml'
m=manifest.read_text().replace('android:label="Little Days"','android:label="A Day To Keep"').replace('android:icon="@drawable/app_icon"','android:icon="@mipmap/ic_launcher" android:roundIcon="@mipmap/ic_launcher_round"')
manifest.write_text(m)
res=root/'app/src/main/res'
def write(rel,text):
 q=res/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text,encoding='utf-8')
write('values/icon_colors.xml','<resources><color name="launcher_background">#F4CFDC</color></resources>')
foreground="""<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
<path android:fillColor="#FFF9F2" android:strokeColor="#8C6E85" android:strokeWidth="1.7" android:pathData="M33,49C24,22 38,17 44,42C50,39 58,39 64,42C70,17 84,22 75,49C94,80 14,80 33,49Z"/>
<path android:fillColor="#EDB0C3" android:pathData="M35,28C32,27 34,37 38,42C42,44 39,31 35,28M73,28C76,27 74,37 70,42C66,44 69,31 73,28M32,62a6,3 0,1 0,12,0a6,3 0,1 0,-12,0M64,62a6,3 0,1 0,12,0a6,3 0,1 0,-12,0"/>
<path android:fillColor="#775C70" android:pathData="M42,55a2,2 0,1 0,0.1,0M64,55a2,2 0,1 0,0.1,0M51,60L57,60L54,64Z"/>
<path android:fillColor="#D694AC" android:pathData="M76,77C68,70 61,80 76,89C91,80 84,70 76,77Z"/>
</vector>"""
write('drawable/launcher_foreground.xml',foreground)
for name in ['ic_launcher','ic_launcher_round']:
 write('mipmap-anydpi-v26/'+name+'.xml','<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/launcher_background"/><foreground android:drawable="@drawable/launcher_foreground"/></adaptive-icon>')
assets=root/'app/src/main/assets/fonts';assets.mkdir(parents=True,exist_ok=True)
fonts=[('Chewy','Chewy-Regular.ttf',['ofl/chewy','apache/chewy']),('PatrickHand','PatrickHand-Regular.ttf',['ofl/patrickhand']),('Mali','Mali-Regular.ttf',['ofl/mali'])]
def download(url):
 last=None
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'A-Day-To-Keep-Build'}),timeout=45) as response:return response.read()
  except Exception as e:last=e;time.sleep(attempt+1)
 raise last
for name,filename,dirs in fonts:
 if (assets/(name+'.ttf')).exists() and (assets/(name+'-LICENSE.txt')).exists():continue
 error=None
 for folder in dirs:
  try:
   base='https://raw.githubusercontent.com/google/fonts/main/'+folder+'/'
   content=download(base+filename)
   if content[:4] not in (b'\x00\x01\x00\x00',b'OTTO',b'ttcf'):raise RuntimeError('Downloaded file is not a font')
   license_text=None
   for license_name in ['OFL.txt','LICENSE.txt']:
    try:
     license_text=download(base+license_name);break
    except Exception:pass
   if license_text is None:raise RuntimeError('Font license not found')
   (assets/(name+'.ttf')).write_bytes(content);(assets/(name+'-LICENSE.txt')).write_bytes(license_text)
   break
  except Exception as e:error=e
 else:raise RuntimeError('Could not download '+name+' and its license: '+str(error))
raw=res/'raw';raw.mkdir(parents=True,exist_ok=True)
for name,notes in [('check',[(660,.08),(880,.13)]),('soft',[(580,.09)]),('ready',[(523.25,.10),(659.25,.10),(783.99,.15)])]:
 samples=[];sr=22050
 for frequency,duration in notes:
  for i in range(int(sr*duration)):
   t=i/sr;fade=min(1,t/.018)*max(0,1-t/duration)**2
   value=.20*fade*(math.sin(2*math.pi*frequency*t)+.16*math.sin(2*math.pi*frequency*2*t))
   samples.append(int(max(-1,min(1,value))*32767))
  samples.extend([0]*int(.012*sr))
 with wave.open(str(raw/(name+'.wav')),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(struct.pack('<'+'h'*len(samples),*samples))
(root/'UPDATE-NOTES.txt').write_text("""A Day To Keep 2.0
Name/icon refresh; five illustrated themes; bundled Chewy, Patrick Hand and Mali fonts;
custom dialog styling; individually repeating checklist items; sound toggle; corrected
schedule positioning; separate home panels. Existing task intervals default to one day.
Repeat intervals are counted from the date a task is checked. All tasks remain visible.
Automatically resetting tasks is optional. Themes, sounds and recurrence data are backed up.
The Android system file picker cannot be reskinned by this app.
Original application ID and signing key preserved. Do not uninstall before updating.
This project was generated with static checks; perform device testing before relying on it.
""")
print('A Day To Keep 2.0 source/assets prepared; original signing identity preserved.')
