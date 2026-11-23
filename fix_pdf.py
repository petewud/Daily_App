#!/usr/bin/env python3
"""A Day To Keep 5.0 startup hardening and PDF-to-image attachments. Run after v4."""
from pathlib import Path
import re
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text(encoding='utf-8')
if '// A_DAY_TO_KEEP_V4' not in s:raise SystemExit('The existing v2/v3/v4 preparation steps must run first.')
MARK='// A_DAY_TO_KEEP_V5'
def replace_section(start,end,replacement):
 global s
 a=s.find(start)
 if a<0:raise RuntimeError('Source section missing: '+start)
 b=s.find(end,a+len(start))
 if b<0:raise RuntimeError('Source section end missing: '+end)
 s=s[:a]+replacement+'\n '+s[b:]
def required(old,new):
 global s
 if old not in s:raise RuntimeError('Expected code missing: '+old[:130])
 s=s.replace(old,new,1)
if MARK not in s:
 # Keep the functional v4 layout, recurrence and theme choices, but remove fragile
 # custom animated Drawable surfaces from the launch screen.
 replace_section('GradientDrawable shape(int color){','class BevelDrawable extends',r"""GradientDrawable shape(int color){GradientDrawable g=new GradientDrawable(GradientDrawable.Orientation.TL_BR,new int[]{blend(color,Color.WHITE,.18f),color});g.setCornerRadius(dp(22));g.setStroke(dp(1),blend(color,INK,.18f));return g;}
 """)
 # Leave the old artwork classes defined for compatibility; only use standard
 # framework surfaces on the main panels until the launch test has passed.
 replace_section('LinearLayout section(int color){','class FloatingCard extends',r"""LinearLayout section(int color){LinearLayout box=col();box.setPadding(dp(11),dp(11),dp(11),dp(11));box.setBackground(shape(color));box.setElevation(dp(2));box.setClipChildren(true);box.setClipToPadding(true);return box;}
 """)
 # Standard inset handling is more conservative across Android versions.
 replace_section('void edgeToEdge(){','LinearLayout section(',r"""void edgeToEdge(){Window w=getWindow();w.setDecorFitsSystemWindows(true);w.setStatusBarColor(CREAM);w.setNavigationBarColor(CREAM);w.getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR|View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);}
 """)
 replace_section('void base(String title,boolean back){','void render(',r"""void base(String title,boolean back){edgeToEdge();cardSequence=0;root=col();root.setBackground(new Gingham());root.setClipChildren(false);root.setClipToPadding(false);root.setPadding(dp(16),dp(10),dp(16),dp(16));setContentView(root);LinearLayout top=row();if(back)top.addView(button("Home","home",WHITE,()->home()));TextView h=label(title,back?22:26);h.setPadding(dp(10),dp(3),0,dp(3));h.setMaxLines(2);top.addView(h,new LinearLayout.LayoutParams(0,dp(58),1));if(!back)top.addView(button("","gear",WHITE,()->settings()));root.addView(top);space(root,8);}
 """)
 # Audio is nonessential: an unavailable audio service must never close the app.
 replace_section('void initSounds(){','void migrateTasks(){',r"""void initSounds(){try{sounds=new android.media.SoundPool.Builder().setMaxStreams(3).setAudioAttributes(new android.media.AudioAttributes.Builder().setUsage(android.media.AudioAttributes.USAGE_ASSISTANCE_SONIFICATION).setContentType(android.media.AudioAttributes.CONTENT_TYPE_SONIFICATION).build()).build();sounds.setOnLoadCompleteListener((pool,id,status)->{if(status==0)loadedSounds.add(id);});checkSound=sounds.load(this,uk.co.littledays.R.raw.check,1);softSound=sounds.load(this,uk.co.littledays.R.raw.soft,1);readySound=sounds.load(this,uk.co.littledays.R.raw.ready,1);}catch(RuntimeException e){android.util.Log.w("ADayToKeep","Sound unavailable",e);if(sounds!=null){try{sounds.release();}catch(RuntimeException ignored){}sounds=null;}}}
 void chime(int id){try{if(sounds==null||data==null||!data.optBoolean("sounds",true)||!loadedSounds.contains(id))return;android.media.AudioManager audio=(android.media.AudioManager)getSystemService(AUDIO_SERVICE);if(audio==null||audio.getRingerMode()!=android.media.AudioManager.RINGER_MODE_NORMAL)return;sounds.play(id,.18f,.18f,1,0,1);}catch(RuntimeException e){android.util.Log.w("ADayToKeep","Could not play sound",e);}}
 """)
 # Retain v4's marker, which was originally immediately before migrateTasks.
 if '// A_DAY_TO_KEEP_V4' not in s:s=s.replace('void migrateTasks(){','// A_DAY_TO_KEEP_V4\n void migrateTasks(){',1)
 # Decoding PDF pages shares exactly the same entry.images array as photo imports.
 start='content.addView(button("Attach images","photo",MINT,()->{'
 a=s.find(start)
 if a<0:raise RuntimeError('Cannot locate original journal attachment button')
 end='startActivityForResult(i,101);}));'
 b=s.find(end,a)
 if b<0:raise RuntimeError('Cannot locate attachment button end')
 s=s[:a]+'attachmentActions(content);'+s[b+len(end):]
 required('if(result!=RESULT_OK||intent==null)return;if(req==101)', 'if(result!=RESULT_OK||intent==null)return;if(req==105){if(intent.getData()!=null)importPdf(intent.getData(),imageDate==null?selected:imageDate);return;}if(req==101)')
 additions=r"""
 // A_DAY_TO_KEEP_V5
 boolean startupFault=false,pdfImportBusy=false;
 void attachmentActions(LinearLayout container){LinearLayout actions=row();View image=button("Add images","photo",MINT,()->{imageDate=selected;Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.setType("image/*");i.putExtra(Intent.EXTRA_ALLOW_MULTIPLE,true);i.addCategory(Intent.CATEGORY_OPENABLE);startActivityForResult(i,101);});View pdf=button("Add PDF","book",LILAC,()->{if(pdfImportBusy){toast("Please wait for the current PDF import");return;}imageDate=selected;Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.setType("application/pdf");i.addCategory(Intent.CATEGORY_OPENABLE);startActivityForResult(i,105);});for(View v:new View[]{image,pdf}){v.setPadding(dp(8),dp(8),dp(8),dp(8));if(v instanceof LinearLayout){LinearLayout r=(LinearLayout)v;if(r.getChildCount()>1&&r.getChildAt(1) instanceof TextView)((TextView)r.getChildAt(1)).setTextSize(14);}}LinearLayout.LayoutParams left=new LinearLayout.LayoutParams(0,-2,1);left.setMargins(0,0,dp(5),0);actions.addView(image,left);LinearLayout.LayoutParams right=new LinearLayout.LayoutParams(0,-2,1);right.setMargins(dp(5),0,0,0);actions.addView(pdf,right);container.addView(actions);}
 void importPdf(Uri uri,LocalDate date){if(pdfImportBusy)return;pdfImportBusy=true;LinearLayout box=col();box.setPadding(dp(22),dp(14),dp(22),dp(18));ProgressBar spinner=new ProgressBar(this);box.addView(spinner,new LinearLayout.LayoutParams(-1,dp(46)));TextView progress=text("Preparing PDF…",16);progress.setPadding(0,dp(10),0,0);box.addView(progress);AlertDialog wait=new AlertDialog.Builder(this).setTitle("Adding PDF pages").setView(box).create();wait.setCancelable(false);showCute(wait);
 worker.execute(()->{File source=null;ArrayList<String> added=new ArrayList<>();String error=null;android.graphics.pdf.PdfRenderer renderer=null;ParcelFileDescriptor descriptor=null;
 try{source=File.createTempFile("cpd-pdf-",".pdf",getCacheDir());try(InputStream in=getContentResolver().openInputStream(uri);OutputStream out=new FileOutputStream(source)){if(in==null)throw new IOException("Cannot read the selected document");byte[] buffer=new byte[32768];long total=0;int count;while((count=in.read(buffer))!=-1){total+=count;if(total>100L*1024*1024)throw new IOException("Please choose a PDF smaller than 100 MB");out.write(buffer,0,count);}}
 descriptor=ParcelFileDescriptor.open(source,ParcelFileDescriptor.MODE_READ_ONLY);renderer=new android.graphics.pdf.PdfRenderer(descriptor);descriptor=null;int pages=renderer.getPageCount();if(pages==0)throw new IOException("This PDF has no pages");if(pages>50)throw new IOException("Please split this PDF into documents of 50 pages or fewer");
 for(int index=0;index<pages;index++){final int pageNumber=index+1;runOnUiThread(()->{if(!isFinishing()&&!isDestroyed())progress.setText("Converting page "+pageNumber+" of "+pages+"…");});android.graphics.pdf.PdfRenderer.Page page=null;Bitmap rendered=null,flat=null;File image=new File(photos(),UUID.randomUUID()+".jpg");
 try{page=renderer.openPage(index);int pw=page.getWidth(),ph=page.getHeight();if(pw<=0||ph<=0)throw new IOException("Invalid page dimensions");float factor=2200f/Math.max(pw,ph);int width=Math.max(1,Math.round(pw*factor)),height=Math.max(1,Math.round(ph*factor));rendered=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888);rendered.eraseColor(Color.WHITE);page.render(rendered,null,null,android.graphics.pdf.PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY);flat=Bitmap.createBitmap(width,height,Bitmap.Config.RGB_565);Canvas canvas=new Canvas(flat);canvas.drawColor(Color.WHITE);canvas.drawBitmap(rendered,0,0,new Paint(Paint.ANTI_ALIAS_FLAG|Paint.FILTER_BITMAP_FLAG));try(OutputStream out=new FileOutputStream(image)){if(!flat.compress(Bitmap.CompressFormat.JPEG,95,out))throw new IOException("Could not save page "+pageNumber);}added.add(image.getName());}
 catch(Exception|OutOfMemoryError ex){image.delete();throw ex;}
 finally{if(page!=null)page.close();if(flat!=null)flat.recycle();if(rendered!=null)rendered.recycle();}
 }
 }catch(SecurityException e){error="This PDF is password-protected or uses unsupported security. Save an unlocked copy and try again.";}catch(OutOfMemoryError e){error="Not enough memory to convert this PDF. Try a smaller document.";}catch(Exception e){error="Could not import PDF: "+e.getMessage();}
 finally{if(renderer!=null){try{renderer.close();}catch(Exception ignored){}}if(descriptor!=null){try{descriptor.close();}catch(Exception ignored){}}if(source!=null)source.delete();}
 final String failure=error;runOnUiThread(()->{pdfImportBusy=false;if(wait.isShowing()&&!isDestroyed())wait.dismiss();if(failure!=null){for(String file:added)new File(photos(),file).delete();toast(failure);return;}if(isDestroyed())load();JSONArray images=entry(date,true).optJSONArray("images");for(String file:added)images.put(file);save();if(!isDestroyed()&&screen.equals("cpd")&&selected.equals(date))journal();chime(readySound);toast(added.size()+" PDF page(s) added as images");});});
 }
 void startupProblem(Throwable problem){startupFault=true;android.util.Log.e("ADayToKeep","A_DAY_TO_KEEP_STARTUP_ERROR",problem);KeepApplication.record(this,problem);String details=android.util.Log.getStackTraceString(problem);LinearLayout panel=new LinearLayout(this);panel.setOrientation(LinearLayout.VERTICAL);panel.setPadding(dp(22),dp(30),dp(22),dp(20));panel.setBackgroundColor(0xFFFFF5F0);TextView heading=new TextView(this);heading.setText("A Day To Keep · startup report");heading.setTextSize(22);heading.setTextColor(0xFF75576C);panel.addView(heading);TextView explanation=new TextView(this);explanation.setText("The app hit a startup error. Your stored data has not been cleared. Copy the technical report below so it can be fixed; do not reinstall.");explanation.setTextSize(16);explanation.setPadding(0,dp(15),0,dp(15));panel.addView(explanation);ScrollView scroll=new ScrollView(this);TextView report=new TextView(this);report.setText(details);report.setTextSize(12);report.setTextIsSelectable(true);report.setContentDescription("A_DAY_TO_KEEP_STARTUP_ERROR");scroll.addView(report);panel.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));Button copy=new Button(this);copy.setText("Copy technical report");copy.setOnClickListener(v->{android.content.ClipboardManager clipboard=(android.content.ClipboardManager)getSystemService(CLIPBOARD_SERVICE);clipboard.setPrimaryClip(ClipData.newPlainText("A Day To Keep startup report",details));Toast.makeText(this,"Technical report copied",Toast.LENGTH_LONG).show();});panel.addView(copy);Button retry=new Button(this);retry.setText("Retry opening the app");retry.setOnClickListener(v->{new File(getFilesDir(),"last-crash.txt").delete();startupFault=false;recreate();});panel.addView(retry);setContentView(panel);}
 """
 required(' JSONObject data;',additions+'\n JSONObject data;')
 # Wrap lifecycle initialization, leaving framework super calls outside the guard.
 def wrap_method(signature):
  global s
  a=s.find(signature)
  if a<0:raise RuntimeError('Lifecycle method missing: '+signature)
  start=s.find('{',a);depth=1;i=start+1;state='code'
  while i<len(s) and depth:
   c=s[i];pair=s[i:i+2]
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
  if depth:raise RuntimeError('Unbalanced lifecycle method')
  body=s[start+1:i-1]
  supercall='super.onCreate(b);' if 'onCreate' in signature else 'super.onResume();'
  if supercall not in body:raise RuntimeError('Expected lifecycle super call missing')
  body=body.replace(supercall,'',1)
  prefix='if(startupFault)return;'
  if 'onCreate' in signature:
   prefix='File previousCrash=new File(getFilesDir(),"last-crash.txt");if(previousCrash.isFile()){try{String report=new String(java.nio.file.Files.readAllBytes(previousCrash.toPath()),java.nio.charset.StandardCharsets.UTF_8);previousCrash.delete();startupProblem(new RuntimeException("Previous app failure:\\n"+report));return;}catch(IOException ignored){}}'
  s=s[:start+1]+supercall+prefix+'try{'+body+'}catch(RuntimeException|LinkageError failure){startupProblem(failure);}'+s[i-1:]
 wrap_method('public void onCreate(Bundle b)')
 wrap_method('protected void onResume()')
 # Clear crash report after a successful launch, and preserve a machine-readable marker.
 s=s.replace('render();handler.postDelayed(midnight,30000);','render();handler.postDelayed(midnight,30000);new File(getFilesDir(),"last-crash.txt").delete();')
 s=s.replace('Version 4.0','Version 5.0')
 p.write_text(s,encoding='utf-8')
# Application-level crash recording also catches a later draw/layout failure on next launch.
app=p.parent/'KeepApplication.java'
app.write_text(r"""package uk.co.littledays;
public class KeepApplication extends android.app.Application {
 public static void record(android.content.Context context,Throwable error){try{java.io.File file=new java.io.File(context.getFilesDir(),"last-crash.txt");try(java.io.FileOutputStream out=new java.io.FileOutputStream(file)){out.write(android.util.Log.getStackTraceString(error).getBytes(java.nio.charset.StandardCharsets.UTF_8));}}catch(Exception ignored){}}
 @Override public void onCreate(){super.onCreate();Thread.UncaughtExceptionHandler original=Thread.getDefaultUncaughtExceptionHandler();Thread.setDefaultUncaughtExceptionHandler((thread,error)->{record(this,error);if(original!=null)original.uncaughtException(thread,error);else android.os.Process.killProcess(android.os.Process.myPid());});}
}
""",encoding='utf-8')
m=Path('app/src/main/AndroidManifest.xml');manifest=m.read_text()
if 'android:name=".KeepApplication"' not in manifest:manifest=manifest.replace('<application ','<application android:name=".KeepApplication" ',1)
m.write_text(manifest)
gradle=Path('app/build.gradle');g=gradle.read_text();g=re.sub(r'versionCode\s+\d+','versionCode 5',g);g=re.sub(r'versionName\s+[\'\"][^\'\"]+[\'\"]','versionName "5.0"',g);gradle.write_text(g)
Path('VERSION-5-NOTES.txt').write_text("""A Day To Keep 5.0
Startup hardening: standard panel gradients instead of floating panel Drawables;
conservative system-bar insets; optional audio failures do not terminate the app.
No confirmed device stack trace was available; a CI emulator launch test is required.
Failures show/capture a technical report without wiping app data. This does not
certify behaviour on every device. Existing theme and v4 task scheduling retained.
Add PDF sits beside Add images. Each page becomes a separate JPEG image attachment
(maximum 2200px longest edge, JPEG quality 95); all pages share normal photo actions,
backup and PDF export. Text/forms are flattened, not kept editable/searchable.
Limits: PDF up to 100 MB, at most 50 pages, unlocked PDFs only. Failed imports roll back
new page images. Original PDFs are not retained and are never deleted from storage.
Signing identity/package unchanged. Save a backup before updating; do not uninstall.
Animated decorative panel stickers are temporarily replaced by stable gradient panels.
Other character artwork, theme previews, fonts and preferences remain available.
""")
print('Version 5 startup hardening and PDF page-image import prepared.')

smoke = "#!/usr/bin/env python3\nimport subprocess, time, re\nfrom pathlib import Path\nimport xml.etree.ElementTree as ET\nout=Path('startup-diagnostics');out.mkdir(exist_ok=True)\npackage='uk.co.littledays'\ndef adb(*args,check=True):\n r=subprocess.run(['adb',*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)\n if check and r.returncode:raise RuntimeError(r.stderr.decode(errors='replace') or r.stdout.decode(errors='replace'))\n return r.stdout.decode(errors='replace')\ndef hierarchy(name):\n last=None\n for attempt in range(4):\n  try:\n   adb('shell','uiautomator','dump','/sdcard/keep-ui.xml')\n   xml=adb('exec-out','cat','/sdcard/keep-ui.xml')\n   (out/(name+'.xml')).write_text(xml)\n   return ET.fromstring(xml)\n  except Exception as e:last=e;time.sleep(2)\n raise RuntimeError('Could not read app UI: '+str(last))\ndef screenshot(name):\n with (out/(name+'.png')).open('wb') as f:subprocess.run(['adb','exec-out','screencap','-p'],stdout=f,check=True,timeout=30)\ndef alive():\n if not adb('shell','pidof',package,check=False).strip():raise RuntimeError('App process exited after launch')\n crash=adb('shell','run-as',package,'cat','files/last-crash.txt',check=False)\n if crash.strip():\n  (out/'recorded-app-crash.txt').write_text(crash)\n  raise RuntimeError('The app recorded a crash or displayed its startup-report screen')\ndef verify(tree,expected):\n text=' '.join(n.get('text','')+' '+n.get('content-desc','') for n in tree.iter('node'))\n if 'A_DAY_TO_KEEP_STARTUP_ERROR' in text or 'startup report' in text:raise RuntimeError('Startup diagnostic screen detected; this is not a successful launch')\n if expected not in text:raise RuntimeError('Expected UI text missing: '+expected)\ndef tap(tree,needle):\n for n in tree.iter('node'):\n  if needle in (n.get('content-desc',''),n.get('text','')) or needle in n.get('content-desc',''):\n   b=[int(x) for x in re.findall(r'\\d+',n.get('bounds',''))]\n   if len(b)==4 and b[2]>b[0] and b[3]>b[1]:\n    adb('shell','input','tap',str((b[0]+b[2])//2),str((b[1]+b[3])//2));return\n raise RuntimeError('Cannot find control: '+needle)\ntry:\n apk=next(Path('android-project/app/build/outputs/apk/debug').glob('*.apk'))\n adb('install','-r',str(apk));adb('logcat','-c')\n for iteration in range(2):\n  adb('shell','am','force-stop',package)\n  result=adb('shell','am','start','-W','-n',package+'/.MainActivity')\n  (out/('launch-'+str(iteration)+'.txt')).write_text(result)\n  if 'Error:' in result or 'Exception' in result:raise RuntimeError(result)\n  time.sleep(8);alive();tree=hierarchy('home-'+str(iteration));verify(tree,'Work Schedule');verify(tree,'Daily Stuff');screenshot('home-'+str(iteration))\n tap(tree,'CPD');time.sleep(4);alive();tree=hierarchy('cpd');verify(tree,'Add PDF');verify(tree,'Add images');screenshot('cpd')\n tap(tree,'Home');time.sleep(3);tree=hierarchy('home-return');verify(tree,'Work Schedule')\n tap(tree,'Settings');time.sleep(4);alive();tree=hierarchy('settings');verify(tree,'Settings');screenshot('settings')\n print('PASS: two launches, CPD attachment buttons, return Home and Settings; no recorded app crash.')\nfinally:\n for name,args in [('logcat.txt',('logcat','-d','-v','threadtime')),('crash-buffer.txt',('logcat','-d','-b','crash'))]:\n  try:(out/name).write_text(adb(*args,check=False))\n  except Exception:pass\n try:(out/'last-crash.txt').write_text(adb('shell','run-as',package,'cat','files/last-crash.txt',check=False))\n except Exception:pass\n"
Path("tools").mkdir(exist_ok=True)
Path("tools/smoke_test.py").write_text(smoke,encoding="utf-8")
