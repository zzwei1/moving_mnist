# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_models.dcn.ipynb (unless otherwise specified).

__all__ = ['DCN']

# Cell
from fastai.vision.all import *
from .conv_rnn import *
try:
    from mmcv.ops import *
except:
    'please install MCV for your Pytorch version'

# Cell
class DCN(Module):
    "A Deformable Convolutional Kernel"
    def __init__(self,
                 in_channels,
                 out_channels,
                 kernel_size,
                 stride,
                 padding,
                 dilation=1,
                 deformable_groups=1):

        channels_ = deformable_groups * 2 * kernel_size[0] * kernel_size[1]
        self.conv_offset = nn.Conv2d(in_channels,
                                     channels_,
                                     kernel_size=kernel_size,
                                     stride=stride,
                                     padding=padding,
                                     bias=True)
        self.dconv = DeformConv2d(in_channels, out_channels, kernel_size, stride, padding, dilation, 1, deformable_groups)
        self.init_offset()

    def init_offset(self):
        self.conv_offset.weight.data.zero_()
        self.conv_offset.bias.data.zero_()

    def forward(self, input):
        out = self.conv_offset(input)
        o1, o2 = torch.chunk(out, 2, dim=1)
        offset = torch.cat((o1, o2), dim=1)
        return self.dconv(input, offset)