#%%
import dbfread
import struct
import sys
import os
import skimage.io
import json

try:
    base = os.path.dirname(os.path.abspath(__file__))
except:
    base = '/home/bbales2/7kaa_sprite_reader/'

sys.path.append(base)

try:
    os.mkdir('{0}/processed'.format(base))
except:
    pass

import sprite_reader
reload(sprite_reader)
#%%

f = open('{0}/7kaa/resource/std.set'.format(base))
b = f.read()
f.close()

records = struct.unpack('h', b[0:2])[0]

recordsList = []
for i in range(records):
    name = ''.join([struct.unpack('c', byte)[0] for byte in b[2 + i * 13 : 2 + i * 13 + 9]]).strip('\x00')
    offset = struct.unpack('I', b[2 + i * 13 + 9 : 2 + (i + 1) * 13])[0]
    print name, offset
    
    recordsList.append((name, offset))
#%%
data = b[129621 : 500943]

f = open('{0}/processed/frames.dbf'.format(base), 'w')
f.write(data)
f.close()
#%%
table = dbfread.DBF('{0}/processed/frames.dbf'.format(base), raw = True, lowernames = True)

entries = [entry for entry in table]

to_local_directions = {
    'E' : 'east',
    'SE' : 'southeast',
    'S' : 'south',
    'SW' : 'southwest',
    'W' : 'west',
    'NW' : 'northwest',
    'N' : 'north',
    'NE' : 'northeast',
    '' : None
}
#%%
processed = {}
for entry in entries:
    name = entry['sprite'].strip().lower()
    
    if name not in processed:
        processed[name] = []
    
    direction = entry['dir'].strip().lower()
    if direction not in to_local_directions:
        print name
    action = entry['action'].strip().lower()
    ox = int(entry['offset_x'].strip())
    frame = int(entry['frame'].strip())
    oy = int(entry['offset_y'].strip())
    
    processed[name].append({
        'frame' : frame,
        'action' : action,
        'direction' : direction,
        'ox' : ox,
        'oy' : oy,
        'filename' : str(entry['filename']).strip(),
        'ptr' : struct.unpack('I', entry['bitmapptr'])[0]
    })
#%%
    
for name in processed:
    processed[name] = sorted(processed[name], key = lambda x : (x['direction'], x['frame']))
    
#%%

cmap = sprite_reader.load_cmap('{0}/7kaa/resource/pal_std.res'.format(base))

for name in processed:
    sprites = sprite_reader.load_sprites(cmap, '{0}/7kaa/sprite/{1}.spr'.format(base, name))

    try:
        os.mkdir('{0}/processed/{1}'.format(base, name))
    except:
        pass
    
    for ptr in sprites:
        skimage.io.imsave('{0}/processed/{1}/{2}.png'.format(base, name, ptr), sprites[ptr].astype('float') / 255.0)
#%%

f = open('{0}/processed.json'.format(base), 'w')

f.write(json.dumps(processed))

f.close()
