import numpy as np
from skimage.transform import rescale, rotate
from torchvision.transforms import Compose

def transforms(norm=None, crop_size=None, angle=None, flip_prob=None):
    transform_list = []

    if norm is not None:
        transform_list.append(Normalize(norm))
    if crop_size is not None:
        transform_list.append(Crop(crop_size))
    if angle is not None:
        transform_list.append(Rotate(angle))
    if flip_prob is not None:
        transform_list.append(HorizontalFlip(flip_prob))

    return Compose(transform_list)
    
class Normalize(object):

    def __init__(self, norm):
        self.norm = norm

    def __call__(self, sample):
        img, mask = sample
        
        img = img - (img.max() - img.min())/2
        if img.max()>0:
            img = (img/img.max())*self.norm[0]/2
        img = img+self.norm[1]
        
        # if img.max()>0:
            # mask = mask/mask.max()

        return img, mask
        
class Crop(object):

    def __init__(self, crop_size):
        self.crop_size = crop_size

    def __call__(self, sample):
        img, mask = sample
        c,x,y = img.shape
        
        img = img[:,int(x/2 - self.crop_size/2):int(x/2 + self.crop_size/2),int(y/2 - self.crop_size/2):int(y/2 + self.crop_size/2)]
        mask = mask[int(x/2 - self.crop_size/2):int(x/2 + self.crop_size/2),int(y/2 - self.crop_size/2):int(y/2 + self.crop_size/2)]

        return img, mask


class Rotate(object):

    def __init__(self, angle):
        self.angle = angle

    def __call__(self, sample):
        image, mask = sample

        angle = np.random.uniform(low=-self.angle, high=self.angle)
        image = np.transpose(image,(1,2,0))
        image = rotate(image, angle, resize=False, preserve_range=True, mode="constant")
        image = np.transpose(image,(2,0,1))
        mask = rotate(mask, angle, resize=False, order=0, preserve_range=True, mode="constant")

        return image, mask


class HorizontalFlip(object):

    def __init__(self, flip_prob):
        self.flip_prob = flip_prob

    def __call__(self, sample):
        image, mask = sample

        if np.random.rand() > self.flip_prob:
            return image, mask
        image = np.transpose(image,(1,2,0))
        image = np.fliplr(image).copy()
        image = np.transpose(image,(2,0,1))
        
        mask = np.fliplr(mask).copy()

        return image, mask