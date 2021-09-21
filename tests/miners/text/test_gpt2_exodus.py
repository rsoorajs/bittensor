import os, sys
from unittest.mock import MagicMock
import unittest.mock as mock
import bittensor
import torch
import numpy
from miners.text.template_miner import Miner,Nucleus


def test_run_template():

    magic = MagicMock(return_value = 1)
    def test_forward(cls,pubkey,inputs_x):
        return magic(pubkey,inputs_x)

    config = Miner.config()
    config.miner.n_epochs = 1
    config.miner.epoch_length = 2
    with mock.patch.object(Miner,'forward_text',new=test_forward):
        gpt2_exodus_miner = Miner( config = config )
        bittensor.neuron.subtensor.connect = MagicMock(return_value = True)  
        bittensor.neuron.subtensor.is_connected = MagicMock(return_value = True)      
        bittensor.neuron.subtensor.subscribe = MagicMock(return_value = True)  
        bittensor.neuron.metagraph.set_weights = MagicMock(return_value = True) 
        gpt2_exodus_miner.run()

        assert magic.call_count == 1
        assert isinstance(magic.call_args[0][0],str)
        assert torch.is_tensor(magic.call_args[0][1])

if __name__ == "__main__":
    test_run_template()