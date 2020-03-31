import bdoread as br

data = br.bdo_bin_to_dict('ex_zmsh2.bdo')

for x, y in data.items():
    print(x)
    print(y)
    print('')
