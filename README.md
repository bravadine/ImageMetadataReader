# ImageMetadataReader

ImageMetadataReader is a simple Python script to read the EXIF/IPTC/XMP metadata of a file. The script uses the Pillow library to read the metadata as well as lxml to help parse XMP metadata.

## Usage

```
usage: ImageMetadataReader.py [-h] [-e] [-i] [-x] file

A Python script to read EXIF, IPTC, and XMP metadata of an image file (attempts to read all
three by default).

positional arguments:
  file        Location of image file to be read.

options:
  -h, --help  show this help message and exit
  -e, --exif  Read EXIF metadata.
  -i, --iptc  Read IPTC metadata.
  -x, --xmp   Read XMP metadata.
```

## Contributing

Pull requests are welcome; please open an issue first for discussion.
