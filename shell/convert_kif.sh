#!/bin/zsh

set -ue

for f in orig_kif/*.kif; do
    #python-shogiから読み込めるように変形する
    cat $f | sed -e 's|( [0-9]*:[0-9]*/)||g' | nkf -Lw | nkf -s > converted_kif/$f:t
done
