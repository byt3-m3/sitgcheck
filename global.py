var = 0
def outer():
    global var                  # line A
    var = 1
    def inner():
        nonlocal var            # line B
        var = 2

        print('inner:', var)

    inner()
    print('outer:', var)

outer()
print('main:', var)