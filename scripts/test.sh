#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR/..
echo "About to run tests on IFCB & LISST-Holo2 data"
rm testdata/ifcb-1/*.json 2> /dev/null
rm testdata/ifcb-1/*.tiff 2> /dev/null
python3 src/microtiff/ifcb.py testdata/ifcb-1/D20230313T140834_IFCB138.roi
SHAOUT=($(sha256sum -b testdata/ifcb-1/*.tiff testdata/ifcb-1/*.json | sha256sum))
if [ "${SHAOUT[0]}" = "d3e2ef1c818399b2e7c8779cce65b79181d409fdd694941aaa0e2d1b8834bc68" ]; then
    echo "[PASS] IFCB Test 1"
    rm testdata/ifcb-1/*.json
    rm testdata/ifcb-1/*.tiff
else
    echo "[FAIL] IFCB Test 1 - Hash (${SHAOUT[0]}) did not match expected output"
fi
rm testdata/lisst-holo-1/*.json 2> /dev/null
rm testdata/lisst-holo-1/*.tiff 2> /dev/null
python3 src/microtiff/lisst_holo.py testdata/lisst-holo-1/003-2516.pgm
SHAOUT=($(sha256sum -b testdata/lisst-holo-1/*.tiff testdata/lisst-holo-1/*.json | sha256sum))
if [ "${SHAOUT[0]}" = "fab34ce1532edf18eb7bb2fc1d357d5f01740da7504b8ff801739e758d2c3d97" ]; then
    echo "[PASS] LISST-Holo Test 1"
    rm testdata/lisst-holo-1/*.json
    rm testdata/lisst-holo-1/*.tiff
else
    echo "[FAIL] LISST-Holo Test 1 - Hash (${SHAOUT[0]}) did not match expected output"
fi
