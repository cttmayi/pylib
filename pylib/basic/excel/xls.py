import xlwings as xw

app = xw.App(visible=True, add_book=False)
app.display_alerts=False
app.screen_updating=False

def quit():
    app.quit()


class Table:
    def __init__(self, rng):
        self.rng = rng
        pass

    def value(self, keys):
        table = self.rng.value

        varray = []
        if len(table) > 1:
            head = table[0]
            del table[0]
            
            for t in table:
                value = {}
                
                for i in range(len(head)):
                    k = head[i]
                    v = t[i]
                    if v is not None:
                        value[k] = v
                varray.append(value)
                
        vmap = {}
        if keys is not None:
            for a in varray:
                key = []
                for k in keys:
                    key.append(a[k])
                key = '.'.join(key)
                vmap[key] = a        
        
        return varray, vmap



class Sheet:
    def __init__(self, sheet):
        self.sheet = sheet


    def find_row_head(self, pos, head, max_col = 100):
        row = pos[0]
        start_col = pos[1]
        head_map = {}

        for name in head:
            for col in range(start_col, max_col): 
                value = self.sheet.range((row, col)).value
                if value == None:
                    break
                if name == value:        
                    head_map[name] = col
        return head_map


    def update_row(self, row, head_map, values):
        for key, value in values.items():
            if key in head_map.keys():
                col = head_map[key]
                self.sheet.range((row, col)).value = value


    def table(self, pos):
        return Table(self.sheet.range(pos).expand('table'))


    def delete_row(self, row):
        self.sheet.range((row, 1)).api.EntireRow.Delete()
    
    
    def is_pos_empty(self, pos):
        value = self.sheet.range(pos).value
        
        if value == None:
            return True
        return False


    def delete_rows(self, start_row, max_row = 10000):
        for row in range(start_row, max_row):
            if self.is_pos_empty((row, 1)):
                break
            self.sheet.range((row, 1)).api.EntireRow.Delete()
        

    def find_row_value(self, row, value, start_col=1, max_col = 20):
        for col in range(start_col, max_col): 
            if value == self.sheet.range((row, col)).value:
                return col
        return None

    def find_col_value(self, col, value, start_row=1, max_row = 20):
        for row in range(start_row, max_row): 
            if value == self.sheet.range((row, col)).value:
                return row
        return None

    def find_value(self, value, max_row, max_col, start_row=1, start_col=1):
        for row in range(start_row, max_row): 
            for col in range(start_col, max_col):
                rvalue = self.sheet.range((row, col)).value
                if value == self.sheet.range((row, col)).value:
                    return row, col
        return None, None


    def value(self, pos):
        return self.sheet.range(pos).value


    def update(self, pos, values):
        self.sheet.range(pos).value = values


class Excel:
    def __init__(self, name):
        self.wb = app.books.open(name)


    def sheet(self, name, ):
        return Sheet(self.wb.sheets[name])


    def save(self):
        self.wb.save()


    def close(self, is_save=True):
        if is_save:
            self.wb.save()
        self.wb.close()

if __name__ == '__main__':
    e = Excel('test_file.xlsx')
    sheet = e.sheet('A')

    row, col = sheet.find_value('TAB', 200, 2)

    if row is not None:
        table = sheet.table((row, col))
        a, m = table.value(['TAB'])
        print(a)
        print(m)

    row, col = sheet.find_value('Start', 20, 20)
    head = sheet.find_row_head((row, col), ['Start', 'Name', 'PIC'])
    value = {
        'Start': 'Y',
        'Name': 'NPC',
        'PIC': 1
    }
    sheet.delete_rows(row+1)
    sheet.update_row(row+1, head, value)

    e.close()
    quit()


