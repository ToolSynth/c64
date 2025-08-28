from typing import TYPE_CHECKING

from src.cpu.instructions.arithmetic import Arithmetic
from src.cpu.instructions.branch import Branch
from src.cpu.instructions.flag import Flag
from src.cpu.instructions.heap import Heap
from src.cpu.instructions.jump import Jump
from src.cpu.instructions.logic import Logic
from src.cpu.instructions.register import Register
from src.cpu.instructions.stack import Stack
from src.cpu.instructions.system import System

if TYPE_CHECKING:
    from src.cpu.cpu import CPU


class InstructionManager:
    def __init__(self, cpu: "CPU") -> None:
        heap = Heap(cpu)
        branch = Branch(cpu)
        system = System(cpu)
        jump = Jump(cpu)
        arithmetic = Arithmetic(cpu)
        logic = Logic(cpu)
        stack = Stack(cpu)
        register = Register(cpu)
        flag = Flag(cpu)

        self.instructions = {
            # Heap instructions
            0xA5: heap.lda_zero_page,
            0xA9: heap.lda_immediate,
            0xAD: heap.lda_absolute,
            0xB1: heap.lda_indirect_y,
            0xBD: heap.lda_absolute_x,
            0xB9: heap.lda_absolute_y,
            0xB5: heap.lda_zeropage_x,
            0x85: heap.sta_zero_page,
            0x8D: heap.sta_absolute,
            0x91: heap.sta_indirect_y,
            0x99: heap.sta_absolute_y,
            0x95: heap.sta_zeropage_x,
            0x9D: heap.sta_absolute_x,
            0xA2: heap.ldx_immediate,
            0xA6: heap.ldx_zero_page,
            0xAE: heap.ldx_absolute,
            0xBE: heap.ldx_absolute_y,
            0x86: heap.stx_zero_page,
            0x8E: heap.stx_absolute,
            0x96: heap.stx_zero_page_y,
            0xA0: heap.ldy_immediate,
            0xA4: heap.ldy_zero_page,
            0xAC: heap.ldy_absolute,
            0xB4: heap.ldy_zero_page_x,
            0xBC: heap.ldy_absolute_x,
            0x84: heap.sty_zero_page,
            0x8C: heap.sty_absolute,
            0x94: heap.sty_zero_page_x,
            0xE6: heap.inc_zero_page,
            0xF6: heap.inc_zero_page_x,
            0xFE: heap.inc_absolute_x,
            0xC6: heap.dec_zero_page,
            0xCE: heap.dec_absolute,
            0xEE: heap.inc_absolute,
            # Branch instructions
            0xF0: branch.beq,
            0xD0: branch.bne,
            0x10: branch.bpl,
            0x30: branch.bmi,
            0x70: branch.bvs,
            0x90: branch.bcc,
            0xB0: branch.bcs,
            0x50: branch.bvc,
            # System instructions
            0x00: system.brk,
            0xEA: system.nop,
            # Jump instructions
            0x6C: jump.jmp_indirect,
            0x4C: jump.jmp_absolute,
            0x20: jump.jsr,
            0x60: jump.rts,
            0x40: jump.rti,
            # Arithmetic instructions
            0xE9: arithmetic.sbc_immediate,
            0xE5: arithmetic.sbc_zero_page,
            0xFD: arithmetic.sbc_absolute_x,
            0xF9: arithmetic.sbc_absolute_y,
            0xED: arithmetic.sbc_absolute,
            0xF1: arithmetic.sbc_indirect_y,
            0xF5: arithmetic.sbc_zero_page_x,
            0xD1: arithmetic.cmp_indirect_y,
            0xC9: arithmetic.cmp_immediate,
            0xC5: arithmetic.cmp_zero_page,
            0xCD: arithmetic.cmp_absolute,
            0xDD: arithmetic.cmp_absolute_x,
            0xD9: arithmetic.cmp_absolute_y,
            0xE0: arithmetic.cpx_immediate,
            0xE4: arithmetic.cpx_zero_page,
            0xEC: arithmetic.cpx_absolute,
            0xC0: arithmetic.cpy_immediate,
            0xC4: arithmetic.cpy_zero_page,
            0x2C: arithmetic.bit_absolute,
            0x24: arithmetic.bit_zero_page,
            0x79: arithmetic.adc_absolute_y,
            0x65: arithmetic.adc_zero_page,
            0x69: arithmetic.adc_immediate,
            # Logic instructions
            0x29: logic.and_immediate,
            0x31: logic.and_indirect_y,
            0x25: logic.and_zero_page,
            0x49: logic.eor_immediate,
            0x45: logic.eor_zero_page,
            0x55: logic.eor_zero_page_x,
            0x41: logic.eor_indirect_x,
            0x09: logic.ora_immediate,
            0x05: logic.ora_zero_page,
            0x0D: logic.ora_absolute,
            0x11: logic.ora_indirect_indexed,
            0x4A: logic.lsr_accumulator,
            0x46: logic.lsr_zero_page,
            0x56: logic.lsr_zero_page_x,
            0x0A: logic.asl_accumulator,
            0x06: logic.asl_zero_page,
            0x16: logic.asl_zero_page_x,
            0x2A: logic.rol_accumulator,
            0x26: logic.rol_zero_page,
            0x6A: logic.ror_accumulator,
            0x66: logic.ror_zero_page,
            0x76: logic.ror_zero_page_x,
            0x6E: logic.ror_absolute,
            # Stack instructions
            0x48: stack.pha,
            0x68: stack.pla,
            0x9A: stack.txs,
            0x08: stack.php,
            0x28: stack.plp,
            0xBA: stack.tsx,
            # Register instructions
            0xAA: register.tax,
            0xA8: register.tay,
            0x8A: register.txa,
            0x98: register.tya,
            0xCA: register.dex,
            0x88: register.dey,
            0xE8: register.inx,
            0xC8: register.iny,
            # Flag instructions
            0x18: flag.clc,
            0xD8: flag.cld,
            0x78: flag.sei,
            0x58: flag.cli,
            0x38: flag.sec,
        }

    def execute(self, opcode: int) -> None:
        """Executes an instruction based on the opcode."""
        if opcode in self.instructions:
            self.instructions[opcode]()
        else:
            raise ValueError(f"Unknown opcode: {hex(opcode)}")
