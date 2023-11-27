import argparse
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.IptcImagePlugin import getiptcinfo
from lxml import etree


def read_exif(file: Image):
    print('------EXIF-----')
    try:
        exif = file._getexif()  # _getexif() is more verbose than getexif()
        if exif:
            # Iterate through all of EXIF's key-value data, then map the key to a known EXIF tag for easy reading
            for tag, value in exif.items():
                print(f'- {TAGS.get(tag, tag):25}: {value}')
            print()
        else:
            # EXIF metadata cannot be found
            print('Image has no EXIF metadata.\n')
    except (AttributeError, KeyError, IndexError):
        print('Cannot read EXIF metadata from file.\n')


def read_iptc(file: Image):
    print('------IPTC----- [WARNING: RAW DATA - may be unreadable]')
    try:
        iptc = getiptcinfo(file)
        if iptc:
            # Iterate through all of IPTC's key-value data, then simply print it
            for key, value in iptc.items():
                # Unfortunately, there is no way to map IPTC's IIM properties using Pillow, so the output data is raw
                print(f'- {key}: {value}')
            print()
        else:
            # IPTC metadata cannot be found
            print('Image has no IPTC metadata.\n')
    except (AttributeError, KeyError, IndexError):
        print('Cannot read IPTC metadata from file.\n')


def read_xmp(file: Image):
    print('------XMP------ [WARNING: RAW DATA - may be unreadable]')
    try:
        # Find the segment and content of the XMP metadata's APPList
        for segment, content in file.applist:
            # Check if segment is valid ("APP1")
            if segment == 'APP1':
                # Split between the marker and the XMP tags
                marker, xmp_tags = content.rsplit(b'\x00', 1)
                # Check if marker is valid ("http://ns.adobe.com/xap/1.0/")
                if marker == b'http://ns.adobe.com/xap/1.0/':
                    # Parse XMP metadata as XML file
                    root = etree.fromstring(xmp_tags)
                    print(etree.tostring(root, pretty_print=True).decode())
    except (AttributeError, KeyError, IndexError):
        print('Cannot read XMP metadata from file.\n')


def main(file, is_exif=False, is_iptc=False, is_xmp=False):
    with Image.open(file) as img:
        if not (is_exif or is_iptc or is_xmp):
            read_exif(img)
            read_iptc(img)
            read_xmp(img)
        else:
            if is_exif:
                read_exif(img)
            if is_iptc:
                read_iptc(img)
            if is_xmp:
                read_xmp(img)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Python script to read EXIF, IPTC, and XMP metadata of an image file'
                                                 ' (attempts to read all three by default).')
    parser.add_argument('file', type=str, help='Location of image file to be read.')
    parser.add_argument('-e', '--exif', action='store_true', help='Read EXIF metadata.')
    parser.add_argument('-i', '--iptc', action='store_true', help='Read IPTC metadata.')
    parser.add_argument('-x', '--xmp', action='store_true', help='Read XMP metadata.')

    args = parser.parse_args()
    main(args.file, args.exif, args.iptc, args.xmp)
