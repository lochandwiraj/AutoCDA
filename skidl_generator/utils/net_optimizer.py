class NetNamingOptimizer:
    
    @staticmethod
    def optimize_net_names(nets_dict):
        optimized = {}
        counter = 1
        
        for net_name, net_obj in nets_dict.items():
            name = net_name.lower()
            if 'power' in name and ('pos' in name or '+' in name):
                new_name = 'VCC'
            elif 'ground' in name or 'gnd' in name:
                new_name = 'GND'
            elif 'input' in name:
                new_name = f'IN{counter}'
                counter += 1
            elif 'output' in name:
                new_name = 'VOUT'
            else:
                new_name = f'N{counter}'
                counter += 1
            
            optimized[new_name] = net_obj
        
        return optimized