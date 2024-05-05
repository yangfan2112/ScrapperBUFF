def beneficio():
    venta = float(input("Introduce el precio de venta en buff chino de esta skin: \n"))
    gasto = float(input("Introduce el precio de gasto en buff español de esta skin: \n"))
    
    beneficio = round(((venta - (venta * 0.025)) - ((venta - (venta * 0.025)) * 0.01)) - (gasto + (gasto * 0.035)), 2)
    
    beneficio_euro = round(beneficio * 0.13, 2)
    
    print("Se obtiene {}RMB como beneficio con esta skin.".format(beneficio))
    
    print("Equivale a {}€".format(beneficio_euro))
    
    
    
beneficio()