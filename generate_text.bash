# Generate text
# $1 - Text to generate
# Path to voices

# Usage
if [ "$#" -ne 4 ]; then
    echo "Usage: generate_text.bash     speaker_id     model_dir     model_name(dont add .pth.tar)     wav_name"
fi

SPEAKER=$1
MODEL_DIR=$2
MODEL_NAME=$3
OUTPUTWAV=$4

PATHTOWAV=~/Desktop/Voices/outputs/$SPEAKER/$OUTPUTWAV.wav
voice_path="~/Desktop/Voices"

touch $PATHTOWAV
tts --text "I would like to tell you a story that I think you may find most interesting. Oh so silly. His name, is Cornelius."\
 --model_path "$voice_path/$SPEAKER/$MODEL_DIR/$MODEL_NAME.pth.tar" \
 --config_path "$voice_path/$SPEAKER/$MODEL_DIR/config.json" \
 --out_path $PATHTOWAV