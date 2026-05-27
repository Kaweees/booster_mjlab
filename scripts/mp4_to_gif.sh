#!/bin/bash

# Convert a video to a gif
# Usage:
#    gif.sh convert <input.mp4> <output.gif>

#
#  Private Impl
#

convert() {
  if [ $# -ne 2 ]; then
    echo "Usage: $0 convert <input.mp4> <output.gif>"
    return 1
  fi

  input="$1"
  output="$2"

  if [ ! -f "$input" ]; then
    echo "Input file $input not found"
    return 1
  fi

  mkdir -p "$(dirname "$output")"

  if ! ffmpeg -y -i "$input" -vf "fps=15,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 "$output"; then
    echo "Error converting $input to $output"
    return 1
  fi

  echo "Successfully converted $input to $output"
  return 0
}

# Main script logic
set -e # Exit on error
case "$1" in
  convert)
    shift
    convert "$@"
    ;;
  *)
    echo "Usage: $0 convert <input.mp4> <output.gif>"
    exit 1
    ;;
esac
