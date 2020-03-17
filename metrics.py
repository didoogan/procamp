from abc import ABC, abstractmethod
from argparse import ArgumentParser

import psutil as pu


CPU_INFORMER_TYPE = 'cpu'
RAM_INFORMER_TYPE = 'ram'
SWAP_INFORMER_TYPE = 'swap'
MEMORY_INFORMER_TYPE = 'mem'

INFORMER_TYPE_ARGUMENT = 'informer_type'


class InfoPrinter:

    def __init__(self, informer):
        self.informer = informer

    def print(self):
        for field in self.informer.info_fields:
            info = self.informer.info
            print(f'{self.informer.info_string}{field} {getattr(info, field)}')


class Informer(ABC):

    def __init__(self, info_fields, info_string):
        self.info_fields = info_fields
        self.info_string = info_string

    def print_info(self):
        InfoPrinter(self).print()

    @property
    @abstractmethod
    def info(self):
        pass


class CpuInformer(Informer):

    @property
    def info(self):
        return pu.cpu_times()


class RamInformer(Informer):

    @property
    def info(self):
        return pu.virtual_memory()


class SwapInformer(Informer):

    @property
    def info(self):
        return pu.swap_memory()


class MemoryInformerFacade:

    def __init__(self, informer_fabric):
        self.fabric = informer_fabric

    def print_info(self):
        ram_informer = self.fabric.factory_method(RAM_INFORMER_TYPE)
        ram_informer.print_info()
        swap_informer = self.fabric.factory_method(SWAP_INFORMER_TYPE)
        swap_informer.print_info()


class ArgumentsParser:

    parser = ArgumentParser()

    def set_arguments(self):
        self.parser.add_argument(
            INFORMER_TYPE_ARGUMENT,
            choices=(CPU_INFORMER_TYPE, MEMORY_INFORMER_TYPE),
            help='Type of informer (cpu or mem'
        )

    def get_argument(self, argument):
        name_space = self.parser.parse_args()
        return getattr(name_space, argument)


class InformerFabric:

    type_informer_map = {
        CPU_INFORMER_TYPE: CpuInformer,
        RAM_INFORMER_TYPE: RamInformer,
        SWAP_INFORMER_TYPE: SwapInformer,
        MEMORY_INFORMER_TYPE: MemoryInformerFacade,
    }
    cpu_fields = (
        'idle',
        'user',
        'guest',
        'iowait',
        'steal',
        'system',
    )
    cpu_info_string = 'system.cpu.'
    ram_fields = (
        'total',
        'used',
        'free',
        'shared',
    )
    ram_info_string = 'virtual '
    swap_fields = (
        'total',
        'used',
        'free',
    )
    swap_string = 'swap '

    @property
    def type_informer_args_map(self):
        return {
            CPU_INFORMER_TYPE: (self.cpu_fields, self.cpu_info_string),
            RAM_INFORMER_TYPE: (self.ram_fields, self.ram_info_string),
            SWAP_INFORMER_TYPE: (self.swap_fields, self.swap_string),
            MEMORY_INFORMER_TYPE: (self,),
        }

    def factory_method(self, informer_type):
        args = self.type_informer_args_map[informer_type]
        informer_cls = self.type_informer_map[informer_type]
        return informer_cls(*args)


if __name__ == '__main__':
    arg_parser = ArgumentsParser()
    arg_parser.set_arguments()
    informer_type = arg_parser.get_argument(INFORMER_TYPE_ARGUMENT)
    informer = InformerFabric().factory_method(informer_type)
    informer.print_info()
