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

