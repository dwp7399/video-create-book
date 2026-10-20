#!/usr/bin/env python3
"""Generate reproducible fault/repair and pinhole-projection lessons.
Only Python stdlib and local FFmpeg/FFprobe; no model or paid API.
"""
from array import array
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import wave

ROOT=Path(__file__).resolve().parents[1]
FPS=24


def call(*args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL)


def read_wav(path):
    with wave.open(str(path),'rb') as w:
        assert w.getnchannels()==1 and w.getsampwidth()==2
        rate=w.getframerate(); data=array('h',w.readframes(w.getnframes()))
    if sys.byteorder!='little': data.byteswap()
    return rate,data


def write_wav(path,rate,data):
    pcm=array('h',data)
    if sys.byteorder!='little': pcm.byteswap()
    with wave.open(str(path),'wb') as w:
        w.setparams((1,2,rate,0,'NONE','not compressed')); w.writeframes(pcm.tobytes())


def probe(path,frames,duration):
    result=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)]))
    v=next(s for s in result['streams'] if s['codec_type']=='video')
    assert int(v['nb_frames'])==frames and abs(float(v['duration'])-duration)<.001
    return result


def faults():
    src=ROOT/'docs/demos/sound-priority'; out=ROOT/'docs/demos/sync-repair'; out.mkdir(parents=True,exist_ok=True)
    rate,base=read_wav(src/'S1.wav'); r,contact=read_wav(src/'CONTACT.wav'); assert rate==r
    delay=rate//2
    shifted=array('h',[0])*delay+contact[:-delay]
    # Quantized arithmetic is exactly reversible: change CONTACT only.
    wrong=[int(a)-int(b)+int(c) for a,b,c in zip(base,contact,shifted)]
    assert max(map(abs,wrong))<32767
    repaired=[a-int(c)+int(b) for a,b,c in zip(wrong,contact,shifted)]
    assert repaired==list(base)
    write_wav(out/'delayed.wav',rate,wrong); write_wav(out/'repaired.wav',rate,repaired)
    for name in ['delayed','repaired']:
        call('ffmpeg','-y','-v','error','-i',str(src/'picture.mp4'),'-i',str(out/f'{name}.wav'),
             '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t','16',
             '-movflags','+faststart',str(out/f'{name}.mp4'))
        probe(out/f'{name}.mp4',384,16)
    def peak_time(samples):
        # Isolate first contact event; later friction is irrelevant here.
        lo,hi=4*rate,6*rate
        return max(range(lo,hi),key=lambda i:abs(samples[i]))/rate
    expected=5.0; before=peak_time(shifted); after=peak_time(contact)
    assert before-expected>.49 and abs(after-expected)<1/FPS
    hashes={}
    for path in [src/'picture.mp4',out/'delayed.mp4',out/'repaired.mp4']:
        hashes[path.name]=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0',
                    '-f','hash','-hash','sha256','-']).decode().strip()
    assert len(set(hashes.values()))==1
    report={'date':'2026-10-13','kind':'controlled fault injection, not an accidental production failure',
            'changed_track':'CONTACT','delay_seconds':.5,'visual_contact_seconds':expected,
            'delayed_contact_peak_seconds':before,'repaired_contact_peak_seconds':after,
            'criterion_seconds':1/FPS,'fault_fails':True,'repair_passes':True,
            'repair_pcm_equals_original_S1':True,'identical_picture':True,
            'note':'Peak localization is valid for this isolated synthesized event, not a general AV-sync detector.'}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


GLYPHS={
 'Z':['11111','00001','00010','00100','01000','10000','11111'],
 'O':['01110','10001','10001','10001','10001','10001','01110'],
 'M':['10001','11011','10101','10101','10001','10001','10001'],
 'D':['11110','10001','10001','10001','10001','10001','11110'],
 'L':['10000','10000','10000','10000','10000','10000','11111'],
 'Y':['10001','10001','01010','00100','00100','00100','00100']}


def params(t):
    u=max(0,min(1,(t-2)/6)); u=u*u*(3-2*u)
    c=2*u
    return c,4/(4-c)


def optics_frame(t):
    w,h=960,420; data=bytearray(bytes((242,240,233))*(w*h))
    def rect(x,y,ww,hh,col):
        x0,x1=max(0,round(x)),min(w,round(x+ww)); y0,y1=max(0,round(y)),min(h,round(y+hh))
        row=bytes(col)*max(0,x1-x0)
        for yy in range(y0,y1): data[(yy*w+x0)*3:(yy*w+x1)*3]=row
    rect(479,0,2,h,(184,181,173))
    c,f=params(t)
    for panel,(cam,focal,title) in enumerate([(0,f,'ZOOM'),(c,1,'DOLLY')]):
        center=240+panel*480
        for i,ch in enumerate(title):
            for y,row in enumerate(GLYPHS[ch]):
                for x,v in enumerate(row):
                    if v=='1': rect(center-len(title)*9+i*18+x*3,25+y*3,3,3,(44,64,68))
        scale_back=400*focal/(8-cam); scale_front=400*focal/(4-cam)
        # All cards are one world unit wide; the two ochre cards are at Z=8.
        for world_x in [-1.6,1.6]:
            rect(center+scale_back*world_x-scale_back/2,220-scale_back/2,scale_back,scale_back,(196,125,69))
        rect(center-scale_front/2,220-scale_front/2,scale_front,scale_front,(45,119,122))
        rect(center-100,370,200,2,(186,184,174))
    return bytes(data)


def optics():
    out=ROOT/'docs/demos/dolly-zoom'; out.mkdir(parents=True,exist_ok=True)
    proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24',
        '-video_size','960x420','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-crf','18',
        '-pix_fmt','yuv420p','-movflags','+faststart',str(out/'comparison.mp4')],stdin=subprocess.PIPE)
    errors=[]
    for n in range(288):
        t=n/FPS; c,f=params(t)
        errors.append(abs(400*f/4-400/(4-c)))
        proc.stdin.write(optics_frame(t))
    proc.stdin.close(); assert proc.wait()==0
    for name,t in [('start',0),('end',10)]:
        subprocess.run(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',
                        '960x420','-i','pipe:0','-frames:v','1',str(out/f'{name}.png')],input=optics_frame(t),check=True)
    probe(out/'comparison.mp4',288,12)
    assert max(errors)<1e-9
    report={'date':'2026-10-13','model':'ideal pinhole, fixed sensor; no lens distortion/depth of field',
            'duration_seconds':12,'fps':24,'frames':288,'audio':'none by design',
            'projection':'pixel_width=400*f*object_width/(object_z-camera_z)',
            'object_width':1,'foreground_z':4,'background_z':8,
            'zoom':{'camera_z':0,'f_start':1,'f_end':2,'end_foreground_px':200,'end_background_px':100},
            'dolly':{'camera_z_start':0,'camera_z_end':2,'f':1,'end_foreground_px':200,'end_background_px':400/6},
            'max_foreground_width_difference_px':max(errors),'checks':{'matched_foreground_every_frame':True,
            'different_background_scale':True,'duration_and_frame_count':True},
            'limits':'Geometry demonstration; does not establish emotional or teaching effectiveness.'}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    svg='''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="280" viewBox="0 0 960 280">
<rect width="960" height="280" fill="#f2f0e9"/><g font-family="sans-serif" fill="#304448">
<text x="35" y="36" font-size="23">机位与物距：数值仅为示意单位</text>
<path d="M100 145H865" stroke="#777" stroke-width="2"/>
<path d="M110 145L430 65M110 145L430 225M110 145L830 65M110 145L830 225" stroke="#d0cbc0" fill="none"/>
<rect x="425" y="85" width="10" height="120" fill="#2d777a"/><rect x="825" y="85" width="10" height="120" fill="#c47d45"/>
<circle cx="110" cy="145" r="10" fill="#304448"/><circle cx="270" cy="145" r="10" fill="#304448"/>
<path d="M125 145H250l-12 -7m12 7l-12 7" fill="none" stroke="#304448" stroke-width="3"/>
<g font-size="18"><text x="55" y="255">起点 C=0</text><text x="220" y="255">推进终点 C=2</text>
<text x="385" y="65">前景 Z=4</text><text x="785" y="65">背景 Z=8</text>
<text x="40" y="92">变焦：留在起点，只改 f</text></g></g></svg>'''
    # Distances use a uniform scale: x=110+90*Z.
    svg=svg.replace('430','470').replace('425','465').replace('270','290').replace('250','270').replace('220" y="255','235" y="255').replace('385','425')
    (out/'layout.svg').write_text(svg+'\n')
    return report


if __name__=='__main__':
    print(json.dumps({'sync':faults(),'optics':optics()},indent=2))
