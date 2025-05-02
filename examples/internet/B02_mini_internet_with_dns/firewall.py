def set_firewall(base, AS, router, cidr):
    block = (
        '#!/bin/bash\n'
        f'iptables -A FORWARD -d {cidr} -j DROP'
    )

    r = base.getAutonomousSystem(AS).getRouter(router)

    r.addSoftware('iptables')
    r.setFile('/tmp/block.sh', block)
    r.appendStartCommand('chmod +x /tmp/block.sh')
    r.appendStartCommand('/tmp/block.sh')
