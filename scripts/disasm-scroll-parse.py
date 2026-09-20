import capstone

with open('deploy_agent/cloudphone-agent-amd64', 'rb') as f:
    f.seek(0x5e3a00)
    code = f.read(0x400)

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

for insn in cs.disasm(code, 0x9e3a00):
    print(f'0x{insn.address:x}: {insn.mnemonic} {insn.op_str}')
