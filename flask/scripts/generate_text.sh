# Generate text
# $1 - Text to generate
# Path to voices

# Usage
if [ "$#" -ne 5 ]; then
    echo "Usage: generate_text.bash     speaker_id     model_dir     model_name(dont add .pth.tar)     wav_name     text_to_generate"
    exit
fi

SPEAKER=$1
MODEL_DIR=$2
MODEL_NAME=$3
OUTPUTWAV=$4
TEXT=$5

# Make directory if speaker does not have one yet
if [ -d "./voices/outputs/$SPEAKER" ] 
then
    echo "Found speaker directory" 
else
    echo "Creating speaker dir for $SPEAKER"
    mkdir ./voices/outputs/$SPEAKER
fi

PATHTOWAV=./output/wavs/$SPEAKER/$OUTPUTWAV.wav
voice_path="./voices"

touch $PATHTOWAV
tts --text "$TEXT"\
 --model_path "$voice_path/$SPEAKER/$MODEL_DIR/$MODEL_NAME.pth.tar" \
 --config_path "$voice_path/$SPEAKER/$MODEL_DIR/config.json" \
 --out_path $PATHTOWAV