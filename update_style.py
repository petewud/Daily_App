#!/usr/bin/env python3
"""Version 3 illustration/layout update. Run after update_app.py; retains signing identity."""
from pathlib import Path
import re
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text(encoding='utf-8')
MARK='// A_DAY_TO_KEEP_V3'
if '// A_DAY_TO_KEEP_V2' not in s:
 raise SystemExit('Run the existing update_app.py before this version-3 update.')
def one(old,new):
 global s
 if old not in s:raise RuntimeError('Expected source missing: '+old[:100])
 s=s.replace(old,new,1)
def block(start,end,new):
 global s
 a=s.find(start)
 if a<0:raise RuntimeError('Expected method missing: '+start)
 b=s.find(end,a+len(start))
 if b<0:raise RuntimeError('Expected next method missing: '+end)
 s=s[:a]+new+'\n '+s[b:]
if MARK not in s:
 # Keep original theme indices so existing saved preferences remain meaningful.
 extra=r""",
  new ThemeSpec("Woodland Fox","Mushrooms, acorns & little forest treasures","fox","Mali","PatrickHand",0xFF795E50,0xFFF2D8C2,0xFFE7DCCB,0xFFDDE8CF,0xFFFFF7ED,0xFFFFFCF7),
  new ThemeSpec("Bamboo Panda","Bamboo sprigs, dumplings & cosy tea","panda","Chewy","Mali",0xFF52665D,0xFFE1EAD8,0xFFE5E4DB,0xFFD5E9DD,0xFFF7FAEF,0xFFFEFFF9),
  new ThemeSpec("Seaside Otter","Seashells, seaweed & drifting bubbles","otter","PatrickHand","Mali",0xFF526D7E,0xFFD8EBEE,0xFFDDE6F7,0xFFD9EFE5,0xFFF0FAFD,0xFFFCFEFF),
  new ThemeSpec("Peach Duck","Peaches, daisies & tiny hearts","duck","Chewy","PatrickHand",0xFF806554,0xFFF8DDCE,0xFFF5E9CC,0xFFE3EAD4,0xFFFFF8EE,0xFFFFFDFA),
  new ThemeSpec("Starry Axolotl","Crystals, planets & sparkling wishes","axolotl","Mali","PatrickHand",0xFF6E5C86,0xFFF0DCEB,0xFFE1DDF7,0xFFDDEAF4,0xFFF8F2FC,0xFFFFFCFF)
 """
 match=re.search(r'(final ThemeSpec\[\] themes=\{)(.*?)(\n\s*\};)',s,re.S)
 if not match:raise RuntimeError('Theme array not found')
 s=s[:match.start()]+match.group(1)+match.group(2).rstrip()+extra+match.group(3)+s[match.end():]
 # Drawn, softly bevelled surfaces retain the original GradientDrawable return type.
 block('GradientDrawable shape(int color){','TextView text(',r"""GradientDrawable shape(int color){return new BevelDrawable(color);}
 class BevelDrawable extends GradientDrawable {
  int base;Paint edge=new Paint(3);
  BevelDrawable(int color){super(GradientDrawable.Orientation.TL_BR,new int[]{blend(color,Color.WHITE,.30f),color,blend(color,INK,.045f)});base=color;setCornerRadius(dp(22));setStroke(dp(1),blend(color,INK,.20f));}
  @Override public void draw(Canvas c){super.draw(c);Rect b=getBounds();edge.setStyle(Paint.Style.STROKE);edge.setStrokeWidth(dp(1));edge.setColor(0xA0FFFFFF);RectF r=new RectF(b.left+dp(2),b.top+dp(2),b.right-dp(2),b.bottom-dp(2));c.drawRoundRect(r,dp(20),dp(20),edge);}
 }
 class IllustratedCard extends BevelDrawable {
  int index;IllustratedCard(int color,int i){super(color);index=i;}
  @Override public void draw(Canvas c){super.draw(c);Rect b=getBounds();int save=c.save();Path clip=new Path();clip.addRoundRect(new RectF(b),dp(22),dp(22),Path.Direction.CW);c.clipPath(clip);String[] names=motifs(index);StickerPainter painter=new StickerPainter();float size=dp(30);painter.draw(c,names[0],b.right-size-dp(8),b.top+dp(7),size,72);painter.draw(c,names[1],b.right-size*2-dp(18),b.bottom-size-dp(4),size,53);c.restoreToCount(save);}
 }
 """)
 one('t.setFontFeatureSettings("kern");','t.setFontFeatureSettings("kern");t.setIncludeFontPadding(true);t.setLineSpacing(dp(1),1f);')
 block('View button(String title,','void base(',r"""View button(String title,String icon,int color,Runnable action){LinearLayout r=row();r.setClipChildren(false);r.setClipToPadding(false);r.setBackground(shape(color));r.setElevation(dp(1));r.setMinimumHeight(dp(56));
 if(title==null||title.trim().isEmpty()){r.setGravity(Gravity.CENTER);r.setPadding(0,0,0,0);r.setMinimumWidth(dp(50));r.setMinimumHeight(dp(50));if(icon!=null)r.addView(new Icon(icon),new LinearLayout.LayoutParams(dp(27),dp(27)));r.setContentDescription("gear".equals(icon)?"Settings":icon);r.setLayoutParams(new LinearLayout.LayoutParams(dp(50),dp(50)));}
 else {r.setPadding(dp(12),dp(9),dp(12),dp(9));if(icon!=null)r.addView(new Icon(icon),new LinearLayout.LayoutParams(dp(27),dp(27)));TextView t=label(title,16);t.setIncludeFontPadding(true);t.setGravity(Gravity.CENTER_VERTICAL);t.setPadding(dp(7),dp(3),dp(3),dp(3));r.addView(t);r.setContentDescription(title);}
 r.setOnClickListener(v->{chime(softSound);action.run();});return r;}
 """)
 # The schedule's mode controls expect an icon followed by a label; all nonempty buttons keep that layout.
 block('void showCute(AlertDialog d){','void ask(',r"""void showCute(AlertDialog d){d.show();Window window=d.getWindow();if(window!=null){window.setBackgroundDrawable(shape(CREAM));window.setDimAmount(.32f);}View content=d.findViewById(android.R.id.content);if(content!=null){styleTree(content);if(content instanceof ViewGroup){((ViewGroup)content).setClipChildren(false);((ViewGroup)content).setClipToPadding(false);}}int titleId=getResources().getIdentifier("alertTitle","id","android");TextView heading=d.findViewById(titleId);if(heading!=null){heading.setTypeface(headingFont);heading.setTextColor(INK);heading.setIncludeFontPadding(true);heading.setTextSize(24);heading.setPadding(heading.getPaddingLeft(),dp(9),heading.getPaddingRight(),dp(9));}
 Runnable measureButtons=()->{int tallest=dp(58);for(int which:new int[]{DialogInterface.BUTTON_POSITIVE,DialogInterface.BUTTON_NEGATIVE,DialogInterface.BUTTON_NEUTRAL}){Button b=d.getButton(which);if(b==null||b.getVisibility()==View.GONE)continue;b.setTypeface(headingFont);b.setTextColor(INK);b.setAllCaps(false);b.setTextSize(17);b.setIncludeFontPadding(true);b.setGravity(Gravity.CENTER);b.setSingleLine(false);b.setMaxLines(2);b.setPadding(dp(17),dp(12),dp(17),dp(12));Paint.FontMetricsInt fm=b.getPaint().getFontMetricsInt();int height=Math.max(dp(58),fm.bottom-fm.top+dp(26));tallest=Math.max(tallest,height);b.setMinHeight(height);b.setMinimumHeight(height);b.setBackground(shape(which==DialogInterface.BUTTON_POSITIVE?PINK:MINT));ViewGroup.LayoutParams raw=b.getLayoutParams();if(raw!=null){raw.height=ViewGroup.LayoutParams.WRAP_CONTENT;if(raw instanceof ViewGroup.MarginLayoutParams){ViewGroup.MarginLayoutParams lp=(ViewGroup.MarginLayoutParams)raw;lp.setMargins(dp(4),dp(6),dp(4),dp(7));}b.setLayoutParams(raw);}ViewParent parent=b.getParent();if(parent instanceof ViewGroup){ViewGroup group=(ViewGroup)parent;group.setClipChildren(false);group.setClipToPadding(false);group.setMinimumHeight(height+dp(22));group.setPadding(group.getPaddingLeft(),dp(4),group.getPaddingRight(),dp(4));ViewGroup.LayoutParams lp=group.getLayoutParams();if(lp!=null){lp.height=ViewGroup.LayoutParams.WRAP_CONTENT;group.setLayoutParams(lp);}}}};measureButtons.run();if(window!=null)window.getDecorView().post(measureButtons);}
 """)
 # Rebuild section backgrounds and align Daily Stuff with the inset task-card edges.
 block('LinearLayout section(int color){','void styleTree(',r"""LinearLayout section(int color){LinearLayout box=col();box.setPadding(dp(11),dp(11),dp(11),dp(11));box.setBackground(new IllustratedCard(color,themeIndex));box.setElevation(dp(2));box.setClipChildren(false);box.setClipToPadding(false);return box;}
 """)
 one('title.addView(label("Daily Stuff",23),new LinearLayout.LayoutParams(0,dp(46),1));', 'TextView dailyHeading=label("Daily Stuff",23);dailyHeading.setPadding(dp(3),dp(4),0,dp(4));title.addView(dailyHeading,new LinearLayout.LayoutParams(0,-2,1));title.setMinimumHeight(dp(56));')
 one('daily.addView(text("Hold & drag to reorder · Swipe right to remove",11));','TextView dailyHelp=text("Hold & drag to reorder · Swipe right to remove",11);dailyHelp.setPadding(dp(3),dp(3),dp(3),dp(5));daily.addView(dailyHelp);')
 one('root.addView(banner);space(root,10);','root.addView(banner);Doodle greeting=new Doodle(themeIndex);root.addView(greeting,new LinearLayout.LayoutParams(-1,dp(35)));space(root,4);')
 one('root.addView(cpd);space(root,12);','Doodle journalTrim=new Doodle(themeIndex);cpd.addView(journalTrim,new LinearLayout.LayoutParams(-1,dp(27)));root.addView(cpd);space(root,12);')
 # Header decoration on each journal date, not just on the home screen.
 one('content.addView(text("What happened? What did you learn?",14));','content.addView(new Doodle(themeIndex),new LinearLayout.LayoutParams(-1,dp(33)));content.addView(text("What happened? What did you learn?",14));')
 # Animations setting is on by default and is included in existing JSON backups automatically.
 one('options.addView(label("Little preferences",22));','options.addView(label("Little preferences",22));Switch animationToggle=new Switch(this);animationToggle.setText("Gentle animations");animationToggle.setTextColor(INK);animationToggle.setTypeface(bodyFont);animationToggle.setPadding(dp(3),dp(12),dp(3),dp(12));animationToggle.setChecked(data.optBoolean("animations",true));animationToggle.setOnCheckedChangeListener((v,on)->{try{data.put("animations",on);save();settings();}catch(Exception ignored){}});options.addView(animationToggle);options.addView(text("Softly floating illustrations and characters. Off keeps the artwork still. Also respects Android\\\'s animation setting.",12));space(options,8);')
 # Avoid apostrophe escaping ambiguities in Java strings.
 s=s.replace("Android\\\'s", "Android's")
 # Replace the original character with a richer set; all drawing stays local/offline.
 block('class Mascot extends View {','JSONObject data;',r"""
 // A_DAY_TO_KEEP_V3
 boolean motionEnabled(){return data!=null&&data.optBoolean("animations",true)&&android.animation.ValueAnimator.areAnimatorsEnabled();}
 abstract class AnimatedArt extends View {
  final Rect visibility=new Rect();
  final Runnable pulse=new Runnable(){public void run(){if(!isAttachedToWindow()||!motionEnabled()||getWindowVisibility()!=View.VISIBLE)return;boolean visible=getGlobalVisibleRect(visibility);if(visible)invalidate();postDelayed(this,visible?80:500);}};
  AnimatedArt(){super(MainActivity.this);setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_NO);}
  @Override protected void onAttachedToWindow(){super.onAttachedToWindow();removeCallbacks(pulse);post(pulse);}
  @Override protected void onDetachedFromWindow(){removeCallbacks(pulse);super.onDetachedFromWindow();}
  @Override protected void onWindowVisibilityChanged(int visibility){super.onWindowVisibilityChanged(visibility);if(pulse!=null){removeCallbacks(pulse);if(visibility==View.VISIBLE)post(pulse);}}
  float phase(){return motionEnabled()?(SystemClock.uptimeMillis()%16000)/1000f:0;}
 }
 String[] motifs(int index){switch(index){case 0:return new String[]{"carrot","strawberry","flower"};case 1:return new String[]{"cloud","star","rainbow"};case 2:return new String[]{"honey","bee","flower"};case 3:return new String[]{"lily","lotus","dragonfly"};case 4:return new String[]{"moon","planet","sparkle"};case 5:return new String[]{"mushroom","acorn","leaf"};case 6:return new String[]{"bamboo","dumpling","teacup"};case 7:return new String[]{"shell","seaweed","bubble"};case 8:return new String[]{"peach","daisy","heart"};default:return new String[]{"crystal","planet","sparkle"};}}
 class Doodle extends AnimatedArt {
  int index;StickerPainter painter=new StickerPainter();Doodle(int i){index=i;}
  protected void onDraw(Canvas c){super.onDraw(c);float size=Math.min(getHeight()-dp(3),dp(37));if(size<=0)return;String[] names=motifs(index);int count=Math.max(3,Math.min(6,(int)(getWidth()/dp(61))));float gap=getWidth()/(float)count;float phase=phase();for(int i=0;i<count;i++){float shift=motionEnabled()?(float)Math.sin(phase*1.5+i)*dp(1.6f):0;float x=(i+.5f)*gap-size/2,y=(getHeight()-size)/2+shift;int save=c.save();c.rotate(motionEnabled()?(float)Math.sin(phase+i)*3:0,x+size/2,y+size/2);painter.draw(c,names[i%3],x,y,size,220);c.restoreToCount(save);}}
 }
 class Mascot extends AnimatedArt {
  String animal;int accent;Paint p=new Paint(3);Mascot(String a,int color){animal=a;accent=color;}
  void fill(int color){p.setStyle(Paint.Style.FILL);p.setColor(color);}
  protected void onDraw(Canvas canvas){Canvas c=canvas;c.save();c.scale(getWidth()/100f,getHeight()/100f);c.translate(0,motionEnabled()?(float)Math.sin(phase()*1.3)*1.3f:0);fill(accent);c.drawCircle(50,51,43,p);int fur=animal.equals("bear")?0xFFD8AE82:animal.equals("frog")?0xFFA9CBA1:animal.equals("fox")?0xFFE5A374:animal.equals("otter")?0xFFC9AA92:animal.equals("duck")?0xFFFFE7A0:animal.equals("axolotl")?0xFFF0C5DD:0xFFFFFCF5;fill(fur);
   if(animal.equals("bunny")){c.drawOval(24,3,41,52,p);c.drawOval(59,3,76,52,p);}
   if(animal.equals("cat")||animal.equals("fox")){Path ears=new Path();ears.moveTo(17,49);ears.lineTo(19,9);ears.lineTo(43,34);ears.lineTo(59,34);ears.lineTo(81,9);ears.lineTo(84,49);ears.close();c.drawPath(ears,p);}
   if(animal.equals("bear")||animal.equals("otter")||animal.equals("panda")){if(animal.equals("panda"))fill(0xFF6F6B70);c.drawCircle(25,29,14,p);c.drawCircle(75,29,14,p);fill(fur);}
   if(animal.equals("frog")){c.drawCircle(28,31,16,p);c.drawCircle(72,31,16,p);}
   if(animal.equals("axolotl")){fill(0xFFD7A4C9);for(int side:new int[]{-1,1}){c.save();c.translate(50,50);for(int i=-1;i<=1;i++){c.save();c.rotate(i*23);c.drawOval(side<0?-49:25,-6,side<0?-25:49,6,p);c.restore();}c.restore();}fill(fur);}
   c.drawOval(14,29,86,86,p);
   if(animal.equals("fox")||animal.equals("otter")){fill(0xFFFFF4E7);c.drawOval(24,48,76,83,p);}
   if(animal.equals("panda")){fill(0xFF777079);c.drawOval(26,43,44,65,p);c.drawOval(56,43,74,65,p);}
   fill(animal.equals("panda")?Color.WHITE:0xFF745C6B);c.drawCircle(36,54,2.8f,p);c.drawCircle(64,54,2.8f,p);
   if(animal.equals("duck")){fill(0xFFE8AA67);c.drawOval(42,60,58,69,p);}else{p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2.4f);c.drawArc(43,57,57,68,0,180,false,p);}
   fill(0xFFEAA5B5);c.drawOval(22,64,35,70,p);c.drawOval(65,64,78,70,p);
   if(animal.equals("bunny")){fill(0xFFEBA1B1);c.drawOval(28,10,36,33,p);c.drawOval(64,10,72,33,p);}
   if(animal.equals("mochi")){fill(0xFFD1BDE7);c.drawCircle(75,22,10,p);fill(accent);c.drawCircle(80,18,9,p);}
   new StickerPainter().draw(c,motifs(characterIndex(animal))[0],70,71,25,255);c.restore();}
 }
 int characterIndex(String name){for(int i=0;i<themes.length;i++)if(themes[i].character.equals(name))return i;return 0;}
 class StickerPainter {
  Paint p=new Paint(3);Canvas c;
  void fill(int color){p.setStyle(Paint.Style.FILL);p.setColor(color);}
  void line(float x,float y,float xx,float yy,int color,float width){p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(width);p.setStrokeCap(Paint.Cap.ROUND);p.setColor(color);c.drawLine(x,y,xx,yy,p);p.setStyle(Paint.Style.FILL);}
  void oval(float x,float y,float xx,float yy,int color){fill(color);c.drawOval(x,y,xx,yy,p);}
  void round(float x,float y,float xx,float yy,float radius,int color){fill(color);c.drawRoundRect(x,y,xx,yy,radius,radius,p);}
  void path(int color,float... points){fill(color);Path path=new Path();path.moveTo(points[0],points[1]);for(int i=2;i<points.length;i+=2)path.lineTo(points[i],points[i+1]);path.close();c.drawPath(path,p);}
  void face(float x,float y){oval(x-6,y-1,x-3,y+2,0xFF806979);oval(x+3,y-1,x+6,y+2,0xFF806979);line(x-1,y+4,x+1,y+4,0xFF806979,1.4f);}
  void star(float x,float y,float radius,int color){fill(color);Path star=new Path();for(int i=0;i<10;i++){double a=-Math.PI/2+i*Math.PI/5;float r=i%2==0?radius:radius*.48f;float xx=x+(float)Math.cos(a)*r,yy=y+(float)Math.sin(a)*r;if(i==0)star.moveTo(xx,yy);else star.lineTo(xx,yy);}star.close();c.drawPath(star,p);}
  void draw(Canvas canvas,String name,float x,float y,float size,int alpha){c=canvas;int save=c.saveLayerAlpha(x-size*.15f,y-size*.15f,x+size*1.15f,y+size*1.15f,alpha);c.translate(x,y);c.scale(size/64,size/64);
   int green=0xFFA9CAA5,pink=0xFFEAA9BE,yellow=0xFFF2D58F,ink=0xFF9C7E8F;
   switch(name){
    case "carrot":path(0xFFE9AF7D,17,22,44,18,31,57);line(28,24,21,20,0xFFD39569,2);line(34,34,40,30,0xFFD39569,2);oval(13,4,29,23,green);oval(28,2,40,22,0xFF94BC96);oval(36,7,49,23,green);break;
    case "strawberry":path(pink,10,23,54,23,46,45,32,57,18,45);oval(10,14,54,37,pink);path(green,11,16,25,12,31,4,37,12,53,16,40,23,25,22);for(int i=0;i<3;i++){oval(22+i*8,30,24+i*8,33,0xFFFFF6D8);oval(25+i*6,40,27+i*6,43,0xFFFFF6D8);}break;
    case "flower":case "daisy":for(int i=0;i<6;i++){c.save();c.rotate(i*60,32,29);oval(25,8,39,30,name.equals("daisy")?0xFFFFFDF5:pink);c.restore();}oval(23,20,41,38,yellow);line(32,39,32,57,green,3);oval(33,44,49,52,green);break;
    case "cloud":oval(6,26,33,49,0xFFD6E8F3);oval(20,12,48,47,0xFFE6F2FA);oval(35,25,60,49,0xFFD6E8F3);face(32,34);break;
    case "star":case "sparkle":star(31,29,23,name.equals("star")?yellow:0xFFD6C0E7);star(53,51,7,pink);break;
    case "rainbow":p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(7);p.setColor(pink);c.drawArc(8,10,56,62,180,180,false,p);p.setColor(yellow);c.drawArc(15,17,49,62,180,180,false,p);p.setColor(0xFFB9D7D7);c.drawArc(22,24,42,62,180,180,false,p);p.setStyle(Paint.Style.FILL);oval(5,40,26,53,0xFFFFF8F1);oval(39,40,60,53,0xFFFFF8F1);break;
    case "honey":round(14,17,50,55,9,0xFFEBC78C);round(11,12,53,23,5,0xFFCBA67E);round(18,29,46,45,5,0xFFFFF2D2);path(pink,28,32,32,35,36,32,39,36,32,42,25,36);line(48,15,56,4,0xFFB89B79,4);break;
    case "bee":oval(14,12,32,30,0xFFE6F0F5);oval(30,10,48,30,0xFFE6F0F5);oval(11,25,53,49,yellow);line(24,28,24,46,ink,4);line(36,27,36,47,ink,4);oval(43,32,46,35,ink);line(9,38,4,35,ink,2);break;
    case "lily":oval(5,22,59,53,green);path(0xFFF2FAEC,32,38,57,23,52,40);line(20,43,42,30,0xFF8FB892,1.5f);break;
    case "lotus":oval(5,38,59,56,green);oval(21,10,43,49,pink);c.save();c.rotate(-35,30,39);oval(13,18,33,48,0xFFF1C9D9);c.restore();c.save();c.rotate(35,34,39);oval(31,18,51,48,0xFFF1C9D9);c.restore();oval(25,36,39,48,yellow);break;
    case "dragonfly":oval(7,14,31,29,0xFFD7E9EF);oval(33,14,57,29,0xFFD7E9EF);oval(8,28,31,40,0xFFE9DDF0);oval(33,28,56,40,0xFFE9DDF0);round(29,17,35,55,3,0xFF9FBFAB);oval(25,10,39,24,0xFF9FBFAB);break;
    case "moon":oval(10,7,54,55,yellow);oval(24,2,60,42,0xFFF6F1FB);star(48,47,8,pink);break;
    case "planet":oval(15,12,51,49,0xFFD6C3E9);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(5);p.setColor(0xFFE6BDD3);c.save();c.rotate(-25,32,32);c.drawOval(4,25,60,41,p);c.restore();p.setStyle(Paint.Style.FILL);oval(24,20,32,27,0xFFEEE1F5);break;
    case "mushroom":round(24,26,40,57,7,0xFFF2E1CE);oval(7,9,57,43,0xFFE3A5A0);round(7,29,57,42,6,0xFFE3A5A0);oval(16,19,24,26,0xFFFFF6ED);oval(34,15,43,23,0xFFFFF6ED);oval(42,29,49,35,0xFFFFF6ED);break;
    case "acorn":oval(17,20,48,56,0xFFD2AC82);round(12,16,52,31,7,0xFFB99477);line(33,16,36,8,0xFFB99477,4);line(22,20,25,26,0xFFD7BA9C,2);line(34,20,37,26,0xFFD7BA9C,2);break;
    case "leaf":oval(12,9,51,50,green);line(15,53,44,19,0xFF86AA8B,3);line(28,37,24,23,0xFF86AA8B,1.5f);line(33,32,44,33,0xFF86AA8B,1.5f);break;
    case "bamboo":round(25,6,36,59,5,0xFFABD1A1);line(25,22,36,22,0xFF84AB8B,2);line(25,41,36,41,0xFF84AB8B,2);oval(33,12,54,24,0xFF91BC94);oval(7,29,27,42,0xFF91BC94);break;
    case "dumpling":oval(7,27,57,53,0xFFF8EDD8);path(0xFFF8EDD8,9,34,21,17,30,23,40,16,55,35);line(22,23,26,34,0xFFD8C4A8,2);line(38,22,35,34,0xFFD8C4A8,2);face(32,39);break;
    case "teacup":round(12,24,46,52,9,0xFFD6E4CF);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(5);p.setColor(0xFFAFC7A6);c.drawOval(40,28,56,44,p);p.setStyle(Paint.Style.FILL);oval(14,19,44,31,0xFFB9CA9C);line(24,14,27,7,0xFFCEC7CA,2);line(35,13,38,6,0xFFCEC7CA,2);break;
    case "shell":path(0xFFE9C2CC,5,27,14,13,26,10,32,16,38,10,51,13,59,27,43,51,21,51);line(17,23,27,46,0xFFD3A6B6,2);line(32,21,32,48,0xFFD3A6B6,2);line(47,23,37,46,0xFFD3A6B6,2);break;
    case "seaweed":for(int i=0;i<3;i++){int save2=c.save();c.translate(i*14,0);p.setStyle(Paint.Style.STROKE);p.setColor(i==1?0xFF9BC8B0:0xFFB9D8BF);p.setStrokeWidth(8);Path stem=new Path();stem.moveTo(17,56);stem.cubicTo(35,35,2,30,18,9);c.drawPath(stem,p);p.setStyle(Paint.Style.FILL);c.restoreToCount(save2);}break;
    case "bubble":oval(8,18,42,52,0xFFCCE5EE);oval(13,22,37,47,0xFFE8F5F7);oval(34,4,56,26,0xFFDFEAF7);oval(17,24,22,30,Color.WHITE);break;
    case "peach":oval(8,19,37,54,0xFFF1C0A8);oval(27,19,56,54,0xFFF1B8AC);line(32,25,32,45,0xFFE2A393,1.5f);oval(30,7,51,20,green);line(31,20,32,10,0xFFAA977D,3);break;
    case "heart":fill(pink);Path heart=new Path();heart.moveTo(32,54);heart.cubicTo(-4,32,12,2,32,22);heart.cubicTo(52,2,68,32,32,54);c.drawPath(heart,p);break;
    case "crystal":path(0xFFD6C6EB,15,24,32,5,49,24,45,52,30,60,17,48);path(0xFFE9DEF4,15,24,32,5,29,57);line(29,57,34,24,0xFFBBA6D7,1.5f);line(17,24,46,24,0xFFBBA6D7,1.5f);break;
    default:star(32,32,20,yellow);
   }c.restoreToCount(save);
  }
 }
 """)
 # Replace the old backgrounds while preserving the existing Gingham/theme preview APIs.
 block('class Pattern extends android.graphics.drawable.Drawable {','class Icon extends',r"""class Pattern extends android.graphics.drawable.Drawable {
  ThemeSpec palette;int kind;Paint paint=new Paint(3);StickerPainter painter=new StickerPainter();Pattern(ThemeSpec t,int k){palette=t;kind=k;}
  public void draw(Canvas c){if(palette==null){c.drawColor(0xFFFFF7F3);return;}c.drawColor(palette.cream);Rect b=getBounds();int width=b.width(),height=b.height();paint.setColor(blend(palette.cream,palette.pink,.42f));int step=dp(25);
   if(kind==0||kind==8){for(int x=0;x<width;x+=step*2)c.drawRect(x,0,x+step,height,paint);for(int y=0;y<height;y+=step*2)c.drawRect(0,y,width,y+step,paint);}
   else if(kind==3||kind==7){paint.setStyle(Paint.Style.STROKE);paint.setStrokeWidth(dp(1));for(int y=dp(30);y<height;y+=dp(80))for(int x=dp(25);x<width;x+=dp(95)){c.drawOval(x-dp(24),y-dp(8),x+dp(24),y+dp(8),paint);c.drawOval(x-dp(17),y-dp(4),x+dp(17),y+dp(4),paint);}paint.setStyle(Paint.Style.FILL);}
   else{for(int y=dp(13);y<height;y+=dp(30))for(int x=dp(12)+(y/dp(30)%2)*dp(15);x<width;x+=dp(30))c.drawCircle(x,y,dp(1.7f),paint);}
   String[] names=motifs(kind);int row=0;for(int y=dp(20);y<height;y+=dp(112),row++){int column=0;for(int x=dp(12)+(row%2)*dp(42);x<width;x+=dp(116),column++){painter.draw(c,names[(row+column)%3],x,y,dp(31),92);}}
  }
  public void setAlpha(int a){}public void setColorFilter(ColorFilter f){}public int getOpacity(){return PixelFormat.OPAQUE;}
 }
 """)
 s=s.replace('Version 2.0','Version 3.0')
 p.write_text(s,encoding='utf-8')
gradle=Path('app/build.gradle');g=gradle.read_text();g=re.sub(r'versionCode\s+\d+','versionCode 3',g);g=re.sub(r'versionName\s+[\'\"][^\'\"]+[\'\"]','versionName "3.0"',g);gradle.write_text(g)
Path('VERSION-3-NOTES.txt').write_text("""A Day To Keep 3.0
Larger, font-aware dialog buttons; centred square settings button; checklist-header
insets; bevelled/outlined cards; many locally drawn themed objects; gentle floating
illustrations and characters; animations toggle default on, respecting system settings.
Ten themes total, preserving the original five theme indices. New themes: Woodland Fox,
Bamboo Panda, Seaside Otter, Peach Duck and Starry Axolotl. No app-data reset intended.
This update preserves signing and app ID. Save an in-app backup before installing.
""")
print('A Day To Keep version 3 artwork/layout changes prepared.')
