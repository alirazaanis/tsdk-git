"""
Telecom Systems Development Kit - tsdk
"""
import io

import pandas as pd

mapping = [
    ['B1', 'L1900C1', 'MB'],
    ['B2', 'L1900C2', 'MB'],
    ['D1', 'L700', 'LB'],
    ['E1', 'L600', 'LB'],
    ['L1', 'L2100', 'MB'],
    ['K1', 'NR600', 'LB'],
    ['T1', 'L2500C1', 'Anchor'],
    ['T2', 'L2500C2', 'Anchor'],
    ['A1', 'NR2500C1', 'Anchor'],
    ['A2', 'NR2500C2', 'Anchor']
]


def find_mapping(sl, f):
    r = None
    for i, e in enumerate(sl):
        try:
            test = e.index(f)
            r = i
            assert test
            break
        except ValueError:
            pass
    return r


def parse_cmd_results(cmd_results):
    # Total: 3 MOs attempted, 3 MOs set
    import numpy
    x = list(
        map(lambda a: [int(a.split(' ')[1].strip()),
                       int(a.split(' ')[4].strip())] if 'Total: ' in a else [0, 0], cmd_results))
    npa = numpy.array(x)
    return npa.sum(axis=0).tolist()


def parse_st_cell(st_cell_results):
    return sorted(
        set(
            filter(
                lambda a: a is not None,
                map(
                    lambda a: (
                                  a.split('=')[2]
                              ).strip()[:1] + (
                                                  a.split('=')[2]
                                              ).strip()[-1:] if len(
                        a.split('=')
                    ) == 3 else None,
                    st_cell_results
                )
            )
        )
    )


def parse_nodes_list(nodes_list_results):
    return sorted(set(map(lambda a: (a.split(' ')[1]).strip(), nodes_list_results)))


class Sshc(object):
    @staticmethod
    def run_cmd(s):
        return [s]

    @staticmethod
    def run_cmd_file(s):
        return [s]


ssh = Sshc()

cmd_path = '/location/'
sites_list = ['NJ01059A', '', '', '']
final_result = ['Site,Node,MOs Attempted,MOs Set']
for site in sites_list:
    nodes_list = ssh.run_cmd(
        'cat /opt/ericsson/amos/moshell/sitefiles/ipdatabase | grep -i -h %s' % site)
    nodes_list = parse_nodes_list(nodes_list)
    for node in nodes_list:
        ssh.run_cmd('amos %s' % node)
        ssh.run_cmd('lt all')
        results = ssh.run_cmd('st cell')
        results = parse_st_cell(results)
        for result in results:
            _, cmd_file_a, cmd_file_b = mapping[find_mapping(mapping, result)]
            result_a = ssh.run_cmd_file(cmd_path + cmd_file_a)
            result_b = ssh.run_cmd_file(cmd_path + cmd_file_b)
            final_result.append('%s,%s,%s' % (site, node,
                                              ','.join(list(map(str, parse_cmd_results(result_a))))))
            final_result.append('%s,%s,%s' % (site, node,
                                              ','.join(list(map(str, parse_cmd_results(result_b))))))
df = pd.read_csv(str(io.StringIO('\n'.join(final_result))), sep=',')
df.to_excel("location/filename.xlsx", sheet_name="final_results", index=False)
