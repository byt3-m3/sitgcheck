def get_neighbors(self):
    """ Returns a list of dicts of the switch's neighbors:
        {hostname, ip, local_port, remote_port} """

    re_text = "-+\r?\nDevice ID: (.+)\\b\r?\n.+\s+\r?\n\s*IP address:\s+(\d+\.\d+\.\d+\.\d+)\s*\r?\n.*\r?\nInterface: (.+),.+Port ID.+: (.+)\\b\r?\n"

    neighbors = list()
    for neighbor in re.findall(re_text, self.cmd('show cdp neighbors detail')):
        n_dict = dict()

        n_dict['hostname'], n_dict['ip'], n_dict['local_port'], n_dict['remote_port'] = neighbor

        neighbors.append(n_dict)

    return neighbors
