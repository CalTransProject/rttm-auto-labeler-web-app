#!/usr/bin/env python3
"""Audit LiDAR .bin frames with records of 4 float32 values (x, y, z, field4)."""
import argparse
import csv
import io
import json
import re
import zipfile
from pathlib import Path
import numpy as np


def scan(source):
    source=Path(source)
    if source.is_dir():
        entries=[(p.name,p.read_bytes()) for p in source.rglob('*.bin')]
    elif source.is_file() and zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as z:
            entries=[(n,z.read(n)) for n in z.namelist() if n.lower().endswith('.bin') and not n.endswith('/')]
    else:
        raise ValueError('Input must be a directory containing .bin files or a ZIP containing .bin files')
    if not entries: raise ValueError('No .bin frames found')
    results=[]
    seen=set()
    for name, data in sorted(entries):
        fname=Path(name).name
        issues=[]
        if fname in seen: issues.append('duplicate filename in archive')
        seen.add(fname)
        if not re.fullmatch(r'\d{6}\.bin',fname): issues.append('nonstandard frame filename')
        if len(data)%16: issues.append('size not divisible by 16 bytes (4 float32 per point)')
        if len(data)==0: issues.append('empty point-cloud file')
        row={'frame':fname,'point_count':0,'file_bytes':len(data),'nonfinite_points':0,'zero_xyz_points':0,'x_min':None,'x_max':None,'y_min':None,'y_max':None,'z_min':None,'z_max':None,'field4_min':None,'field4_max':None,'issues':issues}
        if len(data)>0 and len(data)%16==0:
            points=np.frombuffer(data,dtype='<f4').reshape(-1,4)
            xyz=points[:,:3]
            finite=np.isfinite(points).all(axis=1)
            row['point_count']=len(points)
            row['nonfinite_points']=int((~finite).sum())
            if row['nonfinite_points']: issues.append('nonfinite coordinate or fourth field')
            if finite.any():
                valid=points[finite]
                row['zero_xyz_points']=int(np.all(valid[:,:3]==0,axis=1).sum())
                if row['zero_xyz_points']: issues.append('zero XYZ points')
                for idx,key in enumerate(('x','y','z','field4')):
                    row[key+'_min']=round(float(valid[:,idx].min()),5)
                    row[key+'_max']=round(float(valid[:,idx].max()),5)
        results.append(row)
    nums=sorted(int(r['frame'][:-4]) for r in results if re.fullmatch(r'\d{6}\.bin',r['frame']))
    gaps=[n for n in range(min(nums),max(nums)+1) if n not in set(nums)] if nums else []
    return {'format_assumption':'four little-endian float32 numbers per point: X,Y,Z,unknown fourth field','frames_scanned':len(results),'total_points':sum(r['point_count'] for r in results),'frames_with_warnings':sum(bool(r['issues']) for r in results),'frame_id_range':[min(nums),max(nums)] if nums else None,'unprovided_frame_ids_in_range':gaps,'note':'Unprovided frame IDs are informational: selected frames do not have to be sequential. Frame positions, vehicle identities and labels cannot be validated from .bin alone.','frames':results}


def write_reports(report,output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    (output/'audit_summary.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    cols=['frame','point_count','file_bytes','nonfinite_points','zero_xyz_points','x_min','x_max','y_min','y_max','z_min','z_max','field4_min','field4_max','issues']
    with (output/'audit_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
        for row in report['frames']:
            w.writerow({**row,'issues':'; '.join(row['issues'])})
    perframe=output/'numbered_txt_reports';perframe.mkdir(exist_ok=True)
    for row in report['frames']:
        stem=Path(row['frame']).stem
        name=stem+'.txt' if re.fullmatch(r'\d{6}',stem) else 'nonstandard_'+stem+'.txt'
        lines=[f"Frame: {row['frame']}",f"Points: {row['point_count']}",f"Bytes: {row['file_bytes']}",f"Non-finite points: {row['nonfinite_points']}",f"Zero XYZ points: {row['zero_xyz_points']}",f"X range: {row['x_min']} to {row['x_max']}",f"Y range: {row['y_min']} to {row['y_max']}",f"Z range: {row['z_min']} to {row['z_max']}",f"Fourth field range: {row['field4_min']} to {row['field4_max']}",f"Warnings: {('; '.join(row['issues']) or 'None')}"]
        (perframe/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')


def main():
    p=argparse.ArgumentParser(description='Check LiDAR frames and output per-frame TXT plus summary CSV/JSON')
    p.add_argument('source',help='ZIP file or folder with .bin files')
    p.add_argument('--output',default='audit_output')
    args=p.parse_args()
    report=scan(args.source);write_reports(report,args.output)
    print(f"Scanned {report['frames_scanned']} frames / {report['total_points']:,} points")
    print(f"Frames with warnings: {report['frames_with_warnings']}")
    print('Unprovided IDs within min/max:',len(report['unprovided_frame_ids_in_range']),'(informational, not errors)')
    print('Reports:',args.output)

if __name__=='__main__':main()
