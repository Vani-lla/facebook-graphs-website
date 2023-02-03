from django.db import models
from django.conf import settings

from os import remove
from re import compile, UNICODE

import json
from datetime import datetime
from pandas import date_range

emoji_pattern = compile("["
                        u"\U0001F600-\U0001F64F"  # emoticons
                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags=UNICODE)


class JsonFile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='json/')
    size = models.IntegerField(default=0)
    name = models.CharField(default='', max_length=100)

    def save(self, modify=False, *args, **kwargs):
        super(JsonFile, self).save(*args, **kwargs)
        if not modify:
            conversation = {}
            days = []
            all_dates = []
            merge = False
            merge_convo = None
            persons_merge = []
            tmp_size = 0

            with open(self.file.path, 'r') as file:
                data = json.load(file)

                participants = list([participant['name'].encode('latin1').decode('utf-8')
                                    for participant in data['participants']])

                name = emoji_pattern.sub(
                    '', data['title'].encode('latin1').decode('utf-8'))

                for convo in JsonFile.objects.filter(user=self.user):
                    if convo.name == name:
                        merge = True
                        merge_convo = convo
                        persons_merge = list(p for p in list(
                            Person.objects.filter(conversation=convo)))

                tmp_size = len(data['messages'])
                for message in data['messages']:
                    sender = message['sender_name'].encode(
                        'latin1').decode('utf-8')
                    date = datetime.fromtimestamp(
                        message['timestamp_ms']//1000).strftime('%Y-%m-%d')

                    if date in days:
                        try:
                            if 'photos' in message:
                                conversation[date][sender]['number'] += 1
                                conversation[date][sender]['media'] += len(
                                    message['photos'])
                            elif 'videos' in message:
                                conversation[date][sender]['media'] += len(
                                    message['videos'])
                                conversation[date][sender]['number'] += 1
                            elif message['is_unsent']:
                                conversation[date][sender]['unsend'] += 1
                            else:
                                conversation[date][sender]['number'] += 1
                        except KeyError:
                            conversation[date][sender] = {
                                "number": 1,
                                "media": 0,
                                "unsend": 0,
                            }
                    else:
                        days.append(date)
                        conversation[date] = {}
                        for participant in participants:
                            if 'photos' in message:
                                conversation[date][participant] = {
                                    "number": 1,
                                    "media": len(message['photos']),
                                    "unsend": 0,
                                }
                            elif 'videos' in message:
                                conversation[date][participant] = {
                                    "number": 1,
                                    "media": len(message['videos']),
                                    "unsend": 0,
                                }
                            elif message['is_unsent']:
                                conversation[date][participant] = {
                                    "number": 1,
                                    "media": 0,
                                    "unsend": 1,
                                }
                            else:
                                conversation[date][participant] = {
                                    "number": 1,
                                    "media": 0,
                                    "unsend": 0,
                                }

            # remove(self.file.path)

            days.sort()
            all_dates = [datetime.strftime(
                date, '%Y-%m-%d') for date in date_range(days[0], days[-1], freq='d')]

            if not merge:
                self.size = tmp_size
                self.name = name
                self.save(modify=True)
                for person in participants:
                    person_model = Person(
                        name=person, conversation=self, user=self.user)
                    person_model.save()

                    for date in all_dates:
                        try:
                            Messages(number=conversation[date][person]['number'], unsend=conversation[date][person]
                                     ['unsend'], media=conversation[date][person]['media'], sender=person_model, date=date).save()
                        except KeyError:
                            Messages(sender=person_model, date=date).save()
            else:
                merge_convo.size += tmp_size
                merge_convo.save(modify=True)
                for person in persons_merge:
                    for date in all_dates:
                        try:
                            Messages(number=conversation[date][person.name]['number'], unsend=conversation[date][person.name]
                                     ['unsend'], media=conversation[date][person.name]['media'], sender=person, date=date).save()
                        except KeyError:
                            Messages(sender=person, date=date).save()
                self.delete()

    def __str__(self):
        persons = [p.name for p in Person.objects.filter(conversation=self)]
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=50)
    conversation = models.ForeignKey(JsonFile, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Messages(models.Model):
    number = models.IntegerField(default=0)
    unsend = models.IntegerField(default=0)
    media = models.IntegerField(default=0)
    date = models.DateField(default=0)
    sender = models.ForeignKey(Person, on_delete=models.CASCADE)

    def to_dict(self):
        super(Messages, self)
        return {
            "number": self.number,
            "unsend": self.unsend,
            "media": self.media,
        }

    def __str__(self):
        return f'{self.date}-{self.sender}'
