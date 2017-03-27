import requests
import re
import json
from .models import Smile


class SmileReaper(object):
    """
    
    """
    LINK = 'http://goodgame.ru/js/minified/global.js'
    PATTERN = r'\s*Smiles : (?P<smiles>\[.*\]),\s*Channel_Smiles : (?P<channel_smiles>{.*}),'

    def __init__(self):
        super(SmileReaper, self).__init__()
        self._data = None

    def _get_data_from_goodgame(self):
        response = requests.get(self.LINK)
        if response.status_code != 200:
            raise ValueError('Cant get data from GG')
        self._data = response.text

    def _parse_goodgame_data(self):
        r = re.search(self.PATTERN, self._data)
        self._data = r.groupdict()
        if 'smiles' not in self._data or not len(self._data['smiles']):
            raise ValueError('Cant parse data')
        for key in self._data:
            self._data[key] = json.loads(self._data[key])

    def _reap_smiles(self):
        for smile in self._data['smiles']:
            smile['gg_id'] = smile['id']
            smile.pop('id')
            obj, created = Smile.objects.update_or_create(defaults=smile, name=smile['name'])
            obj.save()

        for channel_id in self._data['channel_smiles']:
            smiles = self._data['channel_smiles'][channel_id]
            for smile in smiles:
                smile['gg_id'] = smile['id']
                smile.pop('id')
                obj, created = Smile.objects.update_or_create(defaults=smile, name=smile['name'])
                obj.save()

    def start(self):
        self._get_data_from_goodgame()
        self._parse_goodgame_data()
        self._reap_smiles()


def start_smile_reaper():
    reaper = SmileReaper()
    reaper.start()
