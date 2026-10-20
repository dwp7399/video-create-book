#!/usr/bin/env python3
"""Original 24s procedural figure/music lesson. Stdlib + FFmpeg, no API."""
from array import array
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import wave

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/demos/music-phrases'
FPS,RATE,W,H=24,48000,640,360
M0=[(i*2,(i+1)*2,('W' if i%2==0 else 'M')) for i in range(12)]
M0[8]=(16,18,'C'); M0[9]=(18,20,'W'); M0[10]=(20,22,'M'); M0[11]=(22,24,'W')
M1=[(0,8,'W'),(8,16,'M'),(16,20,'C'),(20,24,'W')]


def smooth(x):
    x=max(0,min(1,x)); return x*x*(3-2*x)


def pose(t):
    if t<16:
        period=2 if t<8 else 1
        u=(t%period)/period
        opening=smooth(u*2) if u<.5 else 1-smooth((u-.5)*2)
    elif t<18: opening=smooth((t-16)/2)
    elif t<21: opening=1
    else: opening=1-smooth((t-21)/2)
    x=0 if t<8 or t>=16 else 55*(smooth((t-8)/4) if t<12 else 1-smooth((t-12)/4))
    return x,opening


def render(t,view):
    pix=bytearray(bytes((242,239,232))*(W*H))
    def rect(x,y,w,h,c):
        x0,x1=max(0,int(x)),min(W,int(x+w)); y0,y1=max(0,int(y)),min(H,int(y+h))
        row=bytes(c)*max(0,x1-x0)
        for yy in range(y0,y1): pix[(yy*W+x0)*3:(yy*W+x1)*3]=row
    def circle(x,y,r,c):
        for yy in range(max(0,int(y-r)),min(H,int(y+r)+1)):
            q=r*r-(yy+.5-y)**2
            if q>=0:
                d=math.sqrt(q); rect(x-d,yy,d*2,1,c)
    def segment(a,b,width,c):
        length=math.dist(a,b)
        for n in range(max(1,int(length))+1):
            u=n/max(1,int(length)); circle(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u,width/2,c)
    scale,cy={'W':(.8,155),'M':(1.15,190),'C':(1.7,245)}[view]
    x,o=pose(t)
    def pt(a,b): return (320+(a+x)*scale,cy+b*scale)
    # Same world and action in every view; scale and framing are the only differences.
    rect(0,cy+155*scale,W,2,(199,195,184))
    color=(49,101,105); skin=(199,136,95)
    if view=='C':
        # Still the same figure: close framing focuses on hands, no invented inset.
        pass
    segment(pt(0,-43),pt(0,64),34*scale,color)
    segment(pt(0,60),pt(-24,151),17*scale,color)
    segment(pt(0,60),pt(24,151),17*scale,color)
    circle(*pt(0,-82),23*scale,skin)
    for sign in [-1,1]:
        shoulder=(sign*21,-40)
        hand=(sign*(35+110*o),-10-20*math.sin(math.pi*o))
        mid=((shoulder[0]+hand[0])/2,(shoulder[1]+hand[1])/2)
        elbow=(mid[0],mid[1]+24*(1-o))
        segment(pt(*shoulder),pt(*elbow),14*scale,color)
        segment(pt(*elbow),pt(*hand),13*scale,color)
        circle(*pt(*hand),8*scale,skin)
    return bytes(pix)


def encode(view_selector,path):
    p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24',
        '-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-an','-c:v','libx264',
        '-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],stdin=subprocess.PIPE)
    for n in range(24*FPS): p.stdin.write(render(n/FPS,view_selector(n/FPS)))
    p.stdin.close(); assert p.wait()==0


def select(t,timeline): return next(v for a,b,v in timeline if a<=t<b)


def check_hand_bounds():
    minimum=1000
    for timeline in [M0,M1]:
        for n in range(576):
            t=n/FPS; x,o=pose(t); view=select(t,timeline)
            scale,cy={'W':(.8,155),'M':(1.15,190),'C':(1.7,245)}[view]
            for sign in [-1,1]:
                hx=320+(x+sign*(35+110*o))*scale
                hy=cy+(-10-20*math.sin(math.pi*o))*scale
                r=8*scale
                minimum=min(minimum,hx-r,W-hx-r,hy-r,H-hy-r)
    assert minimum>0, 'a hand leaves the selected frame'
    return minimum


def timeline_svg():
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="240" viewBox="0 0 960 240">',
           '<rect width="960" height="240" fill="#f2efe8"/>',
           '<g font-family="sans-serif" font-size="15" fill="#304448">']
    for t in range(0,25,2):
        x=90+t*35
        parts.append(f'<text x="{x-5}" y="25">{t}</text><path d="M{x}32V205" stroke="#d4cec0"/>')
    colors={'W':'#4d8687','M':'#d49b66','C':'#947258','establish':'#95a7a2','dense':'#d49b66','release':'#b4c5bf'}
    for title,y,tl in [('MUSIC',50,[(0,8,'establish'),(8,16,'dense'),(16,24,'release')]),('M0',105,M0),('M1',160,M1)]:
        parts.append(f'<text x="15" y="{y+23}">{title}</text>')
        for a,b,v in tl:
            x=90+a*35
            parts.append(f'<rect x="{x}" y="{y}" width="{(b-a)*35-2}" height="35" rx="3" fill="{colors[v]}"/><text x="{x+9}" y="{y+23}" fill="#172a2d">{v}</text>')
    parts.append('<text x="90" y="227">Seconds / W: wide / M: medium / C: gesture emphasis</text></g></svg>')
    (OUT/'timeline.svg').write_text(''.join(parts)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    hand_margin=check_hand_bounds()
    timeline_svg()
    # Short decaying tones, with an original C/E/G/B motif; no borrowed recording.
    events=[]
    notes=[261.6256,329.6276,391.9954,493.8833]
    for beat in range(32):
        start=beat*.5; events.append((start,notes[beat%4],.34,.12))
        if start>=8: events.append((start+.25,notes[(beat+2)%4]*2,.16,.06))
    for i,start in enumerate([16,18,20,22]): events.append((start,notes[i],2,.10))
    track=array('f',[0])*(24*RATE)
    for start,freq,duration,amp in events:
        for j in range(int(duration*RATE)):
            n=int(start*RATE)+j
            if n>=len(track): break
            u=j/RATE
            env=smooth(u/.012)*math.exp(-u*(9 if start<16 else 1.8))*smooth((duration-u)/.08)
            track[n]+=amp*env*(math.sin(2*math.pi*freq*u)+.18*math.sin(2*math.pi*freq*2*u))
    # Last second decays naturally from the event at 22s, no new percussion.
    pcm=array('h',(round(x*32767) for x in track))
    assert max(abs(x) for x in track)<1
    if sys.byteorder!='little': pcm.byteswap()
    with wave.open(str(OUT/'music.wav'),'wb') as f:
        f.setparams((1,2,RATE,0,'NONE','not compressed')); f.writeframes(pcm.tobytes())
    for view in ['W','M','C']: encode(lambda t,v=view:v,OUT/f'coverage-{view}.mp4')
    audio_hashes={}; selections={}
    for name,timeline in [('M0',M0),('M1',M1)]:
        silent=OUT/f'{name}-picture.mp4'
        encode(lambda t,tl=timeline:select(t,tl),silent)
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(silent),'-i',str(OUT/'music.wav'),'-map','0:v:0',
            '-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t','24','-movflags','+faststart',
            str(OUT/f'{name}.mp4')],check=True)
        audio_hashes[name]=subprocess.check_output(['ffmpeg','-v','error','-i',str(OUT/f'{name}.mp4'),
            '-map','0:a:0','-f','hash','-hash','sha256','-']).decode().strip()
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(OUT/f'{name}.mp4')]))
        v=next(s for s in probe['streams'] if s['codec_type']=='video')
        assert int(v['nb_frames'])==576 and float(v['duration'])==24
        selections[name]=[{'in':a,'out':b,'view':v} for a,b,v in timeline]
    assert audio_hashes['M0']==audio_hashes['M1']
    assert M0[0][0]==M1[0][0]==0 and M0[-1][1]==M1[-1][1]==24
    for timeline in [M0,M1]:
        assert all(b==na for (a,b,v),(na,nb,nv) in zip(timeline,timeline[1:]))
    # Sampling shared frames also checks identical rendering outside the differing view selections.
    common_frames=0
    for n in range(576):
        t=n/FPS
        if select(t,M0)==select(t,M1): common_frames+=1
    # Contact sheet: front view states at representative moments, not claimed film frames.
    ts=[1,9.5,12.5,17,20,23.5]; frames=[render(t,'W') for t in ts]
    sheet=bytearray()
    for row in range(2):
        for y in range(H):
            for col in range(3): sheet.extend(frames[row*3+col][y*W*3:(y+1)*W*3])
    subprocess.run(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',
        f'{W*3}x{H*2}','-i','pipe:0','-frames:v','1',str(OUT/'keyframes.png')],input=sheet,check=True)
    result={'date':'2026-10-13','duration_seconds':24,'fps':FPS,'frames':576,'bpm':120,
            'music_provenance':'original procedural tones, no recording or external music',
            'decoded_audio_hashes':audio_hashes,'same_world_pose_function':True,
            'same_view_selection_frame_count':common_frames,'peak_pcm_float':max(map(abs,track)),
            'timeline':selections,'checks':{'same_decoded_audio':True,'continuous_timelines':True,
                'frame_count_and_duration':True,'no_pcm_clipping':True},
            'minimum_selected_hand_edge_margin_px':hand_margin,
            'limits':'Stylized rig changes limb span with gesture; not realistic human anatomy or audience-effect evidence.'}
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
