import os
import math
from src.utils.delete_file_from import delete_file_from
import random
import pandas as pd
from tqdm import tqdm
import csv
from src.types.subset_type import SubsetType
from src.utils.add_suffix import add_suffix
from src.config.config import NAME_OF_FILE_WITH_SUBSET_SIZES


class DataSetSplitter:
    
    def __init__(self, path_to_save, train_size, test_size, valid_size, label_counter, normalization_size):
        self.directory_path = path_to_save
        self.size_file_name = NAME_OF_FILE_WITH_SUBSET_SIZES
        self.create_state(train_size, test_size, valid_size)
        self.delete_files_in_directory()
        self.counter_dataframe = label_counter.copy()
        self.normalize(normalization_size)  
        self.prepare_counters()
        self.save_counters()

        
    def create_state(self, train_size, test_size, valid_size):
        self.state = {
            SubsetType.Train.value: {
                'path': os.path.sep.join([self.directory_path, add_suffix(SubsetType.Train.value)]),
                'size': train_size
            
            },
            SubsetType.Test.value: {
                'path': os.path.sep.join([self.directory_path, add_suffix(SubsetType.Test.value)]),
                'size': test_size
            
            },
            SubsetType.Valid.value: {
                'path': os.path.sep.join([self.directory_path, add_suffix(SubsetType.Valid.value)]),
                'size': valid_size
            
            },
        }
        
    def normalize(self, normalization_size):
        if normalization_size is not None:
            self.counter_dataframe.iloc[:, 0] =  normalization_size
               
    def prepare_counters(self):
        dataset_counters = {name:{} for name in self.state.keys()}
    
        for key in dataset_counters.keys():
            set_key_counter = {}
            for author_id, row in self.counter_dataframe.iterrows():
                count = row[0]
                set_key_counter[author_id] = math.floor(count * self.state[key]['size'])
            dataset_counters[key] = set_key_counter
    
        
        self.dataset_counters = dataset_counters
        
    def get_path(self, label):
        picks = []
    
        for key in self.dataset_counters.keys():
            if self.dataset_counters[key][label] > 0:
                picks.append(key)
        
        if len(picks) == 0:
            return None
        #choice one
        pick = random.choice(picks)
        #subtract
        self.dataset_counters[pick][label] -= 1
        #return path according to pick
        return self.state[pick]['path']
    
    def save_counters(self):
        counters = pd.DataFrame.from_dict(self.dataset_counters, orient='index')
        counters.to_csv(os.path.sep.join([self.directory_path, self.size_file_name]), sep=';')
        
        
    def delete_files_in_directory(self):
        for v in self.state.values():
            current_subset_path = v['path']
            delete_file_from(current_subset_path)
        delete_file_from(os.path.sep.join([self.directory_path, self.size_file_name]))
                
                
    def build_subsets(self, dataset):
        print(f'Building subsest with state {self.state}')
        for line in tqdm(dataset.shuffle(10000).as_numpy_iterator()):
            #label = author Id
            text, label = line
            text = bytes.decode(text)
            
            #TODO: DELETE! 
            label = bytes.decode(label)
            
            path = self.get_path(label)
            if path is None:
                continue
                
            with open(path, 'a', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                value = [text, label]
                writer.writerow(value)