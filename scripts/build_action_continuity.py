#!/usr/bin/env python3
"""Original geometric action: source time, not screen position, defines continuity."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/demos/action-continuity'
W,H,FPS,N=640,360,24,192
VARIANTS={'continuous':0,'repeat':-24,'skip':24}

def source_frame(i,offset):
    return i if i<96 else i+offset

def render(n,close):
    t=n/FPS
    # Object slides linearly during source seconds 1..6, then rests.
    p=max(0,min(1,(t-1)/5))
    x=-120+240*p
    scale=1.3 if close else .9
    b=bytearray(bytes((241,245,249))*(W*H))
    def rect(x,y,w,h,c):
        x0=max(0,round(x));x1=min(W,round(x+w));y0=max(0,round(y));y1=min(H,round(y+h))
        if x1<=x0 or y1<=y0:return
        row=bytes(c)*(x1-x0)
        for yy in range(y0,y1):b[(yy*W+x0)*3:(yy*W+x1)*3]=row
    def world(xx,yy,ww,hh,c):rect(320+xx*scale,180+yy*scale,ww*scale,hh*scale,c)
    world(-190,35,380,18,(148,163,184))
    for xx in [-120,0,120]:world(xx-2,54,4,15,(71,85,105))
    world(x-16,0,32,35,(14,116,144))
    # Abstract gripper follows; no realistic fingers or physical-force claim.
    world(x-60,10,42,12,(194,65,12))
    rect(24,24,90 if not close else 150,6,(14,116,144))
    rect(24,316,592,8,(203,213,225));rect(24,316,592*p,8,(14,116,144))
    return b

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    ff=shutil.which('ffmpeg');fp=shutil.which('ffprobe');assert ff and fp
    reports={}
    for name,offset in VARIANTS.items():
        dst=OUT/f'{name}.mp4'
        proc=subprocess.Popen([ff,'-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(dst)],stdin=subprocess.PIPE)
        frames=[source_frame(i,offset) for i in range(N)]
        for i,n in enumerate(frames):proc.stdin.write(render(n,i>=96))
        proc.stdin.close();assert proc.wait()==0
        probe=json.loads(subprocess.check_output([fp,'-v','error','-show_streams','-of','json',str(dst)]))
        stream=probe['streams'][0]
        assert int(stream['nb_frames'])==N and float(stream['duration'])==8
        step=frames[96]-frames[95]
        assert step==1+offset
        reports[name]={'frames':N,'duration_seconds':8,'source_frame_before_cut':frames[95],
                       'source_frame_after_cut':frames[96],'source_step_at_cut':step,
                       'repeated_source_frames':len(frames)-len(set(frames)),
                       'skipped_source_frames_at_cut':max(0,step-1),
                       'decoded_video_sha256':subprocess.check_output([ff,'-v','error','-i',str(dst),'-f','hash','-hash','sha256','-']).decode().strip()}
    # Lossless render of two frames around each cut for tool inspection.
    tile=bytearray(W*2*H*3*3)
    for row,offset in enumerate(VARIANTS.values()):
        for col,i in enumerate([95,96]):
            frame=render(source_frame(i,offset),i>=96)
            for y in range(H):
                start=((row*H+y)*W*2+col*W)*3
                tile[start:start+W*3]=frame[y*W*3:(y+1)*W*3]
    subprocess.run([ff,'-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W*2}x{H*3}','-i','-','-frames:v','1',str(OUT/'cut-frames.png')],input=tile,check=True)
    reports['scope']='Original silent geometric model; source-phase verification, not perceptual proof or real performance.'
    (OUT/'verification.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps(reports))

if __name__=='__main__':main()
