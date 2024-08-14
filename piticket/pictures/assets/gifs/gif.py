import time
from PIL import Image 
# with Image.open('Spinner.gif') as im:
#     try:
#         while 1:
#             frame_num = im.tell()
#             with open(f'Spinner_frame_{frame_num}.png','wb') as fp:
#                 fp.write(im.tobytes())
#                 fp.close()
#             im.seek(frame_num+1)
#     except EOFError:
#         pass 
#     except Exception:
#         pass

from PIL import ImageSequence
im = Image.open('Spinner.gif')
i = 0
for frame in ImageSequence.Iterator(im):
    # print(i, ": ", im.tell())
    # frame.show()
    # time.sleep(1)
    # i += 1
    with open(f'Spinner_frame_{im.tell()}.jpeg','wb') as fp:
        fp.write()
        fp.close()
    
        
    