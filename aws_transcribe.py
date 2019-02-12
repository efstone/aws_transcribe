import json


class AwsTranscript:
    def __init__(self, json_transcript_file=None, *speaker_list):
        if json_transcript_file is None:
            print("Please include a json transcript file.")
            return
        self.speaker_list = list(speaker_list)
        self.speakers = {}
        self.json_transcript = json.load(json_transcript_file)
        self.speaker_count = self.json_transcript['results']['speaker_labels']['speakers']
        try:
            self.segments = self.json_transcript['results']['speaker_labels']['segments']
        except KeyError:
            print("You must use a transcript file with speakers.")
            return
        if len(speaker_list) < self.speaker_count:
            print("You did not enter all speaker names. Numbered default labels will be used--numbers do not "
                  "correspond with speaker number from transcript. It's recommended to make your own default labels.")
            for i in range(self.speaker_count - len(speaker_list)):
                self.speaker_list.append(f'unknown{str(i + 1).zfill(2)}')
        self.words = self.json_transcript['results']['items']
        self.show_seg_num = False

        for idx, speaker in enumerate(self.speaker_list):
            self.speakers[f'spk_{idx}'] = speaker

    def count_segments(self):
        return len(self.segments)

    def get_segment_start(self, segment_num=None):
        # shows the start time, in seconds, of the requested segment
        return self.segments[segment_num]['start_time']

    def print_segment(self, segment_num=None):
        # neatly prints all the "words" from the requested segment, prefaced with speaker name and including punctuation
        # zero-filled line numbers can be added by setting "show_seg_num" to true
        cur_segment_start = float(self.segments[segment_num]['start_time'])
        cur_segment_end = float(self.segments[segment_num]['end_time'])
        phrase = []
        phrase_start = None
        for idx, word in enumerate(self.words):
            try:
                word_check = word['start_time']
                if float(word['start_time']) >= cur_segment_start and float(word['start_time']) <= cur_segment_end:
                    if float(word['end_time']) <= cur_segment_end:
                        if phrase_start is None:
                            phrase_start = idx
                if float(word['end_time']) == cur_segment_end:
                    phrase_end = idx
                    break
            except KeyError:
                continue
        for i in range(phrase_start, phrase_end + 2):
            phrase.append(self.words[i])
        if self.show_seg_num is True:
            neat_phrase = f"{str(segment_num).zfill(4)} "
        else:
            neat_phrase = ''
        neat_phrase += f"{self.speakers[self.segments[segment_num]['speaker_label']]}:"
        for word in phrase:
            if word['type'] == 'punctuation':
                neat_phrase += word['alternatives'][0]['content']
            else:
                neat_phrase += f" {word['alternatives'][0]['content']}"
        return neat_phrase
