#!/usr/bin/env python3
"""A Day To Keep v4; run after the existing v2 and v3 scripts."""
from pathlib import Path
import re
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text(encoding='utf-8')
MARK='// A_DAY_TO_KEEP_V4'
if '// A_DAY_TO_KEEP_V3' not in s:raise SystemExit('Run update_app.py then update_style.py before update_refine.py')
def one(old,new):
 global s
 if old not in s:raise RuntimeError('Expected source not found: '+old[:140])
 s=s.replace(old,new,1)
def block(start,end,new):
 global s
 a=s.find(start)
 if a<0:raise RuntimeError('Expected method missing: '+start)
 b=s.find(end,a+len(start))
 if b<0:raise RuntimeError('Expected next method missing: '+end)
 s=s[:a]+new+'\n '+s[b:]
if MARK not in s:
 extra=r""",
  new ThemeSpec("Lavender Lamb","Lavender blossoms, yarn & fluffy clouds","lamb","PatrickHand","Mali",0xFF6B6081,0xFFE8DFF2,0xFFE0E1F5,0xFFE5EDDC,0xFFF9F5FD,0xFFFFFDFF),
  new ThemeSpec("Sakura Shiba","Cherry blossoms, peaches & warm little paws","shiba","Chewy","PatrickHand",0xFF875F64,0xFFF6D9E1,0xFFF0DEDA,0xFFE6EDD9,0xFFFFF5F5,0xFFFFFDFC),
  new ThemeSpec("Cosy Capybara","Oranges, tea & a little garden pond","capybara","Mali","PatrickHand",0xFF79624F,0xFFF2DDC1,0xFFE9E3CE,0xFFDCEAD9,0xFFFFFAEF,0xFFFFFEF9),
  new ThemeSpec("Snowdrop Penguin","Icy bubbles, snowflakes & tiny stars","penguin","PatrickHand","Mali",0xFF526E85,0xFFDDEBF5,0xFFE4E5F5,0xFFE0EFEB,0xFFF3FAFF,0xFFFDFFFF),
  new ThemeSpec("Little Dream Dragon","Pastel potions, crystals & wishes","dragon","Chewy","Mali",0xFF666483,0xFFE5DEF4,0xFFDCE7F4,0xFFDBEEDD,0xFFF6F5FE,0xFFFDFDFF)
 """
 match=re.search(r'(final ThemeSpec\[\] themes=\{)(.*?)(\n\s*\};)',s,re.S)
 if not match:raise RuntimeError('Theme array not found')
 s=s[:match.start()]+match.group(1)+match.group(2).rstrip()+extra+match.group(3)+s[match.end():]
 # Fixed, creation-anchored recurrence. Old task creation dates were not stored.
 block('void migrateTasks(){','LinearLayout section(',r"""// A_DAY_TO_KEEP_V4
 void migrateTasks(){boolean changed=false;for(int i=0;i<tasks.length();i++){JSONObject t=tasks.optJSONObject(i);if(t==null)continue;try{if(!t.has("repeat")){t.put("repeat",1);changed=true;}if(!t.has("createdOn")){t.put("createdOn",LocalDate.now().toString());changed=true;}if(t.optBoolean("done")&&!t.has("completedOn")){t.put("completedOn",data.optString("lastDay",LocalDate.now().toString()));changed=true;}}catch(Exception ignored){}}if(changed)save();}
 boolean taskDue(JSONObject t,LocalDate day){try{LocalDate anchor=LocalDate.parse(t.optString("createdOn",day.toString()));long elapsed=java.time.temporal.ChronoUnit.DAYS.between(anchor,day);return elapsed>=0&&elapsed%Math.max(1,t.optInt("repeat",1))==0;}catch(Exception e){return true;}}
 int cardSequence=0;
 void edgeToEdge(){Window w=getWindow();w.setDecorFitsSystemWindows(false);w.setStatusBarColor(Color.TRANSPARENT);w.setNavigationBarColor(Color.TRANSPARENT);w.setStatusBarContrastEnforced(false);w.setNavigationBarContrastEnforced(false);WindowInsetsController controller=w.getInsetsController();if(controller!=null)controller.setSystemBarsAppearance(WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS|WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS,WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS|WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS);}
 """)
 block('void resetDaily(){','int dp(',r"""void resetDaily(){String today=LocalDate.now().toString();boolean changed=false;if(data.optBoolean("resetDaily",true)){for(int i=0;i<tasks.length();i++){JSONObject t=tasks.optJSONObject(i);if(t==null||!taskDue(t,LocalDate.now())||!t.optBoolean("done"))continue;if(!today.equals(t.optString("completedOn"))){try{t.put("done",false);t.remove("completedOn");changed=true;}catch(Exception ignored){}}}}if(!today.equals(data.optString("lastDay"))){try{data.put("lastDay",today);}catch(Exception ignored){}changed=true;}if(changed)save();}
 """)
 one('o.put("repeat",interval);','o.put("repeat",interval);o.put("createdOn",LocalDate.now().toString());')
 s=s.replace('Completed tasks reset after this many days.\\nAll tasks stay visible in your list.','Show this task every N days, starting today.\\nOnly scheduled tasks appear on the home screen.')
 # The literal Java text contains a single slash-n escape.
 s=s.replace(r'Completed tasks reset after this many days.\nAll tasks stay visible in your list.',r'Show this task every N days, starting today.\nOnly scheduled tasks appear on the home screen.')
 old='Each task resets using its own repeat interval, counted from the day you check it. Every day = 1; every two days = 2. With this off, ticks stay until you clear them. Tasks are never hidden or removed. When the app is closed, resets happen on the next open.'
 new='Tasks appear on their scheduled dates, counting from creation: 1 = daily; 2 = every other day. This switch clears the tick on the next scheduled appearance. Off keeps ticks until you clear them. Off-day tasks are hidden, not deleted. Existing tasks start their schedule on the first opening after this update.'
 one(old,new)
 # Root draws behind transparent bars; interactive content remains inside system/IME insets.
 block('void base(String title,boolean back){','void render(',r"""void base(String title,boolean back){edgeToEdge();cardSequence=0;root=col();root.setBackground(new Gingham());root.setClipChildren(false);root.setClipToPadding(false);root.setPadding(dp(16),dp(10),dp(16),dp(20));setContentView(root);root.setOnApplyWindowInsetsListener((view,insets)->{android.graphics.Insets bars=insets.getInsets(WindowInsets.Type.systemBars()|WindowInsets.Type.displayCutout());android.graphics.Insets keyboard=insets.getInsets(WindowInsets.Type.ime());view.setPadding(dp(16)+bars.left,dp(10)+bars.top,dp(16)+bars.right,dp(20)+Math.max(bars.bottom,keyboard.bottom));return insets;});root.requestApplyInsets();LinearLayout top=row();if(back)top.addView(button("Home","home",WHITE,()->home()));TextView h=label(title,back?22:26);h.setPadding(dp(10),dp(3),0,dp(3));h.setMaxLines(2);top.addView(h,new LinearLayout.LayoutParams(0,dp(58),1));if(!back)top.addView(button("","gear",WHITE,()->settings()));root.addView(top);space(root,8);}
 """)
 one('getWindow().setStatusBarColor(CREAM);getWindow().setNavigationBarColor(CREAM);','getWindow().setStatusBarColor(Color.TRANSPARENT);getWindow().setNavigationBarColor(Color.TRANSPARENT);')
 block('LinearLayout section(int color){','void styleTree(',r"""LinearLayout section(int color){LinearLayout box=col();box.setPadding(dp(11),dp(11),dp(11),dp(11));box.setBackground(new FloatingCard(color,themeIndex,++cardSequence));box.setElevation(dp(2));box.setClipChildren(true);box.setClipToPadding(true);return box;}
 class FloatingCard extends BevelDrawable {
  final int index,seed;final StickerPainter painter=new StickerPainter();final Paint shine=new Paint(3);
  final Runnable frame=()->invalidateSelf();
  FloatingCard(int color,int i,int id){super(color);index=i;seed=1777+i*101+id*997;}
  @Override public boolean setVisible(boolean visible,boolean restart){if(!visible)unscheduleSelf(frame);return super.setVisible(visible,restart);}
  @Override public void draw(Canvas c){super.draw(c);Rect b=getBounds();int save=c.save();Path clip=new Path();clip.addRoundRect(new RectF(b),dp(22),dp(22),Path.Direction.CW);c.clipPath(clip);String[] names=motifs(index);Random random=new Random(seed);float phase=motionEnabled()?(SystemClock.uptimeMillis()%24000)/1000f:0;float area=Math.max(1,b.width()/(float)dp(75))*Math.max(1,b.height()/(float)dp(75));int count=Math.max(6,Math.min(26,(int)(area*1.2f)));
   for(int i=0;i<count;i++){float size=dp(23+random.nextInt(14));float xx=b.left+dp(4)+random.nextFloat()*Math.max(1,b.width()-size-dp(8));float yy=b.top+dp(4)+random.nextFloat()*Math.max(1,b.height()-size-dp(8));float offset=random.nextFloat()*6.28f;float tilt=random.nextFloat()*34-17;if(motionEnabled()){xx+=(float)Math.sin(phase*1.1+offset)*dp(3.5f);yy+=(float)Math.cos(phase*1.35+offset)*dp(4.5f);tilt+=(float)Math.sin(phase*.9+offset)*8;}int rotation=c.save();c.rotate(tilt,xx+size/2,yy+size/2);painter.draw(c,names[random.nextInt(names.length)],xx,yy,size,88);c.restoreToCount(rotation);}
   c.restoreToCount(save);if(motionEnabled()&&isVisible()){unscheduleSelf(frame);scheduleSelf(frame,SystemClock.uptimeMillis()+40);}else unscheduleSelf(frame);
  }
 }
 """)
 block('void home(){','String ordinal(',r"""void home(){screen="home";editor=null;resetDaily();base("A Day To Keep",false);
 LinearLayout banner=row();banner.addView(new Mascot(theme.character,PINK),new LinearLayout.LayoutParams(dp(52),dp(54)));LinearLayout words=col();words.setPadding(dp(9),0,0,0);words.addView(label("Make a little room for you",18));words.addView(text("Little plans. Lovely memories.",13));banner.addView(words,new LinearLayout.LayoutParams(0,-2,1));root.addView(banner);space(root,9);
 LinearLayout work=section(LILAC);work.addView(button("Work Schedule","calendar",WHITE,()->calendar("work",LocalDate.now(),null)),new LinearLayout.LayoutParams(-1,-2));space(work,8);
 HorizontalScrollView strip=new HorizontalScrollView(this);strip.setHorizontalScrollBarEnabled(false);strip.setOverScrollMode(View.OVER_SCROLL_NEVER);strip.setClipChildren(true);strip.setClipToPadding(true);strip.setPadding(0,0,0,0);LinearLayout days=row();days.setClipChildren(true);LocalDate today=LocalDate.now();int width=Math.max(dp(46),(getResources().getDisplayMetrics().widthPixels-dp(54))/6);final View[] todayCard={null};
 for(int n=-30;n<=365;n++){LocalDate d=today.plusDays(n);LinearLayout card=col();card.setGravity(Gravity.CENTER);card.setPadding(dp(1),dp(7),dp(1),dp(7));GradientDrawable background=shape(d.equals(today)?PINK:WHITE);if(d.equals(today))background.setStroke(dp(2),INK);card.setBackground(background);TextView dow=label(d.format(DateTimeFormatter.ofPattern("EEE",Locale.UK)),13);dow.setGravity(Gravity.CENTER);card.addView(dow);Icon icon=new Icon(schedule.optString(d.toString(),"unset"));card.addView(icon,new LinearLayout.LayoutParams(dp(28),dp(30)));TextView date=text(d.format(DateTimeFormatter.ofPattern("MMM",Locale.UK))+" "+ordinal(d.getDayOfMonth()),11);date.setGravity(Gravity.CENTER);card.addView(date);LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(width-dp(4),dp(87));cp.setMargins(dp(2),0,dp(2),0);days.addView(card,cp);if(d.equals(today))todayCard[0]=card;card.setContentDescription(d.format(pretty)+", "+schedule.optString(d.toString(),"not set"));card.setOnClickListener(v->calendar("work",d,null));}
 strip.addView(days,new HorizontalScrollView.LayoutParams(-2,-2));work.addView(strip,new LinearLayout.LayoutParams(-1,dp(87)));root.addView(work);strip.post(()->{if(todayCard[0]!=null)strip.scrollTo(Math.max(0,todayCard[0].getLeft()-dp(2)),0);});space(root,12);
 LinearLayout cpd=section(PINK);cpd.addView(button("CPD · Your daily journal","book",WHITE,()->{selected=LocalDate.now();journal();}),new LinearLayout.LayoutParams(-1,-2));TextView caption=text("A place for today's thoughts & discoveries",12);caption.setPadding(dp(9),dp(5),0,0);cpd.addView(caption);root.addView(cpd);space(root,12);
 LinearLayout daily=section(MINT);LinearLayout title=row();TextView dailyHeading=label("Daily Stuff",23);dailyHeading.setPadding(dp(3),dp(4),0,dp(4));title.addView(dailyHeading,new LinearLayout.LayoutParams(0,-2,1));title.setMinimumHeight(dp(56));title.addView(button("Add","plus",WHITE,()->addTask()));daily.addView(title);TextView help=text("Hold & drag to reorder · Swipe right to remove",11);help.setPadding(dp(3),dp(3),dp(3),dp(5));daily.addView(help);space(daily,6);
 FrameLayout viewport=new FrameLayout(this);viewport.setClipChildren(true);viewport.setClipToPadding(true);ScrollView scroll=new ScrollView(this);scroll.setClipChildren(true);scroll.setClipToPadding(true);scroll.setPadding(0,0,0,0);scroll.setOverScrollMode(View.OVER_SCROLL_NEVER);scroll.setVerticalScrollBarEnabled(false);LinearLayout list=col();list.setClipChildren(true);list.setClipToPadding(true);scroll.addView(list,new ScrollView.LayoutParams(-1,-2));viewport.addView(scroll,new FrameLayout.LayoutParams(-1,-1));LinearLayout.LayoutParams area=new LinearLayout.LayoutParams(-1,0,1);area.setMargins(dp(3),0,dp(3),dp(3));daily.addView(viewport,area);root.addView(daily,new LinearLayout.LayoutParams(-1,0,1));buildTasks(list);
 }
 """)
 block('void buildTasks(LinearLayout list){','JSONObject entry(',r"""void buildTasks(LinearLayout list){int shown=0;
 for(int n=0;n<tasks.length();n++){JSONObject task=tasks.optJSONObject(n);if(task==null||!taskDue(task,LocalDate.now()))continue;shown++;String id=task.optString("id");LinearLayout r=row();r.setPadding(dp(8),dp(7),dp(10),dp(7));r.setBackground(shape(WHITE));r.setElevation(0);CheckBox box=new CheckBox(this);box.setButtonTintList(android.content.res.ColorStateList.valueOf(blend(LILAC,INK,.35f)));box.setChecked(task.optBoolean("done"));box.setClickable(false);box.setFocusable(false);r.addView(box);TextView t=text(task.optString("text"),17);t.setPadding(dp(4),dp(8),dp(4),dp(8));if(task.optBoolean("done"))t.setPaintFlags(t.getPaintFlags()|Paint.STRIKE_THRU_TEXT_FLAG);r.addView(t,new LinearLayout.LayoutParams(0,-2,1));TextView grip=text("≡",23);r.addView(grip);LinearLayout.LayoutParams rp=new LinearLayout.LayoutParams(-1,-2);rp.setMargins(0,0,0,dp(6));list.addView(r,rp);
 Runnable toggle=()->{try{boolean checked=!task.optBoolean("done");task.put("done",checked);if(checked)task.put("completedOn",LocalDate.now().toString());else task.remove("completedOn");save();chime(checked?checkSound:softSound);home();}catch(Exception ignored){}};
 final float[] start={0,0};final boolean[] dragging={false},swiped={false};
 r.setOnLongClickListener(v->{dragging[0]=true;r.setAlpha(.45f);v.startDragAndDrop(ClipData.newPlainText("task",id),new View.DragShadowBuilder(v),id,0);return true;});
 r.setOnTouchListener((v,e)->{switch(e.getActionMasked()){case MotionEvent.ACTION_DOWN:start[0]=e.getRawX();start[1]=e.getRawY();swiped[0]=false;dragging[0]=false;break;case MotionEvent.ACTION_MOVE:if(!dragging[0]&&e.getRawX()-start[0]>dp(24)&&Math.abs(e.getRawY()-start[1])<dp(42)){swiped[0]=true;r.setBackground(shape(PINK));v.getParent().requestDisallowInterceptTouchEvent(true);}break;case MotionEvent.ACTION_UP:if(swiped[0]&&!dragging[0]){ask("Remove task?","Remove ‘"+task.optString("text")+"’ from Daily Stuff?",()->{int i=taskIndex(id);if(i>=0)tasks.remove(i);save();home();},()->r.setBackground(shape(WHITE)));return true;}break;case MotionEvent.ACTION_CANCEL:r.setBackground(shape(WHITE));break;}return false;});r.setOnClickListener(v->toggle.run());
 r.setOnDragListener((v,e)->{switch(e.getAction()){case DragEvent.ACTION_DRAG_STARTED:return e.getLocalState() instanceof String;case DragEvent.ACTION_DRAG_ENTERED:r.setBackground(shape(LILAC));return true;case DragEvent.ACTION_DRAG_EXITED:r.setBackground(shape(WHITE));return true;case DragEvent.ACTION_DROP:String source=(String)e.getLocalState();int from=taskIndex(source),to=taskIndex(id);if(from>=0&&to>=0&&from!=to){JSONObject moving=tasks.optJSONObject(from);tasks.remove(from);JSONArray arr=new JSONArray();for(int k=0;k<=tasks.length();k++){if(k==to)arr.put(moving);if(k<tasks.length())arr.put(tasks.optJSONObject(k));}tasks=arr;try{data.put("tasks",tasks);}catch(Exception ignored){}save();}home();return true;case DragEvent.ACTION_DRAG_ENDED:r.setAlpha(1);r.setBackground(shape(WHITE));return true;}return true;});
 }
 if(shown==0){TextView empty=text(tasks.length()==0?"A fresh little list, ready for you.":"A little breathing space — no tasks scheduled today.",16);empty.setPadding(dp(14),dp(18),dp(14),dp(18));empty.setBackground(shape(WHITE));list.addView(empty,new LinearLayout.LayoutParams(-1,-2));}}
 """)
 # Reparent the native action buttons into an explicitly padded, wrap-content footer.
 # getButton() retains the same Button instances so existing custom click listeners still work.
 block('void showCute(AlertDialog d){','void ask(',r"""void showCute(AlertDialog d){d.show();Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(shape(CREAM));w.setDimAmount(.32f);}View content=d.findViewById(android.R.id.content);if(content!=null)styleTree(content);int titleId=getResources().getIdentifier("alertTitle","id","android");TextView heading=d.findViewById(titleId);if(heading!=null){heading.setTypeface(headingFont);heading.setTextColor(INK);heading.setTextSize(24);heading.setIncludeFontPadding(true);heading.setPadding(heading.getPaddingLeft(),dp(10),heading.getPaddingRight(),dp(12));}
 ArrayList<Button> buttons=new ArrayList<>();ViewGroup panel=null;for(int which:new int[]{DialogInterface.BUTTON_NEUTRAL,DialogInterface.BUTTON_NEGATIVE,DialogInterface.BUTTON_POSITIVE}){Button b=d.getButton(which);if(b!=null&&b.getVisibility()!=View.GONE){buttons.add(b);if(panel==null&&b.getParent() instanceof ViewGroup)panel=(ViewGroup)b.getParent();}}
 if(panel!=null){for(Button b:buttons){if(b.getParent() instanceof ViewGroup)((ViewGroup)b.getParent()).removeView(b);}panel.removeAllViews();panel.setClipChildren(false);panel.setClipToPadding(false);panel.setPadding(0,0,0,0);panel.setMinimumHeight(0);if(panel instanceof LinearLayout)((LinearLayout)panel).setOrientation(LinearLayout.VERTICAL);ViewGroup.LayoutParams pl=panel.getLayoutParams();if(pl!=null){pl.height=ViewGroup.LayoutParams.WRAP_CONTENT;panel.setLayoutParams(pl);}LinearLayout footer=row();footer.setGravity(Gravity.CENTER);footer.setPadding(dp(18),dp(16),dp(18),dp(18));footer.setClipChildren(false);footer.setClipToPadding(false);
  for(Button b:buttons){boolean positive=b==d.getButton(DialogInterface.BUTTON_POSITIVE);b.setTypeface(headingFont);b.setTextColor(INK);b.setTextSize(17);b.setAllCaps(false);b.setIncludeFontPadding(true);b.setGravity(Gravity.CENTER);b.setSingleLine(false);b.setMaxLines(2);b.setPadding(dp(10),dp(16),dp(10),dp(16));b.setMinHeight(dp(76));b.setMinimumHeight(dp(76));b.setStateListAnimator(null);b.setElevation(0);b.setTranslationY(0);b.setBackground(shape(positive?PINK:MINT));LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(0,-2,1);bp.setMargins(dp(4),0,dp(4),0);footer.addView(b,bp);}panel.addView(footer,new ViewGroup.LayoutParams(-1,-2));panel.requestLayout();}
 if(w!=null)w.getDecorView().post(()->{if(d.isShowing()){w.getDecorView().requestLayout();}});
 }
 """)
 # Faster, more noticeable motion without flashing; retains app/system animation toggles.
 s=s.replace('postDelayed(this,visible?80:500);','postDelayed(this,visible?40:500);')
 s=s.replace('Math.sin(phase*1.5+i)*dp(1.6f)','Math.sin(phase*1.5+i)*dp(3.2f)')
 s=s.replace('Math.sin(phase+i)*3:0','Math.sin(phase+i)*6:0')
 s=s.replace('Math.sin(phase()*1.3)*1.3f','Math.sin(phase()*1.3)*2.8f')
 block('String[] motifs(int index){','class Doodle extends',r"""String[] motifs(int index){switch(index){case 0:return new String[]{"carrot","strawberry","flower"};case 1:return new String[]{"cloud","star","rainbow"};case 2:return new String[]{"honey","bee","flower"};case 3:return new String[]{"lily","lotus","dragonfly"};case 4:return new String[]{"moon","planet","sparkle"};case 5:return new String[]{"mushroom","acorn","leaf"};case 6:return new String[]{"bamboo","dumpling","teacup"};case 7:return new String[]{"shell","seaweed","bubble"};case 8:return new String[]{"peach","daisy","heart"};case 9:return new String[]{"crystal","planet","sparkle"};case 10:return new String[]{"yarn","flower","cloud"};case 11:return new String[]{"sakura","peach","heart"};case 12:return new String[]{"orange","teacup","lily"};case 13:return new String[]{"snowflake","bubble","star"};default:return new String[]{"potion","crystal","sparkle"};}}
 """)
 # New mascot anatomy, sharing the existing expressive facial details.
 one('int fur=animal.equals("bear")?', 'int fur=animal.equals("lamb")?0xFFFFF8EC:animal.equals("shiba")?0xFFE4B07B:animal.equals("capybara")?0xFFC9A480:animal.equals("penguin")?0xFF90ACC4:animal.equals("dragon")?0xFFB9CEBC:animal.equals("bear")?')
 one('c.drawOval(14,29,86,86,p);',r"""if(animal.equals("lamb")){for(int i=0;i<7;i++){double a=Math.PI+i*Math.PI/6;c.drawCircle(50+(float)Math.cos(a)*30,43+(float)Math.sin(a)*15,12,p);}c.drawOval(13,39,29,60,p);c.drawOval(71,39,87,60,p);}
 if(animal.equals("shiba")){Path ears=new Path();ears.moveTo(18,46);ears.lineTo(22,8);ears.lineTo(43,34);ears.lineTo(58,34);ears.lineTo(78,8);ears.lineTo(83,46);ears.close();c.drawPath(ears,p);}
 if(animal.equals("capybara")){c.drawCircle(26,31,10,p);c.drawCircle(74,31,10,p);}
 if(animal.equals("dragon")){fill(0xFFE8CD9A);Path horns=new Path();horns.moveTo(25,37);horns.lineTo(28,10);horns.lineTo(42,34);horns.moveTo(58,34);horns.lineTo(72,10);horns.lineTo(75,37);c.drawPath(horns,p);fill(fur);c.drawOval(10,43,26,72,p);c.drawOval(74,43,90,72,p);}
 c.drawOval(14,29,86,86,p);
 if(animal.equals("penguin")){fill(0xFFFFFAF0);c.drawOval(24,41,76,88,p);}
 if(animal.equals("shiba")){fill(0xFFFFF1DE);c.drawOval(26,52,74,83,p);}
 if(animal.equals("capybara")){fill(0xFFB88E72);c.drawOval(32,57,68,77,p);}
 """)
 one('case "carrot":',r"""case "yarn":oval(10,13,53,55,0xFFD3BCE7);line(15,23,44,48,0xFFB69ACE,2);line(12,33,36,53,0xFFB69ACE,2);line(25,15,51,37,0xFFB69ACE,2);line(44,49,58,57,0xFFB69ACE,2);break;
 case "sakura":for(int i=0;i<5;i++){c.save();c.rotate(i*72,32,32);oval(23,6,41,32,0xFFF0B9CF);c.restore();}oval(26,26,38,38,0xFFF2D79B);break;
 case "orange":oval(10,16,55,57,0xFFF1BD79);oval(19,23,24,27,0xFFF9D6A2);line(32,18,34,10,0xFF9CB48B,3);oval(33,6,51,17,0xFFACC799);break;
 case "snowflake":for(int i=0;i<6;i++){c.save();c.rotate(i*60,32,32);line(32,9,32,33,0xFFADCFE6,3);line(24,16,32,24,0xFFADCFE6,2);line(40,16,32,24,0xFFADCFE6,2);c.restore();}oval(28,28,36,36,0xFFD9EAF7);break;
 case "potion":round(22,7,42,17,3,0xFFBDA8D4);round(26,15,38,29,3,0xFFE7E5F5);oval(12,24,52,58,0xFFDCE7EE);oval(16,33,48,55,0xFFCBB6DF);star(32,43,8,0xFFFFE6AA);break;
 case "carrot":
 """)
 s=s.replace('Version 3.0','Version 4.0')
 p.write_text(s,encoding='utf-8')
gradle=Path('app/build.gradle');g=gradle.read_text();g=re.sub(r'versionCode\s+\d+','versionCode 4',g);g=re.sub(r'versionName\s+[\'\"][^\'\"]+[\'\"]','versionName "4.0"',g);gradle.write_text(g)
Path('VERSION-4-NOTES.txt').write_text("""A Day To Keep 4.0
Creation-anchored checklist schedules. Only due tasks are displayed; no interval labels.
New tasks start on their actual creation day. Earlier versions did not record creation
so existing tasks are anchored to the first opening after this update, then remain fixed.
No existing tasks are deleted. Reordering and deletion operate on the stored task IDs.
Inset schedule/checklist scroll viewports; bottom shadow room; rebuilt dialog action footer.
More visible animation and scattered animated panel artwork instead of home doodle strips.
Edge-to-edge background under system bars; content kept clear of bars, cutouts and keyboard.
Five new themes (15 total), preserving older theme indices. Uses existing bundled fonts.
Includes all prior app features; signing key and package name unchanged. Backup first.
Generated with static checks only; GitHub build and on-device testing are still required.
""")
print('Version 4 recurrence, clipping, animated panels, edge-to-edge and five themes prepared.')
