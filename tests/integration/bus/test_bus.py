def test_ram_read_write(bus) -> None:
    address = 0x0002
    value = 0xAA
    bus.write(address, value)
    assert bus.read(address) == value


def test_rom_read_write(bus) -> None:
    address = 0xA123
    value = 0x55
    expected = (address - 0xA000) % 256
    assert bus.read(address) == expected
    bus.write(address, value)
    assert bus.read(address) == expected
    assert bus.ram.read(address) == value


def test_color_ram_read_write(bus) -> None:
    bus.write(0x0001, 0x37)
    address = 0xD900
    bus.write(address, 0xAB)
    assert bus.read(address) == 0x0B


def test_pla_address_mapping(bus) -> None:
    bus.write(0x0001, 0x33)
    assert bus.pla.decode_address(0x0002) is bus.ram
    assert bus.pla.decode_address(0xA000) is bus.basic_rom
    assert bus.pla.decode_address(0xE000) is bus.kernel_rom
    assert bus.pla.decode_address(0x1000) is bus.chargen_rom
    bus.write(0x0001, 0x37)
    assert bus.pla.decode_address(0xD020) is bus.vic
    assert bus.pla.decode_address(0xD400) is bus.sid
    assert bus.pla.decode_address(0xDC00) is bus.cia_1
    assert bus.pla.decode_address(0xDD00) is bus.cia_2
    assert bus.pla.decode_address(0xD800) is bus.color_ram
