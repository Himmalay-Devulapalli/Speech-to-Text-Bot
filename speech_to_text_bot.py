from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import speech_recognition as sr
from pydub import AudioSegment
import pydub
from gtts import gTTS

#default commands handlers
def start(update,context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('welcome to voice bot')

def help_command(update,context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('I am a Voice bot')

#custom commands handler and outputs
def echo(update,context): ## text output handler
    msg=update.message.text
    update.message.reply_text(msg)


# converting speech to text
#initial_voice os the audio file user sent to bot
def speech_to_text(initial_voice):
    r = sr.Recognizer()
    #download the file in .oga format
    initial_voice.download("hello.oga")

    #To convert audio into text we use google speech recognition and it doesn't support .oga format.
    #so to convert .oga audio to wav we use pydub
    # pydub needs ffmpeg software to convert the audio transcripts.
    #MAKE SURE YOU HAVE ffmpeg.exe FILE IN YOUR WORKING DIRECTORY
    pydub.AudioSegment.ffmpeg = "path to ffmpeg.exe file/ffmpeg"
    #use AudioSegment method to convert .oga audio transcripts to .wav transcripts
    AudioSegment.from_file("hello.oga").export("input_audio2.wav", format="wav")

    #configure the generated wav file as source for the recognizer
    with sr.WavFile("input_audio2.wav") as source:
        #record the audio data from  source to audio_data variable
        audio_data = r.record(source)
        try:
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data,language='en-IN')
            return text
        #any errors in recognizing the text from audio will be handled here
        except:
            return "Sorry...the audio file is not clear enough to extract the text"

def text_to_speech(text):
    myobj = gTTS(text=text,lang='en')
    myobj.save("output_audio1.mp3")
    AudioSegment.from_file("output_audio1.mp3").export("output_audio2.ogg", format="ogg")
    print('saved')
    return

#triggers when the bot receives audio file, NOTE THAT THE AUDIO FORMAT SUPPORTED BY TELEGRAM IS oga.
#so,you get your audio file in ogg format
def voice_handler(update,context):
    #in the entire set of message the bot is receiving,audio file can be accessed by update.message.voice.file_id
    file = context.bot.getFile(update.message.voice.file_id)

    #Now we need to convert the audio into text.
    #calling speech_to_text function and passing the audio file as parameter
    resp=speech_to_text(file)

    #sending back the text form of audio to the user
    update.message.reply_text(resp)

#main handler, heart of the bot where you filter the voice message and handle them
# refer https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.html for documentation
def main():
    try:
        ##configure the updater with your bot token
        updater = Updater("your bot token here", use_context=True)

        ##configure a dispatcher (responsible for receiving messages from bot )
        dp = updater.dispatcher

        """
        telegram bots have a default command '/start', 
        when you try to make a conversation with the bot for the first time, you can use the /start command
        You can add your custom commands using add_handler method.
        CommandHandler is responsible for handling the command type messages, they usually look like /start,/help,etc
        """
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))

        """
        Just like command handler, we have MessageHandler which takes care of all the incoming messages other than commands
        we can filter out the various messages using Filters.text or Filters.audio
        where Filters.text will handle all the plain text messages sent to the bot 
        Filters.audio will handle all the audio files sent to the bot    
        """
        #text message handler
        dp.add_handler(MessageHandler(Filters.text,echo))

        #voice message handler
        dp.add_handler(MessageHandler(Filters.voice, voice_handler))

        # Start getting updates from the bot
        updater.start_polling()
        updater.idle()
    # exception handling can be used in this manner as deploying this bot will give you many webhook errors,etc if not configured properly
    # handle them carefully, if not this may lead to program crash in production.
    except:
        # in case of any errors, i am calling the main function  to reset the program execution.
        main()

#call the main function
print("bot started on sever")
main()
