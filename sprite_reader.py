#%%
import struct
import numpy

def load_sprites(cmap, path):
    #'/home/bbales2/Downloads/7kaa/sprite/norman.spr'
    f = open(path)#resource/i_hill1.res')#sprite/japanese.spr')
    
    b = f.read()
    
    f.close()
    
    #plt.imshow(nu
    frames = {}
    
    s = 0
    while s < len(b):
        a = struct.unpack('I', b[s : s + 4])[0]
        w = struct.unpack('h', b[s + 4 : s + 6])[0]
        h = struct.unpack('h', b[s + 6 : s + 8])[0]
        
        image = [struct.unpack('B', byte)[0] for byte in b[s + 8 : s + 4 + a]]
        
        b2 = []
        i = 0
        while i < len(image):
            byte = image[i]
            if byte == 0xf8:
                b2 += [0] * image[i + 1]
                
                i += 2
                continue
            elif byte > 0xf8 and byte <= 0xff:
                b2 += [0] * (256 - byte)
            else:
                b2 += [byte]
            
            i += 1
    
        if len(b2) < w * h:
            print 'error', (w * h - len(b2))
            b2 += [0] * (w * h - len(b2))

        data = numpy.array([cmap[v] for v in b2]).reshape(h, w, 3) 
        
        frames[s] = data
        
        #plt.imshow(numpy.array(b2).reshape(h, w, order = 'C'), interpolation = 'NONE')
        #plt.imshow(, interpolation = 'NONE')
        #plt.show()
        
        s += 4 + a
    return frames

#%%

def load_cmap(path):
    #'/home/bbales2/Downloads/7kaa/resource/pal_std.res'#/home/bbales2/Downloads/7kaa/image/credits1.col')
    f = open(path)
    b = f.read()
    f.close()

    cmap = numpy.array([struct.unpack('B', byte)[0] for byte in b[8:]]).reshape(256, 3)

    return cmap
    