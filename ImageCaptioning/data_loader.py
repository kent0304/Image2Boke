import torch
import torchvision.transforms as transforms
import torch.utils.data as data
import os
import pickle
import numpy as np
import nltk
from PIL import Image
from build_vocab import Vocabulary, unpickle
# from pycocotools.coco import COCO

import random



class BoketeDataset(data.Dataset):
    """Bokete Custom Dataset compatible with torch.utils.data.DataLoader."""
    def __init__(self, image_dir, vocab, transform=None):
        """Set the path for images, captions and vocabulary wrapper.
        
        Args:
            image_dir: image directory.
            vocab: vocabulary wrapper.
            transform: image transformer.
        """
        self.image_dir = image_dir
        # self.text = text
        # self.coco = COCO(json)
        # self.ids = list(self.coco.anns.keys())
        self.vocab = vocab
        self.transform = transform

        # self.tokenized_text_list = unpickle('tokenized_bokete_text.pkl')
        self.tokenized_text_list = unpickle('tokenized_text_list_mecab.pkl')


    def __getitem__(self, index):
        """Returns one data pair (image and caption)."""
        image_dir = self.image_dir
        vocab = self.vocab

        try:
            caption = self.tokenized_text_list[index]
        except:
            caption = random.choice(self.tokenized_text_list)


        image = Image.open(image_dir + str(index) +'.jpg').convert('RGB')
        if self.transform is not None:
            image = self.transform(image)

        # Convert caption (string) to word ids.
        # tokens = nltk.tokenize.word_tokenize(str(caption).lower())
        tokens = caption
        caption = []
        caption.append(vocab('<start>'))
        caption.extend([vocab(token) for token in tokens])
        caption.append(vocab('<end>'))
        # print(caption)
        target = torch.Tensor(caption)
        return image, target

    def __len__(self):
        return len(self.tokenized_text_list)


def collate_fn(data):
    """Creates mini-batch tensors from the list of tuples (image, caption).
    
    We should build custom collate_fn rather than using default collate_fn, 
    because merging caption (including padding) is not supported in default.
    Args:
        data: list of tuple (image, caption). 
            - image: torch tensor of shape (3, 256, 256).
            - caption: torch tensor of shape (?); variable length.
    Returns:
        images: torch tensor of shape (batch_size, 3, 256, 256).
        targets: torch tensor of shape (batch_size, padded_length).
        lengths: list; valid length for each padded caption.
    """
    # Sort a data list by caption length (descending order).
    data.sort(key=lambda x: len(x[1]), reverse=True)
    images, captions = zip(*data)

    # Merge images (from tuple of 3D tensor to 4D tensor).
    images = torch.stack(images, 0)

    # Merge captions (from tuple of 1D tensor to 2D tensor).
    lengths = [len(cap) for cap in captions]
    targets = torch.zeros(len(captions), max(lengths)).long()
    for i, cap in enumerate(captions):
        end = lengths[i]
        targets[i, :end] = cap[:end]        
    return images, targets, lengths

def get_loader(image_dir, vocab, transform, batch_size, shuffle, num_workers):
    """Returns torch.utils.data.DataLoader for custom coco dataset."""
    bokete = BoketeDataset(image_dir=image_dir,
                       vocab=vocab,
                       transform=transform)
    
    # Data loader for COCO dataset
    # This will return (images, captions, lengths) for each iteration.
    # images: a tensor of shape (batch_size, 3, 224, 224).
    # captions: a tensor of shape (batch_size, padded_length).
    # lengths: a list indicating valid length for each caption. length is (batch_size).
    data_loader = torch.utils.data.DataLoader(dataset=bokete, 
                                              batch_size=batch_size,
                                              shuffle=shuffle,
                                              num_workers=num_workers,
                                              collate_fn=collate_fn)
    return data_loader