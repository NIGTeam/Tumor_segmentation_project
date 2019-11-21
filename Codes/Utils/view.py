import matplotlib.pyplot as plt
import numpy as np

# Show scalar map (FA, MD, etc..)
def show_scalar_field(SM, voxel_sizes=np.array([1,1,1])):
    import numpy as np
    # image and graphic
    from IPython.display import Image
    from IPython.display import display
    import matplotlib.pyplot as plt
    get_ipython().magic('matplotlib')
        
    from matplotlib.widgets import Slider

    sx, sy, sz = SM.shape

    fig = plt.figure(figsize=(15,15))
    xy = fig.add_subplot(1,3,1)
    plt.title("Axial Slice")
    xz = fig.add_subplot(1,3,2)
    plt.title("Coronal Slice")
    yz = fig.add_subplot(1,3,3)
    plt.title("Sagittal Slice")

    # make the slider frame
    pos = 0
    axframe = plt.axes([0.25, 0.1+pos, 0.65, 0.03])
    sframe = Slider(axframe, 'Slice', 0, 1, valinit=0,valfmt='%f')

    s = 0
    
    aspect_1 = voxel_sizes[1]/voxel_sizes[2]
    aspect_2 = voxel_sizes[0]/voxel_sizes[2]
    aspect_3 = voxel_sizes[0]/voxel_sizes[1]

    #normalize for visualization purpose
    maximo = np.max(np.abs(SM)) # max e min usados para fazer o FA ocupar toda faixa 0-1
    minimo = np.min(np.abs(SM))

    xy.imshow(SM[:,:,s].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0, vmax=maximo, aspect=aspect_1)
    xz.imshow(SM[:,s,:].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0, vmax=maximo, aspect=aspect_2)
    yz.imshow(SM[s,:,:].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0, vmax=maximo, aspect=aspect_3)


    plt.axis("off")

    def update(val):
        s = sframe.val
        xy.imshow(SM[:,:,int(np.floor(s*sz))].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0 , vmax=maximo, aspect=aspect_1)
        xz.imshow(SM[:,int(np.floor(s*sy)),:].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0 , vmax=maximo, aspect=aspect_2)
        yz.imshow(SM[int(np.floor(s*sx)),:,:].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0 , vmax=maximo, aspect=aspect_3)

    # connect callback to slider   
    sframe.on_changed(update)
    plt.show()
	    
def show_multi_scalar_field(SM, voxel_sizes=np.array([1,1,1])):
    
    import numpy as np
    from IPython.display import Image
    from IPython.display import display
    import matplotlib.pyplot as plt
    get_ipython().magic('matplotlib')
    
    from matplotlib.widgets import Slider

    ni, sx, sy, sz = SM.shape
    # set up figure
    fig = plt.figure(figsize=(15,15))
    xy = fig.add_subplot(1,3,1)
    plt.title("Axial Slice")
    xz = fig.add_subplot(1,3,2)
    plt.title("Coronal Slice")
    yz = fig.add_subplot(1,3,3)
    plt.title("Sagittal Slice")

    # make the slider frame
    pos = 0
    axframe = plt.axes([0.25, 0.1+pos, 0.65, 0.03])
    sframe = Slider(axframe, 'Slice', 0, 1, valinit=0,valfmt='%f')
    
    # make the slider volume_index
    pos = 0.05
    axindex = plt.axes([0.25, 0.1+pos, 0.65, 0.03])
    sindex = Slider(axindex, 'volume_index', 0, ni-1, valinit=0,valfmt='%d')

    s = 0
    volume_index = 0
    
    aspect_1 = voxel_sizes[1]/voxel_sizes[2]
    aspect_2 = voxel_sizes[0]/voxel_sizes[2]
    aspect_3 = voxel_sizes[0]/voxel_sizes[1]

    #normalize for visualization purpose
    maximo = np.max(np.abs(SM)) # max e min usados para fazer o FA ocupar toda faixa 0-1
    minimo = np.min(np.abs(SM))

    xy.imshow(SM[volume_index,:,:,s].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0, vmax=maximo, aspect=aspect_1)
    xz.imshow(SM[volume_index,:,s,:].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0, vmax=maximo, aspect=aspect_2)
    yz.imshow(SM[volume_index,s,:,:].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0, vmax=maximo, aspect=aspect_3)


    plt.axis("off")

    def update(val):
        volume_index = sindex.val
        s = sframe.val
        xy.imshow(SM[int(np.floor(volume_index)),:,:,int(np.floor(s*sz))].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0 , vmax=maximo, aspect=aspect_1)
        xz.imshow(SM[int(np.floor(volume_index)),:,int(np.floor(s*sy)),:].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0 , vmax=maximo, aspect=aspect_2)
        yz.imshow(SM[int(np.floor(volume_index)),int(np.floor(s*sx)),:,:].T, origin='lower', interpolation='nearest', cmap="gray",vmin=0 , vmax=maximo, aspect=aspect_3)


    # connect callback to slider   
    sindex.on_changed(update)
    sframe.on_changed(update)
    plt.show()
    
def volume_show(data, voxel_sizes=np.array([1,1,1])):
    if len(data.shape) == 3:
        show_scalar_field(data,voxel_sizes)
    if len(data.shape) == 4:
        show_multi_scalar_field(data,voxel_sizes)
		
