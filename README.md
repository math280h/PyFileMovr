# PyFileMovr

This script is made to move all files from a folder and all sub folders to a single destination without any third party library's

## Usage

Download the newest release from the releases tab and run the main.py script, you must supply the following arguments:
* `--input`
    * Input path (Where to move the files from)
* `--output`
    * Output path (Where to move the files to)
   
Like so
```bash
python3 main.py --input /opt/filemess --output /newstorage/
or
python3 main.py --input A:\filemess --output A:\newstorage
```

### Options

A full list of arguments

* `--input` or `-i`
    * Input path (Where to move the files from)
        * Default: None
        * Required: Yes
* `--output` or `-i`
    * Output path (Where to move the files to)
        * Default: None
        * Required: Yes
* `--extension` or `-e`
    * File extension (Only files that match this extension will be moved - Must by provided as such: `.txt`)
        * Default: * (All files)
        * Required: No
* `--duplicates` or `-d`
    * File duplicates (If this is true only the first of a series of duplicates will be moved - Checked using a sha256 hash of the content of the files)
        * Default: False
        * Required: No
* `--debug`
    * Debug mode (Enables/disables debug mode)
        * Default: False
        * Required: No