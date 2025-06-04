import React, { useState } from 'react';
import { ReactMic } from 'react-mic';
import OpenAI from 'openai';
import './App.css';

// TODO: Replace 'YOUR_API_KEY' with your actual OpenAI API key.
// Consider using environment variables for better security.
const openai = new OpenAI({
  apiKey: 'YOUR_API_KEY', // This is a placeholder
  dangerouslyAllowBrowser: true // Required for client-side usage
});

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioData, setAudioData] = useState(null);
  const [transcribedText, setTranscribedText] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  const startRecording = () => {
    setIsRecording(true);
    setStatusMessage('Recording...');
    setTranscribedText(''); // Clear previous transcription
  };

  const stopRecording = () => {
    setIsRecording(false);
    setStatusMessage('Processing audio...');
  };

  const transcribeAudio = async (audioFile) => {
    console.log('Transcribing audio:', audioFile);
    setStatusMessage('Transcribing, please wait...');
    try {
      const response = await openai.audio.transcriptions.create({
        model: 'whisper-1',
        file: audioFile,
      });
      console.log('Transcription Response:', response);
      if (response && response.text) {
        console.log('Transcription Text:', response.text);
        setTranscribedText(response.text);
        setStatusMessage('Transcription complete.');
      } else {
        console.log('No transcription text found in response.');
        setTranscribedText('');
        setStatusMessage('No transcription text found in API response.');
      }
    } catch (error) {
      console.error('Error transcribing audio:', error);
      setTranscribedText('');
      setStatusMessage(`Error transcribing audio: ${error.message}`);
    }
  };

  const onStop = (recordedBlob) => {
    console.log('recordedBlob is: ', recordedBlob);
    setAudioData(recordedBlob);
    setStatusMessage('Audio recorded. Preparing for transcription...');

    // Create a File object from the blob
    const audioFile = new File([recordedBlob.blob], "recording.wav", { type: recordedBlob.blob.type || "audio/wav" });
    transcribeAudio(audioFile);
  };

  const onMicError = (error) => {
    console.error("Microphone error:", error);
    setStatusMessage("Microphone error. Please check permissions and try again.");
    setIsRecording(false); // Ensure recording state is reset
  }

  return (
    <div className="App">
      <header className="App-header">
        <ReactMic
          record={isRecording}
          className="sound-wave"
          onStop={onStop}
          onError={onMicError}
          strokeColor="#000000"
          backgroundColor="#FF4081" />
        <button onClick={isRecording ? stopRecording : startRecording} type="button" disabled={statusMessage === "Transcribing, please wait..."}>
          {isRecording ? 'Stop' : 'Record'}
        </button>
        {statusMessage && <p className="status-message">{statusMessage}</p>}
        <div className="transcription-output">
          {transcribedText || (statusMessage === 'Transcription complete.' ? '' : "Transcription will appear here...")}
          {audioData && !transcribedText && statusMessage !== 'Transcription complete.' && statusMessage !== "Transcribing, please wait..." && (
            <div>
              <p>Recording complete. Waiting for transcription or play audio below.</p>
              <audio controls src={audioData.blobURL} />
            </div>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
