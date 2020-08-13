import os
import sys
import struct

class MethodTrace():
    def __init__(self):
        self.info_log = {}
        self.info_method_call = {}
        self.info_method_call_entry = {}
        self.info_threads = {}
        self.info_methods = {}
        
        self.file_key = None
        self.file_data = None

    
    def __sub_filename(self, sfile, ext):
        file_dir = os.path.dirname(sfile)
        p = os.path.basename(sfile)
        f= os.path.splitext(p)[0]
        filePath = os.path.join(file_dir, f  + '.' + ext)
        return filePath
        
    def open_tracefile(self, sfile):
        fp = open(sfile, 'rb')
        self.file_key = self.__sub_filename(sfile, 'key')
        self.file_data = self.__sub_filename(sfile, 'data')
        
        fp_key = open(self.file_key, 'wb')
        fp_data = open(self.file_data, 'wb')

        key_mode = True
        key_str = '*end\n'
        n = 0

        while(True):
            datas = fp.read(10000)
            if datas:
                if key_mode == True:
                    for s in datas:
                        if key_mode == True:
                            fp_key.write(s)
                            if s == key_str[n]:
                                n = n + 1
                                if n == len(key_str):
                                    key_mode = False
                            else:
                                n = 0
                        else:
                            fp_data.write(s)
                else:
                    fp_data.write(datas)
            else:
                break

        fp.close()
        fp_key.close()
        fp_data.close()

    def parse(self):
        fp_key = open(self.file_key, 'r')

        file_mode = None
        for line in fp_key.readlines():
            if line[0] == '*':
                if line == '*version\n':
                    file_mode = 0
                elif line == '*threads\n':
                    file_mode = 1
                elif line == '*methods\n':
                    file_mode = 2
                elif line == '*end\n':
                    file_mode = 3
            else:
                if file_mode == 1: # thread
                    sp = line.split()
                    self.info_threads[int(sp[0])] = sp[1]
                    pass
                elif file_mode == 2: # method
                    sp = line.split()
                    c = sp[1].replace('/', '.')
                    self.info_methods[int(sp[0], 16)] = c + '.' + sp[2]
                    pass
        fp_key.close()

        fp_data = open(self.file_data, 'rb')
        lid = 0
        if fp_data.read(4) != 'SLOW':
            return False

        version = struct.unpack('H', fp_data.read(2))[0]
        
        if version != 3 and version != 1:
            print('error')
            return False
        
        offset = struct.unpack('H', fp_data.read(2))[0]
        fp_data.seek(offset)

        while(True):
            if version == 1:
                data = fp_data.read(1)
                if data:
                    try:
                        id_thread = struct.unpack('B', data)[0]
                        t = struct.unpack('I', fp_data.read(4))[0]
                        mode_method = t & 3
                        id_method = t & 0xFFFFFFFC
                        time_call = struct.unpack('I', fp_data.read(4))[0]
                    except:
                        continue
                else:
                    break                
            elif version == 3:
                data = fp_data.read(2)
                if data:
                    try:
                        id_thread = struct.unpack('H', data)[0]
                        t = struct.unpack('I', fp_data.read(4))[0]
                        mode_method = t & 3
                        id_method = t & 0xFFFFFFFC
                        time_call = struct.unpack('I', fp_data.read(4))[0]
                        #r = struct.unpack('I', fpData.read(4))[0]
                        fp_data.read(4)
                    except:
                        continue
                else:
                    break
            key = (('%09u' % time_call) + '-' + ('%09u' % lid))

            self.info_log[key] = [ time_call, id_thread, id_method, mode_method ]
            lid = lid + 1
            
            key = self.info_methods[id_method]
            if mode_method == 0: # method enter
                if key not in self.info_method_call:
                    self.info_method_call[key] = []
                    self.info_method_call_entry[key] = 0
                    self.info_method_call[key].append([ time_call ])
                else:
                    self.info_method_call[key].append([ time_call ])
            else:
                if key not in self.info_method_call:
                    pass
                else:
                    self.info_method_call[key][self.info_method_call_entry[key]].append( time_call )
                    self.info_method_call_entry[key] = self.info_method_call_entry[key] + 1

        fp_data.close()
        return True

    def output_log(self, out_file = None, in_filter_threads = None, out_filter_threads = None):
        infoMode = ['enter', 'exit', 'e-exit']
        
        if out_file != None:
            fp = open(out_file, 'w')
        else:
            fp = sys.stdout
        
        for key in sorted(self.info_log.keys()):
            time_call = self.info_log[key][0]
            id_thread = self.info_log[key][1]
            id_method = self.info_log[key][2]
            mode_method = self.info_log[key][3]
            if out_filter_threads != None and self.info_threads[id_thread] in out_filter_threads:
                pass
            elif in_filter_threads == None or self.info_threads[id_thread] in in_filter_threads:
                out_string = ('%10u' % time_call) + ' ' + ('%15s' % self.info_threads[id_thread]) \
                 + ('%8s' % infoMode[mode_method]) + ' ' + self.info_methods[id_method] + '\n'
                fp.write(out_string)

        if out_file != None:
            fp.close()

    def get_method_time(self, method_name):
        try:
            return self.info_method_call[method_name]
        except:
            return None


class TraceView:
    def __init__(self, sfile):
        self.trace = MethodTrace()
        self.trace.open_tracefile(sfile)
        if not self.trace.parse():
            self.trace = None


    def saveLog(self, sfile = None, in_filters = None, out_filters = None):
        if self.trace != None:
            self.trace.output_log(sfile, in_filters, out_filters)
            

if __name__ == '__main__':
    tv = TraceView('ddms.trace')
    tv.saveLog('log', None, ['FinalizerWatchdogDaemon', 'JDWP'])










