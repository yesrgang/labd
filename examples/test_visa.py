# replace 
#     import visa
# with
#     from labd._visa import VisaProxy
#     visa = VisaProxy(('yesr5.colorado.edu', 4292))

from labd._visa import VisaProxy
visa = VisaProxy(('yesr13.colorado.edu', 4292))

# talk to ds345 on yesr5
rm = visa.ResourceManager()
print(rm.list_resources())
inst = rm.open_resource('GPIB0::21::INSTR')
inst.write('FREQ 666')
print(inst.query('FREQ?'))
