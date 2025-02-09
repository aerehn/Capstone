import pyaudio
import wave
import ntplib
import time

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 10 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

#method for getting the current date and time
def get_filename():
    # ntp_client = ntplib.NTPClient() 
    # response = ntp_client.request('pool.ntp.org')
    #use local time, otherwise timeout from server will terminate program
    timestamp = time.ctime()
    array = timestamp.split(" ")
    timestamp = array[4] + "_" + array[3] + "-" + array[1] + "-" + array[5]
    return timestamp
# create pyaudio stream

stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)

chunk_counter = 0
print("recording")

while 1>0:
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("finished recording")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print(get_filename())
    print(wav_output_filename)
    wav_output_filename= str(get_filename())+".wav"
    # save the audio frames as .wav file
    wavefile = wave.open('recordings/' + wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    print("Saved chunk " + str(chunk_counter) + ':  ' + wav_output_filename )
    chunk_counter += 1

    audio = pyaudio.PyAudio() # create pyaudio instantiation
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
