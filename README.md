# dicomifier-werkzeug

This project is a simple [Werkzeug](http://werkzeug.pocoo.org/)-based webservice around [Dicomifier](https://github.com/lamyj/dicomifier).

The webservice has the following routes:
- `POST /bruker2dicom`, with a JSON request containing
    - `source`: the path on the server to the Bruker directory to be converted
    - `destination`: the path on the server to the destination DICOM directory
- `POST /dicom2nifti`, with a JSON request containing
    - `source`: the path on the server to the DICOM directory to be converted
    - `destination`: the path on the server to the destination NIfTI directory

The environment variables of the Werkzeug application 
