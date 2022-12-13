const pollForTranslation = async (translationId) => {
    while (true) {
        await new Promise(r => setTimeout(r, 2000));
        console.log('Querying job status.')
        try {
            const response = await fetch(`http://127.0.0.1:5000/translation/${translationId}`)

            const translationInfo = await response.json()
            console.log(translationInfo)
            const { status, translation } = translationInfo

            if (status.message === 'FAILURE') {
                return translation // TODO: catch this error somehow without loopingdocker 
            }

            if (status.message !== 'IN_QUEUE' && status.message !== 'PROCESSING') {
                return translation
            }
        } catch (err) {
            console.log(err)
            console.log('Trying again.')
        }
    }
}

const handleRecordStop = async (event, recordedChunks) => {
    event.preventDefault()
    const recordingBlob = new Blob(recordedChunks)
    recordedChunks.length = 0
    const outputLanguage = document.querySelector('#input-output-language').value

    // TODO: handle fetch response and manage the domain
    try {
        const response = await fetch(`http://127.0.0.1:5000/translation?outputLanguage=${outputLanguage}&userId=`, {
            method: 'POST',
            mode: 'cors',
            body: recordingBlob,
            headers: {
                'Content-Type': 'audio/mpeg',
                'Access-Control-Allow-Origin': '*'
            }
        })

        if (response.status >= 400) {
            throw new Error(response.statusText)
        }

        const translationInfo = await response.json()
        const translationId = translationInfo['_id']
        const translation = await pollForTranslation(translationId)
        console.log(translation)
        document.querySelector('#translation-display').textContent = JSON.stringify(translation)
    } catch (err) {
        console.log(err)
    }
}

const getLocalStream = () => {
    navigator.mediaDevices.getUserMedia({ video: false, audio: true })
        .then((stream) => {
            const recordedChunks = []
            const mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm'
            })

            mediaRecorder.addEventListener('dataavailable', (event) => {
                if (event.data.size > 0) recordedChunks.push(event.data)
            })

            mediaRecorder.addEventListener('stop', (event) => handleRecordStop(event, recordedChunks))

            document.querySelector('#btn-record').addEventListener('mousedown', () => mediaRecorder.start())

            document.querySelector('#btn-record').addEventListener('mouseup', () => mediaRecorder.stop())
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
