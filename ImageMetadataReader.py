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
            # Iterate through all of EXIF's key-value pairs, then map the key to a known EXIF tag
            for tag, value in exif.items():
                print(f'- {TAGS.get(tag, tag):25}: {value}')
            print()
        else:
            print('Image has no EXIF metadata.\n')
    except (AttributeError, KeyError, IndexError):
        print('Cannot read EXIF metadata from file.\n')


def read_iptc(file: Image):
    print('------IPTC----- [WARNING: RAW DATA - may be unreadable]')
    try:
        iptc = getiptcinfo(file)
        if iptc:
            for key, value in iptc.items():
                print(f'- {key}: {value}')  # Unfortunately, there is no way to map IPTC's IIM properties using Pillow
            print()
        else:
            print('Image has no IPTC metadata.\n')
    except (AttributeError, KeyError, IndexError):
        print('Cannot read IPTC metadata from file.\n')


def read_xmp(file: Image):
    print('------XMP------ [WARNING: RAW DATA - may be unreadable]')
    try:
        for segment, content in file.applist:
            if segment == 'APP1':
                marker, xmp_tags = content.rsplit(b'\x00', 1)
                if marker == b'http://ns.adobe.com/xap/1.0/':
                    root = etree.fromstring(xmp_tags)
                    print(etree.tostring(root, pretty_print=True).decode())
    except (AttributeError, KeyError, IndexError):
        print('Cannot read XMP metadata from file.\n')


def main(args):
    with Image.open(args.file) as img:
        if not (args.exif or args.iptc or args.xmp):
            read_exif(img)
            read_iptc(img)
            read_xmp(img)
        else:
            if args.exif:
                read_exif(img)
            if args.iptc:
                read_iptc(img)
            if args.xmp:
                read_xmp(img)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Python script to read EXIF, IPTC, and XMP metadata of an image file'
                                                 ' (attempts to read all three by default).')
    parser.add_argument('file', type=str, help='Location of image file to be read.')
    parser.add_argument('-e', '--exif', action='store_true', help='Read EXIF metadata.')
    parser.add_argument('-i', '--iptc', action='store_true', help='Read IPTC metadata.')
    parser.add_argument('-x', '--xmp', action='store_true', help='Read XMP metadata.')

    main(parser.parse_args())
