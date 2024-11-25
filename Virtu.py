'''
CHANGES: 
1.FIXED THE LABELS ISSUE  AND BACKTRACKCING ISSUES , 
2. ALSO , OUR MEMEORY SPACES IS SET TO ZERO INITALLY  INSTEAD  OF NONE , EASIER TO WORK WITH INTS 
3. CREATED THE OPCODE PRINTING STRINGS, ONLY WORKS FOR STRINGS WITHTOUT SPACES 
   HOW IT WORKS : WE STORE STRINGS CHARACTERS BY  CHAR IN MEMORY TERMINATED BY A NULL TGERMINATING CHAR - \0
   IN THE CODE SECTION WE STORE THE POINTER(ADDRS) TO THE START OF THE STRING





'''


import sys
from dataclasses import dataclass

class Label:
    def __init__(self, name: str, addr: int = -1, decl: bool = False):
        self.name: str = name
        self.addr: int = addr
        self.declared: bool = decl

class LabelTable:
    labels: list[Label] = []

    def __init__(self):
        pass

    def getLabelIndex(self, name: str) -> int:
        for l, lab in enumerate(self.labels):
            if lab.name == name:
                return l

    def add(self, name: str, addr: int, declaring: bool) -> int:
        inside: bool = self.contains(name)
        if inside and not declaring:
            labelInd = self.getLabelIndex(name)
            prevAddr: int = self.labels[labelInd].addr
            self.labels[labelInd].addr = addr
            return prevAddr

        elif inside and declaring:
            labelInd = self.getLabelIndex(name)
            prevAddr: int = self.labels[labelInd].addr
            self.labels[labelInd].addr = addr
            self.labels[labelInd].declared = True
            return prevAddr

        elif not inside and not declaring:
            self.labels.append(Label(name, addr))
            return -1

        else:  # not inside and declaring
            self.labels.append(Label(name, addr, declaring))
            return -1

    def contains(self, name: str) -> bool:
        for lab in self.labels:
            if lab.name == name:
                return True
        return False

class COUNTER:
    def __init__(self, i: int):
        self.cnt = i

    def cn(self) -> int:
        self.cnt += 1
        return self.cnt - 1

@dataclass
class OP:
    CN = COUNTER(0)
    ALLOC: int = CN.cn()
    VAR: int = CN.cn()
    STO: int = CN.cn()
    VAL: int = CN.cn()
    PUSH: int = CN.cn()
    ADD: int = CN.cn()
    SUB: int = CN.cn()
    INPTI: int = CN.cn()
    PRNT: int = CN.cn()
    PRNTS: int = CN.cn()
    PRNTI: int = CN.cn()
    MUL: int = CN.cn()
    DIV: int = CN.cn()
    MOD: int = CN.cn()
    EQL: int = CN.cn()
    CLT: int = CN.cn()
    CGT: int = CN.cn()
    CLE: int = CN.cn()
    CGE: int = CN.cn()
    AND: int = CN.cn()
    OR: int = CN.cn()
    XOR: int = CN.cn()
    NOT: int = CN.cn()
    LABEL: int = CN.cn()
    JFALSE: int = CN.cn()
    JTRUE: int = CN.cn()
    JUMP: int = CN.cn()
    CALL: int = CN.cn()
    RET: int = CN.cn()
    NOP: int = CN.cn()
    HALT: int = CN.cn()

class CPU:
    MEM_SIZE = 1000

    def __init__(self, cp: int, vp: int):
        self.ip: int = 0  # Instruction Pointer
        self.cp: int = cp
        self.vp: int = vp
        self.hp: int = vp + 1
        self.sp: int = self.MEM_SIZE
        self.mem: list[int] = []

    def initialize(self) -> None:
        self.mem = [0] * self.MEM_SIZE  #Initialize memory with 0

    def allocate_mem(self, var_mem: int) -> None:
        if var_mem > 0 and (self.vp + var_mem < self.hp):
            self.hp = self.vp + var_mem - 1

class VM:
    cpu: CPU = CPU(500, 600)

    def __init__(self, filename: str):
        self.cpu.initialize()
        self.filename: str = filename
        self.tos: int = -1
        self.running: bool = True
        self.lt = LabelTable()
        self.load_code()

    def load_code(self) -> None:
        def map_op(op_string: str) -> int:
            op_map = {
                "ALLOC": OP.ALLOC,
                "VAR": OP.VAR,
                "STO": OP.STO,
                "VAL": OP.VAL,
                "PUSH": OP.PUSH,
                "ADD": OP.ADD,
                "SUB": OP.SUB,
                "PRNTS": OP.PRNTS,
                "PRNT": OP.PRNT,
                "MUL": OP.MUL,
                "DIV": OP.DIV,
                "MOD": OP.MOD,
                "EQL": OP.EQL,
                "CLT": OP.CLT,
                "CGT": OP.CGT,
                "CLE": OP.CLE,
                "CGE": OP.CGE,
                "AND": OP.AND,
                "OR": OP.OR,
                "XOR": OP.XOR,
                "NOT": OP.NOT,
                "LABEL": OP.LABEL,
                "JTRUE": OP.JTRUE,
                "JFALSE": OP.JFALSE,
                "INPTI": OP.INPTI,
                "JUMP": OP.JUMP,
                "CALL": OP.CALL,
                "RET": OP.RET,
                "HALT": OP.HALT,
            }
            return op_map.get(op_string, -1)

        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
                self.CODES = [
                    word
                    for line in lines
                    for word in line.strip().split()
                ]

                k = 0
                self.CODE = []

                while k < len(self.CODES):
                    if self.CODES[k] == "LABEL":
                        label_name = self.CODES[k + 1]
                        addr = self.lt.add(label_name, len(self.CODE), True)

                        while addr != -1:   #backtracking happens here 
                            if addr >= len(self.CODE):
                                raise IndexError(f"Address {addr} is out of range.")
                            temp = self.CODE[addr]
                            self.CODE[addr] = len(self.CODE)
                            addr = temp

                        self.CODE.append(OP.NOP)
                        k += 2  #skip the label and name 

                    elif self.CODES[k] in ["JFALSE", "JTRUE", "JUMP" , "CALL"]:
                        opcode = map_op(self.CODES[k])
                        label_name = self.CODES[k + 1]
                        addr = self.lt.add(label_name, len(self.CODE) + 1, False)
                        self.CODE.append(opcode)
                        self.CODE.append(addr)
                        k += 2   #skip over the label and label name 

                    elif self.CODES[k] == "PRNT":
                        opcode = map_op(self.CODES[k])
                        self.CODE.append(opcode)
                        self.CODE.append(self.cpu.cp)
                        s: str = self.CODES[k + 1]

                        if s.startswith('"') and s.endswith('"'):
                            s = s[1:-1]  # Remove surrounding quotes so ths

                        try:
                            # Decode escape sequences like \n, \t, etc.
                            s = bytes(s, "utf-8").decode("unicode_escape")  #encode the escape chars so that they are treated as strings
                        except ValueError:
                            print(f"Error decoding escape sequences in string: {s}")
                            sys.exit(1)

                        for ch in s:
                            self.cpu.mem[self.cpu.cp] = ord(ch)  #store char by char as int in memeory , in the constant pool
                            self.cpu.cp += 1

                        self.cpu.mem[self.cpu.cp] = ord('\0')  # Null-terminate the string
                        self.cpu.cp += 1
                        k += 2   #skip oveer the prnt and the string 

                    else:
                        token = self.CODES[k]
                        if token.isalpha():
                            self.CODE.append(map_op(token))
                        else:
                            self.CODE.append(int(token))
                        k += 1

                print(self.CODE)

                for i, code in enumerate(self.CODE):
                    self.cpu.mem[i] = code

        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            self.running = False
        except ValueError as e:
            print(f"ValueError while loading code: {e}")
            self.running = False
        except IndexError as e:
            print(f"IndexError while loading code: {e}")
            self.running = False

    def fetch(self) -> None:
        self.cpu.ip += 1

    def push(self, val: int) -> None:
        self.cpu.sp -= 1
        self.cpu.mem[self.cpu.sp] = val

    def pop(self) -> int:
        val = self.cpu.mem[self.cpu.sp]
        self.cpu.mem[self.cpu.sp] = None
        self.cpu.sp += 1
        return val

    def printStack(self) -> None:
        print(self.cpu.mem[self.cpu.sp: self.cpu.MEM_SIZE])
        print(" ")

    def execute(self) -> None:
        instr = self.cpu.mem[self.cpu.ip - 1]
        match instr:
            case OP.PUSH:
                self.push(self.cpu.mem[self.cpu.ip])
                self.fetch()

            case OP.ALLOC:
                self.cpu.allocate_mem(self.cpu.mem[self.cpu.ip])
                self.fetch()

            case OP.VAR:
                self.push(self.cpu.vp + self.cpu.mem[self.cpu.ip])
                self.fetch()

            case OP.STO:
                val = self.pop()
                addr = self.pop()
                self.cpu.mem[addr] = val

            case OP.VAL:
                addr = self.pop()
                self.push(self.cpu.mem[addr])

            case OP.ADD:
                self.push(self.pop() + self.pop())

            case OP.SUB:
                tos, sos = self.pop(), self.pop()
                self.push(sos - tos)

            case OP.MUL:
                self.push(self.pop() * self.pop())

            case OP.DIV:
                tos, sos = self.pop(), self.pop()
                self.push(sos // tos if tos != 0 else 0)

            case OP.MOD:
                tos, sos = self.pop(), self.pop()
                self.push(sos % tos if tos != 0 else 0)

            case OP.EQL:
                self.push(1 if self.pop() == self.pop() else 0)

            case OP.CLT:
                tos, sos = self.pop(), self.pop()
                self.push(1 if sos < tos else 0)

            case OP.CGT:
                tos, sos = self.pop(), self.pop()
                self.push(1 if sos > tos else 0)

            case OP.CLE:
                tos, sos = self.pop(), self.pop()
                self.push(1 if sos <= tos else 0)

            case OP.CGE:
                tos, sos = self.pop(), self.pop()
                self.push(1 if sos >= tos else 0)

            case OP.AND:
                self.push(1 if self.pop() and self.pop() else 0)

            case OP.OR:
                self.push(1 if self.pop() or self.pop() else 0)

            case OP.XOR:
                tos, sos = self.pop(), self.pop()
                self.push(1 if (sos and not tos) or (tos and not sos) else 0)

            case OP.NOT:
                tos = self.pop()
                self.push(1 if not tos else 0)

            case OP.PRNTS:
                print(self.pop())

            case OP.JUMP : 
                self.cpu.ip = self.cpu.mem[self.cpu.ip]
                self.fetch()

            case OP.JTRUE:
                if self.pop() == 1:
                    self.cpu.ip = self.cpu.mem[self.cpu.ip] - 1
                self.fetch()

            case OP.JFALSE:
                if self.pop() == 0:
                    self.cpu.ip = self.cpu.mem[self.cpu.ip] - 1
                self.fetch()

            case OP.PRNT:
                poolPointer: int = self.cpu.mem[self.cpu.ip]   # get the pointer to the start of the string
                while self.cpu.mem[poolPointer] != ord('\0'):  #get the next char until we hit the null terminated char 
                    
                    print(chr(self.cpu.mem[poolPointer]), end='')  #print the string , use end='' ., simnce we are printing char by char and we dont to print a new line char , similar to println and print in java 
                    #rememeber we stored chars as int , we  need to convert them back to chars
                    poolPointer += 1
                self.fetch()

            case OP.INPTI:
                k: int = int(input(""))   #get user input , pretty trivia :)
                self.push(k)
            case OP.CALL:
                currAdr = self.cpu.ip
                self.cpu.ip = self.cpu.mem[self.cpu.ip]
                self.fetch()
                self.push(currAdr + 3)

            case OP.RET:
            	self.cpu.ip =  self.pop() 


            case OP.NOP:
                pass

            case OP.HALT:
                self.running = False

            case _:
                print(f"Unknown instruction: {instr} {self.cpu.ip}")
                self.running = False

    def run(self) -> None:
        while self.running:
            self.fetch()
            self.execute()
            self.printStack()

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <name of the file>")
        sys.exit(1)
    virtu = VM(sys.argv[1])
    virtu.run()

if __name__ == "__main__":
    main()



'''
fetch-execute//
fetch 
	-> opcodes 

stack based machine: 
[2 ,2]  //last in , last out 

>[2 , 97 , 2]
push  2 
 
push  2
ADD      [2 , 99]	//pop tos , pop sos , add the two AND PUSH THE RESULT
	 				//prints whatever is  tos

tos - sos , tos/sos , tos%sos

"abcdef"   -> [a ,  b , d , e , f]

[1] TOS: 1  , SOS : 2
OPCODES:
	ALLOC  5 , FIVE SPACES FOR 5 VARIABLES  
	OUTS > OUTPUT A STRING/char,
	OUT >  INT,
	OUTB , 1 > TRUE , 0 > FALSE

	Arith opcodes > add, mul , sub , mod , div , 
	logic: eql , or , and , xor , not ,  cgt , cge , clt (sos), cle ,  


var 0 
STO 10 ,  

MEMORY:
PUSH = 2
[ PUSH , 2  , PUSH , 2]


>IP 	  >CP           >VP					   >HEAP		  						>SP
0	

X = INOUT();
INT K[X];


int k ; int i ; 
k = 9 
i = 10 
i = k 


///

//STORE SOS = TOS    ///ABSTRACTION
//PUT TOS INTO THE MEMORY SLOT / VARIABLE DEFINED BY SOS  ---

K = 1 ; 
I = K ;

VAR 0 := K . VAR 1 := I
ALLOC 2   
VAR 0   	;LOAD ADDR OF VAR 0 
PUSH 1 
STO   		;STORE 5 INTO THE  VAR 0
VAR 1 		
VAR 0
VAL         ; GET THE VALUE AT THE ADDRESS WHICH IS TOS
STO          


[491]


ALLOC 2 
VAR 0 
PUSH 5 
STO
VAR 0 
VAL
call fucn 
PRNT

Label func 
push 1 
prn
ret 

'''
