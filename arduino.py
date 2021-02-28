from pyfirmata import Arduino, util
import IPython.display
from ipywidgets.widgets import Layout
import ipywidgets as widgets


placa = Arduino('/dev/ttyUSB0')

botao = widgets.Button(description="Luz",mycolor='white',layout=Layout(width='1213px'))
botao.style.button_color = 'green'
#botao2 = widgets.Button(description="Luz",button_style='warning',layout=Layout(width='1213px'))
estado_botao = widgets.Output()
display(botao, estado_botao)
    

def liga_desliga(b):
    with estado_botao:
        estado = placa.digital[13].read()
        if estado == True:
            placa.digital[13].write(0)
            botao.style.button_color = 'green'
        else:
            placa.digital[13].write(1)
            botao.style.button_color = 'gold'
        IPython.display.clear_output(wait=True)
                        

botao.on_click(liga_desliga)