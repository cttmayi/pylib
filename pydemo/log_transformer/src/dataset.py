

# pytorch dataset for log transformer
# https://github.com/huggingface/transformers/blob/main/examples/pytorch/language-modeling/run_mlm.py

from torch.utils.data import Dataset, DataLoader
from pylib.basic.file import jsonl_read

FILE = 'data/Android_2k.log_structured.csv'


_str_dict = {}
def str2int(s):
    s = str(s)
    if s not in _str_dict:
        _str_dict[s] = len(_str_dict)
    return _str_dict[s]

class LogDataset(Dataset):
    def __init__(self, data_path, data_len=512):
        self.data = []

        lines = jsonl_read(data_path)
            
        one_data = []
        for l, row in enumerate(lines):
            if l == 0:
                continue
            # ['1506', '03-17', '16:15:49.587', '2227', '2227', 'V', 'PhoneStatusBar', 'setLightsOn(true)', 'E123', 'setLightsOn(true)']
            one_data.append(str2int(row['Pid'])) # pid
            one_data.append(str2int(row['EventId'])) # event id
            for v in row['EventArgs'].values():
                    one_data.append(str2int('*'))
            if len(one_data) > data_len:
                self.data.append(one_data[0:data_len])
                one_data = []


    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        
        result = {}

        if isinstance(idx, int):
            item = self.data[idx]
            result['input_ids'] = item
            result['attention_mask'] = [1] * len(item)
            result['labels'] = item.copy()
        else:
            items = self.data[idx]
            result['input_ids'] = items
            result['attention_mask'] = []
            for item in items:
                result['attention_mask'].append([1] * len(item))
            result['labels'] = items.copy()
        return result


def create_dataloader(data_path, batch_size, shuffle=True):
    dataset = LogDataset(data_path)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    return dataloader

def create_dataset(data_path):
    dataset = LogDataset(data_path)
    return dataset