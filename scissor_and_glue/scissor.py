import numpy
import random
from PIL import Image
import pathlib
def latest_file(path: pathlib.Path, pattern: str = "*.jpg"):
    files = path.glob(pattern)
    return max(files, key=lambda x: x.stat().st_ctime)
try:
    path = pathlib.Path(__file__).parent.resolve()
    path = latest_file(path)
    a = Image.open(path)
    a = numpy.array(a)
    value = []
    for x in a:
        for y in range(0, len(x)):
            temp = [random.randrange(0, 255), random.randrange(
                0, 255), random.randrange(0, 255)]
            b = numpy.array(temp)
            x[y] = x[y]-b
            value.append(temp)
    a = Image.fromarray(a)
    b = Image.new('RGB', a.size, (255, 255, 255))
    b = numpy.array(b)
    counter = 0
    for x in b:
        for y in range(0, len(x)):
            x[y] = tuple(value[counter])
            counter += 1
    b = Image.fromarray(b)
    path = pathlib.Path(__file__).parent.resolve()
    a.save(str(path)+'\\output\\part1.png')
    b.save(str(path)+'\\output\\part2.png')
except:
    pass
