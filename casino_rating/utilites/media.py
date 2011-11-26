#coding: utf-8
import os
import settings
import Image
from funcs import generate_filename, get_file_extension
from uuid import uuid4


def is_file_image(file_path):
    """
    Check is file image or no
    """
    try:
        image = Image.open(file_path)
        return True
    except IOError:
        return False


def image_thumbnail(value, size='200x200', folders=("photo", "logo", "avatars",)):
    """
    Create thumbnail from image filename
    """
    if not value:
        return ""

    filename = value
    miniature = None
    x, y = [int(x) for x in size.split('x')]
    for folder in folders:
        if 0 == filename.find(folder):
            miniature = filename.replace("%s/" % folder, "thumbs/%s/%s/" % (size, folder,))

    if not miniature:
        return ""
    
    origin_filename = os.path.join(settings.MEDIA_ROOT, filename)
    miniature_filename = os.path.join(settings.MEDIA_ROOT, miniature)
    miniature_url = os.path.join(settings.MEDIA_URL, miniature)
    if not os.path.exists(miniature_filename):
        if not create_thumbnail(origin_filename, miniature_filename, size):
            return False
    return miniature_url


def create_thumbnail(image_path, thumb_path, size, output_format="JPEG", color="#ffffff"):
    """
    Create thumbnail for image
    """
    try:
        image = Image.open(image_path)
    except Exception, e:
        print e
        return False

    filedir = os.path.dirname(thumb_path)
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    m_w, m_h = [int(x) for x in size.split("x")]
    w, h = image.size
    if w != m_w or h != m_h:
        image.thumbnail((m_w, m_h))
        pos_x = (m_w - image.size[0]) / 2 if image.size[0] < m_w else 0
        pos_y = (m_h - image.size[1]) / 2 if image.size[1] < m_h else 0
        
        new_image = Image.new("RGBA", (m_w, m_h), color)
        new_image.paste(image, (pos_x, pos_y))
        new_image.save(thumb_path, output_format)
    else:
        image.save(thumb_path, output_format)
        new_image = image
    
    return new_image


def save_image_file(field, folder, rfile):
    """
    Upload and save image file to field storage
    """
    path = generate_filename(folder, get_file_extension(rfile.name))
    new_file = field.storage.save(path, rfile)
    new_file_path = "%s%s" % (settings.MEDIA_ROOT, new_file)
    new_file_url = "%s%s" % (settings.MEDIA_URL, new_file)
    
    if not is_file_image(new_file_path):
        os.remove(new_file_path)
        return None

    return {"name" : new_file, "url" : new_file_url, "path" : new_file_path, }


def upload_image_file(folder, rfile):
    """
    Upload image file to target folder. Generate filename and create needed path
    """
    path, name = generate_filename(folder, get_file_extension(rfile["filename"]), get_name=True)
    fullpath = settings.MEDIA_ROOT + path

    filedir = os.path.dirname(fullpath)
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    new_file = open(fullpath, 'w+')
    new_file.write(rfile['body'])
    new_file.close()
    
    if not is_file_image(fullpath):
        os.remove(fullpath)
        return None

    return {"name" : name, "url" : "%s%s" % (settings.MEDIA_URL, path), 
    "path" : fullpath, }


def upload_file(f):
    """
    Save uploaded file
    """
    filepath = "/tmp/%s" % uuid4()
    destination = open(filepath, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return filepath


def upload_image(f):
    """
    Save uploaded image. Check is uploaded file image or delete it
    """
    filepath = upload_file(f)
    if not is_file_image(filepath):
        os.remove(filepath)
        return None
    return filepath


def _save_upload(uploaded, extension, raw_data):
    ''' 
    raw_data: if True, upfile is a HttpRequest object with raw post data
    as the file, rather than a Django UploadedFile from request.FILES 
    '''
    filename = "/tmp/%s.%s" % (uuid4(), extension)
    try:
        with BufferedWriter(FileIO(filename, "wb")) as dest:
            # if the "advanced" upload, read directly from the HTTP request 
            # with the Django 1.3 functionality
            if raw_data:
                foo = uploaded.read(1024)
                while foo:
                    dest.write(foo)
                    foo = uploaded.read(1024) 
            # if not raw, it was a form upload so read in the normal Django chunks fashion
            else:
                for c in uploaded.chunks():
                    dest.write(c)
            return filename
    except IOError:
        # could not open the file most likely
        return False
    except Exception, e:
        return str(e)
