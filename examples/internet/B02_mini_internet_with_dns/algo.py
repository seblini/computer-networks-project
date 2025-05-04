def include_reroute(base, AS, router, nextAS):
    reroute = """if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <subnet> <AS_num>"
    exit 1
fi

sn=$1
as="u_as${2}"

cp /etc/bird/bird.conf /etc/bird/bird_new.conf

sed -i -e "/^protocol bgp ${as} {/{n;N;N;N;N;N;N;N;N;N;d;}" /etc/bird/bird_new.conf

sed -i "/^protocol bgp ${as} {/ a\\\\
    ipv4 {\\\\
        table t_bgp;\\\\
        import filter {\\\\
          bgp_large_community.add(PROVIDER_COMM);\\\\
          if net = ${sn} then {\\\\
            bgp_local_pref = 20;\\\\
            accept;\\\\
          } else {\\\\
            bgp_local_pref = 10;\\\\
            accept;\\\\
          }\\\\
        };\\\\
        export where bgp_large_community ~ [LOCAL_COMM, CUSTOMER_COMM];\\\\
        next hop self;\\\\
    };
" /etc/bird/bird_new.conf

birdc 'configure "/etc/bird/bird_new.conf"'
    """

    r = base.getAutonomousSystem(AS).getRouter(router)

    r.setFile('/bin/reroute.sh', reroute)
    r.appendStartCommand('chmod +x /bin/reroute.sh')
