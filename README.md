# cut_gbk.py

Extract a segment from a GenBank file using coordinates or locus_tags.

```bash
usage: cut_gbk.py [-h] -i INPUTFILE -s START -e END [-c CONTIG]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputfile INPUTFILE
                        a GenBank file
  -s START, --start START
                        start coordinate or locus_tag
  -e END, --end END     end coordinate or locus_tag
  -c CONTIG, --contig CONTIG
                        identifier of contig to be cut (needed when
                        coordinates are given and there is more than one
                        GenBank record in the input file)
```
