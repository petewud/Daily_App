  @Override protected void onDraw(Canvas c){long now=SystemClock.uptimeMillis();float dt=Math.min(.05f,(now-last)/1000f);last=now;float t=(now-born)/1000f;int W=getWidth(),H=getHeight();if(W==0)return;step(dt);
   scale=Math.max(3,Math.round(W/140f));float vw=W/(float)scale,vh=H/(float)scale;cx0=sn(Math.max(0,Math.min(WW-vw,px-vw/2)));cy0=sn(Math.max(0,Math.min(WH-vh,py-vh/2)));
   c.drawColor(0xFF3E72C6);c.save();c.scale(scale,scale);c.translate(-cx0,-cy0);c.drawBitmap(world,0,0,pix);
   fill.setColor(0x99FFFFFF);for(float[] f:sparks){float ph=(t*1.1f+f[2])%3f;if(ph<.6f)c.drawRect(f[0],f[1],f[0]+2,f[1]+1,fill);}
   for(Plot p:plots)c.drawBitmap(p.wet?holeWet:holeDry,p.cx*12+1,p.cy*12+4,pix);
   for(float[] s:spots)if(s[3]==0){Bitmap b=itemBmp[(int)s[2]];c.drawBitmap(b,Math.round(s[0])-b.getWidth()/2,Math.round(s[1])-b.getHeight()+2,pix);}
   if(hasT){int r=((int)(t*6))%3;int x=Math.round(tx),y=Math.round(ty);fill.setColor(0xDDFFFFFF);c.drawRect(x-2-r,y-2-r,x-1-r,y-1-r,fill);c.drawRect(x+2+r,y-2-r,x+3+r,y-1-r,fill);c.drawRect(x-2-r,y+2+r,x-1-r,y+3+r,fill);c.drawRect(x+2+r,y+2+r,x+3+r,y+3+r,fill);}
   java.util.ArrayList<float[]> lst=new java.util.ArrayList<>(things);for(int i=0;i<plots.size();i++){Plot p=plots.get(i);if(p.crop>=0)lst.add(new float[]{p.cx*12+6,p.cy*12+9,10,0,i});}
   java.util.Collections.sort(lst,(u,k2)->Float.compare(u[1],k2[1]));
   int first=py<=by?0:1;float y1=Math.min(py,by),y2=Math.max(py,by);boolean d1=false,d2=false;
   for(float[] o:lst){if(!d1&&o[1]>y1){drawDyn(c,first);d1=true;}if(!d2&&o[1]>y2){drawDyn(c,1-first);d2=true;}drawThing(c,o);}if(!d1)drawDyn(c,first);if(!d2)drawDyn(c,1-first);
   for(float[] f:flies){float x=sn(f[0]+(float)Math.sin(t*.5f+f[2])*22),y=sn(f[1]+(float)Math.cos(t*.8f+f[2])*14);boolean flap=((((int)(t*9+f[2]*3)))&1)==0;fill.setColor(0xFF3A2A30);c.drawRect(x,y,x+1,y+2,fill);fill.setColor(flyCol[(int)f[3]%5]);if(flap){c.drawRect(x-2,y-1,x,y+1,fill);c.drawRect(x+1,y-1,x+3,y+1,fill);}else{c.drawRect(x-1,y,x,y+1,fill);c.drawRect(x+1,y,x+2,y+1,fill);}}
   for(Part q:parts){fill.setColor(q.col);float x=sn(q.x),y=sn(q.y);c.drawRect(x,y,x+1,y+1,fill);}
   c.restore();int ov=tint();if(ov!=0)c.drawColor(ov);
   fill.setColor(0xFFFFFFFF);for(int i=0;i<spots.size();i++){float[] s=spots.get(i);if(s[3]!=0)continue;float sx=(s[0]-cx0)*scale,sy=(s[1]-cy0)*scale-scale*7;int n=(((int)(t*3+i))&1)==0?2:1;float g=scale;for(int k=-n;k<=n;k++){c.drawRect(sx+k*g-g/2,sy-g/2,sx+k*g+g/2,sy+g/2,fill);c.drawRect(sx-g/2,sy+k*g-g/2,sx+g/2,sy+k*g+g/2,fill);}}
   float rr2=dens*28,bcx=W-insR-dens*16-rr2,bcy=H-insB-dens*16-rr2;bagRect.set(bcx-rr2,bcy-rr2,bcx+rr2,bcy+rr2);closeRect.set(W-insR-dens*60,insT+dens*12,W-insR-dens*12,insT+dens*60);
   fill.setColor(0xCCFFFFFF);c.drawRoundRect(closeRect,dens*16,dens*16,fill);ink.setColor(0xFF6A5560);ink.setStrokeWidth(dens*3);ink.setStrokeCap(Paint.Cap.ROUND);float mx=closeRect.centerX(),my=closeRect.centerY(),q8=dens*8;c.drawLine(mx-q8,my-q8,mx+q8,my+q8,ink);c.drawLine(mx+q8,my-q8,mx-q8,my+q8,ink);
   String cs=""+coins;ink.setTextSize(dens*15);ink.setTextAlign(Paint.Align.LEFT);float cw=ink.measureText(cs)+dens*54;fill.setColor(0xCCFFFFFF);c.drawRoundRect(insL+dens*12,insT+dens*12,insL+dens*12+cw,insT+dens*48,dens*16,dens*16,fill);icon2(c,coinBmp,insL+dens*30,insT+dens*30,dens*2.4f);ink.setColor(0xFF6A5560);c.drawText(cs,insL+dens*44,insT+dens*35,ink);
   ink.setTextAlign(Paint.Align.CENTER);ink.setTextSize(dens*15);
   if(talk>0){float tw0=ink.measureText(line);if(tw0>W-dens*40){ink.setTextSize(dens*15*(W-dens*40)/tw0);tw0=ink.measureText(line);}float tw=tw0+dens*24;float sx=(bx-cx0)*scale,sy=(by-26-cy0)*scale;float l=Math.max(dens*8,Math.min(W-tw-dens*8,sx-tw/2));fill.setColor(0xF5FFFFFF);c.drawRoundRect(l,sy-dens*40,l+tw,sy-dens*6,dens*14,dens*14,fill);ink.setColor(0xFF6A5560);c.drawText(line,l+tw/2,sy-dens*18,ink);ink.setTextSize(dens*15);}
   if(toastT>0){float tw0=ink.measureText(toast);if(tw0>W-dens*40){ink.setTextSize(dens*15*(W-dens*40)/tw0);tw0=ink.measureText(toast);}float tw=tw0+dens*28;float top=insT+dens*70;fill.setColor(0xF2FFF7F0);c.drawRoundRect(W/2f-tw/2,top,W/2f+tw/2,top+dens*40,dens*16,dens*16,fill);ink.setColor(0xFF6A5560);c.drawText(toast,W/2f,top+dens*26,ink);ink.setTextSize(dens*15);}
   if(t<8&&!panel&&!shop&&!logOpen){int al=(int)(255*Math.min(1f,(8-t)/2f));String hint="Tap to walk \u00b7 open the bag for your tools";float tw=ink.measureText(hint)+dens*28;float top=bagRect.top-dens*70;fill.setColor((al*3/5)<<24);c.drawRoundRect(W/2f-tw/2,top,W/2f+tw/2,top+dens*40,dens*16,dens*16,fill);ink.setColor((al<<24)|0xFFFFFF);c.drawText(hint,W/2f,top+dens*26,ink);}
   float pl=insL+dens*10,pr=W-insR-dens*10,gap=dens*6,sw=(pr-pl-dens*16-gap*4)/5f,shh=dens*72;int cols=5;
   if(panel&&!shop&&!logOpen){slotsBuild();int n=slots.size(),rows=(n+cols-1)/cols;float ph=dens*34+rows*(shh+gap)+dens*40;float pb=bagRect.top-dens*10,pt=pb-ph;panelRect.set(pl,pt,pr,pb);
    fill.setColor(0xF4FFF7F0);c.drawRoundRect(panelRect,dens*18,dens*18,fill);ink.setTextSize(dens*12);ink.setColor(0xFF8A7080);ink.setTextAlign(Paint.Align.LEFT);c.drawText("Pockets",pl+dens*12,pt+dens*21,ink);ink.setTextAlign(Paint.Align.CENTER);
    logBtn.set(pr-dens*104,pt+dens*6,pr-dens*10,pt+dens*30);fill.setColor(0xFFF3E6DE);c.drawRoundRect(logBtn,dens*12,dens*12,fill);txt(c,"Bug log "+Integer.bitCount(bugSeen&1023)+"/10",logBtn.centerX(),logBtn.centerY()+dens*4,dens*11,dens*84,0xFF6A5560);
    slotR.clear();
    for(int i=0;i<n;i++){int[] s=slots.get(i);int row=i/cols,col=i%cols;float l=pl+dens*8+col*(sw+gap),tp=pt+dens*30+row*(shh+gap);RectF r=new RectF(l,tp,l+sw,tp+shh);slotR.add(r);
     boolean eq=(s[0]==0&&tool==s[1])||(s[0]==1&&tool==2&&seed==s[1]);fill.setColor(eq?0xFFFFD9A8:0xFFF3E6DE);c.drawRoundRect(r,dens*14,dens*14,fill);
     iconFit(c,slotBmp(s),r.centerX(),r.top+dens*24,dens*30);txt(c,slotName(s),r.centerX(),r.bottom-dens*22,dens*10,sw-dens*6,0xFF6A5560);
     String lb=s[0]==0?(s[1]==3?water+"/10":s[1]==5?"x"+s[2]:""):"x"+s[2];if(lb.length()>0)txt(c,lb,r.centerX(),r.bottom-dens*7,dens*12,sw-dens*6,0xFF8A7080);
     if((seen&bit(s))==0){fill.setColor(0xFFF0607E);c.drawRoundRect(r.right-dens*30,r.top+dens*3,r.right-dens*3,r.top+dens*17,dens*7,dens*7,fill);txt(c,"New!",r.right-dens*16.5f,r.top+dens*13.5f,dens*9,dens*26,0xFFFFFFFF);}}
    fastRect.set(pl+dens*8,pb-dens*30,pr-dens*8,pb-dens*8);fill.setColor(fast?0xFFFFD9A8:0xFFF3E6DE);c.drawRoundRect(fastRect,dens*12,dens*12,fill);txt(c,"Fast growth (testing): "+(fast?"on":"off"),fastRect.centerX(),fastRect.centerY()+dens*4,dens*12,pr-pl-dens*40,0xFF6A5560);}
   if(shop){cardsBuild();int nb=0;for(int[] q:cardI)if(q[0]!=2&&q[0]!=3)nb++;int ns=cardI.size()-nb;int rb=(nb+cols-1)/cols,rs=Math.max(1,(ns+cols-1)/cols);float ph=dens*60+rb*(shh+gap)+dens*20+rs*(shh+gap)+dens*8;float pb=bagRect.top-dens*10,pt=pb-ph;panelRect.set(pl,pt,pr,pb);
    fill.setColor(0xF4FFF7F0);c.drawRoundRect(panelRect,dens*18,dens*18,fill);ink.setTextAlign(Paint.Align.LEFT);ink.setTextSize(dens*15);ink.setColor(0xFF6A5560);c.drawText("Clover's Stall",pl+dens*12,pt+dens*26,ink);ink.setTextSize(dens*12);ink.setColor(0xFF8A7080);c.drawText("Buy",pl+dens*12,pt+dens*52,ink);c.drawText("Sell - tap an item",pl+dens*12,pt+dens*60+rb*(shh+gap)+dens*12,ink);
    shopX.set(pr-dens*44,pt+dens*6,pr-dens*8,pt+dens*38);ink.setColor(0xFF6A5560);ink.setStrokeWidth(dens*2.5f);float xx=shopX.centerX(),xy=shopX.centerY(),xq=dens*6;c.drawLine(xx-xq,xy-xq,xx+xq,xy+xq,ink);c.drawLine(xx+xq,xy-xq,xx-xq,xy+xq,ink);ink.setTextAlign(Paint.Align.CENTER);
    cardR.clear();int bi=0,si=0;
    for(int i=0;i<cardI.size();i++){int[] q=cardI.get(i);boolean buy=q[0]!=2&&q[0]!=3;int idx=buy?bi++:si++;int row=idx/cols,col=idx%cols;float l=pl+dens*8+col*(sw+gap);float tp=buy?pt+dens*60+row*(shh+gap):pt+dens*60+rb*(shh+gap)+dens*20+row*(shh+gap);RectF r=new RectF(l,tp,l+sw,tp+shh);cardR.add(r);
     fill.setColor(buy&&coins<q[2]?0xFFE9DDD6:0xFFF3E6DE);c.drawRoundRect(r,dens*14,dens*14,fill);
     iconFit(c,cardBmp(q),r.centerX(),r.top+dens*22,dens*28);txt(c,cardName(q),r.centerX(),r.bottom-dens*22,dens*10,sw-dens*6,0xFF6A5560);
     icon2(c,coinBmp,r.centerX()-dens*14,r.bottom-dens*10,dens*1.3f);txt(c,""+q[2],r.centerX()+dens*8,r.bottom-dens*6,dens*12,sw-dens*26,0xFF6A5560);
     if(!buy){int have=q[0]==2?it[q[1]]:bug[q[1]];txt(c,"x"+have,r.right-dens*14,r.top+dens*13,dens*11,dens*24,0xFF8A7080);}}
    if(ns==0)txt(c,"Nothing to sell yet",panelRect.centerX(),pt+dens*60+rb*(shh+gap)+dens*20+shh/2f,dens*12,pr-pl-dens*40,0xFF8A7080);}
   if(logOpen){float ph=dens*50+2*(shh+gap)+dens*10;float pb=bagRect.top-dens*10,pt=pb-ph;panelRect.set(pl,pt,pr,pb);fill.setColor(0xF4FFF7F0);c.drawRoundRect(panelRect,dens*18,dens*18,fill);
    ink.setTextAlign(Paint.Align.LEFT);ink.setTextSize(dens*15);ink.setColor(0xFF6A5560);c.drawText("Bug log  "+Integer.bitCount(bugSeen&1023)+"/10",pl+dens*12,pt+dens*26,ink);
    logX.set(pr-dens*44,pt+dens*6,pr-dens*8,pt+dens*38);ink.setStrokeWidth(dens*2.5f);float xx=logX.centerX(),xy=logX.centerY(),xq=dens*6;c.drawLine(xx-xq,xy-xq,xx+xq,xy+xq,ink);c.drawLine(xx+xq,xy-xq,xx-xq,xy+xq,ink);ink.setTextAlign(Paint.Align.CENTER);
    for(int i=0;i<10;i++){int row=i/cols,col=i%cols;float l=pl+dens*8+col*(sw+gap),tp=pt+dens*46+row*(shh+gap);RectF r=new RectF(l,tp,l+sw,tp+shh);boolean got=((bugSeen>>i)&1)!=0;fill.setColor(0xFFF3E6DE);c.drawRoundRect(r,dens*14,dens*14,fill);
     if(got)iconFit(c,bugBmp[i],r.centerX(),r.top+dens*24,dens*30);else sil(c,bugBmp[i],r.centerX(),r.top+dens*24,dens*30);
     txt(c,got?bname[i]:"???",r.centerX(),r.bottom-dens*22,dens*10,sw-dens*6,0xFF6A5560);if(bug[i]>0)txt(c,"x"+bug[i],r.centerX(),r.bottom-dens*7,dens*12,sw-dens*6,0xFF8A7080);}}
   ink.setTextAlign(Paint.Align.CENTER);fill.setColor(panel||shop||logOpen?0xFFFFD9A8:0xF4FFF7F0);c.drawCircle(bcx,bcy,rr2,fill);iconFit(c,bagBmp,bcx,bcy,dens*34);
   chipRect.setEmpty();
   if(tool!=0){float chx=bcx-rr2-dens*32;chipRect.set(chx-dens*22,bcy-dens*22,chx+dens*22,bcy+dens*22);fill.setColor(0xF4FFF7F0);c.drawCircle(chx,bcy,dens*22,fill);Bitmap b=tool==2?packBmp[seed]:tool==4?axeBmp:tool==5?sapBmp[1]:tool==6?netBmp:toolBmp[tool];iconFit(c,b,chx,bcy,dens*28);
    if(tool==3||tool==2||tool==5)txt(c,""+(tool==3?water:tool==2?seeds[seed]:sapN),chx,bcy+dens*34,dens*11,dens*30,0xFF6A5560);}
   if(pop!=0){fill.setColor(0x99000000);c.drawRect(0,0,W,H,fill);float pw=Math.min(W-dens*40,dens*300),ph2=dens*290;float l=(W-pw)/2f,tp=(H-ph2)/2f,cxm=W/2f;popRect.set(l,tp,l+pw,tp+ph2);fill.setColor(0xFFFFF7F0);c.drawRoundRect(popRect,dens*22,dens*22,fill);
    int[] pc=new int[]{popType,popId,popPrice};iconFit(c,cardBmp(pc),cxm,tp+dens*46,dens*56);txt(c,cardName(pc),cxm,tp+dens*98,dens*17,pw-dens*40,0xFF6A5560);
    if(popMax>1){pMinus.set(cxm-dens*104,tp+dens*112,cxm-dens*56,tp+dens*158);pPlus.set(cxm+dens*56,tp+dens*112,cxm+dens*104,tp+dens*158);pMax.set(cxm-dens*36,tp+dens*164,cxm+dens*36,tp+dens*190);
     fill.setColor(0xFFF3E6DE);c.drawRoundRect(pMinus,dens*14,dens*14,fill);c.drawRoundRect(pPlus,dens*14,dens*14,fill);c.drawRoundRect(pMax,dens*12,dens*12,fill);
     txt(c,"-",pMinus.centerX(),pMinus.centerY()+dens*8,dens*26,dens*40,0xFF6A5560);txt(c,"+",pPlus.centerX(),pPlus.centerY()+dens*8,dens*26,dens*40,0xFF6A5560);txt(c,"Max",pMax.centerX(),pMax.centerY()+dens*5,dens*13,dens*60,0xFF6A5560);txt(c,""+popQty,cxm,tp+dens*146,dens*26,dens*60,0xFF6A5560);}
    else{pMinus.setEmpty();pPlus.setEmpty();pMax.setEmpty();}
    txt(c,(pop==1?"You'll get ":"Costs ")+(popQty*popPrice)+" coins",cxm,tp+dens*218,dens*15,pw-dens*40,0xFF8A7080);
    pOk.set(l+dens*28,tp+dens*232,l+pw-dens*28,tp+dens*276);fill.setColor(pop==1||coins>=popQty*popPrice?0xFFFFB766:0xFFE0D2C8);c.drawRoundRect(pOk,dens*18,dens*18,fill);txt(c,pop==1?"Sell":"Buy",pOk.centerX(),pOk.centerY()+dens*6,dens*18,dens*80,0xFF5A3A28);}
   else{popRect.setEmpty();pOk.setEmpty();pMinus.setEmpty();pPlus.setEmpty();pMax.setEmpty();}
   if(running)postInvalidateOnAnimation();}
 }
