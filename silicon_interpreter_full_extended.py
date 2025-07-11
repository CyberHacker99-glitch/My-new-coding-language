
# SiliconLang Interpreter - Full Version

# Language Extension: .sil
# Author: Abhay Pratap Singh Sengar 

import sys
import re
import platform

registers = {'A': 0, 'B': 0}
memory = {}
stack = []
labels = {}
flags = {'ZF': 0, 'CF': 0, 'GF': 0, 'LF': 0, 'INT': 0}
vector_table = {}
encoding = 'utf-8'
trace = False
halt = False

def trace_log(msg):
    if trace:
        print(f"[TRACE] {msg}")

def evaluate(val):
    try:
        return int(val)
    except:
        return registers.get(val.strip(), 0)

# ----- Command Functions -----

def cmd_COPY(args):
    x, y = args.replace(' ', '').split('=')
    registers[x] = evaluate(y)

def cmd_GETMA(args):
    ma = args.strip('[] =')
    registers['A'] = memory.get(ma, 0)

def cmd_INF(_):
    print("CPU:", platform.processor())
    print("Platform:", platform.platform())

def cmd_STORMA(args):
    addr = args.split('=')[0].strip('[] ')
    memory[addr] = registers['A']

def cmd_GETADDR(args):
    addr = args.split('=')[0].strip('[] ')
    registers['A'] = memory.get(addr, 0)

def cmd_STORADDR(args):
    addr = args.split('=')[0].strip('[] ')
    memory[addr] = registers['A']

def cmd_ADD(args):
    registers['A'] += evaluate(args.split('+')[1])

def cmd_SUBT(args):
    registers['A'] -= evaluate(args.split('-')[1])

def cmd_MULT(args):
    registers['A'] *= evaluate(args.split('*')[1])

def cmd_DIVI(args):
    registers['A'] //= evaluate(args.split('/')[1])

def cmd_INCR(args):
    registers['A'] += 1

def cmd_DECR(args):
    registers['A'] -= 1

def cmd_BITAND(args):
    a, b = args.split(',')
    registers['A'] = evaluate(a) & evaluate(b)

def cmd_BITXOR(args):
    a, b = args.split(',')
    registers['A'] = evaluate(a) ^ evaluate(b)

def cmd_BITOR(args):
    a, b = args.split(',')
    registers['A'] = evaluate(a) | evaluate(b)

def cmd_BITNO(args):
    registers['A'] = ~registers['A']

def cmd_BLS(args):
    registers['A'] <<= int(args.strip('A[]'))

def cmd_BRS(args):
    registers['A'] >>= int(args.strip('A[]'))

def cmd_COMPARE(args):
    a, b = args.strip('[]').split(',')
    a_val = evaluate(a)
    b_val = evaluate(b)
    flags['ZF'] = int(a_val == b_val)
    flags['GF'] = int(a_val > b_val)
    flags['LF'] = int(a_val < b_val)

def cmd_JUM(label):
    return labels.get(label.strip('[]'), -1)

def cmd_JUMIF(label):
    return labels.get(label.strip('[]'), -1) if flags['ZF'] else -1

def cmd_JUME(label):
    return labels.get(label.strip('[]'), -1) if not flags['ZF'] else -1

def cmd_JUMG(label):
    return labels.get(label.strip('[]'), -1) if flags['GF'] else -1

def cmd_JUML(label):
    return labels.get(label.strip('[]'), -1) if flags['LF'] else -1

def cmd_ENT(args):
    stack.append(evaluate(args))

def cmd_BAC(_):
    if stack:
        registers['A'] = stack.pop()

def cmd_KILL(_):
    global halt
    halt = True

def cmd_NOOPR(_): pass

def cmd_SINTE(n):
    print(f"[INTERRUPT] System Interrupt {n}")

def cmd_INP(args):
    port, reg = args.strip().split()
    val = input(f"Input from {port}: ")
    registers[reg] = int(val)

def cmd_OUT(args):
    port, reg = args.strip().split()
    print(f"Output to {port}: {registers[reg]}")

def cmd_CLEAR(args):
    registers[args.strip()] = 0

def cmd_SWAP(args):
    a, b = args.split(',')
    registers[a], registers[b] = registers[b], registers[a]

def cmd_TEST(args):
    a, b = args.split(',')
    _ = evaluate(a) & evaluate(b)

def cmd_LOADEA(args):
    a, b = args.split(',')
    registers[a] = memory.get(registers.get(b.strip('[]'), '0'), 0)

def cmd_EXC(args):
    a, b = args.split(',')
    registers[a], registers[b] = registers[b], registers[a]

def cmd_WAIT(_):
    input("[WAIT] Press Enter to continue...")

def cmd_VECTSET(args):
    n, addr = args.split(',')
    vector_table[int(n)] = addr.strip()

def cmd_CLEANI(_):
    flags['INT'] = 0

def cmd_SETI(_):
    flags['INT'] = 1

def cmd_HALTCPU(_):
    exit(0)

def cmd_ENCRYPT(args):
    print("[Encryption] Code is protected. Password feature is not implemented yet.")

def cmd_SETURL(args):
    print(f"[IoT] Connecting to URL: {args.strip()}")

def cmd_CLOOP(args):
    return int(args.split(':')[-1].strip())

def cmd_STRMAP():
    print("REG:", registers)
    print("MEM:", memory)
    print("STACK:", stack)

def cmd_ENCODE(args):
    global encoding
    encoding = args.strip()
    print(f"[Encoding] set to {encoding}")

def cmd_LOGICNOT(args):
    registers[args.strip()] = int(not registers[args.strip()])

def cmd_LOGICAND(args):
    a, b = args.split(',')
    registers['A'] = int(evaluate(a) and evaluate(b))

def cmd_BREAK(_):
    raise StopIteration

def cmd_PRI(args):
    if args.startswith('"'):
        print(args.strip('"'))
    else:
        print(registers.get(args.strip(), 0))

def cmd_WRI(_):
    registers['A'] = int(input("Enter value: "))

def cmd_LOGALL(_):
    print("[LOG]", registers, memory)

def cmd_TRAC(args):
    global trace
    trace = args.strip().lower() == 'on'

def cmd_ERR(args):
    raise RuntimeError(f"Error code {args.strip()}")

def cmd_ASSERT(args):
    a, b = args.strip('[]').split('==')
    if evaluate(a) != evaluate(b):
        raise AssertionError(f"Assertion failed: {a} != {b}")



def cmd_CAL(label):
    stack.append(i + 1)
    return labels.get(label.strip('[]'), -1)

def cmd_CALBACK(_):
    if stack:
        return stack.pop()

def cmd_BUV(args):
    # For demonstration: rotate bits up (cyclic left shift)
    n = int(args.strip('A[]'))
    val = registers['A']
    for _ in range(n):
        val = ((val << 1) | (val >> (val.bit_length() or 1))) & 0xFFFFFFFF
    registers['A'] = val

def cmd_BDV(args):
    # For demonstration: rotate bits down (cyclic right shift)
    n = int(args.strip('A[]'))
    val = registers['A']
    for _ in range(n):
        val = ((val >> 1) | (val << (val.bit_length() or 1))) & 0xFFFFFFFF
    registers['A'] = val

def cmd_ORIG(args):
    print(f"[ORIG] Program origin address set to {args.strip()} (non-functional placeholder)")

def cmd_DDEF(args):
    print(f"[DEFINE] {args.strip()} (simulated)")

def cmd_HELP(_):
    print("Available Commands:")
    for cmd in command_map:
        print(" -", cmd)

def cmd_HELPCODE(_):
    print("[HelpCode] Auto-correct placeholder (not implemented)")


command_map = {
    'COPY': cmd_COPY, 'GET[MA]': cmd_GETMA, 'INF': cmd_INF, 'STOR[MA]': cmd_STORMA,
    'GET[addr]': cmd_GETADDR, 'STOR[addr]': cmd_STORADDR, 'ADD': cmd_ADD, 'SUBT': cmd_SUBT,
    'MULT': cmd_MULT, 'DIVI': cmd_DIVI, 'INCR': cmd_INCR, 'DECR': cmd_DECR, 'BIT[AND]': cmd_BITAND,
    'BIT[XOR]': cmd_BITXOR, 'BIT[OR]': cmd_BITOR, 'BIT[NO]': cmd_BITNO, 'BLS': cmd_BLS, 'BRS': cmd_BRS,
    'COMPARE': cmd_COMPARE, 'JUM[LAB]': cmd_JUM, 'JUM[LAB]IF': cmd_JUMIF, 'JUM[LAB]E': cmd_JUME,
    'JUM[LAB]G': cmd_JUMG, 'JUM[LAB]L': cmd_JUML, 'ENT': cmd_ENT, 'BAC': cmd_BAC, 'KILL': cmd_KILL,
    'NO[OPR]': cmd_NOOPR, 'SINTE': cmd_SINTE, 'INP[port]': cmd_INP, 'OUT[port]': cmd_OUT,
    'CLEAR': cmd_CLEAR, '[SWAP]': cmd_SWAP, '[TEST]': cmd_TEST, 'LOAD[EA]': cmd_LOADEA,
    'EXC': cmd_EXC, '[WAIT]': cmd_WAIT, 'VECT[SET]': cmd_VECTSET, 'CLEAN[I]': cmd_CLEANI,
    'SET[I]': cmd_SETI, 'HALT[CPU]': cmd_HALTCPU, 'Encrypt[Code]': cmd_ENCRYPT, 'SetURL': cmd_SETURL,
    'C[LOOP]': cmd_CLOOP, 'str.map()': cmd_STRMAP, 'ENCODE': cmd_ENCODE, 'LOGIC[NOT]': cmd_LOGICNOT,
    'LOGIC[AND]': cmd_LOGICAND, 'BREAK': cmd_BREAK, 'PRI': cmd_PRI, 'WRI': cmd_WRI, 'PRI[A]': cmd_PRI,
    'LOG[ALL]': cmd_LOGALL, 'TRAC': cmd_TRAC, 'ERR': cmd_ERR, 'ASSERT': cmd_ASSERT,

    'CAL[LAB]': cmd_CAL,
    'CAL[BACK]': cmd_CALBACK,
    'BUV': cmd_BUV,
    'BDV': cmd_BDV,
    'ORIG[addr]': cmd_ORIG,
    'D,Def[B,val]': cmd_DDEF,
    'D,Def[W,val]': cmd_DDEF,
    '[HelpMe]': cmd_HELP,
    'HelpCode[...]': cmd_HELPCODE,
}

def parse_and_run(lines):
    global halt
    i = 0
    while i < len(lines):
        if halt:
            break
        line = lines[i].strip()
        if not line or line.startswith("CMT") or line.startswith("[") or line.startswith("#"):
            i += 1
            continue
        if ':' in line and not line.startswith('PRI'):
            label = line.split(':')[0].strip('[] ')
            labels[label] = i
            line = line.split(':')[-1].strip()
            if not line:
                i += 1
                continue
        trace_log(f"[{i}] {line}")
        for key, func in command_map.items():
            if line.startswith(key):
                arg = line[len(key):].strip()
                ret = func(arg)
                if isinstance(ret, int):
                    i = ret
                    break
        else:
            pass
        i += 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python silicon_interpreter.py <file.sil> [--trace]")
        exit(1)
    filename = sys.argv[1]
    if '--trace' in sys.argv:
        trace = True
    with open(filename, encoding=encoding) as f:
        code = f.readlines()
    parse_and_run(code)
