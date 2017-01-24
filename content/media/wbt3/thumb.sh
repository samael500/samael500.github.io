#!/bin/bash
for i in *.png; do
echo "Prcoessing image $i ..."
/usr/bin/convert -thumbnail 600 $i thumb.$i
done

