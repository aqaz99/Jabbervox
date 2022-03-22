# Generate text
# $1 - Text to generate
# Path to voices

# Usage
if [ "$#" -ne 3 ]; then
    echo "Usage: generate_text.bash     speaker_id      wav_name     text_to_generate"
    exit
fi

SPEAKER=$1
OUTPUTWAV=$2
TEXT=$3

# Make directory if speaker does not have one yet
if [ -d "./outputs/$SPEAKER" ] 
then
    echo "Found speaker directory" 
else
    echo "Creating speaker dir for $SPEAKER"
    mkdir ./outputs/$SPEAKER
fi

PATHTOWAV=./outputs/$SPEAKER/$OUTPUTWAV.wav
voice_path="./voices"
echo "HELO"
echo $PATHTOWAV
echo "GOODBYE"
touch $PATHTOWAV
tts --text "$TEXT"\
 --model_path "$voice_path/$SPEAKER/best_model.pth.tar" \
 --config_path "$voice_path/$SPEAKER/config.json" \
 --out_path $PATHTOWAV