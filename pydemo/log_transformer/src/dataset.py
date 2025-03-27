import time
from torch.utils.data import Dataset, DataLoader
from pylib.basic.file import jsonl_read, gzip_read
from src.encoder import ID_IGORNED


class LogDataset(Dataset):
    def __init__(self, data_path, per_log_length=256):
        super().__init__()

        start_time = time.time()

        self.input_ids_list = []
        self.labels_list = []

        lines = gzip_read(data_path)

        print(f"load data time: {time.time() - start_time}")

        for offset in range(0, len(lines)-per_log_length, 4):# range(len(lines) - data_len//3):
            input_ids = []
            labels = []
            for v1, v2 in lines[offset:offset+per_log_length]:
                # input_ids.append(ID_START) # start
                input_ids.append(v1) # tid
                input_ids.append(v2) # event id
                # labels.append(ID_IGORNED) # start
                labels.append(ID_IGORNED) # tid
                labels.append(v2) # event id
                # for v in row['EventArgs'].values():
                #         one_data.append(str2int('*'))

            self.input_ids_list.append(input_ids)
            self.labels_list.append(labels)            
        print(f"load dataset time: {time.time() - start_time}")
        print(f"dataset length: {len(self.input_ids_list)}")
        # print(self.input_ids_list[-1])


    def __len__(self):
        return len(self.input_ids_list)

    def __getitem__(self, idx):
        result = {}

        if isinstance(idx, int):
            input_ids = self.input_ids_list[idx]
            labels = self.labels_list[idx]
            result['input_ids'] = input_ids
            result['attention_mask'] = [1] * len(input_ids)
            result['labels'] = labels
        else:
            raise NotImplementedError()
        #     items = self.input_ids[idx]
        #     result['input_ids'] = items
        #     result['attention_mask'] = []
        #     for item in items:
        #         result['attention_mask'].append([1] * len(item))
        #     result['labels'] = items.copy()
        return result


def create_dataloader(data_path, batch_size, shuffle=True):
    dataset = LogDataset(data_path)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    return dataloader

def create_dataset(data_path):
    dataset = LogDataset(data_path)
    return dataset