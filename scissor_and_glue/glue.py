from PIL import Image
import numpy
import pathlib
import os
try:
    path = pathlib.Path(__file__).parent.resolve()
    part1=str(path)+'\\merge_input\\part1.png'
    part2=str(path)+'\\merge_input\\part2.png'
    part1=Image.open(part1)
    part2=Image.open(part2)
    part1=numpy.array(part1)
    part2=numpy.array(part2)
    res=numpy.add(part1,part2)
    res=Image.fromarray(res)
    res.save(str(path)+'\\output\\merged.png')
    path = pathlib.Path(__file__).parent.resolve()
    os.remove(str(path)+'\\merge_input\\part1.png')
    os.remove(str(path)+'\\merge_input\\part2.png')
except:
    pass
