#!/usr/bin/env python
#
# Copyright (c) 2018 Andrei Skopenko <andrei@skopenko.net>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import socket
import telnetlib
import yaml

from checks import AgentCheck


class Beanstalkd(AgentCheck):
    '''Tracks beanstalkd metrics
    '''

    def check(self, instance):
        # Attempt to load the host setting from the instance config.
        if 'host' not in instance:
            host = 'localhost'
        else:
            host = instance.get('host')

        # Attempt to load the port setting from the instance config.
        if 'port' not in instance:
            port = '11300'
        else:
            port = int(instance.get('port'))

        # Attempt to load the tags from the instance config.
        tags = instance.get('tags', [])

        # Append the tag 'server: server:port' to the tags list,
        # based on the values loaded from the instance config.
        tags.append("server: {}:{}".format(host, port))

        # Open telnet connection to beanstalkd
        self.connect(host, port)

        # Get beanstalkd stats
        stats = self._get_stats()
        self.log.debug(u"Beanstalkd stats: {0}".format(stats))

        # Get beanstalkd tube stats
        tube_stats = self._get_tube_stats()
        self.log.debug(u"Beanstalkd tube_stats: {0}".format(tube_stats))

        # Close connection to beanstalkd
        self.disconnect()

        # Submit stats metrics
        for metrics_name, metrics in {'beanstalkd.stats': stats, 'beanstalkd.tube_stats': tube_stats}.iteritems():
            for metric, value in metrics.iteritems():
                try:
                    self.gauge('%s.%s' % (metrics_name, metric), value, tags)
                except Exception as e:
                    self.log.error(u'Could not submit metric: %s: %s' % (repr(metric), str(e)))

    def connect(self, host, port):
        try:
            self.telnet_connection = telnetlib.Telnet()
            self.telnet_connection.open(host, port)
        except Exception as e:
            self.log.error(u'Could not connect to beanstalkd: %s' % str(e))
            raise

    def disconnect(self):
        self.telnet_connection.close()

    def interact(self, cmd):
        self.telnet_connection.write('%s\r\n' % cmd)
        status = self.telnet_connection.read_until("\r\n")

        if status is not None and 'OK' in status:
            response = self.telnet_connection.read_until("\n\r\n")
            return yaml.load(response)
        else:
            self.log.error(u'Beanstalkd error for cmd (%s): %s' % (cmd, status))
            return None

    def _get_stats(self):
        return self.interact('stats')

    def get_tubes_list(self):
        return self.interact('list-tubes')

    def prefix_keys(self, tube_name, stats):
        '''
        Our plugin output must be a flat dict. Since each tube returns the
        same key/value stats we must prefix key names with the tube name e.g.
        the key total-jobs for tube 'email_signup' becomes email_signup-total-jobs.
        '''
        new_dict = {}

        # SD does not allow full stop (period) characters in key names
        # http://support.serverdensity.com/knowledgebase/articles/76015-plugin-restrictions
        tube_name = tube_name.replace('.', '_')

        for k, v in stats.items():
            # The value must be an integer or a float for Server Density to store the value.
            if k == 'name':
                continue
            key = '%s.%s' % (tube_name, k)
            new_dict[key] = v

        return new_dict

    def _get_tube_stats(self):
        stats = {}
        for tube in self.get_tubes_list():
            tube_stats = self.interact('stats-tube %s' % tube)
            tube_stats = self.prefix_keys(tube, tube_stats)
            stats.update(tube_stats)

        return stats


if __name__ == '__main__':
    # Load the check and instance configurations
    check, instances = Beanstalkd.from_yaml('/etc/sd-agent/conf.d/beanstalkd.yaml')
    for instance in instances:
        print "\nRunning the check against host: {}:{}".format(instance['host'], instance.get('port', 11300))
        check.check(instance)
        print 'Metrics: {}'.format(check.get_metrics())
