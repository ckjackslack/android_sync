#!/bin/bash
set -o pipefail

dirs=(
    "DCIM/Camera"
    "DCIM/Creative"
    "DCIM/Facebook"
    "DCIM/Screenshots"
    "Download"
    "MIUI"
    "MiVideoDownload"
    "Movies"
    "Pictures"
    "Recordings"
    "Reddit videos"
    "Telegram"
)
root_dir="/storage/self/primary"
filename="files_list.txt"
outfile="${root_dir}/${filename}"
first_dir=${dirs[0]}
exit_code=`adb devices | awk '(NR>1)' | grep "device"`


if [ $? -eq 0 ]; then
    adb shell "ls ${first_dir} > ${outfile} 2>&1"
    echo "Saved file list from ${first_dir} in ${outfile}."
    adb pull $outfile ~
    cd ~
    python3 divideandcopy.py
else
    echo "No devices found."
fi

# destination="/path/to/local/directory"
# for dir in ${dirs[@]};
# do
    # python3 syncphone.py $dir $destination
# done
