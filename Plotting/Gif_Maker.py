import os
import glob
import imageio

input_folder = 'X'
input_filenames = []

os.chdir(input_folder)

for file in glob.glob('*.png'):
    print file
    print file.split('/')[-1]
    input_filenames.append(file.split('/')[-1])
    
print 'Creating GIF'
images = []
for filename in sorted(input_filenames):
    images.append(imageio.imread(filename))
gif_savename = input_filenames[0][:10]
imageio.mimsave(gif_savename, images)
print 'GIF Created'
