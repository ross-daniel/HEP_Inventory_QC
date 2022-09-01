import usb.core

dev = usb.core.find(idVendor=0x0111, idProduct=0x0111)
if dev is None:
    raise ValueError('No USB Device Detected, Please Check Scanner Connection')
else:
    print(dev[0])
ep = dev[0].interfaces()[0].endpoints()[0]
i = dev[0].intefaces()[0].bInterfaceNumber
dev.reset()

if dev.is_kernel_driver_active(i):
    dev.detach_kernel_driver(i)

dev.set_configuration()
eaddr = ep.bEndpointAddress

r = dev.read(eaddr, 18)
print(r)