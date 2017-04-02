import os
import time

# code = os.system('feh -Y -x -q -F -Z -D 2 -R 10 -S filename -B black --cycle-once -r ./data/image')
code = 0;

while code == 0:
    code = os.system('feh -Y -q -F -Z -D 5 -R 10 -S filename -B black --cycle-once -r ./data/image')
    print code
    time.sleep(0.5)
