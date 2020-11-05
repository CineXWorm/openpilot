#!/usr/bin/env python3.7
import sys
try:
    sys.path.index('/data/openpilot/')
except ValueError:
    sys.path.append('/data/openpilot/')

import cereal.messaging as messaging

from selfdrive.car.volkswagen.radar_interface import RadarInterface

#for calibration we only want fixed objects within 1 m of the center line and between 2.5 and 4.5 m far from radar
MINX = 2.5
MAXX = 7.5
MINY = -2.0
MAXY = 2.0

def get_rrext_by_trackId(rrext,trackId):
  if rrext is not None:
    for p in rrext:
      if p.trackId == trackId:
        return p
  return None

if __name__ == "__main__":
  CP = None
  RI = RadarInterface(CP)
  can_sock = messaging.sub_sock('can')
  while 1:
    can_strings = messaging.drain_sock_raw(can_sock, wait_for_one=True)
    rr,rrext,ahb = RI.update(can_strings,0.)

    if (rr is None) or (rrext is None):
      continue

    print(chr(27) + "[2J")

    for pt in rr.points:
      if (pt.dRel >= MINX) and (pt.dRel <= MAXX) and (pt.yRel >= MINY) and (pt.yRel <= MAXY):
        extpt = get_rrext_by_trackId(rrext,pt.trackId)
        print (pt,extpt)
