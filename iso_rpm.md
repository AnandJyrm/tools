# Tools to unpack and extract from iso content

## view iso directory listing
```bash
isoinfo -R -f -i <iso>
isoinfo -R -x <file> -i <iso>
```

## extract iso:
```bash
#!/usr/local/bin/bash

function print_size {
    local size=`du -hs "$1" | cut -f1`
    printf "%s" "$size"
}

# Extract an ISO file to a directory
function extract_iso() {
    local isofile="$1"
    local isodir="$2"
    local size=`print_size "$isofile"`

    mkdir -p "$isodir"
    printf "Extracting ISO '%s' (%s) to: %s\n" "$isofile" "$size" "$isodir"
    files=(`isoinfo -f -R -i "$isofile"`)
    for f in "${files[@]}"; do
        d=`dirname "$isodir/$f"`
        if [ -f "$d" -a ! -s "$d" ]; then
            rm "$d" || error "Cannot remove '$d'"
            mkdir "$d" || error "Cannot create directory '$d'"
        fi
        isoinfo -R -x "$f" -i "$isofile" > "$isodir/$f" || error "Cannot extract '$f'"
    done
    printf "  Unpacked to %s\n" "`print_size "$isodir"`"
}

extract_iso $1 $2

```

```bash
./extract.sh $PWD/iso $PWD/extract_location
Extracting ISO 'iso' (1.6G) to: extract_location/
  Unpacked to 1.6G
```


## squashfs contents:
```
unsquashfs packages.squashfs

mksquashfs package image/boot/package.squashfs -noappend -no-xattrs
```

## view rpm content:
```
rpm -ql <rpm> --provides

```

## extract rpm content:
```bash
rpm2cpio <rpm> | cpio -idv 2> /dev/null
```
