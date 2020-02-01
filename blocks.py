

class Block:

    def __init__(self, name, start_addr, end_addr):
        self.name = name
        self.ranges = [(start_addr, end_addr)]

    def __iter__(self):
        return BlockIterator(self)


class BlockIterator:

    def __init__(self, block):
        self._block = block
        self._range_index = 0
        self._last_addr = None
        self._sample_count = 0
        self._step_size = 0
        


    def __next__(self):
        i = self._range_index
        start = self._block.ranges[i][0]
        end = self._block.ranges[i][1]
        size = end - start
        

        if self._sample_count == 0:
            self._last_addr = start
            #TODO: calculate step size
            self._step_size = 1
        elif self._sample_count == 1:
            self._last_addr += 1
        elif self._sample_count == 2:
            if 4 >= size <= 10:
                self._last_addr = end - 1
            elif size > 10:
                self._last_addr += 4
            else:
                self._range_index += 1
                self._sample_count = 0
        else:
            if self._sample_count == 3 and size <= 10:
                self._last_addr += 1
            else:
                self._last_addr += self._step_size
        
        if self._last_addr == end:
            self._range_index += 1
            self._sample_count = 0
        if self._range_index == len(self._block.ranges):
            raise StopIteration
        self._sample_count += 1
        return self._last_addr


if __name__ == "__main__":
    a1 = Block("A1", 0x0, 0x1)
    a = Block("A", 0x0, 0x4)
    b = Block("B", 0x0, 0x10)
    c = Block("C", 0x0, 11)

    for x in c:
        print("%X"%x)
