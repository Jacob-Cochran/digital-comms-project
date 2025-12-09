import numpy 
pi = numpy.pi



# angles = numpy.linspace(0, 2*pi, 16)


angles = numpy.arange(0, 360, 22.5)
# print(angles)

angles = numpy.radians(angles)

symbols = numpy.exp(1j*angles)

vals = numpy.exp(1j* numpy.radians(numpy.arange(0, 360, 22.5)))
print(vals)

# for s in symbols:
#     print(f"{s.real:.6f} + {s.imag:.6f}j", end=',')


symbolsMapping = [10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 8, 9]


# print("Symbols for 16-PSK:", symbols, len(symbols))

print("\n\n", symbolsMapping, len(symbolsMapping))
