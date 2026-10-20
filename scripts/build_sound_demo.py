#!/usr/bin/env python3
"""Original geometric animatic and synthetic sound; Python stdlib + FFmpeg.

Run from any directory. No downloaded media, image models or recording claims.
Outputs only docs/demos/sound-priority. All three variants share one encoded picture.
"""
from array import array
import hashlib
import json
import math
from pathlib import Path
import random
import subprocess
import wave

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'demos' / 'sound-priority'
W, H, FPS, RATE, SECONDS = 640, 360, 24, 48000, 16


def smooth(x):
    x = max(0, min(1, x))
    return x*x*(3-2*x)


def gate(t, a, b, ramp=.08):
    return smooth((t-a)/ramp) * smooth((b-t)/ramp)


def state(t):
    angle = math.radians(8) * (smooth((t-5)/.7) if t < 8 else 1-smooth((t-8)/3))
    c, s = math.cos(angle), math.sin(angle)
    def cup(x, y):
        return (450+x*c-y*s, 280+x*s+y*c)
    contact = cup(-66, -60)  # tip radius 6: tangent to cup's left side
    if t < 5:
        u = smooth(t/5)
        tip = (250+(contact[0]-250)*u, 175+(contact[1]-175)*u)
    elif t < 11:
        tip = contact
    else:
        u = smooth(t-11)
        tip = (384+(345-384)*u, 220+(198-220)*u)
    return cup, tip


def frame(t):
    p = bytearray(bytes((241, 239, 233))*(W*H))
    def rect(x0,y0,x1,y1,color):
        x0,x1=max(0,int(x0)),min(W,int(x1))
        row=bytes(color)*max(0,x1-x0)
        for y in range(max(0,int(y0)),min(H,int(y1))):
            p[(y*W+x0)*3:(y*W+x1)*3]=row
    def polygon(points,color):
        for y in range(max(0,int(min(v[1] for v in points))),min(H,int(max(v[1] for v in points))+1)):
            xs=[]
            for a,b in zip(points,points[1:]+points[:1]):
                if min(a[1],b[1]) <= y+.5 < max(a[1],b[1]):
                    xs.append(a[0]+(y+.5-a[1])*(b[0]-a[0])/(b[1]-a[1]))
            xs.sort()
            for l,r in zip(xs[::2],xs[1::2]): rect(math.ceil(l),y,math.ceil(r),y+1,color)
    def circle(x,y,r,color):
        for yy in range(max(0,int(y-r)),min(H,int(y+r)+1)):
            d=r*r-(yy+.5-y)**2
            if d>=0:
                dx=math.sqrt(d); rect(x-dx,yy,x+dx,yy+1,color)
    def line(a,b,width,color):
        dx,dy=b[0]-a[0],b[1]-a[1]; length=math.hypot(dx,dy)
        nx,ny=-dy/length*width/2,dx/length*width/2
        polygon([(a[0]+nx,a[1]+ny),(b[0]+nx,b[1]+ny),(b[0]-nx,b[1]-ny),(a[0]-nx,a[1]-ny)],color)
        circle(*a,width/2,color); circle(*b,width/2,color)
    # Quiet background, fixed desktop and floor-contact line.
    rect(0,280,W,300,(207,204,193)); rect(0,300,W,H,(226,222,211))
    rect(85,274,170,280,(171,174,164)); rect(90,254,165,274,(50,69,73))
    cup,tip=state(t)
    # Cup rotates about bottom-right corner, keeping contact with the table.
    handle=[cup(x,y) for x,y in [(0,-73),(24,-73),(28,-60),(24,-36),(0,-36)]]
    for a,b in zip(handle,handle[1:]): line(a,b,8,(188,102,67))
    polygon([cup(-60,0),cup(0,0),cup(0,-96),cup(-60,-96)],(204,116,75))
    line(cup(-59,-96),cup(-1,-96),4,(246,212,177))
    line(cup(-54,-8),cup(-54,-85),3,(222,145,100))
    shoulder=(128,250); dx,dy=tip[0]-128,tip[1]-250
    d=math.hypot(dx,dy); height=math.sqrt(145**2-(d/2)**2)
    elbow=((128+tip[0])/2+dy/d*height,(250+tip[1])/2-dx/d*height)
    for a,b in [(shoulder,elbow),(elbow,tip)]:
        line(a,b,21,(43,80,85)); line(a,b,11,(80,128,131))
    for joint in [shoulder,elbow]:
        circle(*joint,14,(40,61,66)); circle(*joint,7,(177,194,186))
    circle(*tip,6,(238,202,115))
    return bytes(p)


def write_wav(path,data):
    pcm=array('h',(round(max(-1,min(1,x))*32767) for x in data))
    import sys
    if sys.byteorder!='little': pcm.byteswap()
    with wave.open(str(path),'wb') as f:
        f.setparams((1,2,RATE,0,'NONE','not compressed')); f.writeframes(pcm.tobytes())


def run(*args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}',
         '-framerate',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',
         '-movflags','+faststart',str(OUT/'picture.mp4')]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(FPS*SECONDS): proc.stdin.write(frame(n/FPS))
    proc.stdin.close()
    if proc.wait(): raise RuntimeError('picture encoding failed')
    # Six stills include before/contact/tilt/recovery/finish; labels live in README.
    moments=[0,4,5,5.75,10,12]
    frames=[frame(t) for t in moments]
    sheet=bytearray()
    for row in range(2):
        for y in range(H):
            for col in range(3): sheet.extend(frames[row*3+col][y*W*3:(y+1)*W*3])
    subprocess.run(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',
                    f'{W*3}x{H*2}','-i','pipe:0','-frames:v','1',str(OUT/'keyframes.png')],input=sheet,check=True)
    rng=random.Random(20261013)
    names=['ENV','CONTACT','MOTOR','DETAIL','AIR']
    stems={name:array('f') for name in names}
    mixes={name:array('f') for name in ['S0','S1','S2']}
    low=slow=0.0
    for n in range(RATE*SECONDS):
        t=n/RATE; noise=rng.uniform(-1,1)
        low+=.18*(noise-low); slow+=.012*(noise-slow)
        motion=gate(t,0,5.7,.15)+gate(t,8,12,.15)
        env=.006*slow
        motor=motion*(.038*math.sin(2*math.pi*147*t)+.012*math.sin(2*math.pi*311*t))
        phase=(t-.35)%.43
        detail=motion*.11*math.exp(-phase*65)*math.sin(2*math.pi*1850*t)
        d=t-5
        hit=(.22*math.exp(-d*16)*math.sin(2*math.pi*890*d) if 0<=d<.6 else 0)
        contact=hit+.025*(low-slow)*gate(t,8,11,.15)
        air=.24*(low-slow)*gate(t,8,11.25,.2)*(0.7+.3*math.sin(math.pi*(t-8)/3)**2)
        duck=1-.82*gate(t,4.5,12,.25)
        replace=gate(t,8,11.25,.25)
        s0=env+contact+motor+detail
        s1=env+contact+motor+detail*duck
        s2=env+contact+motor*(1-replace)+air+detail*duck
        for name,value in zip(names,[env,contact,motor,detail,air]): stems[name].append(value)
        for name,value in zip(mixes,[s0,s1,s2]): mixes[name].append(value)
    metrics={}
    for name,data in {**stems,**mixes}.items():
        write_wav(OUT/f'{name}.wav',data)
        peak=max(abs(x) for x in data); rms=math.sqrt(sum(x*x for x in data)/len(data))
        metrics[name]={'samples':len(data),'peak':peak,'rms_dbfs':20*math.log10(max(rms,1e-12))}
    hashes={}
    for name in mixes:
        run('ffmpeg','-y','-v','error','-i',str(OUT/'picture.mp4'),'-i',str(OUT/f'{name}.wav'),
            '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k',
            '-t',str(SECONDS),'-movflags','+faststart',str(OUT/f'{name}.mp4'))
        decoded=subprocess.check_output(['ffmpeg','-v','error','-i',str(OUT/f'{name}.mp4'),
                    '-map','0:v:0','-f','hash','-hash','sha256','-'])
        hashes[name]=decoded.decode().strip()
    probes={}
    for name in ['picture','S0','S1','S2']:
        probes[name]=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
                       '-show_format','-of','json',str(OUT/f'{name}.mp4')]))
        probes[name]['format']['filename']=f'{name}.mp4'  # 不把本机绝对路径写进报告
        stream=next(x for x in probes[name]['streams'] if x['codec_type']=='video')
        assert stream['nb_frames']=='384' and abs(float(stream['duration'])-16)<.001
    assert len(set(hashes.values()))==1, 'variants must share decoded video'
    assert all(x['peak']<1 for x in metrics.values()), 'PCM clipping'
    # Intentional constraints, measured on the actual generated samples.
    a,b=12*RATE,16*RATE
    assert mixes['S0'][a:b]==mixes['S1'][a:b]==mixes['S2'][a:b]==stems['ENV'][a:b]
    assert mixes['S0'][:4*RATE]==mixes['S1'][:4*RATE]==mixes['S2'][:4*RATE]
    report={'date':'2026-10-13','dimensions':[W,H],'fps':FPS,'seconds':SECONDS,
            'sample_rate':RATE,'channels':1,'provenance':'original procedural geometry and synthesized audio',
            'metrics':metrics,'decoded_video_hashes':hashes,'checks':{
                '384_frames_each':True,'identical_decoded_picture':True,'pcm_no_clipping':True,
                'first_four_seconds_identical':True,'last_four_seconds_env_only':True},
            'not_checked':['human listening','audience response','perceptual loudness matching'],
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (OUT/'probe.json').write_text(json.dumps(probes,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
