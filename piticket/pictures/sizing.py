def new_size_keep_aspect_ratio(original_size:tuple, target_size:tuple, resize_type='inner'):
    """Return size tuple given the original size and target size.
    :param original_size: the size of the image
    :type original_size: tuple
    :param target_size: resize image to this size
    :type targe_size: tuple
    :return: size for resizing image
    :rtype: tuple
    """
    # Get the current aspect ratio
    image_ratio = original_size[0] / float(original_size[1])
    # Get target ratio
    target_ratio = target_size[0] / float(target_size[1])

    ox, oy = original_size 
    tx, ty = target_size 

    if target_ratio > image_ratio:
        # fit to width
        scale_factor = target_size[0] / float(ox)
        ty = scale_factor * oy
        if ty > target_size[1] and resize_type == 'inner':
            scale_factor = target_size[1] / float(oy)
            tx = scale_factor * ox
            ty = target_size[1]
    elif target_ratio < image_ratio:
        # fit to height
        scale_factor = target_size[1] / float(oy)
        tx = scale_factor * ox 
        if tx > target_size[0] and resize_type == 'inner':
            scale_factor = target_size[0] / float(ox)
            tx = target_size[0]
            ty = scale_factor * oy
    return (int(tx),int(ty))

def new_size_by_croping_ratio(original_size, target_size, crop_type='center'):
    """Return a tuple of the top-left and bottom-right points (x1, y1, x2, y2) by
    croping the original size but corresponding to the aspect ratio of the target size
    
    Note: target_size is only used to calculate aspect ratio, the returned size doesn't fit
    to it.
    
    The position of the rectangle can be determined by the crop_type
    
    * top-left
    * top-center
    * top-right
    * center-left
    * center
    * center-right
    * bottom-left
    * bottom-center
    * bottom-right
    """

    # Get current and desired ratio of the images
    img_ratio = original_size[0] / float(original_size[1])
    target_ratio = target_size[0] / float(target_size[1])

    tx, ty = original_size 
    if target_ratio > img_ratio:
        # crop on constant width
        ty = int(original_size[0] / target_ratio)
    elif target_ratio < img_ratio:
        # crop on constant height
        tx = int(target_ratio * original_size[1])
    
    x, y = position_picture(original_size, (tx,ty), crop_type)

    return (x, y, tx + x, ty + y)

def new_size_by_croping(original_size, target_size, crop_type='center'):
    """Return a tuple of top-left and bottom-right points (x1, y1, x2, y2) corresponding
    to a crop of the original size. The position of the rectangle can be defined by the
    crop_type parameter.
    crop_type parameter:
    
        * top-left
        * top-center
        * top-right
        * center-left
        * center
        * center-right
        * bottom-left
        * bottom-center
        * bottom-right
    """    
    x, y = position_picture(original_size, target_size, crop_type)
    return x, y, target_size[0] + x, target_size[1] + y

def position_picture(original_size, target_size, crop_type):
    """Return a tuple of x, y position
    """
    x, y = 0, 0
    if crop_type.endswith('left'):
        x = 0
    elif crop_type.endswith('center'):
        x = (original_size[0] - target_size[0]) // 2
    elif crop_type.endswith('right'):
        x = original_size[0] - target_size[0]

    if crop_type.startswith('top'):
        y = 0
    elif crop_type.startswith('center'):
        y = (original_size[1] - target_size[1]) // 2
    elif crop_type.startswith('bottom'):
        y = original_size[1] - ty 

    return x, y
