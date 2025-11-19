from skidl import Net, POWER

class PowerNetMapper:
    """Handles VCC, GND, and other power nets"""

    @staticmethod
    def create_power_nets():
        """Create standard power nets"""
        gnd = Net("GND")
        gnd.drive = POWER
        
        vcc = Net("VCC")
        vcc.drive = POWER
        
        return {"GND": gnd, "VCC": vcc}
    
    @staticmethod
    def create_custom_net(net_name, is_power=False):
        """Create any net by name"""
        net = Net(net_name)
        if is_power:
            net.drive = POWER
        return net
