import capstone

with open('deploy_agent/cloudphone-agent-amd64', 'rb') as f:
    f.seek(0x5cf960)
    code = f.read(0x130)

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

for insn in cs.disasm(code, 0x9cf960):
    print(f'0x{insn.address:x}: {insn.mnemonic} {insn.op_str}')
