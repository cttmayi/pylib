import pptx2md

import collections 
import collections.abc
from pptx import Presentation
#from pptx2md.global_var import g
import pptx2md.outputter as outputter
from pptx2md.parser import parse
#from pptx2md.tools import fix_null_rels
#import argparse
#import os, re

file_path = 'test/test_pptx.pptx'
out_path = 'output.md'
prs = Presentation(file_path)
out = outputter.madoko_outputter(out_path)
parse(prs, out)