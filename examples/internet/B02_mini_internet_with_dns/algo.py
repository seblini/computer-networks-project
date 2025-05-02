def update_BGP_conf(base, AS, router, nextAS):
    update = (
        '#!/bin/bash\n'
        'birdc\n'
        f'define prefer_u_as{nextAS} = function() {{\n'
        'bgp_local_pref = 20;\n'
        'accept;\n'
        '};\n'
        f'reload in u_as{nextAS}'
    )

    r = base.getAutonomousSystem(AS).getRouter(router)

    # r.addBuildCommand('apt install traceroute')
    r.setFile('/tmp/update.sh', update)
    r.appendStartCommand('chmod +x /tmp/update.sh')
    # r.appendStartCommand('/tmp/update.sh')
