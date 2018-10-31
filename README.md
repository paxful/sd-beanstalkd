# ServerDensity plugin for BeanstalkD


   * [ServerDensity plugin for BeanstalkD](#serverdensity-plugin-for-beanstalkd)
      * [Overview](#overview)
      * [Requirements](#requirements)
      * [Installation](#installation)
      * [Metrics](#metrics)
         * [Global metrics](#global-metrics)
         * [Tube metrics](#tube-metrics)
      * [Contributing](#contributing)
      * [License &amp; Authors](#license--authors)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

## Overview

[Beanstalk](https://beanstalkd.github.io/) plugin for [ServerDensity](http://serverdensity.io).   
Tested with sd-agent v2.2.1.

## Requirements

Requires [PyYAML](http://pyyaml.org/).

## Installation

* Copy the `beanstalk.py` script to `sd-agent` plugins folder `/usr/share/python/sd-agent/checks.d`.   
* Copy configuration file `beanstalkd.yaml.example` to `/etc/sd-agent/conf.d/beanstalkd.yaml`.
* Restart `sd-agent`

## Metrics

### Global metrics

* `current-jobs-urgent` is the number of ready jobs with priority < 1024.

* `current-jobs-ready` is the number of jobs in the ready queue.

* `current-jobs-reserved` is the number of jobs reserved by all clients.

* `current-jobs-delayed` is the number of delayed jobs.

* `current-jobs-buried` is the number of buried job's.

* `cmd-put` is the cumulative number of put commands.

* `cmd-peek` is the cumulative number of peek commands.

* `cmd-peek-ready` is the cumulative number of peek-ready commands.

* `cmd-peek-delayed` is the cumulative number of peek-delayed commands.

* `cmd-peek-buried` is the cumulative number of peek-buried commands.

* `cmd-reserve` is the cumulative number of reserve commands.

* `cmd-use` is the cumulative number of use commands.

* `cmd-watch` is the cumulative number of watch commands.

* `cmd-ignore` is the cumulative number of ignore commands.

* `cmd-delete` is the cumulative number of delete commands.

* `cmd-release` is the cumulative number of release commands.

* `cmd-bury` is the cumulative number of bury commands.

* `cmd-kick` is the cumulative number of kick commands.

* `cmd-stats` is the cumulative number of stats commands.

* `cmd-stats-job` is the cumulative number of stats-job commands.

* `cmd-stats-tube` is the cumulative number of stats-tube commands.

* `cmd-list-tubes` is the cumulative number of list-tubes commands.

* `cmd-list-tube-used` is the cumulative number of list-tube-used commands.

* `cmd-list-tubes-watched` is the cumulative number of list-tubes-watched
commands.

* `cmd-pause-tube` is the cumulative number of pause-tube commands

* `job-timeouts` is the cumulative count of times a job has timed out.

* `total-jobs` is the cumulative count of jobs created.

* `max-job-size` is the maximum number of bytes in a job.

* `current-tubes` is the number of currently-existing tubes.

* `current-connections` is the number of currently open connections.

* `current-producers` is the number of open connections that have each
issued at least one put command.

* `current-workers` is the number of open connections that have each issued
at least one reserve command.

* `current-waiting` is the number of open connections that have issued a
reserve command but not yet received a response.

* `total-connections` is the cumulative count of connections.

* `pid` is the process id of the server.

* `version` is the version string of the server.

* `rusage-utime` is the cumulative user CPU time of this process in seconds
and microseconds.

* `rusage-stime` is the cumulative system CPU time of this process in
seconds and microseconds.

* `uptime` is the number of seconds since this server process started running.

* `binlog-oldest-index` is the index of the oldest binlog file needed to
store the current jobs

* `binlog-current-index` is the index of the current binlog file being
written to. If binlog is not active this value will be 0

* `binlog-max-size` is the maximum size in bytes a binlog file is allowed
to get before a new binlog file is opened

* `binlog-records-written` is the cumulative number of records written
to the binlog

* `binlog-records-migrated` is the cumulative number of records written
as part of compaction

### Tube metrics

* `current-jobs-urgent` is the number of ready jobs with priority < 1024 in
this tube.

* `current-jobs-ready` is the number of jobs in the ready queue in this tube.

* `current-jobs-reserved` is the number of jobs reserved by all clients in
this tube.

* `current-jobs-delayed` is the number of delayed jobs in this tube.

* `current-jobs-buried` is the number of buried jobs in this tube.

* `total-jobs` is the cumulative count of jobs created in this tube in
the current beanstalkd process.

* `current-using` is the number of open connections that are currently
using this tube.

* `current-waiting` is the number of open connections that have issued a
reserve command while watching this tube but not yet received a response.

* `current-watching` is the number of open connections that are currently
watching this tube.

* `pause` is the number of seconds the tube has been paused for.

* `cmd-delete` is the cumulative number of delete commands for this tube

* `cmd-pause-tube` is the cumulative number of pause-tube commands for this
tube.

* `pause-time-left` is the number of seconds until the tube is un-paused.


## Contributing
1. Fork the repository on Github
2. Create a named feature branch (like `add_component_x`)
3. Write your change
4. Write tests for your change (if applicable)
5. Run the tests, ensuring they all pass
6. Submit a Pull Request using Github

## License & Authors
* Author:: Andrei Skopenko (andrei@skopenko.net)

```text
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
