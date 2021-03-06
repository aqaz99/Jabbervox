# Generate text
# $1 - Text to generate
# Path to voices

# Usage
if [ "$#" -ne 4 ]; then
    echo "Usage: generate_text.bash     speaker_id      wav_name     text_to_generate     conversation(true/false)"
    exit
fi

SPEAKER=$1
OUTPUTWAV=$2
TEXT=$3
CONVERSATION=$4

# Make directory if speaker does not have one yet
if [ -d "./outputs/$SPEAKER" ] 
then
    echo "Found speaker directory" 
else
    echo "Creating speaker dir for $SPEAKER"
    mkdir ./outputs/$SPEAKER
fi

if [ $CONVERSATION == "true" ]
then
    PATHTOWAV=./outputs/conversation/$OUTPUTWAV.wav
else
    PATHTOWAV=./outputs/$SPEAKER/$OUTPUTWAV.wav
fi

voice_path="./voices"
# echo "HELO"
# echo $PATHTOWAV
# echo "GOODBYE"
touch $PATHTOWAV
tts --text "$TEXT"\
 --model_path "$voice_path/$SPEAKER/best_model.pth.tar" \
 --config_path "$voice_path/$SPEAKER/config.json" \
 --out_path $PATHTOWAV