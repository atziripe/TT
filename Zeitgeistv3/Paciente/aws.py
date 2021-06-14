from __future__ import print_function
from boto3 import Session
import os
import time
import boto3
import logging
import requests
import json
from botocore.exceptions import ClientError

boto_sess = Session(region_name='us-west-1')

def get_transcription(name, audio_name):
    try:
        transcribe = boto_sess.client('transcribe')
        job_name = "transcribe"+name
        job_uri = "s3://tamizajebucketzeitgeist/"+audio_name+""
        transcribe.start_transcription_job(
            TranscriptionJobName= job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='ogg',
            LanguageCode='es-US'
        )
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("Not ready yet...")
            time.sleep(5)
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            response = requests.get(status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"])
            transcript = json.loads(response.content)['results']['transcripts']
            return(transcript[0]["transcript"])
        else:
            traceback  = "Falló el transcript"
    except:
        return traceback

