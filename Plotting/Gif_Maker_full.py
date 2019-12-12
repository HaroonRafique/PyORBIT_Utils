import os
import glob
import imageio

# Tune

input_folder = 'Tune'
input_filenames = []

os.chdir(input_folder)

for file in glob.glob('*.png'):
    #print file
    #print file.split('/')[-1]
    input_filenames.append(file.split('/')[-1])
    
print 'Creating Tune GIF'
images = []
for filename in sorted(input_filenames):
    images.append(imageio.imread(filename))
gif_savename = input_filenames[0][:10] + '.gif'
imageio.mimsave(gif_savename, images)
print 'Tune GIF Created'

# Y

input_folder = 'Y'
input_filenames = []

os.chdir(str('../' + input_folder))

for file in glob.glob('*.png'):
    #print file
    #print file.split('/')[-1]
    input_filenames.append(file.split('/')[-1])
    
print 'Creating Y GIF'
images = []
for filename in sorted(input_filenames):
    images.append(imageio.imread(filename))
gif_savename = input_filenames[0][:10] + '.gif'
imageio.mimsave(gif_savename, images)
print 'Y GIF Created'

# zdE

input_folder = 'zdE'
input_filenames = []

os.chdir(str('../' + input_folder))

for file in glob.glob('*.png'):
    #print file
    #print file.split('/')[-1]
    input_filenames.append(file.split('/')[-1])
    
print 'Creating zdE GIF'
images = []
for filename in sorted(input_filenames):
    images.append(imageio.imread(filename))
gif_savename = input_filenames[0][:10] + '.gif'
imageio.mimsave(gif_savename, images)
print 'zdE GIF Created'

# XY 

input_folder = 'XY'
input_filenames = []

os.chdir(str('../' + input_folder))

for file in glob.glob('*.png'):
    #print file
    #print file.split('/')[-1]
    input_filenames.append(file.split('/')[-1])
    
print 'Creating XY GIF'
images = []
for filename in sorted(input_filenames):
    images.append(imageio.imread(filename))
gif_savename = input_filenames[0][:10] + '.gif'
imageio.mimsave(gif_savename, images)
print 'XY GIF Created'

# X

input_folder = 'X'
input_filenames = []

os.chdir(str('../' + input_folder))

for file in glob.glob('*.png'):
    #print file
    #print file.split('/')[-1]
    input_filenames.append(file.split('/')[-1])
    
print 'Creating X GIF'
images = []
for filename in sorted(input_filenames):
    images.append(imageio.imread(filename))
gif_savename = input_filenames[0][:10] + '.gif'
imageio.mimsave(gif_savename, images)
print 'X GIF Created'
