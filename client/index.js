const handleRecordStop = (event, recordedChunks) => {
    event.preventDefault()
    const downloadLink = document.createElement('a')
    downloadLink.textContent = 'Download Audio'
    downloadLink.href = URL.createObjectURL(new Blob(recordedChunks))
    downloadLink.download = 'test.wav'
    document.body.appendChild(downloadLink)

    // TODO: send fetch from in here
}

const handleRecordStart = (event, stream) => {
    event.preventDefault()
    
    const recordedChunks = []
    const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
    })

    mediaRecorder.addEventListener('dataavailable', (event) => {
        if (event.data.size > 0) recordedChunks.push(event.data)
    })

    mediaRecorder.addEventListener('stop', (event) => handleRecordStop(event, recordedChunks))

    document.querySelector('#btn-record').addEventListener('mouseup', () => {
        mediaRecorder.stop()
    })

    mediaRecorder.start()
}

const getLocalStream = () => {
    navigator.mediaDevices.getUserMedia({ video: false, audio: true })
        .then((stream) => {
            document.querySelector('#btn-record').addEventListener('mousedown', (event) => handleRecordStart(event, stream))
        })
        .catch((err) => {
            console.log('Error retrieving stream')
            console.log(err)
        })
}

const main = () => {
    getLocalStream()
}

document.addEventListener('DOMContentLoaded', main)
