#!/usr/bin/env python3
"""7.1: screenshot-led layout refinements, masonry/reorderable notes and twelve themes."""
from pathlib import Path
import re,xml.etree.ElementTree as ET
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text(encoding='utf-8')
if '// A_DAY_TO_KEEP_EDGEFIX_703' not in s:raise SystemExit('Preserve the working update_edgefix.py before update_comfort.py.')
MARK='// A_DAY_TO_KEEP_COMFORT_71'
def end_block(text,start):
 brace=text.find('{',start)
 if brace<0:raise RuntimeError('Opening brace missing')
 i=brace+1;depth=1;state='code'
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
 if depth:raise RuntimeError('Unbalanced Java block near '+text[start:start+70])
 return i

def bounds(text,signature):
 a=text.find(signature)
 if a<0:raise RuntimeError('Source section missing: '+signature)
 return a,end_block(text,a)
def balanced(text):
 stack=[];state='code';i=0
 while i<len(text):
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
   elif c in '({[':stack.append(c)
   elif c in ')}]':
    if not stack or stack.pop()!={')':'(',']':'[','}':'{'}[c]:raise RuntimeError('Mismatched Java delimiter at '+str(i))
  i+=1
 if stack or state not in ('code','line'):raise RuntimeError('Unclosed Java delimiter/string/comment')
def replace(signature,new):
 global s
 balanced(new)
 a,b=bounds(s,signature);s=s[:a]+new+s[b:]
def edit(signature,fn):
 global s
 a,b=bounds(s,signature);new=fn(s[a:b]);balanced(new);s=s[:a]+new+s[b:]
def need(text,old,new):
 if old not in text:raise RuntimeError('Expected code missing: '+old[:100])
 return text.replace(old,new,1)
if MARK not in s:
 edit('void home(){',lambda t:need(t,'root.addView(banner);','LinearLayout.LayoutParams compactBanner=new LinearLayout.LayoutParams(-1,dp(98));compactBanner.topMargin=-dp(18);root.addView(banner,compactBanner);'))
 replace('View calendarArrow(',r"""View calendarArrow(String symbol,Runnable action){FrameLayout arrow=new FrameLayout(this);arrow.setBackground(shape(WHITE));arrow.setMinimumWidth(dp(56));arrow.setMinimumHeight(dp(56));arrow.setContentDescription(symbol.equals("<")?"Previous month":"Next month");CalendarChevron chevron=new CalendarChevron(symbol.equals("<"));arrow.addView(chevron,new FrameLayout.LayoutParams(dp(30),dp(30),Gravity.CENTER));arrow.setOnClickListener(v->{chime(softSound);action.run();});wirePress(arrow);return arrow;}""")
 replace('NumberPicker timeWheel(',r"""NumberPicker timeWheel(int max,int value){NumberPicker wheel=new RoundedTimeWheel();wheel.setMinValue(0);wheel.setMaxValue(max);wheel.setWrapSelectorWheel(true);wheel.setValue(value);wheel.setFormatter(v->String.format(Locale.UK,"%02d",v));wheel.setDescendantFocusability(NumberPicker.FOCUS_BLOCK_DESCENDANTS);wheel.setTextColor(INK);wheel.setTextSize(dp(27));wheel.setSelectionDividerHeight(0);wheel.setBackground(shape(LILAC));return wheel;}""")
 edit('void showCute(AlertDialog d){',lambda t:t[:-1]+'if(d.getWindow()!=null)hideReminderCaption(d.getWindow().getDecorView());}')
 edit('class Icon extends View {',lambda t:need(t,'protected void onDraw(Canvas canvas){','protected void onDraw(Canvas canvas){if(kind.equals("notes")){drawNotesSymbol(canvas,getWidth(),getHeight());return;}'))
 helpers=r"""
 // A_DAY_TO_KEEP_COMFORT_71
 class CalendarChevron extends View {boolean previous;Paint pen=new Paint(3);CalendarChevron(boolean back){super(MainActivity.this);previous=back;}@Override protected void onDraw(Canvas c){int save=c.save();c.scale(getWidth()/40f,getHeight()/40f);pen.setColor(INK);pen.setStyle(Paint.Style.STROKE);pen.setStrokeWidth(3);pen.setStrokeCap(Paint.Cap.ROUND);pen.setStrokeJoin(Paint.Join.ROUND);Path path=new Path();path.moveTo(previous?24:16,11);path.lineTo(previous?15:25,20);path.lineTo(previous?24:16,29);c.drawPath(path,pen);c.restoreToCount(save);}}
 class RoundedTimeWheel extends NumberPicker {Path clip=new Path();Paint lines=new Paint(3);RoundedTimeWheel(){super(MainActivity.this);setClipChildren(true);setClipToPadding(true);setClipToOutline(true);setOutlineProvider(new ViewOutlineProvider(){@Override public void getOutline(View view,Outline outline){outline.setRoundRect(0,0,view.getWidth(),view.getHeight(),dp(22));}});setVerticalFadingEdgeEnabled(false);}@Override public void draw(Canvas c){int save=c.save();clip.reset();clip.addRoundRect(new RectF(0,0,getWidth(),getHeight()),dp(22),dp(22),Path.Direction.CW);c.clipPath(clip);super.draw(c);lines.setColor(blend(LILAC,INK,.35f));lines.setStrokeWidth(Math.max(1,dp(0.6f)));float half=Math.min(dp(23),getHeight()/5f);c.drawLine(dp(9),getHeight()/2f-half,getWidth()-dp(9),getHeight()/2f-half,lines);c.drawLine(dp(9),getHeight()/2f+half,getWidth()-dp(9),getHeight()/2f+half,lines);c.restoreToCount(save);}}
 void hideReminderCaption(View view){if(view instanceof TextView){String value=((TextView)view).getText().toString();if(value.startsWith("Reminder time")&&value.contains("24"))view.setVisibility(View.GONE);}if(view instanceof ViewGroup){ViewGroup group=(ViewGroup)view;for(int i=0;i<group.getChildCount();i++)hideReminderCaption(group.getChildAt(i));}}
 void drawNotesSymbol(Canvas canvas,int width,int height){int save=canvas.save();canvas.scale(width/40f,height/40f);Paint pen=new Paint(3);pen.setColor(WHITE);canvas.drawRoundRect(5,5,29,35,3,3,pen);pen.setStyle(Paint.Style.STROKE);pen.setStrokeWidth(2.1f);pen.setColor(INK);canvas.drawRoundRect(5,5,29,35,3,3,pen);pen.setStrokeWidth(1.7f);for(int y=12;y<=24;y+=6)canvas.drawLine(10,y,22,y,pen);int pencil=canvas.save();canvas.rotate(31,29,22);pen.setStyle(Paint.Style.FILL);pen.setColor(PINK);canvas.drawRoundRect(26,5,32,29,1.5f,1.5f,pen);pen.setColor(INK);pen.setStyle(Paint.Style.STROKE);pen.setStrokeWidth(1.5f);canvas.drawRoundRect(26,5,32,29,1.5f,1.5f,pen);Path tip=new Path();tip.moveTo(26,29);tip.lineTo(32,29);tip.lineTo(29,35);tip.close();pen.setStyle(Paint.Style.FILL);pen.setColor(0xFFF0D9B0);canvas.drawPath(tip,pen);pen.setColor(INK);canvas.drawCircle(29,33,1.2f,pen);canvas.restoreToCount(pencil);canvas.restoreToCount(save);}
 int noteTint(String id){int[] colors={PINK,LILAC,MINT,blend(PINK,MINT,.45f),blend(LILAC,PINK,.45f),blend(LILAC,MINT,.55f),blend(CREAM,PINK,.55f),blend(CREAM,MINT,.55f),blend(CREAM,LILAC,.55f)};return colors[Math.floorMod(id.hashCode(),colors.length)];}
 ArrayList<JSONObject> orderedNotes(){ArrayList<JSONObject> result=new ArrayList<>(),unranked=new ArrayList<>();LinkedHashMap<String,JSONObject> available=new LinkedHashMap<>();JSONArray all=noteItems();for(int i=0;i<all.length();i++){JSONObject note=all.optJSONObject(i);if(note!=null)available.put(note.optString("id"),note);}JSONArray order=data.optJSONArray("noteOrder");if(order!=null)for(int i=0;i<order.length();i++){JSONObject note=available.remove(order.optString(i));if(note!=null)result.add(note);}unranked.addAll(available.values());unranked.sort((a,b)->Long.compare(b.optLong("createdAt",b.optLong("updatedAt")),a.optLong("createdAt",a.optLong("updatedAt"))));result.addAll(0,unranked);JSONArray next=new JSONArray();for(JSONObject note:result)next.put(note.optString("id"));if(order==null||!order.toString().equals(next.toString())){try{data.put("noteOrder",next);save();}catch(Exception error){android.util.Log.w("ADayToKeep","Could not save note order",error);}}return result;}
 void moveNote(String id,String target){if(id.equals(target))return;ArrayList<JSONObject> ordered=orderedNotes();int from=-1,to=-1;for(int i=0;i<ordered.size();i++){String current=ordered.get(i).optString("id");if(current.equals(id))from=i;if(current.equals(target))to=i;}if(from<0||to<0)return;JSONObject moved=ordered.remove(from);ordered.add(Math.min(to,ordered.size()),moved);JSONArray next=new JSONArray();for(JSONObject note:ordered)next.put(note.optString("id"));try{data.put("noteOrder",next);save();}catch(Exception error){android.util.Log.w("ADayToKeep","Could not reorder note",error);}}
 class NoteBoard extends ViewGroup {
  ArrayList<Rect> slots=new ArrayList<>();Paint highlight=new Paint(3);String dragged="";int hover=-1;float screenX,screenY;boolean dragging=false;
  final Runnable edgeScroll=new Runnable(){@Override public void run(){if(!dragging||!(getParent() instanceof ScrollView))return;ScrollView parent=(ScrollView)getParent();int[] where=new int[2];parent.getLocationOnScreen(where);float local=screenY-where[1];if(local<dp(65))parent.scrollBy(0,-dp(12));else if(local>parent.getHeight()-dp(65))parent.scrollBy(0,dp(12));getLocationOnScreen(where);updateHover(screenX-where[0],screenY-where[1]);postDelayed(this,45);}};
  NoteBoard(){super(MainActivity.this);setPadding(dp(4),dp(4),dp(4),dp(88));setClipChildren(true);setOnDragListener((v,event)->handleDrag(event));}
  @Override protected LayoutParams generateDefaultLayoutParams(){return new LayoutParams(-1,-2);}
  @Override protected void onMeasure(int widthSpec,int heightSpec){int width=MeasureSpec.getSize(widthSpec),gap=dp(9),column=Math.max(1,(width-getPaddingLeft()-getPaddingRight()-gap)/2);int[] bottoms={getPaddingTop(),getPaddingTop()};slots.clear();for(int i=0;i<getChildCount();i++){View child=getChildAt(i);child.measure(MeasureSpec.makeMeasureSpec(column,MeasureSpec.EXACTLY),MeasureSpec.makeMeasureSpec(0,MeasureSpec.UNSPECIFIED));int side=bottoms[0]<=bottoms[1]?0:1,left=getPaddingLeft()+side*(column+gap),top=bottoms[side];slots.add(new Rect(left,top,left+column,top+child.getMeasuredHeight()));bottoms[side]=top+child.getMeasuredHeight()+gap;}int height=Math.max(bottoms[0],bottoms[1])+getPaddingBottom();setMeasuredDimension(width,resolveSize(height,heightSpec));}
  @Override protected void onLayout(boolean changed,int l,int t,int r,int b){for(int i=0;i<getChildCount()&&i<slots.size();i++){Rect slot=slots.get(i);getChildAt(i).layout(slot.left,slot.top,slot.right,slot.bottom);}}
  void updateHover(float x,float y){int nearest=-1;float best=Float.MAX_VALUE;for(int i=0;i<slots.size();i++){Rect rect=slots.get(i);float dx=Math.max(rect.left-x,Math.max(0,x-rect.right)),dy=Math.max(rect.top-y,Math.max(0,y-rect.bottom)),distance=dx*dx+dy*dy;if(distance<best){best=distance;nearest=i;}}if(nearest!=hover){hover=nearest;invalidate();}}
  boolean handleDrag(DragEvent event){switch(event.getAction()){case DragEvent.ACTION_DRAG_STARTED:if(!(event.getLocalState() instanceof String))return false;dragged=(String)event.getLocalState();dragging=true;hover=-1;for(int i=0;i<getChildCount();i++)if(dragged.equals(getChildAt(i).getTag()))getChildAt(i).setAlpha(.45f);int[] begin=new int[2];getLocationOnScreen(begin);screenX=begin[0]+event.getX();screenY=begin[1]+event.getY();removeCallbacks(edgeScroll);postDelayed(edgeScroll,45);return true;case DragEvent.ACTION_DRAG_LOCATION:int[] where=new int[2];getLocationOnScreen(where);screenX=where[0]+event.getX();screenY=where[1]+event.getY();updateHover(event.getX(),event.getY());return true;case DragEvent.ACTION_DROP:updateHover(event.getX(),event.getY());if(hover>=0&&hover<getChildCount()){moveNote(dragged,String.valueOf(getChildAt(hover).getTag()));post(()->notes());}return true;case DragEvent.ACTION_DRAG_EXITED:hover=-1;invalidate();return true;case DragEvent.ACTION_DRAG_ENDED:dragging=false;removeCallbacks(edgeScroll);for(int i=0;i<getChildCount();i++)getChildAt(i).setAlpha(1);hover=-1;invalidate();return true;default:return true;}}
  @Override protected void dispatchDraw(Canvas canvas){super.dispatchDraw(canvas);if(dragging&&hover>=0&&hover<slots.size()){highlight.setColor(INK);highlight.setStyle(Paint.Style.STROKE);highlight.setStrokeWidth(dp(2));Rect slot=slots.get(hover);canvas.drawRoundRect(new RectF(slot.left+dp(1),slot.top+dp(1),slot.right-dp(1),slot.bottom-dp(1)),dp(22),dp(22),highlight);}}
  @Override protected void onDetachedFromWindow(){dragging=false;removeCallbacks(edgeScroll);super.onDetachedFromWindow();}
 }
 """
 balanced(helpers)
 s=need(s,' JSONObject data;',helpers+'\n JSONObject data;')
 replace('void notes(){',r"""void notes(){screen="notes";editor=null;base("Notes",true);FrameLayout area=new FrameLayout(this);area.setClipChildren(true);root.addView(area,new LinearLayout.LayoutParams(-1,0,1));ScrollView scroll=new ScrollView(this);scroll.setClipChildren(true);scroll.setClipToPadding(true);NoteBoard board=new NoteBoard();scroll.addView(board,new ScrollView.LayoutParams(-1,-2));area.addView(scroll,new FrameLayout.LayoutParams(-1,-1));ArrayList<JSONObject> items=orderedNotes();if(items.isEmpty()){TextView empty=text("A little space for ideas, lists and things to remember.",18);empty.setPadding(dp(20),dp(30),dp(20),dp(30));FrameLayout.LayoutParams message=new FrameLayout.LayoutParams(-1,-2,Gravity.TOP);area.addView(empty,message);}for(JSONObject note:items){String id=note.optString("id");LinearLayout card=section(noteTint(id));TextView title=label(note.optString("title").trim().isEmpty()?"Untitled note":note.optString("title"),19);title.setMaxLines(2);title.setEllipsize(TextUtils.TruncateAt.END);card.addView(title);TextView preview=text(note.optString("body").isEmpty()?"Tap to write…":note.optString("body"),15);preview.setMaxLines(6);preview.setEllipsize(TextUtils.TruncateAt.END);preview.setPadding(0,dp(7),0,0);card.addView(preview);card.setTag(id);card.setContentDescription("Open note: "+title.getText()+". Hold to rearrange.");card.setOnClickListener(v->{selectedNoteId=id;noteEditor();});card.setOnLongClickListener(v->{v.performHapticFeedback(HapticFeedbackConstants.LONG_PRESS);return v.startDragAndDrop(ClipData.newPlainText("Note",id),new View.DragShadowBuilder(v),id,0);});board.addView(card,new ViewGroup.LayoutParams(-1,-2));}View add=button("","plus",MINT,()->addNote());add.setContentDescription("Add note");FrameLayout.LayoutParams plus=new FrameLayout.LayoutParams(dp(58),dp(58),Gravity.RIGHT|Gravity.BOTTOM);plus.setMargins(dp(10),dp(10),dp(10),dp(12));add.setElevation(dp(12));area.addView(add,plus);}""")
 replace('void noteEditor(){',r"""void noteEditor(){JSONObject note=findNote(selectedNoteId);if(note==null){notes();return;}screen="note";base("Note",true);FrameLayout header=(FrameLayout)root.getChildAt(0);View remove=glyphButton("Delete note","trash",PINK,()->ask("Remove note?","Remove this note?",()->{JSONArray all=noteItems();for(int i=all.length()-1;i>=0;i--){JSONObject item=all.optJSONObject(i);if(item!=null&&selectedNoteId.equals(item.optString("id")))all.remove(i);}save();selectedNoteId="";notes();},null));FrameLayout.LayoutParams removeLp=new FrameLayout.LayoutParams(dp(50),dp(50),Gravity.RIGHT|Gravity.CENTER_VERTICAL);header.addView(remove,removeLp);EditText title=new EditText(this);title.setSingleLine(false);title.setMaxLines(2);title.setTextSize(22);title.setTypeface(headingFont);title.setTextColor(INK);title.setHint("Title");title.setContentDescription("Note title");title.setBackground(shape(WHITE));title.setPadding(dp(15),dp(12),dp(15),dp(12));title.setText(note.optString("title"));root.addView(title,new LinearLayout.LayoutParams(-1,-2));space(root,8);EditText body=new EditText(this);body.setTextSize(18);body.setTypeface(bodyFont);body.setTextColor(INK);body.setGravity(Gravity.TOP);body.setInputType(android.text.InputType.TYPE_CLASS_TEXT|android.text.InputType.TYPE_TEXT_FLAG_MULTI_LINE|android.text.InputType.TYPE_TEXT_FLAG_CAP_SENTENCES);body.setHorizontallyScrolling(false);body.setVerticalScrollBarEnabled(true);body.setHint("Keep a little thought…");body.setContentDescription("Note body");body.setBackground(shape(WHITE));body.setPadding(dp(15),dp(15),dp(15),dp(15));body.setText(note.optString("body"));root.addView(body,new LinearLayout.LayoutParams(-1,0,1));TextWatcher watcher=new TextWatcher(){public void beforeTextChanged(CharSequence text,int start,int count,int after){}public void onTextChanged(CharSequence text,int start,int before,int count){try{note.put("title",title.getText().toString());note.put("body",body.getText().toString());note.put("updatedAt",System.currentTimeMillis());save();}catch(Exception error){android.util.Log.w("ADayToKeep","Could not save note",error);}}public void afterTextChanged(Editable text){}};title.addTextChangedListener(watcher);body.addTextChangedListener(watcher);editor=body;root.setFocusableInTouchMode(true);root.requestFocus();}""")
 replace('void viewer(LocalDate d,String file){',r"""void viewer(LocalDate d,String file){Dialog full=new Dialog(this,android.R.style.Theme_Material_Light_NoActionBar);FrameLayout stage=new FrameLayout(this);stage.setBackground(new Gingham());stage.setClipChildren(true);ScheduleViewport imageBounds=new ScheduleViewport();Zoom zoom=new Zoom();imageBounds.addView(zoom,new FrameLayout.LayoutParams(-1,-1));FrameLayout.LayoutParams imageLp=new FrameLayout.LayoutParams(-1,-1);imageLp.topMargin=dp(94);stage.addView(imageBounds,imageLp);LinearLayout toolbar=col();toolbar.setBackgroundColor(CREAM);LinearLayout buttons=row();buttons.setPadding(dp(10),dp(8),dp(10),dp(5));buttons.addView(new View(this),new LinearLayout.LayoutParams(0,1,1));View remove=glyphButton("Delete attachment","trash",PINK,()->ask("Remove this attachment?","This removes the image or PDF page from this CPD entry, not the original file on your phone.",()->{JSONObject value=entry(d,false);if(value!=null){JSONArray images=value.optJSONArray("images");if(images!=null)for(int i=images.length()-1;i>=0;i--)if(images.optString(i).equals(file))images.remove(i);save();new File(photos(),file).delete();}full.dismiss();journal();},null));LinearLayout.LayoutParams deleteLp=new LinearLayout.LayoutParams(dp(52),dp(52));deleteLp.setMargins(0,0,dp(9),0);buttons.addView(remove,deleteLp);View close=glyphButton("Close attachment","close",LILAC,()->full.dismiss());buttons.addView(close,new LinearLayout.LayoutParams(dp(52),dp(52)));toolbar.addView(buttons);TextView hint=text("Pinch to zoom · Drag to pan · Double-tap to reset",12);hint.setGravity(Gravity.CENTER);hint.setPadding(dp(4),0,dp(4),dp(7));toolbar.addView(hint);toolbar.setElevation(dp(24));toolbar.setTranslationZ(dp(24));stage.addView(toolbar,new FrameLayout.LayoutParams(-1,-2,Gravity.TOP));toolbar.bringToFront();full.setContentView(stage);full.show();if(full.getWindow()!=null)full.getWindow().setLayout(-1,-1);worker.execute(()->{Bitmap image=decode(new File(photos(),file),3000);runOnUiThread(()->{if(full.isShowing())zoom.setImageBitmap(image);else if(image!=null)image.recycle();});});}""")

 extra_themes=r""",
 new ThemeSpec("Peony Piglet","Peony petals, tiny hearts & rosy snouts","piglet","Mali","PatrickHand",0xFF865F70,0xFFF2D3DE,0xFFE9DCF0,0xFFDDEAD7,0xFFFFF5F8,0xFFFFFCFD),
 new ThemeSpec("Apricot Hamster","Apricot treats, cosy cups & little paws","hamster","Chewy","Mali",0xFF82654F,0xFFF3DAC1,0xFFEADFD5,0xFFDFE8CD,0xFFFFF8EE,0xFFFFFDFA),
 new ThemeSpec("Moonlit Moth","Velvet wings, sleepy moons & sparkling skies","moth","PatrickHand","Mali",0xFF71647F,0xFFE6D9ED,0xFFDBDFF2,0xFFDEE8E4,0xFFF8F5FC,0xFFFDFBFF),
 new ThemeSpec("Cloudy Lamb","Fluffy clouds, meadow flowers & soft wool","lamb","Mali","PatrickHand",0xFF737D73,0xFFE2EADD,0xFFE4E0ED,0xFFD5E8DC,0xFFF9FCF4,0xFFFFFFFC),
 new ThemeSpec("Jade Dragon","Jade leaves, little crystals & friendly horns","dragon","Chewy","Mali",0xFF58796C,0xFFD1E8DC,0xFFDCE5EA,0xFFDEE9BD,0xFFF2FBF2,0xFFFCFFFA),
 new ThemeSpec("Peach Seal","Peachy shells, gentle waves & little whiskers","seal","Mali","PatrickHand",0xFF79717E,0xFFF2DBD7,0xFFE1DFF0,0xFFDCEBE7,0xFFFFF8F5,0xFFFFFDFC),
 new ThemeSpec("Lavender Llama","Lavender flowers, rainbow wishes & soft ears","llama","PatrickHand","Mali",0xFF7A6988,0xFFE8D9EF,0xFFDEDEF4,0xFFDEEAD9,0xFFFBF6FF,0xFFFFFDFF),
 new ThemeSpec("Dusky Bat","Little moon wings, stars & blueberry skies","bat","Chewy","Mali",0xFF67647F,0xFFDEDCEC,0xFFD6DFF1,0xFFE4E8D8,0xFFF5F6FF,0xFFFDFDFF),
 new ThemeSpec("Marshmallow Yeti","Snowy fluff, icy bubbles & gentle giants","yeti","Mali","PatrickHand",0xFF5E7B87,0xFFD8EBF0,0xFFDEE3F4,0xFFDFECE6,0xFFF4FCFF,0xFFFCFFFF),
 new ThemeSpec("Rose Flamingo","Rosy feathers, lily ponds & warm sunshine","flamingo","PatrickHand","Mali",0xFF8B6677,0xFFF3D4DE,0xFFEBDDEB,0xFFD9EBDD,0xFFFFF5F6,0xFFFFFCFC),
 new ThemeSpec("Citrus Chameleon","Citrus leaves, curious eyes & curled tails","chameleon","Chewy","Mali",0xFF6D7E4E,0xFFE0EAC2,0xFFE9E3D1,0xFFD3E9CF,0xFFFAFDEF,0xFFFFFEF7),
 new ThemeSpec("Toffee Squirrel","Toffee treasures, acorns & fluffy tails","squirrel","Mali","PatrickHand",0xFF82634E,0xFFEFDBC4,0xFFE9DFD6,0xFFDDE8CC,0xFFFFF8EF,0xFFFFFDFA)
 """
 match=re.search(r'(final ThemeSpec\[\] themes=\{)(.*?)(\n\s*\};)',s,re.S)
 if not match:raise RuntimeError('Theme array missing')
 s=s[:match.start()]+match.group(1)+match.group(2).rstrip()+extra_themes+match.group(3)+s[match.end():]
 def more_characters(text):
  prefix='int fur=animal.equals("piglet")?0xFFEFBBCB:animal.equals("hamster")?0xFFE5BE91:animal.equals("moth")?0xFFD4C3DA:animal.equals("lamb")?0xFFF8F4E9:animal.equals("dragon")?0xFFABD3BC:animal.equals("seal")?0xFFDEE0E5:animal.equals("llama")?0xFFF4E7DF:animal.equals("bat")?0xFFB8AECF:animal.equals("yeti")?0xFFD9EBF3:animal.equals("flamingo")?0xFFF0B7C9:animal.equals("chameleon")?0xFFC6DB9C:animal.equals("squirrel")?0xFFD5A477:'
  text=need(text,'int fur=',prefix)
  head='c.drawOval(14,29,86,86,p);'
  before=r"""if(animal.equals("piglet")){Path ears=new Path();ears.moveTo(16,46);ears.lineTo(16,13);ears.lineTo(40,33);ears.lineTo(60,33);ears.lineTo(84,13);ears.lineTo(84,46);ears.close();c.drawPath(ears,p);}
   if(animal.equals("hamster")){c.drawCircle(25,30,12,p);c.drawCircle(75,30,12,p);}
   if(animal.equals("moth")){fill(0xFFC2ADD4);c.drawOval(0,27,40,82,p);c.drawOval(60,27,100,82,p);fill(0xFFE9D6ED);c.drawCircle(17,47,8,p);c.drawCircle(83,47,8,p);p.setStyle(Paint.Style.STROKE);p.setColor(0xFF8D799F);p.setStrokeWidth(2.5f);c.drawLine(40,35,32,13,p);c.drawLine(60,35,68,13,p);fill(fur);}
   if(animal.equals("lamb")){c.drawOval(3,38,28,66,p);c.drawOval(72,38,97,66,p);for(int n=0;n<5;n++)c.drawCircle(24+n*13,30-(n%2)*5,13,p);}
   if(animal.equals("dragon")){fill(0xFFE8DAB3);Path horns=new Path();horns.moveTo(22,40);horns.lineTo(23,9);horns.lineTo(38,34);horns.lineTo(62,34);horns.lineTo(77,9);horns.lineTo(78,40);horns.close();c.drawPath(horns,p);fill(fur);c.drawOval(0,38,29,58,p);c.drawOval(71,38,100,58,p);}
   if(animal.equals("seal")){c.drawOval(0,64,29,84,p);c.drawOval(71,64,100,84,p);}
   if(animal.equals("llama")){c.drawOval(23,1,39,48,p);c.drawOval(61,1,77,48,p);fill(0xFFE6C8D8);c.drawOval(28,8,34,37,p);c.drawOval(66,8,72,37,p);fill(fur);}
   if(animal.equals("bat")){fill(0xFFADA0C7);Path wings=new Path();wings.moveTo(31,44);wings.lineTo(0,25);wings.lineTo(4,66);wings.quadTo(15,55,22,77);wings.lineTo(35,71);wings.moveTo(69,44);wings.lineTo(100,25);wings.lineTo(96,66);wings.quadTo(85,55,78,77);wings.lineTo(65,71);c.drawPath(wings,p);fill(fur);Path ears=new Path();ears.moveTo(17,42);ears.lineTo(24,7);ears.lineTo(40,34);ears.lineTo(60,34);ears.lineTo(76,7);ears.lineTo(83,42);ears.close();c.drawPath(ears,p);}
   if(animal.equals("yeti")){for(int n=0;n<5;n++)c.drawCircle(23+n*14,31-(n%2)*5,11,p);c.drawCircle(17,53,12,p);c.drawCircle(83,53,12,p);}
   if(animal.equals("flamingo")){c.drawOval(44,12,52,41,p);c.drawOval(51,16,58,41,p);}
   if(animal.equals("chameleon")){p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(8);c.drawArc(65,45,97,88,-100,285,false,p);fill(fur);}
   if(animal.equals("squirrel")){c.drawOval(71,39,99,89,p);c.drawOval(20,13,35,45,p);c.drawOval(65,13,80,45,p);}
   """
  after=r"""
   if(animal.equals("hamster")||animal.equals("squirrel")){fill(0xFFFFECD8);c.drawOval(20,59,44,80,p);c.drawOval(56,59,80,80,p);}
   if(animal.equals("chameleon")){fill(fur);c.drawCircle(37,49,10,p);c.drawCircle(63,49,10,p);}
   if(animal.equals("yeti")){fill(0xFFF4FBFE);c.drawOval(24,40,76,84,p);}
   """
  text=need(text,head,before+head+after)
  face_tail=r"""if(animal.equals("piglet")){fill(0xFFD992AD);c.drawOval(38,59,62,76,p);fill(0xFFA96F85);c.drawCircle(45,67,2.2f,p);c.drawCircle(55,67,2.2f,p);}
   if(animal.equals("hamster")){fill(Color.WHITE);c.drawRoundRect(46,68,54,77,1,1,p);}
   if(animal.equals("seal")){p.setStyle(Paint.Style.STROKE);p.setColor(0xFF96919F);p.setStrokeWidth(1.4f);c.drawLine(25,62,11,57,p);c.drawLine(25,66,10,68,p);c.drawLine(75,62,89,57,p);c.drawLine(75,66,90,68,p);}
   if(animal.equals("flamingo")){fill(0xFFF0D89D);c.drawOval(43,57,64,73,p);fill(0xFF8D7583);c.drawOval(54,61,64,73,p);}
   """
  text=need(text,'fill(0xFFEAA5B5);c.drawOval(22,64,35,70,p);',face_tail+'fill(0xFFEAA5B5);c.drawOval(22,64,35,70,p);')
  return text
 edit('class Mascot extends AnimatedArt {',more_characters)
 def more_motifs(text):
  cases=r"""case 31:return new String[]{"flower","heart","sakura"};case 32:return new String[]{"orange","teacup","peach"};case 33:return new String[]{"moon","sparkle","crystal"};case 34:return new String[]{"cloud","flower","leaf"};case 35:return new String[]{"leaf","crystal","bamboo"};case 36:return new String[]{"shell","bubble","peach"};case 37:return new String[]{"flower","rainbow","heart"};case 38:return new String[]{"moon","star","planet"};case 39:return new String[]{"snowflake","bubble","star"};case 40:return new String[]{"lily","flower","shell"};case 41:return new String[]{"orange","leaf","flower"};case 42:return new String[]{"acorn","leaf","mushroom"};"""
  return need(text,'default:return new String[]{"flower","heart","star"};',cases+'default:return new String[]{"flower","heart","star"};')
 edit('String[] motifs(',more_motifs)
 gradle=Path('app/build.gradle');g=gradle.read_text();v=re.search(r'versionCode\s+(\d+)',g)
 if not v:raise RuntimeError('versionCode missing')
 s=s.replace(MARK,MARK+'\n // COMFORT_VERSION_CODE:'+str(int(v.group(1))+1),1)
 s=s.replace('Version 7.0','Version 7.1')
 balanced(s)
 p.write_text(s,encoding='utf-8')
# Studio recreates Java notification resources on every run; reapply the icon each time.
icon='<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:fillType="evenOdd" android:pathData="M5.5,10C4,4 4,1 6,1C8,1 9,5 9.5,8C11,7.5 13,7.5 14.5,8C15,5 16,1 18,1C20,1 20,4 18.5,10C21,12 22,14 21,17C20,22 4,22 3,17C2,14 3,12 5.5,10Z M7.8,13a1,1 0,1 0,2,0a1,1 0,1 0,-2,0Z M14.2,13a1,1 0,1 0,2,0a1,1 0,1 0,-2,0Z M8.6,16C9.8,19 14.2,19 15.4,16L14.1,16C13.4,17.4 10.6,17.4 9.9,16Z M5.8,3C5.1,3 6.1,7.7 6.8,8.8L7.6,8.3C7.1,6.4 6.5,3 5.8,3Z M18.2,3C18.9,3 17.9,7.7 17.2,8.8L16.4,8.3C16.9,6.4 17.5,3 18.2,3Z"/></vector>'
ET.fromstring(icon)
target=Path('app/src/main/res/drawable/ic_notification_bunny.xml');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(icon,encoding='utf-8')
count=0
for source in Path('app/src/main/java/uk/co/littledays').rglob('*.java'):
 text=source.read_text(encoding='utf-8')
 updated,n=re.subn(r'\.setSmallIcon\([^()\n;]+\)', '.setSmallIcon(uk.co.littledays.R.drawable.ic_notification_bunny)',text)
 if n:
  balanced(updated);source.write_text(updated,encoding='utf-8');count+=n
if not count:raise RuntimeError('No notification small-icon call found; stop rather than silently leave a white square')
s=p.read_text(encoding='utf-8');saved=re.search(r'// COMFORT_VERSION_CODE:(\d+)',s)
if not saved:raise RuntimeError('Saved comfort version code missing')
gradle=Path('app/build.gradle');g=gradle.read_text();g=re.sub(r'versionCode\s+\d+','versionCode '+saved.group(1),g);g=re.sub(r'versionName\s+[\'\"][^\'\"]+[\'\"]','versionName "7.1"',g);gradle.write_text(g)
Path('VERSION-7.1-NOTES.txt').write_text("""A Day To Keep 7.1
Home character/tagline moved up 18dp without moving the centered title/settings button.
Calendar arrows use centered vector chevrons rather than baseline-sensitive text.
Reminder small icon is a transparent monochrome bunny-face stencil, not a launcher tile.
Attachment viewer image is clipped below a high-elevation toolbar drawn last.
Notes use gap-filling shortest-column placement, nine theme-matched pastel blends chosen
stably per note ID, and saved long-press drag-to-reorder. New notes precede existing saved
order; edits do not reshuffle saved notes. Deletion remains inside the editor only.
The note editor no longer has an All notes row. Delete sits top right; title remains
outside the body and there is no outer form ScrollView. Body shrinks at its bottom for
the keyboard using the existing note IME inset handling. Android Back returns to Notes.
Reminder wheels have explicit rounded drawing clips, native dividers disabled and two
local-width custom separators per wheel. Redundant 24-hour caption is hidden.
Home Notes shortcut has a paper-and-pencil icon distinct from CPD.
12 themes appended without changing old indices: Peony Piglet, Apricot Hamster,
Moonlit Moth, Cloudy Lamb, Jade Dragon, Peach Seal, Lavender Llama, Dusky Bat,
Marshmallow Yeti, Rose Flamingo, Citrus Chameleon, Toffee Squirrel. 43 themes total.
New data field noteOrder stores note IDs only; notes themselves are not removed/recreated.
Full JSON backups preserve order. Existing notes/tasks, reminders, widgets, PDFs and the
working edge-to-edge/keyboard repairs remain. App ID/signing materials are unchanged.
Static generator/Java delimiter tests only here; actual Android compilation and emulator
checks run on GitHub. Physical drag, keyboard, zoom and notification appearance still
require phone validation. Save an in-app backup before installing over the existing app.
""",encoding='utf-8')
print('Version 7.1 notes layout/reordering, UI refinements, bunny notification and twelve themes prepared.')
